#!/usr/bin/env python3
"""Append-only research journal.

append: writes one dated entry to the end of the journal; never rewrites existing text.
read:   prints entries, optionally only those older than N days or of one kind.
Exit 0 on success, 2 on usage errors. Python 3.10+, standard library only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
from pathlib import Path

KINDS = ("idea", "prediction", "hindsight", "review")
HEADING = re.compile(r"^## (\d{4}-\d{2}-\d{2}) (idea|prediction|hindsight|review): (.*)$")
DEFAULT = Path(os.environ.get("CREDO_JOURNAL", "~/research/journal.md")).expanduser()


def append(path: Path, kind: str, title: str, fields: list[str]) -> int:
    if kind not in KINDS:
        print(f"usage error: kind must be one of {', '.join(KINDS)}", file=sys.stderr)
        return 2
    if not title.strip() or "\n" in title:
        print("usage error: title must be one non-empty line", file=sys.stderr)
        return 2
    lines = [f"## {dt.date.today().isoformat()} {kind}: {title.strip()}"]
    for f in fields:
        if "=" not in f:
            print(f"usage error: --field needs key=value, got {f!r}", file=sys.stderr)
            return 2
        k, v = f.split("=", 1)
        lines.append(f"- {k.strip()}: {v.strip()}")
    if path.exists() and not path.is_file():
        print(f"usage error: {path} is not a file", file=sys.stderr)
        return 2
    path.parent.mkdir(parents=True, exist_ok=True)
    needs_gap = path.exists() and path.stat().st_size > 0 and not path.read_bytes().endswith(b"\n\n")
    with path.open("a", encoding="utf-8") as fh:  # append mode only; existing bytes are never rewritten
        if needs_gap:
            fh.write("\n" if path.read_bytes().endswith(b"\n") else "\n\n")
        fh.write("\n".join(lines) + "\n\n")
    print(f"appended\t{path}\t{lines[0]}")
    return 0


def read(path: Path, older_than: int | None, kind: str | None) -> int:
    if not path.is_file():
        print(f"usage error: {path} does not exist", file=sys.stderr)
        return 2
    cutoff = dt.date.today() - dt.timedelta(days=older_than) if older_than is not None else None
    keep = False
    shown = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        m = HEADING.match(line)
        if m:
            d = dt.date.fromisoformat(m.group(1))
            keep = (cutoff is None or d <= cutoff) and (kind is None or m.group(2) == kind)
            shown += keep
        if keep:
            print(line)
    print(f"summary\t{shown} entr{'y' if shown == 1 else 'ies'} shown", file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Append-only research journal.")
    ap.add_argument("--path", type=Path, default=DEFAULT, help=f"journal file (default {DEFAULT})")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("append", help="append one dated entry")
    a.add_argument("--kind", required=True, help="idea | prediction | hindsight | review")
    a.add_argument("--title", required=True)
    a.add_argument("--field", action="append", default=[], help="key=value (repeatable)")
    r = sub.add_parser("read", help="print entries")
    r.add_argument("--older-than", type=int, help="only entries dated at least N days ago")
    r.add_argument("--kind", help="only this kind")
    args = ap.parse_args(argv)
    if args.cmd == "append":
        return append(args.path, args.kind, args.title, args.field)
    return read(args.path, args.older_than, args.kind)


if __name__ == "__main__":
    sys.exit(main())
