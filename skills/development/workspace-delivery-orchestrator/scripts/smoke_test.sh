#!/usr/bin/env bash
# 스모크 테스트: init_docs.sh 로 임시 디렉터리에 산출물을 만들고,
# 세 validator (plan/progress/result) 를 그 산출물에 돌려 모두 exit 0 인지 확인한다.
# init -> validate 회귀(예: 템플릿에 누락된 heading) 를 커밋 단계에서 잡기 위한 것.
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

if [ "$fail" -ne 0 ]; then
  echo "SMOKE TEST FAILED" >&2
  exit 1
fi

echo "SMOKE TEST PASSED"
