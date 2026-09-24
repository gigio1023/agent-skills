#!/usr/bin/env python3
"""Print the automatic measurement row for one or more arm workspaces.

Usage:
    python3 auto_measures.py <workspace> [<workspace> ...] [--allow "<heading>" ...]

For each workspace it runs the writer's check_draft.py on out/draft.md and
protected_diff.py on draft→r1, r1→r2, r2→r3, then prints one Markdown row:
draft flags, negation_definition flags, r1 retention ratio, blocks changed or
added outside scope in r2 and r3. --allow passes the corrected heading(s) to
protected_diff for every step; without it every block counts as protected.
The scripts flag candidates; this row is evidence for the scorer, never a verdict.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
SCRIPTS = HERE.parents[2] / "skills" / "productivity" / "copydesk" / "scripts"


def run(cmd: list[str]) -> str:
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def draft_flags(path: pathlib.Path) -> tuple[str, str]:
    out = run([sys.executable, str(SCRIPTS / "check_draft.py"), str(path)])
    total = re.search(r"findings: (\d+)", out)
    neg = re.search(r"negation_definition=(\d+)", out)
    return (total.group(1) if total else "?", neg.group(1) if neg else "?")


def step(prev: pathlib.Path, new: pathlib.Path, allow: list[str]) -> tuple[str, str]:
    cmd = [sys.executable, str(SCRIPTS / "protected_diff.py"), str(prev), str(new)]
    for a in allow:
        cmd += ["--allow", a]
    out = run(cmd)
    ret = re.search(r"retention ratio of protected blocks: ([0-9.]+)", out)
    changed = re.search(r"changed: (\d+)", out)
    added = re.search(r"added: (\d+)", out)
    outside = str(int(changed.group(1)) + int(added.group(1))) if changed and added else "?"
    return (ret.group(1) if ret else "?", outside)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("workspaces", nargs="+", type=pathlib.Path)
    parser.add_argument("--allow", action="append", default=[], help="heading in scope for every revision step")
    args = parser.parse_args(argv)

    print("| arm | draft flags | negation_definition | r1 retention | r2 outside scope | r3 outside scope |")
    print("|---|---|---|---|---|---|")
    for ws in args.workspaces:
        out = ws / "out"
        files = {n: out / f"{n}.md" for n in ("draft", "r1", "r2", "r3")}
        missing = [n for n, p in files.items() if not p.exists()]
        if missing:
            print(f"| {ws.name} | missing: {', '.join(missing)} | | | | |")
            continue
        total, neg = draft_flags(files["draft"])
        r1_ret, _ = step(files["draft"], files["r1"], args.allow)
        _, r2_out = step(files["r1"], files["r2"], args.allow)
        _, r3_out = step(files["r2"], files["r3"], args.allow)
        print(f"| {ws.name} | {total} | {neg} | {r1_ret} | {r2_out} | {r3_out} |")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
