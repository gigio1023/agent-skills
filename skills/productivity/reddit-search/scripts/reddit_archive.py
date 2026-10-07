#!/usr/bin/env python3
"""Search and read Reddit posts and comment trees through the Arctic Shift archive.

Reddit refuses most agent and script traffic: anonymous ``.json`` returns 403,
old.reddit.com redirects to login, and the HTML is a JavaScript challenge.
Arctic Shift (https://arctic-shift.photon-reddit.com) is a free archive run by
one person that ingests posts and comments as they appear. This helper keeps
requests sequential, small, and paced, as that service asks.

Standard library only: skill helpers run with a bare ``python3`` and no install
step, so API records stay as parsed JSON mappings rather than Pydantic models.

Exit codes: 0 success, 2 bad arguments or rejected parameters, 3 archive query
timeout after one retry, 4 rate limited, 5 network failure.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

API_ROOT: str = "https://arctic-shift.photon-reddit.com/api"
USER_AGENT: str = "reddit-search-skill/1.0 (personal lookup; +https://github.com/gigio1023/agent-skills)"
MIN_INTERVAL_SECONDS: float = 1.5
TIMEOUT_RETRY_WAIT_SECONDS: float = 3.0
MAX_RATE_LIMIT_WAIT_SECONDS: float = 60.0
# The archive stores a post the moment it appears and refreshes score and
# comment counts about 36 hours later; before that they read as 0 or 1.
COUNTS_SETTLE_SECONDS: int = 36 * 3600
# Tried in order when a keyword search has no explicit period. Offsets use the
# archive's documented forms (1year, 3m for months, 2d).
DEFAULT_KEYWORD_WINDOWS: tuple[str, ...] = ("1year", "3m")
NARROWING_HINT: str = (
    "narrow --after/--before around the expected date, use fewer or rarer words, "
    "or list the period without --query/--title and match titles yourself"
)

# Parsed JSON from the archive. Fields are read defensively at each use site.
Json = dict[str, Any]

_last_request_at: float = 0.0


class ArchiveError(Exception):
    """A failure the caller should report with a specific exit code."""

    def __init__(self, message: str, exit_code: int) -> None:
        super().__init__(message)
        self.exit_code: int = exit_code


def _is_timeout(message: str) -> bool:
    lowered: str = message.lower()
    return "timeout" in lowered or "timed out" in lowered


def call_api(path: str, params: dict[str, str | int]) -> Any:
    """GET one archive endpoint and return its ``data`` field.

    Retries once on a query timeout (the archive database sometimes needs to
    warm up) and once on a short rate-limit reset; everything else raises.
    """
    global _last_request_at
    query: str = urllib.parse.urlencode({k: v for k, v in params.items() if v != ""})
    url: str = f"{API_ROOT}/{path}?{query}"
    for attempt in (1, 2):
        wait: float = MIN_INTERVAL_SECONDS - (time.monotonic() - _last_request_at)
        if wait > 0:
            time.sleep(wait)
        request: urllib.request.Request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        body: str
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as error:
            _last_request_at = time.monotonic()
            detail: str = error.read().decode("utf-8", "replace")[:300]
            if error.code == 429:
                reset: str | None = error.headers.get("X-RateLimit-Reset")
                reset_seconds: float = float(reset) if reset and reset.replace(".", "", 1).isdigit() else -1.0
                if attempt == 1 and 0 <= reset_seconds <= MAX_RATE_LIMIT_WAIT_SECONDS:
                    time.sleep(reset_seconds + 1)
                    continue
                raise ArchiveError(f"rate limited (429, reset {reset or 'unknown'}s); stop and retry later", 4)
            if _is_timeout(detail) and attempt == 1:
                time.sleep(TIMEOUT_RETRY_WAIT_SECONDS)
                continue
            if _is_timeout(detail):
                raise ArchiveError(f"archive query timed out twice: {detail}", 3)
            raise ArchiveError(f"HTTP {error.code} from archive: {detail}", 2)
        except (urllib.error.URLError, TimeoutError) as error:
            raise ArchiveError(f"network failure reaching archive: {error}", 5)
        _last_request_at = time.monotonic()
        payload: Json = json.loads(body)
        message: str | None = payload.get("error")
        if message:
            if _is_timeout(message) and attempt == 1:
                time.sleep(TIMEOUT_RETRY_WAIT_SECONDS)
                continue
            if _is_timeout(message):
                raise ArchiveError(f"archive query timed out twice: {message}", 3)
            raise ArchiveError(f"archive rejected the query: {message}", 2)
        return payload.get("data")
    raise ArchiveError("archive query failed after retry", 3)


def parse_post_id(target: str) -> str:
    """Accept a reddit.com or redd.it URL, a ``t3_`` fullname, or a bare base-36 id."""
    patterns: tuple[str, ...] = (r"/comments/([a-z0-9]+)", r"redd\.it/([a-z0-9]+)", r"^(?:t3_)?([a-z0-9]{4,10})$")
    for pattern in patterns:
        match: re.Match[str] | None = re.search(pattern, target.strip(), re.IGNORECASE)
        if match:
            return match.group(1).lower()
    raise ArchiveError(f"cannot find a post id in {target!r}", 2)


def _date(created_utc: float | int | None) -> str:
    if created_utc is None:
        return "unknown-date"
    return datetime.fromtimestamp(float(created_utc), timezone.utc).strftime("%Y-%m-%d")


def _fresh_note(created_utc: float | int | None) -> str:
    if created_utc is None:
        return ""
    age: float = time.time() - float(created_utc)
    return "  [under 36h old: score and comment counts not final]" if age < COUNTS_SETTLE_SECONDS else ""


def _clip(text: str, width: int) -> str:
    flat: str = " ".join(text.split())
    return flat if len(flat) <= width else flat[: width - 3] + "..."


def post_url(post: Json) -> str:
    return f"https://www.reddit.com/r/{post.get('subreddit', '_')}/comments/{post.get('id', '')}/"


def format_post_line(post: Json, width: int) -> str:
    header: str = (
        f"{_date(post.get('created_utc'))}  score {post.get('score', '?')}  "
        f"comments {post.get('num_comments', '?')}  {post.get('id', '')}  r/{post.get('subreddit', '?')}"
    )
    return f"{header}{_fresh_note(post.get('created_utc'))}\n  {_clip(str(post.get('title', '')), width)}\n  {post_url(post)}"


def keyword_search(path: str, params: dict[str, str | int], keyword: bool, all_time: bool) -> tuple[list[Json], str]:
    """Run a search, bounding keyword queries in time so the archive can answer.

    Unbounded keyword searches over busy subreddits time out (observed on
    r/LocalLLaMA for both ``query`` and multi-word ``title``), while the same
    search limited to the last year returns in seconds. Returns the results and
    a note describing any window the helper applied.
    """
    if not keyword:
        return call_api(path, params) or [], ""
    if params.get("after") or params.get("before"):
        try:
            return call_api(path, params) or [], ""
        except ArchiveError as error:
            if error.exit_code != 3:
                raise
            raise ArchiveError(f"{error}; {NARROWING_HINT}", 3) from error
    windows: tuple[str, ...] = ("",) if all_time else DEFAULT_KEYWORD_WINDOWS
    for window in windows:
        try:
            results: list[Json] = call_api(path, {**params, "after": window}) or []
        except ArchiveError as error:
            if error.exit_code != 3:
                raise
            continue
        note: str = f"searched the last {window}; pass --after/--before for another period" if window else ""
        return results, note
    raise ArchiveError(f"keyword search timed out even over a short window; {NARROWING_HINT}", 3)


def command_posts(args: argparse.Namespace) -> int:
    if not (args.sub or args.author):
        raise ArchiveError("posts needs --sub or --author (the archive rejects keyword search without one)", 2)
    params: dict[str, str | int] = {
        "subreddit": args.sub or "",
        "author": args.author or "",
        "query": args.query or "",
        "title": args.title or "",
        "after": args.after or "",
        "before": args.before or "",
        # The archive sorts only by date, so a score ranking needs the fullest page.
        "limit": 100 if args.by_score else args.limit,
        "sort": "asc" if args.asc else "desc",
    }
    posts: list[Json]
    note: str
    posts, note = keyword_search("posts/search", params, bool(args.query or args.title), args.all_time)
    if args.by_score and posts:
        dates: list[str] = sorted(_date(post.get("created_utc")) for post in posts)
        span: str = f"ranked {len(posts)} matches posted {dates[0]} to {dates[-1]}"
        if len(posts) >= 100:
            span += "; the archive returns 100 per request, so older matches were not ranked (set --before to reach them)"
        note = f"{note}; {span}" if note else span
        posts = sorted(posts, key=lambda post: post.get("score") or 0, reverse=True)[: args.limit]
    if args.json:
        print(json.dumps(posts, ensure_ascii=False, indent=1))
        return 0
    if note:
        print(f"note: {note}")
    if not posts:
        print("no matching posts (keyword search needs every word; try fewer or different words, or another period)")
        return 0
    for post in posts:
        print(format_post_line(post, args.width))
    return 0


def _children(listing: Any) -> list[Json]:
    """Return the child nodes of a ``replies`` listing, which may be "" or absent."""
    if isinstance(listing, dict):
        data: Any = listing.get("data", {})
        if isinstance(data, dict):
            children: Any = data.get("children", [])
            return children if isinstance(children, list) else []
    return []


def flatten_tree(nodes: list[Json], depth: int = 0) -> list[tuple[int, Json]]:
    """Depth-first list of (depth, comment), siblings ordered by score, highest first.

    Collapsed ``more`` stubs are skipped; raise ``--max-comments`` to fetch them.
    """
    comments: list[Json] = [node.get("data", node) for node in nodes if node.get("kind", "t1") == "t1"]
    comments.sort(key=lambda comment: comment.get("score") or 0, reverse=True)
    ordered: list[tuple[int, Json]] = []
    for comment in comments:
        ordered.append((depth, comment))
        ordered.extend(flatten_tree(_children(comment.get("replies")), depth + 1))
    return ordered


def comment_url(post: Json, comment: Json) -> str:
    return f"{post_url(post)}_/{comment.get('id', '')}/"


def command_thread(args: argparse.Namespace) -> int:
    post_id: str = parse_post_id(args.target)
    found: list[Json] = call_api("posts/ids", {"ids": post_id}) or []
    if not found:
        raise ArchiveError(f"post {post_id} is not in the archive (deleted before capture, or a wrong id)", 2)
    post: Json = found[0]
    tree: list[Json] = call_api("comments/tree", {"link_id": post_id, "limit": args.max_comments}) or []
    ordered: list[tuple[int, Json]] = flatten_tree(tree)
    if args.json:
        print(json.dumps({"post": post, "comments": tree}, ensure_ascii=False, indent=1))
        return 0

    out_dir: Path = Path(args.out) if args.out else Path(tempfile.gettempdir()) / "reddit-search"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path: Path = out_dir / f"{post_id}.md"
    full_lines: list[str] = [
        f"# {post.get('title', '')}",
        "",
        f"- url: {post_url(post)}",
        f"- author: u/{post.get('author', '?')}  date: {_date(post.get('created_utc'))}  "
        f"score: {post.get('score', '?')}  comments reported: {post.get('num_comments', '?')}  "
        f"comments archived: {len(ordered)}{_fresh_note(post.get('created_utc'))}",
        f"- link: {post.get('url', '')}" if not post.get("is_self", True) else "",
        "",
        str(post.get("selftext", "")).strip(),
        "",
        "## Comments (siblings by score)",
        "",
    ]
    for index, (depth, comment) in enumerate(ordered, start=1):
        indent: str = "  " * depth
        full_lines.append(
            f"{indent}[{index}] u/{comment.get('author', '?')}  score {comment.get('score', '?')}  "
            f"{_date(comment.get('created_utc'))}  {comment_url(post, comment)}"
        )
        body: str = str(comment.get("body", "")).strip()
        full_lines.extend(f"{indent}    {line}" for line in body.splitlines() if line.strip())
        full_lines.append("")
    out_path.write_text("\n".join(full_lines), encoding="utf-8")

    print(format_post_line(post, args.width))
    print(f"  author u/{post.get('author', '?')}  comments archived {len(ordered)}")
    selftext: str = str(post.get("selftext", "")).strip()
    if selftext:
        print(f"\n{_clip(selftext, args.body_width)}")
    print(f"\nTop {args.show} top-level comments by score, {args.replies} replies each:")
    shown: int = 0
    replies_left: int = 0
    for index, (depth, comment) in enumerate(ordered, start=1):
        if depth == 0:
            if shown >= args.show:
                break
            shown += 1
            replies_left = args.replies
        elif depth == 1 and replies_left > 0:
            replies_left -= 1
        else:
            continue
        prefix: str = "    " * depth
        print(f"{prefix}[{index}] score {comment.get('score', '?')}  u/{comment.get('author', '?')}: "
              f"{_clip(str(comment.get('body', '')), args.width)}")
    print(f"\nFull thread: {out_path}  (the [n] indices match; grep it rather than printing it all)")
    return 0


def command_comments(args: argparse.Namespace) -> int:
    link: str = parse_post_id(args.link) if args.link else ""
    if not (args.sub or args.author or link):
        raise ArchiveError("comments needs --sub, --author, or --link with --body", 2)
    params: dict[str, str | int] = {
        "subreddit": args.sub or "",
        "author": args.author or "",
        "link_id": link,
        "body": args.body or "",
        "after": args.after or "",
        "before": args.before or "",
        "limit": args.limit,
    }
    comments: list[Json]
    note: str
    # One post's comments are few enough to search without a default period.
    comments, note = keyword_search("comments/search", params, not link, args.all_time)
    if args.json:
        print(json.dumps(comments, ensure_ascii=False, indent=1))
        return 0
    if note:
        print(f"note: {note}")
    if not comments:
        print("no matching comments")
        return 0
    for comment in comments:
        post_id: str = str(comment.get("link_id", "")).removeprefix("t3_")
        url: str = f"https://www.reddit.com/r/{comment.get('subreddit', '_')}/comments/{post_id}/_/{comment.get('id', '')}/"
        print(f"{_date(comment.get('created_utc'))}  score {comment.get('score', '?')}  post {post_id}  "
              f"u/{comment.get('author', '?')}{_fresh_note(comment.get('created_utc'))}\n"
              f"  {_clip(str(comment.get('body', '')), args.width)}\n  {url}")
    return 0


def command_subs(args: argparse.Namespace) -> int:
    subs: list[Json] = call_api("subreddits/search", {"subreddit_prefix": args.prefix, "limit": args.limit}) or []
    if args.json:
        print(json.dumps(subs, ensure_ascii=False, indent=1))
        return 0
    for sub in subs:
        description: str = _clip(str(sub.get("public_description") or sub.get("title") or ""), args.width)
        print(f"r/{sub.get('display_name', '?')}  subscribers {sub.get('subscribers', '?')}  {description}")
    if not subs:
        print("no subreddits with that prefix")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--json", action="store_true", help="print raw archive JSON instead of the summary")
    parser.add_argument("--width", type=int, default=300, help="characters per title or comment in summaries")
    commands: Any = parser.add_subparsers(dest="command", required=True)

    posts: argparse.ArgumentParser = commands.add_parser("posts", help="keyword search posts in a subreddit or by an author")
    posts.add_argument("--sub", help="subreddit name, with or without r/")
    posts.add_argument("--author", help="username, with or without u/")
    posts.add_argument("--query", help="words that must all appear in title or body")
    posts.add_argument("--title", help="words that must all appear in the title")
    posts.add_argument("--after", help="date (2026-01-01) or offset (1year, 3m for months, 2d)")
    posts.add_argument("--before", help="date or offset")
    posts.add_argument("--limit", type=int, default=25, help="1 to 100")
    posts.add_argument("--asc", action="store_true", help="oldest first (default newest first)")
    posts.add_argument("--by-score", action="store_true", help="fetch 100 in the period and show the top --limit by score")
    posts.add_argument("--all-time", action="store_true", help="do not bound keyword searches to the last year")
    posts.set_defaults(handler=command_posts)

    thread: argparse.ArgumentParser = commands.add_parser("thread", help="read one post and its comment tree")
    thread.add_argument("target", help="reddit URL, redd.it link, t3_ fullname, or post id")
    thread.add_argument("--show", type=int, default=15, help="top-level comments to preview")
    thread.add_argument("--replies", type=int, default=2, help="replies to preview under each")
    thread.add_argument("--body-width", type=int, default=1500, help="characters of the post body to preview")
    thread.add_argument("--max-comments", type=int, default=3000, help="comments to fetch before collapsing")
    thread.add_argument("--out", help="directory for the full thread file (default: system temp/reddit-search)")
    thread.set_defaults(handler=command_thread)

    comments: argparse.ArgumentParser = commands.add_parser("comments", help="full-text search comments")
    comments.add_argument("--sub")
    comments.add_argument("--author")
    comments.add_argument("--link", help="restrict to one post (URL or id)")
    comments.add_argument("--body", required=True, help="search words; supports \"phrase\", OR, -exclude")
    comments.add_argument("--after")
    comments.add_argument("--before")
    comments.add_argument("--limit", type=int, default=25)
    comments.add_argument("--all-time", action="store_true", help="do not bound the search to the last year")
    comments.set_defaults(handler=command_comments)

    subs: argparse.ArgumentParser = commands.add_parser("subs", help="find subreddits by name prefix")
    subs.add_argument("prefix", help="start of the subreddit name, e.g. localllama or ask")
    subs.add_argument("--limit", type=int, default=15)
    subs.set_defaults(handler=command_subs)
    return parser


def main() -> int:
    args: argparse.Namespace = build_parser().parse_args()
    try:
        return int(args.handler(args))
    except ArchiveError as error:
        print(f"error: {error}", file=sys.stderr)
        return error.exit_code


if __name__ == "__main__":
    sys.exit(main())
