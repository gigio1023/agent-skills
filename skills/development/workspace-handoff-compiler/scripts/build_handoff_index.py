#!/usr/bin/env python3
"""Build a concise JSON index of handoff-related artifacts in the current directory."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _first_heading(text: str) -> str | None:
    pattern = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", re.MULTILINE)
    match = pattern.search(text)
    return match.group(1).strip() if match else None


def _file_summary(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    stat = path.stat()
    return {
        "file": path.name,
        "size_bytes": stat.st_size,
        "line_count": text.count("\n") + (1 if text and not text.endswith("\n") else 0),
        "modified_at": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
        "first_heading": _first_heading(text),
    }


def build_index(base_dir: Path) -> dict[str, Any]:
    plan_path = base_dir / "plan.md"
    progress_path = base_dir / "progress.md"
    task_path = base_dir / "task.md"
    result_path = base_dir / "result.md"

    progress_selected: Path | None = None
    if progress_path.is_file():
        progress_selected = progress_path
    elif task_path.is_file():
        progress_selected = task_path

    artifacts: dict[str, dict[str, Any] | None] = {
        "plan": _file_summary(plan_path) if plan_path.is_file() else None,
        "progress": _file_summary(progress_selected) if progress_selected else None,
        "result": _file_summary(result_path) if result_path.is_file() else None,
    }

    missing = [name for name, value in artifacts.items() if value is None]
    present = [name for name, value in artifacts.items() if value is not None]

    return {
        "cwd": str(base_dir.resolve()),
        "generated_at": datetime.now(tz=timezone.utc).isoformat(),
        "artifacts": artifacts,
        "present": present,
        "missing": missing,
        "handoff_ready_hint": not missing,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect current directory and summarize plan/progress/task/result markdown artifacts."
    )
    parser.add_argument(
        "--dir",
        default=".",
        help="Directory to inspect (default: current directory).",
    )
    args = parser.parse_args()

    base_dir = Path(args.dir)
    if not base_dir.exists():
        print(f"error: directory not found: {base_dir}", file=sys.stderr)
        return 2
    if not base_dir.is_dir():
        print(f"error: not a directory: {base_dir}", file=sys.stderr)
        return 2

    try:
        summary = build_index(base_dir)
    except OSError as exc:
        print(f"error: failed to inspect files: {exc}", file=sys.stderr)
        return 2

    json.dump(summary, sys.stdout, ensure_ascii=False, separators=(",", ":"))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
