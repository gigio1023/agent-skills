#!/usr/bin/env python3
import re
import sys
from pathlib import Path

RE_HEADING = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*$")
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


def heading_sequence(path: Path) -> list[tuple[int, str]]:
    headings: list[tuple[int, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = RE_HEADING.match(line)
        if m:
            headings.append((len(m.group(1)), normalize(m.group(2))))
    return headings


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "plan.md")
    if not path.exists():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2
    if not path.is_file():
        print(f"error: not a file: {path}", file=sys.stderr)
        return 2

    headings = heading_sequence(path)
    matches: list[tuple[str, list[int]]] = []
    for label, options in REQUIRED:
        positions = [
            index
            for index, (level, heading) in enumerate(headings)
            if level == 2 and heading in options
        ]
        matches.append((label, positions))

    errors: list[str] = []
    missing = [label for label, positions in matches if not positions]
    if missing:
        errors.append(f"missing H2 headings: {', '.join(missing)}")

    duplicates = [label for label, positions in matches if len(positions) > 1]
    if duplicates:
        errors.append(f"duplicate required headings: {', '.join(duplicates)}")

    if not missing and not duplicates:
        actual_positions = [positions[0] for _, positions in matches]
        if actual_positions != sorted(actual_positions):
            actual_order = [
                label
                for _, label in sorted(
                    (positions[0], label) for label, positions in matches
                )
            ]
            expected_order = [label for label, _ in REQUIRED]
            errors.append(
                "required headings out of order; "
                f"expected {expected_order}, found {actual_order}"
            )

    if errors:
        print(f"error: invalid plan structure in {path}:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"ok: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
