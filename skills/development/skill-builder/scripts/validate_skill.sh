#!/usr/bin/env bash
# 스킬 디렉터리 하나를 받아 SKILL.md 의 이식성(portability)과 frontmatter 엄격성을
# 정적으로 검증한다. SKILL.md 의 Validate 체크리스트를 기계로 강제하는 도구이며,
# 어느 harness 에서도 돌도록 의존 패키지 없이 bash + grep + awk 만 쓴다.
#
# 사용법:  scripts/validate_skill.sh <skill-dir>
# 종료 코드: 위반이 하나도 없으면 0, 하나라도 있으면 1.
set -euo pipefail

skill_dir="${1:-.}"
skill_md="${skill_dir}/SKILL.md"
fail=0

# 위반을 한 줄로 출력하고 fail 플래그를 올리는 헬퍼.
report() {
  echo "FAIL: $1"
  fail=1
}

if [[ ! -f "${skill_md}" ]]; then
  echo "FAIL: ${skill_md} 없음"
  exit 1
fi

# --- 1) frontmatter 추출 (첫 번째 --- 와 두 번째 --- 사이) ---
# awk 로 두 구분선 사이만 뽑아 frontmatter 키를 본다.
frontmatter="$(awk 'NR==1 && $0=="---"{f=1; next} f && $0=="---"{exit} f{print}' "${skill_md}")"

# 최상위 키(들여쓰기 없는 "key:")만 추출. 멀티라인 description 의
# 후속 줄(들여쓰기 있음)은 키로 세지 않는다.
top_keys="$(printf '%s\n' "${frontmatter}" | grep -E '^[A-Za-z_]+:' | sed -E 's/^([A-Za-z_]+):.*/\1/' || true)"

# frontmatter 는 name, description 두 키만 허용 (A9: 엄격 런타임 호환).
for key in ${top_keys}; do
  case "${key}" in
    name|description) ;;
    *) report "frontmatter 에 비표준 키 '${key}' 존재 (name/description 만 허용)";;
  esac
done
printf '%s\n' "${top_keys}" | grep -qx "name" || report "frontmatter 에 name 누락"
printf '%s\n' "${top_keys}" | grep -qx "description" || report "frontmatter 에 description 누락"

# --- 2) 본문 크기 (A1: ~8KB / 500 줄 목표, 500 줄은 상한) ---
bytes="$(wc -c < "${skill_md}" | tr -d ' ')"
lines="$(wc -l < "${skill_md}" | tr -d ' ')"
[[ "${lines}" -le 500 ]] || report "SKILL.md ${lines} 줄, 500 줄 상한 초과"
# 8KB 는 목표치라 경고만 (exit 비실패).
if [[ "${bytes}" -gt 8192 ]]; then
  echo "WARN: SKILL.md ${bytes} bytes, ~8KB 목표 초과 (Codex 등에서 컨텍스트 압박 가능)"
fi

# --- 3) 이식성: 절대 경로 / 백슬래시 경로 금지 (A1) ---
# 코드펜스 안 예시까지 포함해 머신 절대 경로가 박혀 있으면 위반.
if grep -nE '(^|[^A-Za-z0-9])(/Users/|/home/|[A-Z]:\\\\)' "${skill_md}" >/dev/null; then
  report "절대 머신 경로(/Users, /home, C:\\) 발견. forward-slash 상대 경로만 허용"
fi

# --- 4) 본문에 TODO/FIXME 같은 미완성 마커 금지 ---
if grep -nE '\b(TODO|FIXME|XXX)\b' "${skill_md}" >/dev/null; then
  report "미완성 마커(TODO/FIXME/XXX) 존재"
fi

# --- 5) 참조 파일 1단계 깊이 + 100줄 초과 시 TOC (A4) ---
# SKILL.md 가 가리키는 references/*.md 가 실제 존재하는지, 길면 TOC 가 있는지.
while IFS= read -r ref; do
  ref_path="${skill_dir}/${ref}"
  if [[ ! -f "${ref_path}" ]]; then
    report "참조 파일 없음: ${ref}"
    continue
  fi
  ref_lines="$(wc -l < "${ref_path}" | tr -d ' ')"
  if [[ "${ref_lines}" -gt 100 ]]; then
    # 앞 100줄 안에 Table of Contents 헤딩이 있어야 한다 (agent 가 head -100 로 미리봄).
    if ! head -100 "${ref_path}" | grep -qiE '^#+ .*table of contents|^#+ .*\bTOC\b'; then
      report "긴 참조(${ref}, ${ref_lines}줄)에 앞 100줄 TOC 없음"
    fi
  fi
done < <(grep -oE 'references/[A-Za-z0-9_.-]+\.md' "${skill_md}" | sort -u)

# --- 6) Gotchas 섹션 존재 ---
grep -qiE '^##+ .*Gotchas' "${skill_md}" || report "Gotchas 섹션 없음"

if [[ "${fail}" -eq 0 ]]; then
  echo "OK: ${skill_dir} portability/frontmatter 검증 통과 (${bytes} bytes, ${lines} lines)"
fi
exit "${fail}"
