#!/usr/bin/env bash
set -euo pipefail

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
skill_dir="$(CDPATH= cd -- "$script_dir/.." && pwd)"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

expect_reject() {
  local label="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    echo "SMOKE TEST FAILED: expected rejection for $label" >&2
    exit 1
  fi
}

echo "== validate untouched templates =="
python3 "$script_dir/validate_handoff_md.py" \
  "$skill_dir/assets/templates/handoff.template.md"
python3 "$script_dir/validate_context_pack.py" \
  "$skill_dir/assets/templates/context-pack.template.json"
python3 "$script_dir/validate_handoff_parity.py" \
  "$skill_dir/assets/templates/handoff.template.md" \
  "$skill_dir/assets/templates/context-pack.template.json"

valid_dir="$tmp_dir/valid"
mkdir -p "$valid_dir"
cat > "$valid_dir/handoff.md" <<'EOF'
# Successor Handoff

## Session Summary
- One task completed.

## Objective/Status
| objective_id | objective | status | confidence | owner |
|---|---|---|---|---|
| O-001 | Verify handoff parity | done | high | agent |

## Completed
| task_id | what changed | why it matters | verification_refs |
|---|---|---|---|
| T-001 | Added claim-specific parity | Prevents unsupported completion | E-001 |

## In-Progress
- None.

## Blockers/Risks
- None.

## Decisions/Assumptions
- Verification IDs are shared across both artifacts.

## Evidence Index
| verification_id | artifact type | location or command | expected signal | notes |
|---|---|---|---|---|
| E-001 | command | `python3 validator.py` | exit code 0 | focused fixture |

## Next 3 Actions
1. [ ] Deliver the handoff.
2. [ ] None.
3. [ ] None.

## Continuation Plan
- Continuation mode: sequential_sufficient

## Handoff Quality Status
- Overall status: partial
EOF

cat > "$valid_dir/context-pack.json" <<'EOF'
{
  "session_id": "SESSION-TEST",
  "timestamp_utc": "2026-07-10T00:00:00Z",
  "objective": "Verify handoff parity",
  "status": "partial",
  "artifacts": {"plan": null, "progress": null, "result": null},
  "tasks": [
    {
      "id": "T-001",
      "title": "Add claim-specific parity",
      "status": "done",
      "owner": "agent",
      "blocked_by": [],
      "next_action": "",
      "verification_refs": ["E-001"]
    }
  ],
  "risks": [],
  "decisions": [],
  "verification": [
    {
      "id": "E-001",
      "name": "Focused parity fixture",
      "result": "pass",
      "evidence": "python3 validator.py exited 0"
    }
  ],
  "next_actions_top3": ["Deliver", "None", "None"],
  "continuation": {
    "continuation_mode": "sequential_sufficient",
    "recommended_roles": [],
    "writer_ownership": [],
    "parallel_tracks": [],
    "serialization_gates": []
  }
}
EOF

echo "== validate claim-specific positive fixture =="
python3 "$script_dir/validate_handoff_md.py" "$valid_dir/handoff.md"
python3 "$script_dir/validate_context_pack.py" "$valid_dir/context-pack.json"
python3 "$script_dir/validate_handoff_parity.py" \
  "$valid_dir/handoff.md" "$valid_dir/context-pack.json"

unsupported="$tmp_dir/unsupported-handoff.md"
sed 's/| T-001 | Added claim-specific parity | Prevents unsupported completion | E-001 |/| T-001 | Unsupported claim | No matching proof | E-MISSING |/' \
  "$valid_dir/handoff.md" > "$unsupported"
expect_reject "missing Completed verification" \
  python3 "$script_dir/validate_handoff_parity.py" \
  "$unsupported" "$valid_dir/context-pack.json"

unrelated="$tmp_dir/unrelated-context-pack.json"
cat > "$unrelated" <<'EOF'
{
  "session_id": "SESSION-TEST",
  "timestamp_utc": "2026-07-10T00:00:00Z",
  "objective": "Reject unrelated evidence",
  "status": "partial",
  "artifacts": {"plan": null, "progress": null, "result": null},
  "tasks": [
    {
      "id": "T-001",
      "title": "Unsupported completion",
      "status": "done",
      "owner": null,
      "blocked_by": [],
      "next_action": "",
      "verification_refs": ["E-002"]
    }
  ],
  "risks": [],
  "decisions": [],
  "verification": [
    {
      "id": "E-001",
      "name": "Unrelated passing check",
      "result": "pass",
      "evidence": "A different command exited 0"
    }
  ],
  "next_actions_top3": ["Fix evidence", "None", "None"],
  "continuation": {
    "continuation_mode": "sequential_sufficient",
    "recommended_roles": [],
    "writer_ownership": [],
    "parallel_tracks": [],
    "serialization_gates": []
  }
}
EOF
expect_reject "unrelated passing verification" \
  python3 "$script_dir/validate_context_pack.py" "$unrelated"

empty_evidence="$tmp_dir/empty-evidence.json"
sed 's/python3 validator.py exited 0/   /' \
  "$valid_dir/context-pack.json" > "$empty_evidence"
expect_reject "passing verification with empty evidence" \
  python3 "$script_dir/validate_context_pack.py" "$empty_evidence"

index_dir="$tmp_dir/index-conflict"
mkdir -p "$index_dir"
cat > "$index_dir/plan.md" <<'EOF'
# plan
EOF
cat > "$index_dir/progress.md" <<'EOF'
# progress
- status: done
EOF
cat > "$index_dir/task.md" <<'EOF'
# task
- status: blocked
EOF
cat > "$index_dir/result.md" <<'EOF'
# result
EOF
python3 "$script_dir/build_handoff_index.py" "$index_dir" > "$tmp_dir/index.json"
python3 - "$tmp_dir/index.json" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    index = json.load(handle)

assert [item["file"] for item in index["progress_candidates"]] == [
    "progress.md",
    "task.md",
]
assert index["artifacts"]["progress"] is None
assert index["progress_selection"] is None
assert index["status_artifact_selection_required"] is True
assert index["status_artifact_conflict"] is True
assert index["handoff_ready_hint"] is False
PY

echo "SMOKE TEST PASSED"
