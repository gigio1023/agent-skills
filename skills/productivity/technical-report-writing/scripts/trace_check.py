#!/usr/bin/env python3
"""List untraced blocks in a traced draft, count markers, and optionally strip them.

Usage:
    python3 scripts/trace_check.py <traced.md> [--strip <clean.md>]

A block is a run of non-blank lines. A block is traced when it ends with a
marker such as ``[src L12-L15]``, ``[src §2.3]``, ``[background]``,
``[assumption: ...]``, or ``[user: ...]``. Headings, code fences, and table
separator rows are not blocks that need a marker. --strip writes a copy with
every marker removed and nothing else changed. Exit status is always 0; the
report is evidence, not a verdict.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

MARKER_RE = re.compile(r"\s*\[(src [^\]]+|background|assumption: [^\]]+|user: [^\]]+)\]\s*$")
ANY_MARKER_RE = re.compile(r"\s*\[(src [^\]]+|background|assumption: [^\]]+|user: [^\]]+)\]")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")


def kind_of(marker: str) -> str:
    return marker.split(" ", 1)[0].rstrip(":")


def blocks(lines: list[str]) -> list[tuple[int, int]]:
    """Return (start, end) line index pairs for runs of non-blank lines outside code fences."""
    out: list[tuple[int, int]] = []
    start: int | None = None
    in_code = False
    for i, line in enumerate(lines):
        if line.strip().startswith(("```", "~~~")):
            in_code = not in_code
            if start is not None:
                out.append((start, i - 1))
                start = None
            continue
        if in_code:
            continue
        if line.strip():
            if start is None:
                start = i
        elif start is not None:
            out.append((start, i - 1))
            start = None
    if start is not None:
        out.append((start, len(lines) - 1))
    return out


def analyze(text: str) -> tuple[list[tuple[int, str]], dict[str, int]]:
    lines = text.splitlines()
    untraced: list[tuple[int, str]] = []
    counts: dict[str, int] = {"src": 0, "background": 0, "assumption": 0, "user": 0}
    for start, end in blocks(lines):
        # Table rows and list items are one block each; split them so every row is checked.
        units: list[tuple[int, str]] = []
        seg = lines[start:end + 1]
        if all(s.lstrip().startswith("|") for s in seg) or all(re.match(r"\s*([-*+]|\d+\.)\s", s) for s in seg):
            units = [(start + k, s) for k, s in enumerate(seg)]
        else:
            units = [(start, " ".join(s.strip() for s in seg))]
        for idx, (lineno, unit) in enumerate(units):
            stripped = unit.strip()
            if not stripped or stripped.startswith("#") or TABLE_SEP_RE.match(stripped):
                continue
            if idx + 1 < len(units) and TABLE_SEP_RE.match(units[idx + 1][1].strip()):
                continue  # table header row
            m = MARKER_RE.search(unit)
            if m:
                counts[kind_of(m.group(1))] += 1
            else:
                untraced.append((lineno + 1, stripped[:80]))
    return untraced, counts


def strip(text: str) -> str:
    """Remove markers outside code fences; every other byte stays."""
    out: list[str] = []
    in_code = False
    for line in text.splitlines():
        if line.strip().startswith(("```", "~~~")):
            in_code = not in_code
            out.append(line)
            continue
        if not in_code and ANY_MARKER_RE.search(line):
            out.append(ANY_MARKER_RE.sub("", line).rstrip())
        else:
            out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("traced", type=pathlib.Path)
    parser.add_argument("--strip", type=pathlib.Path, help="write the clean copy here")
    args = parser.parse_args(argv)
    text = args.traced.read_text(encoding="utf-8")
    untraced, counts = analyze(text)
    print(f"UNTRACED BLOCKS ({len(untraced)})")
    for lineno, head in untraced:
        print(f"  line {lineno}: {head}")
    print("MARKERS")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    if args.strip:
        args.strip.write_text(strip(text), encoding="utf-8")
        print(f"CLEAN COPY {args.strip}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
