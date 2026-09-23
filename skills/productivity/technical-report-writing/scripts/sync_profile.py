#!/usr/bin/env python3
"""Copy references/writing-profile.md into an instruction file between markers.

Usage:
    python3 scripts/sync_profile.py <instruction-file> [--check] [--source <profile>]

The block between ``<!-- writing-profile:start -->`` and ``<!-- writing-profile:end -->``
is replaced with the current profile text. A file without markers gets the block
appended. ``--check`` changes nothing and exits 1 when the file is out of date.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

START = "<!-- writing-profile:start -->"
END = "<!-- writing-profile:end -->"
DEFAULT_SOURCE = pathlib.Path(__file__).resolve().parent.parent / "references" / "writing-profile.md"


def render(target_text: str, profile_text: str) -> str:
    block = f"{START}\n{profile_text.rstrip()}\n{END}\n"
    start = target_text.find(START)
    end = target_text.find(END)
    if start == -1 and end == -1:
        base = target_text.rstrip("\n")
        return (base + "\n\n" if base else "") + block
    if start == -1 or end == -1 or end < start:
        raise ValueError("unpaired writing-profile markers")
    end_line = end + len(END)
    if target_text[end_line:end_line + 1] == "\n":
        end_line += 1
    return target_text[:start] + block + target_text[end_line:]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("target", type=pathlib.Path)
    parser.add_argument("--check", action="store_true", help="report drift without writing")
    parser.add_argument("--source", type=pathlib.Path, default=DEFAULT_SOURCE)
    args = parser.parse_args(argv)

    profile_text = args.source.read_text(encoding="utf-8")
    target_text = args.target.read_text(encoding="utf-8") if args.target.exists() else ""
    try:
        rendered = render(target_text, profile_text)
    except ValueError as exc:
        print(f"{args.target}: {exc}", file=sys.stderr)
        return 2
    if rendered == target_text:
        print(f"{args.target}: up to date")
        return 0
    if args.check:
        print(f"{args.target}: out of date")
        return 1
    args.target.write_text(rendered, encoding="utf-8")
    print(f"{args.target}: updated")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
