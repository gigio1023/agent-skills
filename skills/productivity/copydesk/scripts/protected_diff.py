"""Show what changed outside the passages a revision instruction actually named.

A correction that says "fix the second paragraph" or "update the numbers under
Results" implicitly promises everything else stays put. This script makes that
promise checkable: it splits both versions into blocks, marks which blocks in
the PREVIOUS file were in scope for the named revision, and reports any
protected block that did not survive byte-identical into REVISED -- plus
anything new that showed up outside the named scope. It never rewrites either
file and always exits 0; it is evidence for the writer to read, not a gate.
"""

from __future__ import annotations

import argparse
import difflib
import sys
from dataclasses import dataclass

HEADING_RE_PREFIX = "#"


@dataclass
class Block:
    start: int
    end: int
    text: str
    kind: str
    heading: str | None


def classify(first_line: str, whole_text: str) -> str:
    """First line usually gives the shape away; equations and figures can start mid-block."""
    stripped = first_line.strip()
    if stripped.startswith("```") or stripped.startswith("~~~"):
        return "code"
    if stripped.startswith("#"):
        return "heading"
    if stripped.startswith("![") or stripped.lower().startswith("figure") or stripped.startswith("그림"):
        return "figure"
    if "$$" in whole_text or "\\[" in whole_text:
        return "equation"
    if stripped.count("|") >= 2:
        return "table"
    if stripped[:1] in ("-", "*", "+") or (stripped[:1].isdigit() and ". " in stripped[:4]):
        return "list"
    return "prose"


def split_blocks(text: str) -> list[Block]:
    """Blank lines separate blocks, except a fenced code block stays one block despite internal blank lines."""
    lines = text.splitlines()
    n = len(lines)
    blocks: list[Block] = []
    i = 0
    current_heading: str | None = None
    while i < n:
        if lines[i].strip() == "":
            i += 1
            continue
        start = i
        stripped = lines[i].lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            fence = stripped[:3]
            j = i + 1
            while j < n and not lines[j].lstrip().startswith(fence):
                j += 1
            end = min(j, n - 1)
            i = end + 1
        else:
            j = i
            while j < n and lines[j].strip() != "":
                j += 1
            end = j - 1
            i = j
        block_lines = lines[start : end + 1]
        block_text = "\n".join(block_lines)
        kind = classify(block_lines[0], block_text)
        heading_for_block = current_heading
        blocks.append(Block(start + 1, end + 1, block_text, kind, heading_for_block))
        if kind == "heading":
            current_heading = block_lines[0].lstrip(HEADING_RE_PREFIX).strip()
    return blocks


def parse_line_range(spec: str) -> tuple[int, int]:
    a, _, b = spec.partition("-")
    return int(a), int(b or a)


def is_allowed(block: Block, allow_terms: list[str], allow_ranges: list[tuple[int, int]]) -> bool:
    """A block is in scope if its own governing heading matches, or its lines fall in an explicit range."""
    if block.heading and any(term.lower() in block.heading.lower() for term in allow_terms):
        return True
    for lo, hi in allow_ranges:
        if block.start <= hi and block.end >= lo:
            return True
    return False


def find_closest(text: str, candidates: list[Block]) -> tuple[Block | None, float]:
    """The nearest match by similarity tells the reader edited (high ratio) from deleted (no close match)."""
    best_block: Block | None = None
    best_ratio = 0.0
    for cand in candidates:
        ratio = difflib.SequenceMatcher(None, text, cand.text).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_block = cand
    return best_block, best_ratio


def first_chars(text: str, n: int = 100) -> str:
    flat = " ".join(text.split())
    return flat if len(flat) <= n else flat[:n]


def build_report(
    previous_text: str,
    revised_text: str,
    allow_terms: list[str],
    allow_ranges: list[tuple[int, int]],
) -> str:
    prev_blocks = split_blocks(previous_text)
    rev_blocks = split_blocks(revised_text)
    rev_texts = {b.text for b in rev_blocks}
    prev_texts = {b.text for b in prev_blocks}

    protected = [b for b in prev_blocks if not is_allowed(b, allow_terms, allow_ranges)]
    changed = [b for b in protected if b.text not in rev_texts]

    added_candidates = [b for b in rev_blocks if b.text not in prev_texts]
    added = [b for b in added_candidates if not is_allowed(b, allow_terms, allow_ranges)]

    removed = [b for b in prev_blocks if b.text not in rev_texts]
    removed_counts: dict[str, int] = {}
    for b in removed:
        removed_counts[b.kind] = removed_counts.get(b.kind, 0) + 1

    lines: list[str] = []
    lines.append(f"CHANGED OUTSIDE ALLOWED SCOPE ({len(changed)})")
    for b in changed:
        closest, ratio = find_closest(b.text, rev_blocks)
        lines.append(f"  line {b.start}: {first_chars(b.text)}")
        if closest is not None:
            lines.append(f"    closest match in REVISED at line {closest.start} (ratio={ratio:.2f}): {first_chars(closest.text)}")
        else:
            lines.append("    no matching block in REVISED (deleted)")
    lines.append("")

    lines.append(f"ADDED OUTSIDE ALLOWED SCOPE ({len(added)})")
    for b in added:
        lines.append(f"  line {b.start}: {first_chars(b.text)}")
    lines.append("")

    lines.append("REMOVED CATEGORIES")
    for kind in ("heading", "table", "figure", "equation", "list", "prose", "code"):
        lines.append(f"  {kind}: {removed_counts.get(kind, 0)}")
    lines.append("")

    total = len(prev_blocks)
    protected_n = len(protected)
    changed_n = len(changed)
    added_n = len(added)
    retention = (protected_n - changed_n) / protected_n if protected_n else 1.0
    lines.append("SUMMARY")
    lines.append(f"  blocks total: {total}")
    lines.append(f"  protected: {protected_n}")
    lines.append(f"  changed: {changed_n}")
    lines.append(f"  added: {added_n}")
    lines.append(f"  retention ratio of protected blocks: {retention:.2f}")

    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Show what changed outside the scope a revision named.")
    parser.add_argument("previous", help="path to the pre-revision Markdown file")
    parser.add_argument("revised", help="path to the post-revision Markdown file")
    parser.add_argument(
        "--allow",
        action="append",
        default=[],
        metavar="HEADING_TEXT",
        help="heading text (case-insensitive substring) whose blocks are in scope; repeatable",
    )
    parser.add_argument(
        "--allow-lines",
        action="append",
        default=[],
        metavar="A-B",
        help="line range (in the PREVIOUS/REVISED file it applies to) that is in scope; repeatable",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    with open(args.previous, encoding="utf-8") as f:
        previous_text = f.read()
    with open(args.revised, encoding="utf-8") as f:
        revised_text = f.read()
    allow_ranges = [parse_line_range(spec) for spec in args.allow_lines]
    report = build_report(previous_text, revised_text, args.allow, allow_ranges)
    print(report)
    return 0  # evidence for the writer to read, not a gate


if __name__ == "__main__":
    sys.exit(main())
