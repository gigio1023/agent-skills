#!/usr/bin/env python3
import re
import sys
from pathlib import Path

RE_HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*$")
REQUIRED = [
    ("Intent", ("intent", "intent (의도)", "objective")),
    ("Background", ("background", "background (배경)", "background and context")),
    ("Goals", ("goals", "goals (목표)")),
    ("Expected Results", ("expected results", "expected results (결과)", "result", "results")),
    ("Scope", ("scope",)),
    ("Constraints", ("constraints",)),
    ("Success Criteria/Acceptance Criteria", ("success criteria", "acceptance criteria")),
    ("Workstreams", ("workstreams",)),
    ("Dependency Graph/Dependencies", ("dependency graph", "dependencies")),
    ("Validation Gates/Validation Plan", ("validation gates", "validation plan")),
    ("Risks and Mitigations", ("risks and mitigations",)),
    (
        "Execution Order/Parallelism Strategy",
        ("execution order", "parallelism strategy", "execution waves / order"),
    ),
    ("Rollback/Containment", ("rollback", "rollback / containment intent", "rollback/containment intent", "containment")),
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
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "plan.md")
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
