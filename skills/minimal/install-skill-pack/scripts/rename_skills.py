#!/usr/bin/env python3
"""Write renamed copies of upstream skill packages for a local install.

Usage:
    python3 scripts/rename_skills.py <checkout> --out <dir> --source <repo> [--renames-file <json>]
    python3 scripts/rename_skills.py <checkout> --out <dir> --rename OLD=NEW [--rename OLD=NEW ...]

The renames file maps a normalized source (``github.com/owner/repo``) to ``{"old": "new"}``.
A renamed package gets the new frontmatter ``name`` and folder. Every package in the
selection is also scanned for references to an old name (``/old``,
``Skill tool with "old"``, ``the `old` skill``, and an exact backticked ``old``) and
rewritten. Packages that change are copied under ``<dir>/skills/<name>``; the rest are
listed as unchanged so they can install from the remote source. Other quoted mentions
of an old name are reported for review and left as written. A JSON summary goes to
stdout.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import shutil
import sys

DEFAULT_RENAMES_FILE = pathlib.Path.home() / ".agents" / "skill-pack-renames.json"
TEXT_SUFFIXES = {".md", ".markdown", ".txt", ".yaml", ".yml", ".json", ".toml"}
MAX_TEXT_BYTES = 2 * 1024 * 1024
NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def normalize_source(source: str) -> str:
    """Return ``host/owner/repo`` for GitHub shorthand, HTTPS, or SSH clone URLs."""
    value = source.strip().split("#", 1)[0].rstrip("/")
    value = re.sub(r"\.git$", "", value)
    ssh = re.match(r"^[\w.-]+@([\w.-]+):(.+)$", value)
    if ssh:
        value = f"{ssh.group(1)}/{ssh.group(2)}"
    value = re.sub(r"^[a-z][a-z0-9+.-]*://", "", value)
    if re.match(r"^[\w.-]+/[\w.-]+$", value):
        value = f"github.com/{value}"
    return value.lower()


def frontmatter_name(skill_md: pathlib.Path) -> str | None:
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            return None
        match = re.match(r"^name:\s*[\"']?([^\"'\s]+)[\"']?\s*$", line)
        if match:
            return match.group(1)
    return None


def discover(checkout: pathlib.Path) -> dict[str, pathlib.Path]:
    packages: dict[str, pathlib.Path] = {}
    for skill_md in sorted(checkout.rglob("SKILL.md")):
        if ".git" in skill_md.relative_to(checkout).parts:
            continue
        name = frontmatter_name(skill_md)
        if name is None:
            continue
        if name in packages:
            raise ValueError(f"duplicate skill name {name!r}: {packages[name]} and {skill_md.parent}")
        packages[name] = skill_md.parent
    return packages


def invocation_patterns(old: str, new: str) -> list[tuple[re.Pattern[str], str]]:
    name = re.escape(old)
    return [
        (re.compile(rf"(?<![\w./-])/{name}(?![\w/-])"), f"/{new}"),
        (re.compile(rf"(Skill tool with\s+)([\"'`]){name}\2"), rf"\g<1>\g<2>{new}\g<2>"),
        (re.compile(rf"([\"'`]){name}\1(\s+skill\b)"), rf"\g<1>{new}\g<1>\g<2>"),
        (re.compile(rf"(?<!`)`{name}`(?!`)"), f"`{new}`"),
    ]


def review_pattern(old: str) -> re.Pattern[str]:
    return re.compile(rf"([\"'`]){re.escape(old)}\1")


def rewrite_text(text: str, renames: dict[str, str], rename_frontmatter: str | None) -> str:
    if rename_frontmatter is not None:
        new = renames[rename_frontmatter]
        head, sep, rest = text.partition("\n---")
        head = re.sub(
            rf"^name:\s*[\"']?{re.escape(rename_frontmatter)}[\"']?\s*$",
            f"name: {new}",
            head,
            count=1,
            flags=re.MULTILINE,
        )
        text = head + sep + rest
    for old, new in renames.items():
        for pattern, replacement in invocation_patterns(old, new):
            text = pattern.sub(replacement, text)
    return text


def text_files(package: pathlib.Path) -> list[pathlib.Path]:
    return sorted(
        path for path in package.rglob("*")
        if path.is_file() and not path.is_symlink() and path.suffix.lower() in TEXT_SUFFIXES
    )


def plan_package(name: str, package: pathlib.Path, renames: dict[str, str]) -> tuple[dict[pathlib.Path, str], list[dict], list[dict]]:
    """Return rewritten texts by relative path, changed lines, and lines left for review."""
    rewritten: dict[pathlib.Path, str] = {}
    changes: list[dict] = []
    review: list[dict] = []
    for path in text_files(package):
        relative = path.relative_to(package)
        if path.stat().st_size > MAX_TEXT_BYTES:
            review.append({"skill": name, "file": str(relative), "line": 0, "text": "skipped: larger than 2 MiB"})
            continue
        original = path.read_text(encoding="utf-8")
        frontmatter_owner = name if relative == pathlib.Path("SKILL.md") and name in renames else None
        updated = rewrite_text(original, renames, frontmatter_owner)
        if updated != original:
            rewritten[relative] = updated
            for number, (before, after) in enumerate(zip(original.splitlines(), updated.splitlines()), start=1):
                if before != after:
                    changes.append({"skill": name, "file": str(relative), "line": number, "after": after.strip()})
        for number, line in enumerate(updated.splitlines(), start=1):
            if any(review_pattern(old).search(line) for old in renames):
                review.append({"skill": name, "file": str(relative), "line": number, "text": line.strip()})
    return rewritten, changes, review


def load_renames(args: argparse.Namespace) -> tuple[str | None, dict[str, str]]:
    source_key = normalize_source(args.source) if args.source else None
    renames: dict[str, str] = {}
    if source_key and args.renames_file.exists():
        data = json.loads(args.renames_file.read_text(encoding="utf-8"))
        entry = data.get(source_key, {})
        if not isinstance(entry, dict):
            raise ValueError(f"{args.renames_file}: entry for {source_key} must be an object")
        renames.update(entry)
    for item in args.rename:
        old, sep, new = item.partition("=")
        if not sep:
            raise ValueError(f"--rename expects OLD=NEW, got {item!r}")
        renames[old] = new
    for old, new in renames.items():
        if not NAME_PATTERN.match(old) or not NAME_PATTERN.match(new) or old == new:
            raise ValueError(f"invalid rename {old!r} -> {new!r}")
    return source_key, renames


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("checkout", type=pathlib.Path, help="reviewed source checkout")
    parser.add_argument("--out", type=pathlib.Path, required=True, help="new or empty output directory")
    parser.add_argument("--source", help="repository source used to look up the renames file")
    parser.add_argument("--renames-file", type=pathlib.Path, default=DEFAULT_RENAMES_FILE)
    parser.add_argument("--rename", action="append", default=[], metavar="OLD=NEW")
    parser.add_argument("--skill", action="append", default=[], help="original skill name to consider; default all")
    args = parser.parse_args(argv)

    try:
        source_key, renames = load_renames(args)
        packages = discover(args.checkout)
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    selection = args.skill or sorted(packages)
    unknown = sorted(name for name in selection if name not in packages)
    if not renames and not unknown:
        print(json.dumps({"source": source_key, "renames": {}, "written": [], "unchanged": selection}, indent=2))
        return 0
    missing = sorted(old for old in renames if old not in packages)
    clashes = sorted(new for old, new in renames.items() if new in packages and new not in renames)
    if missing or clashes or unknown:
        print(f"error: renamed skill not in source: {missing}; new name already in source: {clashes}; unknown selection: {unknown}", file=sys.stderr)
        return 2
    if args.out.exists() and any(args.out.iterdir()):
        print(f"error: output directory is not empty: {args.out}", file=sys.stderr)
        return 2

    written: list[str] = []
    unchanged: list[str] = []
    changes: list[dict] = []
    review: list[dict] = []
    for name in selection:
        rewritten, package_changes, package_review = plan_package(name, packages[name], renames)
        review.extend(package_review)
        if not rewritten:
            unchanged.append(name)
            continue
        target_name = renames.get(name, name)
        target = args.out / "skills" / target_name
        shutil.copytree(packages[name], target, symlinks=True, ignore=shutil.ignore_patterns(".git"))
        for relative, text in rewritten.items():
            (target / relative).write_text(text, encoding="utf-8")
        written.append(target_name)
        changes.extend(package_changes)

    print(json.dumps({
        "source": source_key,
        "renames": renames,
        "written": written,
        "unchanged": unchanged,
        "changes": changes,
        "review": review,
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
