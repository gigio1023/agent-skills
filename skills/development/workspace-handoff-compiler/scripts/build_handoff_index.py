#!/usr/bin/env python3
"""Build a concise JSON index of handoff-related artifacts in the current directory."""

from __future__ import annotations

import argparse
import hashlib
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
        "content_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "first_heading": _first_heading(text),
    }


def build_index(base_dir: Path) -> dict[str, Any]:
    plan_path = base_dir / "plan.md"
    progress_path = base_dir / "progress.md"
    task_path = base_dir / "task.md"
    result_path = base_dir / "result.md"

    progress_candidates = [
        _file_summary(path)
        for path in (progress_path, task_path)
        if path.is_file()
    ]
    status_selection_required = len(progress_candidates) > 1
    status_artifact_conflict = (
        status_selection_required
        and len({item["content_sha256"] for item in progress_candidates}) > 1
    )
    progress_selected = progress_candidates[0] if len(progress_candidates) == 1 else None

    artifacts: dict[str, dict[str, Any] | None] = {
        "plan": _file_summary(plan_path) if plan_path.is_file() else None,
        # Never silently prefer progress.md when task.md also exists. The caller
        # must resolve authority before this slot receives a selected artifact.
        "progress": progress_selected,
        "result": _file_summary(result_path) if result_path.is_file() else None,
    }

    availability = {
        "plan": artifacts["plan"] is not None,
        "progress": bool(progress_candidates),
        "result": artifacts["result"] is not None,
    }
    missing = [name for name, available in availability.items() if not available]
    present = [name for name, available in availability.items() if available]

    return {
        "cwd": str(base_dir.resolve()),
        "generated_at": datetime.now(tz=timezone.utc).isoformat(),
        "artifacts": artifacts,
        "progress_candidates": progress_candidates,
        "progress_selection": progress_selected["file"] if progress_selected else None,
        "status_artifact_selection_required": status_selection_required,
        "status_artifact_conflict": status_artifact_conflict,
        "present": present,
        "missing": missing,
        "handoff_ready_hint": not missing and not status_selection_required,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect a directory and summarize plan/progress/task/result markdown artifacts."
    )
    # 디렉터리는 두 가지 형태를 모두 받는다.
    #   1) 위치 인자: build_handoff_index.py <artifact_dir>  (문서에 표기된 형태)
    #   2) 옵션 인자: build_handoff_index.py --dir <artifact_dir>
    # 위치 인자를 생략하면 --dir 값(기본 ".")을 그대로 쓴다. 둘 다 주면 위치 인자가 우선한다.
    parser.add_argument(
        "--dir",
        default=".",
        help="Directory to inspect (default: current directory).",
    )
    parser.add_argument(
        "dir_pos",
        nargs="?",
        default=None,
        metavar="artifact_dir",
        help="Directory to inspect (positional form; defaults to --dir value).",
    )
    args = parser.parse_args()

    # 위치 인자가 주어졌으면 그 값을, 아니면 --dir 값을 사용한다.
    target = args.dir_pos if args.dir_pos is not None else args.dir
    base_dir = Path(target)
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
