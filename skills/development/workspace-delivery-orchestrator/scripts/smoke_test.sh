#!/usr/bin/env bash
# 스모크 테스트: init_docs.sh 산출물의 positive path 와 plan heading 순서/중복
# negative path 를 함께 검증한다. 템플릿-검증기 계약과 validator fail-open 회귀를
# 커밋 단계에서 잡기 위한 것.
set -euo pipefail

# 이 스크립트가 있는 위치 기준으로 skill 디렉터리를 잡는다 (호출 위치에 의존하지 않음).
script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

# 임시 작업 디렉터리. 종료 시(성공/실패/중단 모두) 정리한다.
tmp_dir="$(mktemp -d)"
cleanup() { rm -rf "$tmp_dir"; }
trap cleanup EXIT

fail=0

# 1) 템플릿에서 plan.md / progress.md / result.md 를 생성한다.
echo "== init_docs.sh -> $tmp_dir =="
bash "$script_dir/init_docs.sh" "$tmp_dir"

# 2) 생성된 각 파일에 해당 validator 를 돌린다. 하나라도 exit 0 이 아니면 실패로 기록.
#    (파일명, validator 스크립트) 쌍을 순서대로 검증한다.
run_validator() {
  local doc="$1"      # 검증 대상 파일명 (tmp_dir 기준)
  local validator="$2" # validator 스크립트명 (script_dir 기준)
  echo "== $validator $doc =="
  if python3 "$script_dir/$validator" "$tmp_dir/$doc"; then
    echo "  exit=0"
  else
    local rc=$?
    echo "  exit=$rc (FAIL)"
    fail=1
  fi
}

run_validator "plan.md" "validate_plan.py"
run_validator "progress.md" "validate_progress.py"
run_validator "result.md" "validate_result.py"

expect_plan_reject() {
  local label="$1"
  local path="$2"
  echo "== validate_plan.py rejects $label =="
  if python3 "$script_dir/validate_plan.py" "$path" >/dev/null 2>&1; then
    echo "  unexpected exit=0 (FAIL)"
    fail=1
  else
    echo "  rejected as expected"
  fi
}

# Canonical headings are present but Goals and Background are reversed.
out_of_order="$tmp_dir/plan.out-of-order.md"
cat > "$out_of_order" <<'EOF'
# plan.md
## Intent (의도)
## Goals (목표)
## Background (배경)
## Expected Results (결과)
## Scope
## Constraints
## Acceptance Criteria
## Workstreams
## Dependency Graph
## Validation Plan
## Risks and Mitigations
## Parallelism Strategy
## Rollback / Containment Intent
EOF
expect_plan_reject "out-of-order headings" "$out_of_order"

# A second alias for the same required section must not be accepted silently.
duplicate="$tmp_dir/plan.duplicate.md"
cp "$tmp_dir/plan.md" "$duplicate"
cat >> "$duplicate" <<'EOF'

## Goals
EOF
expect_plan_reject "duplicate required heading" "$duplicate"

if [ "$fail" -ne 0 ]; then
  echo "SMOKE TEST FAILED" >&2
  exit 1
fi

echo "SMOKE TEST PASSED"
