#!/usr/bin/env python3
import re
import sys
from pathlib import Path

RE_HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*$")
REQUIRED = [
    ("Summary/Final Summary", ("summary", "final summary")),
    ("Completed Outcomes/Goal-by-Goal Outcome", ("completed outcomes", "goal-by-goal outcome")),
    ("Evidence", ("evidence", "evidence-backed validation")),
    ("Pending Items/Follow-Ups", ("pending items", "follow-ups")),
    ("Risks and Decisions/Risk and Incident Review", ("risks and decisions", "risk and incident review")),
    ("Next Minimal Actions/Handoff Notes for Next AI", ("next minimal actions", "handoff notes for next ai")),
    ("Handoff Status/Result Metadata", ("handoff status", "result metadata")),
]


def normalize(text: str) -> str:
    return " ".join(text.strip().strip("#").lower().split())


def heading_set(path: Path) -> set[str]:
    headings: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        m = RE_HEADING.match(line)
        if m:
            headings.add(normalize(m.group(1)))
    return headings


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "result.md")
    if not path.exists():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2

    headings = heading_set(path)
    missing = [label for label, options in REQUIRED if not any(x in headings for x in options)]
    if missing:
        print(f"error: missing headings in {path}: {', '.join(missing)}", file=sys.stderr)
        return 1

    print(f"ok: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
