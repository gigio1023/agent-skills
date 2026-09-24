#!/usr/bin/env python3
"""Create one comparison-arm workspace from the packet template.

Usage:
    python3 make_arm.py <workspace-dir> --skills "<path or list>" \
        --source <report.md> --diff <pr.diff> \
        --keep-section "실험 설계의 mechanism과 비교 조건 설명" \
        --keep-reason "첫 후보를 먼저 고르는 이유" \
        --candidate-a "<name>" --candidate-b "<name>"

The workspace receives packet.md (placeholders filled), source-report.md, pr.diff,
and an empty out/ directory. Arms differ only in --skills, so the same command
with another skills value builds the next arm. Existing workspaces are refused.
"""
from __future__ import annotations

import argparse
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
TEMPLATE = HERE / "packet-template.md"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("workspace", type=pathlib.Path)
    parser.add_argument("--skills", required=True, help="skill paths the arm may read, one line each")
    parser.add_argument("--source", required=True, type=pathlib.Path, help="research document copied as source-report.md")
    parser.add_argument("--diff", required=True, type=pathlib.Path, help="PR diff copied as pr.diff")
    parser.add_argument("--keep-section", required=True)
    parser.add_argument("--keep-reason", required=True)
    parser.add_argument("--candidate-a", required=True)
    parser.add_argument("--candidate-b", required=True)
    args = parser.parse_args(argv)

    if args.workspace.exists():
        print(f"{args.workspace}: exists, refusing to overwrite", file=sys.stderr)
        return 2
    packet = TEMPLATE.read_text(encoding="utf-8")
    filled = (
        packet.replace("__SKILLS__", args.skills.strip())
        .replace("__KEEP_SECTION__", args.keep_section)
        .replace("__KEEP_REASON__", args.keep_reason)
        .replace("__CANDIDATE_A__", args.candidate_a)
        .replace("__CANDIDATE_B__", args.candidate_b)
    )
    if "__" in filled:
        print("unfilled placeholder remains in packet", file=sys.stderr)
        return 2
    (args.workspace / "out").mkdir(parents=True)
    (args.workspace / "packet.md").write_text(filled, encoding="utf-8")
    shutil.copyfile(args.source, args.workspace / "source-report.md")
    shutil.copyfile(args.diff, args.workspace / "pr.diff")
    print(f"{args.workspace}: packet.md, source-report.md, pr.diff, out/")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
