#!/usr/bin/env python3
"""handoff.md 와 context-pack.json 사이의 cross-file 정합성을 검증한다.

단일 파일 검증기(validate_handoff_md.py, validate_context_pack.py)는 각 파일 내부만 본다.
이 스크립트는 두 파일을 함께 읽어 다음 두 가지 cross-file 불변식을 강제한다.

  1) overall 상태 동등성
     handoff.md 의 "Handoff Quality Status" 에 적힌 overall 상태(complete/partial/blocked)와
     context-pack.json 의 top-level "status" 가 같아야 한다.

  2) 완료 클레임마다 관련 검증 근거 존재
     handoff.md Completed 행의 task_id/verification_refs 와 context-pack.json 의
     done task/verification ID 를 대응시킨다. 각 완료 항목은 자기 task 가 참조한
     pass 결과와 비어 있지 않은 evidence 를 가져야 한다. 무관한 pass 하나로 여러
     완료 주장을 인증하지 않는다.

상태 어휘의 단일 출처는 references/context-pack-schema.md 의 Status Vocabulary 다.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

# overall 핸드오프 상태 집합 (per-task 집합과 분리)
OVERALL_STATUS_ENUM = {"complete", "partial", "blocked"}


def _read_text(path: Path, errors: list[str]) -> str | None:
    if not path.exists():
        errors.append(f"file not found: {path}")
        return None
    if not path.is_file():
        errors.append(f"not a file: {path}")
        return None
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"failed to read {path}: {exc}")
        return None


def _extract_handoff_status(text: str) -> str | None:
    """handoff.md 본문에서 overall 상태 토큰을 찾는다.

    1순위: 'Overall status:' 라벨이 붙은 줄의 값을 그대로 읽는다(가장 명시적).
    2순위: 라벨 줄이 없으면 본문에서 overall 상태 토큰을 단어 경계로 찾는다.
    어느 경우든 후보를 파이프로 나열한 placeholder 줄(예: 'complete | partial | blocked')은 건너뛴다.
    """
    # "complete | partial | blocked" 처럼 후보를 파이프로 나열한 placeholder 줄은 제외한다.
    candidate_line = re.compile(r"complete\s*\|\s*partial\s*\|\s*blocked")
    label = re.compile(r"overall\s+status\s*:?\s*[`'\"]?\s*(\w+)", re.IGNORECASE)

    # 1순위: 명시적 'Overall status:' 라벨 줄.
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or candidate_line.search(line):
            continue
        match = label.search(line)
        if match and match.group(1).lower() in OVERALL_STATUS_ENUM:
            return match.group(1).lower()

    # 2순위: 라벨이 없으면 본문 첫 overall 토큰.
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or candidate_line.search(line):
            continue
        for token in OVERALL_STATUS_ENUM:
            if re.search(rf"\b{token}\b", line):
                return token
    return None


def _section_lines(text: str, title: str) -> list[str]:
    """Return lines inside a Markdown section until the next peer heading."""
    lines = text.splitlines()
    wanted = re.sub(r"[^a-z0-9]+", "", title.lower())
    heading = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*$")
    start: int | None = None
    section_level = 0
    for index, line in enumerate(lines):
        match = heading.match(line)
        if not match:
            continue
        normalized = re.sub(r"[^a-z0-9]+", "", match.group(2).lower())
        if normalized == wanted:
            start = index + 1
            section_level = len(match.group(1))
            break
    if start is None:
        return []

    end = len(lines)
    for index in range(start, len(lines)):
        match = heading.match(lines[index])
        if match and len(match.group(1)) <= section_level:
            end = index
            break
    return lines[start:end]


def _table_cells(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.count("|") < 3:
        return []
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def _verification_refs(cell: str) -> list[str]:
    refs: list[str] = []
    for raw in cell.replace("<br/>", ",").replace("<br>", ",").split(","):
        value = raw.strip().strip("`")
        if value:
            refs.append(value)
    return refs


def _completed_rows(text: str) -> list[dict[str, Any]]:
    """Parse substantive rows from the handoff Completed table."""
    rows: list[dict[str, Any]] = []
    for line in _section_lines(text, "Completed"):
        cells = _table_cells(line)
        if len(cells) < 4:
            continue
        if cells[0].lower() in {"item", "task_id"}:
            continue
        if all(re.fullmatch(r":?-+:?", cell.replace(" ", "")) for cell in cells[:4]):
            continue
        task_id, changed, why, refs_cell = cells[:4]
        if not any((changed, why, refs_cell)):
            continue
        rows.append(
            {
                "task_id": task_id.strip("`"),
                "verification_refs": _verification_refs(refs_cell),
            }
        )
    return rows


def _tasks_by_id(pack: dict[str, Any]) -> dict[str, dict[str, Any]]:
    tasks = pack.get("tasks")
    if not isinstance(tasks, list):
        return {}
    return {
        task["id"]: task
        for task in tasks
        if isinstance(task, dict) and isinstance(task.get("id"), str) and task["id"].strip()
    }


def _verification_by_id(pack: dict[str, Any]) -> dict[str, dict[str, Any]]:
    verification = pack.get("verification")
    if not isinstance(verification, list):
        return {}
    return {
        item["id"]: item
        for item in verification
        if isinstance(item, dict) and isinstance(item.get("id"), str) and item["id"].strip()
    }


def _is_passing_evidence(item: dict[str, Any] | None) -> bool:
    return bool(
        item
        and item.get("result") == "pass"
        and isinstance(item.get("evidence"), str)
        and item["evidence"].strip()
    )


def _check_completed_claims(
    handoff_text: str, pack: dict[str, Any], errors: list[str]
) -> None:
    """Require claim-specific parity across the human and structured outputs.

    Free prose is not scanned for the word "done". Only Completed table rows and
    structured task statuses count as completion claims.
    """
    completed_rows = _completed_rows(handoff_text)
    tasks = _tasks_by_id(pack)
    verifications = _verification_by_id(pack)
    done_task_ids = {task_id for task_id, task in tasks.items() if task.get("status") == "done"}
    completed_task_ids: set[str] = set()

    for row in completed_rows:
        task_id = row["task_id"]
        refs = row["verification_refs"]
        if not task_id:
            errors.append("handoff.md Completed row: task_id is required")
            continue
        if task_id in completed_task_ids:
            errors.append(f"handoff.md Completed row: duplicate task_id '{task_id}'")
            continue
        completed_task_ids.add(task_id)

        task = tasks.get(task_id)
        if task is None:
            errors.append(f"handoff.md Completed row '{task_id}': task missing from context-pack.json")
            continue
        if task.get("status") != "done":
            errors.append(f"handoff.md Completed row '{task_id}': context task is not done")

        task_refs = task.get("verification_refs")
        task_ref_set = {
            ref for ref in task_refs if isinstance(ref, str) and ref.strip()
        } if isinstance(task_refs, list) else set()
        row_ref_set = set(refs)
        if not row_ref_set:
            errors.append(f"handoff.md Completed row '{task_id}': verification_refs required")
        elif row_ref_set != task_ref_set:
            errors.append(
                f"verification ref mismatch for '{task_id}': "
                f"handoff={sorted(row_ref_set)} context={sorted(task_ref_set)}"
            )

        for ref in row_ref_set:
            if not _is_passing_evidence(verifications.get(ref)):
                errors.append(
                    f"handoff.md Completed row '{task_id}': verification '{ref}' "
                    "must resolve to pass with non-empty evidence"
                )

    for task_id in sorted(done_task_ids - completed_task_ids):
        errors.append(f"context done task '{task_id}' missing from handoff.md Completed table")

    if pack.get("status") == "complete" and not done_task_ids:
        errors.append("overall complete status requires at least one done task with related evidence")


def check_parity(handoff_text: str, pack: dict[str, Any], errors: list[str]) -> None:
    # 1) overall 상태 동등성
    handoff_status = _extract_handoff_status(handoff_text)
    pack_status = pack.get("status")
    if handoff_status is None:
        errors.append(
            "handoff.md: overall status (complete/partial/blocked) not found in body"
        )
    elif not isinstance(pack_status, str) or pack_status not in OVERALL_STATUS_ENUM:
        errors.append("context-pack.json: top-level status missing or not in overall set")
    elif handoff_status != pack_status:
        errors.append(
            f"status mismatch: handoff.md='{handoff_status}' vs context-pack.json='{pack_status}'"
        )

    # 2) 완료 클레임마다 같은 task/verification ID 로 연결된 통과 근거가 존재
    _check_completed_claims(handoff_text, pack, errors)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate cross-file parity between handoff.md and context-pack.json."
    )
    parser.add_argument("handoff", help="Path to handoff.md")
    parser.add_argument("context_pack", help="Path to context-pack.json")
    args = parser.parse_args()

    errors: list[str] = []

    handoff_text = _read_text(Path(args.handoff), errors)
    pack_text = _read_text(Path(args.context_pack), errors)
    if handoff_text is None or pack_text is None:
        for item in errors:
            print(f"- {item}", file=sys.stderr)
        return 2

    try:
        pack = json.loads(pack_text)
    except json.JSONDecodeError as exc:
        print(
            f"error: invalid json in {args.context_pack}: {exc.msg} (line {exc.lineno}, col {exc.colno})",
            file=sys.stderr,
        )
        return 2
    if not isinstance(pack, dict):
        print("error: context-pack json top-level must be an object", file=sys.stderr)
        return 1

    check_parity(handoff_text, pack, errors)

    if errors:
        print("error: parity validation failed:", file=sys.stderr)
        for item in errors:
            print(f"- {item}", file=sys.stderr)
        return 1

    print("ok: handoff/context-pack parity valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
