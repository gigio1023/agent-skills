#!/usr/bin/env python3
"""Validate required section headings in handoff.md."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = [
    "Session Summary",
    "Objective/Status",
    "Completed",
    "In-Progress",
    "Blockers/Risks",
    "Decisions/Assumptions",
    "Evidence Index",
    "Next 3 Actions",
    "Continuation Plan",
    "Handoff Quality Status",
]


def _normalize_heading(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def _extract_headings(text: str) -> set[str]:
    pattern = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", re.MULTILINE)
    return {_normalize_heading(match.group(1).strip()) for match in pattern.finditer(text)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate required headings in handoff markdown.")
    parser.add_argument("path", nargs="?", default="handoff.md", help="Path to handoff markdown file.")
    args = parser.parse_args()

    target = Path(args.path)
    if not target.exists():
        print(f"error: file not found: {target}", file=sys.stderr)
        return 2
    if not target.is_file():
        print(f"error: not a file: {target}", file=sys.stderr)
        return 2

    try:
        text = target.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"error: failed to read {target}: {exc}", file=sys.stderr)
        return 2

    found = _extract_headings(text)
    missing = [heading for heading in REQUIRED_HEADINGS if _normalize_heading(heading) not in found]
    if missing:
        print("error: missing required headings:", file=sys.stderr)
        for heading in missing:
            print(f"- {heading}", file=sys.stderr)
        return 1

    print("ok: handoff headings valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
