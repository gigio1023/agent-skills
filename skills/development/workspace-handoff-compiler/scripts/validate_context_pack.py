#!/usr/bin/env python3
"""Validate required keys, basic types, and enums in context-pack.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

TOP_LEVEL_TYPES: dict[str, type] = {
    "session_id": str,
    "timestamp_utc": str,
    "objective": str,
    "status": str,
    "artifacts": dict,
    "tasks": list,
    "risks": list,
    "decisions": list,
    "verification": list,
    "next_actions_top3": list,
    "swarm_continuation": dict,
}

STATUS_ENUM = {"complete", "partial", "blocked"}
TASK_STATUS_ENUM = {"todo", "in_progress", "blocked", "done"}
IMPACT_ENUM = {"low", "medium", "high"}
VERIFY_ENUM = {"pass", "fail", "unknown"}
MODE_ENUM = {"swarm_required", "single_agent_allowed"}


def _expect_type(errors: list[str], value: Any, expected: type, path: str) -> bool:
    if not isinstance(value, expected):
        errors.append(f"{path}: expected {expected.__name__}")
        return False
    return True


def _expect_enum(errors: list[str], value: Any, allowed: set[str], path: str) -> bool:
    if not isinstance(value, str) or value not in allowed:
        values = "|".join(sorted(allowed))
        errors.append(f"{path}: expected one of {values}")
        return False
    return True


def _is_str_or_null(value: Any) -> bool:
    return value is None or isinstance(value, str)


def _validate_object_shape(errors: list[str], data: dict[str, Any]) -> None:
    for key, expected_type in TOP_LEVEL_TYPES.items():
        if key not in data:
            errors.append(f"missing key: {key}")
            continue
        _expect_type(errors, data[key], expected_type, key)

    if "status" in data:
        _expect_enum(errors, data["status"], STATUS_ENUM, "status")

    artifacts = data.get("artifacts")
    if isinstance(artifacts, dict):
        for key in ("plan", "progress", "result"):
            if key not in artifacts:
                errors.append(f"artifacts.{key}: missing")
            elif not _is_str_or_null(artifacts[key]):
                errors.append(f"artifacts.{key}: expected string or null")

    tasks = data.get("tasks")
    if isinstance(tasks, list):
        for index, item in enumerate(tasks):
            path = f"tasks[{index}]"
            if not _expect_type(errors, item, dict, path):
                continue
            for required in ("id", "title", "status", "blocked_by", "next_action"):
                if required not in item:
                    errors.append(f"{path}.{required}: missing")
            if "id" in item:
                _expect_type(errors, item["id"], str, f"{path}.id")
            if "title" in item:
                _expect_type(errors, item["title"], str, f"{path}.title")
            if "status" in item:
                _expect_enum(errors, item["status"], TASK_STATUS_ENUM, f"{path}.status")
            if "owner" in item and not _is_str_or_null(item["owner"]):
                errors.append(f"{path}.owner: expected string or null")
            if "blocked_by" in item:
                if _expect_type(errors, item["blocked_by"], list, f"{path}.blocked_by"):
                    for j, dep in enumerate(item["blocked_by"]):
                        if not isinstance(dep, str):
                            errors.append(f"{path}.blocked_by[{j}]: expected string")
            if "next_action" in item:
                _expect_type(errors, item["next_action"], str, f"{path}.next_action")

    risks = data.get("risks")
    if isinstance(risks, list):
        for index, item in enumerate(risks):
            path = f"risks[{index}]"
            if not _expect_type(errors, item, dict, path):
                continue
            for required in ("id", "description", "impact", "mitigation"):
                if required not in item:
                    errors.append(f"{path}.{required}: missing")
            if "impact" in item:
                _expect_enum(errors, item["impact"], IMPACT_ENUM, f"{path}.impact")

    decisions = data.get("decisions")
    if isinstance(decisions, list):
        for index, item in enumerate(decisions):
            path = f"decisions[{index}]"
            if not _expect_type(errors, item, dict, path):
                continue
            for required in ("id", "decision", "reason", "date_utc"):
                if required not in item:
                    errors.append(f"{path}.{required}: missing")

    verification = data.get("verification")
    if isinstance(verification, list):
        for index, item in enumerate(verification):
            path = f"verification[{index}]"
            if not _expect_type(errors, item, dict, path):
                continue
            for required in ("name", "result", "evidence"):
                if required not in item:
                    errors.append(f"{path}.{required}: missing")
            if "result" in item:
                _expect_enum(errors, item["result"], VERIFY_ENUM, f"{path}.result")

    next_actions = data.get("next_actions_top3")
    if isinstance(next_actions, list):
        if len(next_actions) != 3:
            errors.append("next_actions_top3: expected exactly 3 items")
        for i, value in enumerate(next_actions):
            if not isinstance(value, str):
                errors.append(f"next_actions_top3[{i}]: expected string")

    swarm = data.get("swarm_continuation")
    if isinstance(swarm, dict):
        for required in (
            "mode",
            "recommended_roles",
            "writer_ownership",
            "parallel_tracks",
            "serialization_gates",
        ):
            if required not in swarm:
                errors.append(f"swarm_continuation.{required}: missing")
        if "mode" in swarm:
            _expect_enum(errors, swarm["mode"], MODE_ENUM, "swarm_continuation.mode")
        for key in ("recommended_roles", "writer_ownership", "parallel_tracks", "serialization_gates"):
            if key in swarm and _expect_type(errors, swarm[key], list, f"swarm_continuation.{key}"):
                for i, value in enumerate(swarm[key]):
                    if not isinstance(value, str):
                        errors.append(f"swarm_continuation.{key}[{i}]: expected string")

        mode = swarm.get("mode")
        if mode == "swarm_required":
            roles = swarm.get("recommended_roles")
            owners = swarm.get("writer_ownership")
            if isinstance(roles, list) and len(roles) == 0:
                errors.append("swarm_continuation.recommended_roles: non-empty for swarm_required mode")
            if isinstance(owners, list) and len(owners) == 0:
                errors.append("swarm_continuation.writer_ownership: non-empty for swarm_required mode")



def main() -> int:
    parser = argparse.ArgumentParser(description="Validate context-pack json schema essentials.")
    parser.add_argument("path", nargs="?", default="context-pack.json", help="Path to context-pack json file.")
    args = parser.parse_args()

    target = Path(args.path)
    if not target.exists():
        print(f"error: file not found: {target}", file=sys.stderr)
        return 2
    if not target.is_file():
        print(f"error: not a file: {target}", file=sys.stderr)
        return 2

    try:
        raw = target.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"error: failed to read {target}: {exc}", file=sys.stderr)
        return 2

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"error: invalid json: {exc.msg} (line {exc.lineno}, col {exc.colno})", file=sys.stderr)
        return 2

    if not isinstance(data, dict):
        print("error: top-level json must be an object", file=sys.stderr)
        return 1

    errors: list[str] = []
    _validate_object_shape(errors, data)

    if errors:
        print("error: validation failed:", file=sys.stderr)
        for item in errors:
            print(f"- {item}", file=sys.stderr)
        return 1

    print("ok: context-pack valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
