#!/usr/bin/env python3
"""handoff.md 와 context-pack.json 사이의 cross-file 정합성을 검증한다.

단일 파일 검증기(validate_handoff_md.py, validate_context_pack.py)는 각 파일 내부만 본다.
이 스크립트는 두 파일을 함께 읽어 다음 두 가지 cross-file 불변식을 강제한다.

  1) overall 상태 동등성
     handoff.md 의 "Handoff Quality Status" 에 적힌 overall 상태(complete/partial/blocked)와
     context-pack.json 의 top-level "status" 가 같아야 한다.

  2) 완료 클레임마다 검증 근거 존재
     완료(complete/done)로 표시된 항목이 하나라도 있으면,
     context-pack.json 의 verification 배열에 result == "pass" 인 항목이 최소 1개 있어야 한다.
     근거 없는 완료 주장(claiming complete without evidence)을 막기 위한 검사다.

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


def _has_completed_claim(pack: dict[str, Any]) -> bool:
    """완료로 표시된 항목이 하나라도 있는지 본다.

    구조화된 context-pack 데이터만 근거로 쓴다(자유 서술의 'done' 단어는 무시).
    근거: overall status == complete, 또는 어떤 task 의 status == done.
    문서 안 어휘 설명 문장에 'done' 이 들어가 있어도 오탐하지 않도록 본문 스캔은 하지 않는다.
    """
    if pack.get("status") == "complete":
        return True
    tasks = pack.get("tasks")
    if isinstance(tasks, list):
        for task in tasks:
            if isinstance(task, dict) and task.get("status") == "done":
                return True
    return False


def _has_passing_verification(pack: dict[str, Any]) -> bool:
    verification = pack.get("verification")
    if not isinstance(verification, list):
        return False
    return any(
        isinstance(item, dict) and item.get("result") == "pass" for item in verification
    )


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

    # 2) 완료 클레임마다 검증 근거 존재
    if _has_completed_claim(pack) and not _has_passing_verification(pack):
        errors.append(
            "completed claim present but no passing verification entry in context-pack.json"
        )


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
