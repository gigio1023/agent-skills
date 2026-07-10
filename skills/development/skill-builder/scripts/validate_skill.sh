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
if [[ "$(head -1 "${skill_md}")" != "---" ]]; then
  report "SKILL.md 첫 줄에 frontmatter 시작 구분선(---) 없음"
fi
closing_line="$(awk 'NR > 1 && $0 == "---" { print NR; exit }' "${skill_md}")"
if [[ -z "${closing_line}" ]]; then
  report "frontmatter 종료 구분선(---) 없음"
fi
frontmatter="$(awk 'NR==1 && $0=="---"{f=1; next} f && $0=="---"{exit} f{print}' "${skill_md}")"

# 의도적으로 작은 YAML subset 만 허용한다. name 은 단일행 scalar,
# description 은 단일행 scalar 또는 들여쓴 > / | block 이어야 한다.
# YAML 파서를 흉내 내기보다 여러 런타임에서 동일하게 읽히는 형태를 강제한다.
frontmatter_structure_error="$(printf '%s\n' "${frontmatter}" | awk '
  function trim(s) {
    sub(/^[[:space:]]+/, "", s)
    sub(/[[:space:]]+$/, "", s)
    return s
  }
  /^[[:space:]]*$/ { next }
  /^[ ]*\t/ { print "frontmatter 들여쓰기에 탭 사용"; exit }
  /^[A-Za-z_][A-Za-z0-9_-]*:/ {
    key=$0
    sub(/:.*/, "", key)
    value=$0
    sub(/^[^:]+:/, "", value)
    value=trim(value)
    block=""
    if (key == "name" && (value == "" || value ~ /^[>|][-+]?$/)) {
      print "name 은 비어 있지 않은 단일행 scalar 여야 함"
      exit
    }
    if (key == "description") {
      if (value ~ /^[>|][-+]?$/) {
        block="description"
        block_indent=0
      }
      else if (value == "") {
        print "description 은 비어 있지 않은 scalar 또는 block 이어야 함"
        exit
      }
    }
    next
  }
  /^[[:space:]]+/ {
    if (block == "description") {
      indent=match($0, /[^ ]/) - 1
      if (block_indent == 0) block_indent=indent
      else if (indent < block_indent) {
        print "description block 의 continuation 들여쓰기가 기준보다 작음"
        exit
      }
      next
    }
    print "block scalar 밖의 예기치 않은 들여쓰기 줄"
    exit
  }
  { print "들여쓰기되지 않은 frontmatter continuation 또는 잘못된 YAML"; exit }
')"
if [[ -n "${frontmatter_structure_error}" ]]; then
  report "frontmatter 구조 오류: ${frontmatter_structure_error}"
fi

# 최상위 키(들여쓰기 없는 "key:")만 추출. 멀티라인 description 의
# 후속 줄(들여쓰기 있음)은 키로 세지 않는다.
top_keys="$(printf '%s\n' "${frontmatter}" | grep -E '^[A-Za-z_][A-Za-z0-9_-]*:' | sed -E 's/^([A-Za-z_][A-Za-z0-9_-]*):.*/\1/' || true)"

# frontmatter 는 name, description 두 키만 허용 (A9: 엄격 런타임 호환).
for key in ${top_keys}; do
  case "${key}" in
    name|description) ;;
    *) report "frontmatter 에 비표준 키 '${key}' 존재 (name/description 만 허용)";;
  esac
done
name_key_count="$(printf '%s\n' "${top_keys}" | grep -xc "name" || true)"
description_key_count="$(printf '%s\n' "${top_keys}" | grep -xc "description" || true)"
[[ "${name_key_count}" -eq 1 ]] || report "frontmatter name 키는 정확히 1개여야 함 (현재 ${name_key_count})"
[[ "${description_key_count}" -eq 1 ]] || report "frontmatter description 키는 정확히 1개여야 함 (현재 ${description_key_count})"

# name/description 값 자체의 공식 제약도 검사한다. 바깥의 matching quote pair 만
# 제거하고 내부 따옴표는 보존한다.
raw_name="$(printf '%s\n' "${frontmatter}" | awk '/^name:[[:space:]]*/ { sub(/^name:[[:space:]]*/, ""); print; exit }' | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//')"
name_value="${raw_name}"
name_quoted=0
if [[ -n "${raw_name}" ]]; then
  first_char="${raw_name:0:1}"
  last_char="${raw_name: -1}"
  if [[ "${first_char}" == "'" || "${first_char}" == '"' || "${last_char}" == "'" || "${last_char}" == '"' ]]; then
    if [[ "${#raw_name}" -ge 2 && "${first_char}" == "${last_char}" && ( "${first_char}" == "'" || "${first_char}" == '"' ) ]]; then
      name_value="${raw_name:1:${#raw_name}-2}"
      name_quoted=1
    else
      report "name 의 바깥 따옴표가 일치하지 않음"
    fi
  fi
fi
lower_name="$(printf '%s' "${raw_name}" | tr '[:upper:]' '[:lower:]')"
if [[ "${name_quoted}" -eq 0 ]]; then
  case "${lower_name}" in
    null|true|false|yes|no|on|off|"~")
      report "name 이 YAML implicit scalar 로 해석될 수 있음; 문자열로 따옴표 처리"
      ;;
  esac
  if [[ "${raw_name}" =~ ^[0-9] ]]; then
    report "숫자로 시작하는 name 은 YAML 문자열로 따옴표 처리"
  fi
fi
if [[ -z "${name_value}" ]]; then
  report "frontmatter name 값을 읽을 수 없음"
else
  [[ "${#name_value}" -le 64 ]] || report "name 이 64자 초과"
  [[ "${name_value}" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || report "name 은 lowercase letters/numbers/hyphens 형식이어야 함: ${name_value}"
  if [[ "${name_value}" == *anthropic* || "${name_value}" == *claude* ]]; then
    report "name 에 예약어(anthropic/claude) 사용: ${name_value}"
  fi
fi

# description: 이후의 scalar 또는 folded YAML 줄을 합쳐 discovery 텍스트를 본다.
raw_description="$(printf '%s\n' "${frontmatter}" | awk '/^description:[[:space:]]*/ { sub(/^description:[[:space:]]*/, ""); print; exit }' | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//')"
description_value="$(printf '%s\n' "${frontmatter}" | awk '
  /^description:[[:space:]]*/ {
    in_description=1
    sub(/^description:[[:space:]]*/, "")
    if ($0 !~ /^[>|][-+]?[[:space:]]*$/) print
    next
  }
  in_description && /^[A-Za-z_][A-Za-z0-9_-]*:/ { exit }
  in_description {
    sub(/^[[:space:]]+/, "")
    print
  }
')"
description_value="$(printf '%s' "${description_value}" | tr '\n' ' ' | sed -E 's/[[:space:]]+/ /g; s/^ //; s/ $//')"

if [[ ! "${raw_description}" =~ ^[\>\|][-+]?$ ]]; then
  description_value="${raw_description}"
  if [[ -n "${raw_description}" ]]; then
    first_char="${raw_description:0:1}"
    last_char="${raw_description: -1}"
    if [[ "${first_char}" == "'" || "${first_char}" == '"' || "${last_char}" == "'" || "${last_char}" == '"' ]]; then
      if [[ "${#raw_description}" -ge 2 && "${first_char}" == "${last_char}" && ( "${first_char}" == "'" || "${first_char}" == '"' ) ]]; then
        description_value="${raw_description:1:${#raw_description}-2}"
        if [[ "${first_char}" == "'" && "${description_value}" == *"'"* ]]; then
          report "single-quoted description 내부 quote 는 이식 가능한 subset 에서 허용하지 않음; block scalar 사용"
        fi
        if [[ "${first_char}" == '"' && ( "${description_value}" == *'"'* || "${description_value}" == *'\'* ) ]]; then
          report "double-quoted description 내부 quote/escape 는 이식 가능한 subset 에서 허용하지 않음; block scalar 사용"
        fi
      else
        report "description 의 바깥 따옴표가 일치하지 않음"
      fi
    else
      first_char="${raw_description:0:1}"
      case "${first_char}" in
        '['|'{'|'*'|'&'|'!'|'?'|'-'|'@'|'`'|'#'|'%'|','|']'|'}'|':')
          report "따옴표 없는 description 이 YAML indicator 로 시작함; 문자열로 따옴표 처리"
          ;;
      esac
      lower_description="$(printf '%s' "${raw_description}" | tr '[:upper:]' '[:lower:]')"
      case "${lower_description}" in
        null|true|false|yes|no|on|off|"~")
          report "description 이 YAML implicit scalar 로 해석될 수 있음; 문자열로 따옴표 처리"
          ;;
      esac
      if [[ "${raw_description}" =~ ^[+.0-9] ]]; then
        report "숫자·날짜처럼 시작하는 description 은 YAML 문자열로 따옴표 처리"
      fi
      if printf '%s\n' "${raw_description}" | grep -Eq ':[[:space:]]|:$|[[:space:]]#'; then
        report "따옴표 없는 단일행 description 에 colon/comment 구문 사용; quoted 또는 block scalar 사용"
      fi
    fi
  fi
fi
[[ -n "${description_value}" ]] || report "description 값이 비어 있음"
[[ "${#description_value}" -le 1024 ]] || report "description 이 1024자 초과"
if printf '%s\n' "${description_value}" | grep -Eq '</?[A-Za-z][^>]*>'; then
  report "description 에 XML/HTML 태그 사용"
fi

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

# fenced code 안의 예시 링크를 제외하고 Markdown 링크를 추출한다. 네 개짜리
# outer fence 안의 세 개짜리 inner fence도 올바르게 무시한다.
strip_fenced_code() {
  awk '
    function leading_run(s, c, count, i) {
      count = 0
      for (i = 1; i <= length(s); i++) {
        if (substr(s, i, 1) == c) count++
        else break
      }
      return count
    }
    {
      s = $0
      sub(/^[[:space:]]*/, "", s)
      c = substr(s, 1, 1)
      n = (c == "`" || c == "~") ? leading_run(s, c) : 0
      if (!in_fence && n >= 3) {
        in_fence = 1
        fence_char = c
        fence_len = n
        next
      }
      if (in_fence) {
        if (c == fence_char && n >= fence_len) in_fence = 0
        next
      }
      print
    }
  ' "$1"
}

extract_markdown_links() {
  strip_fenced_code "$1" \
    | grep -oE '\]\((<)?[^)#]+\.md(#[^)]*)?(>)?\)' \
    | sed -E 's/^\]\(<?//; s/>?\)$//; s/#.*$//; s/[[:space:]]+$//' \
    || true
}

# --- 5) 모든 직접 Markdown 참조 + 100줄 초과 시 TOC + 체인 금지 (A4) ---
# Markdown 링크와 references/... 경로 표기를 합쳐 검사한다.
while IFS= read -r ref; do
  case "${ref}" in
    ""|http://*|https://*|mailto:*) continue ;;
  esac
  ref_path="${skill_dir}/${ref}"
  if [[ ! -f "${ref_path}" ]]; then
    report "참조 파일 없음: ${ref}"
    continue
  fi
  ref_lines="$(wc -l < "${ref_path}" | tr -d ' ')"
  if [[ "${ref_lines}" -gt 100 ]]; then
    # 앞 100줄 안에 Table of Contents 헤딩이 있어야 한다 (agent 가 head -100 로 미리봄).
    if ! head -100 "${ref_path}" | grep -qiE '^#+[[:space:]]+((table of )?contents|toc)([[:space:]]|$)'; then
      report "긴 참조(${ref}, ${ref_lines}줄)에 앞 100줄 TOC 없음"
    fi
  fi

  while IFS= read -r nested_ref; do
    case "${nested_ref}" in
      ""|http://*|https://*|mailto:*) continue ;;
    esac
    nested_path="$(dirname "${ref_path}")/${nested_ref}"
    if [[ -f "${nested_path}" ]]; then
      report "참조 체인 발견: ${ref} -> ${nested_ref}. 두 파일을 SKILL.md 에서 직접 링크"
    fi
  done < <(extract_markdown_links "${ref_path}")
done < <(
  {
    extract_markdown_links "${skill_md}"
    grep -oE 'references/[A-Za-z0-9_./-]+\.md' "${skill_md}" || true
  } | sort -u
)

# --- 6) reasoning-extraction 위험 문구는 자동 판정 대신 검토 경고 ---
# 부정문("요청하지 말라")도 같은 단어를 포함할 수 있으므로 실패로 처리하지 않는다.
if grep -niE 'chain[- ]of[- ]thought|internal reasoning|private reasoning|hidden reasoning|reasoning trace|scratchpad' "${skill_md}" >/dev/null; then
  echo "WARN: 비공개 추론/chain-of-thought 관련 문구 발견. 이를 출력하라는 지시가 아닌지 수동 검토"
fi

# --- 7) Gotchas 섹션 존재 ---
grep -qiE '^##+ .*Gotchas' "${skill_md}" || report "Gotchas 섹션 없음"

if [[ "${fail}" -eq 0 ]]; then
  echo "OK: ${skill_dir} portability/frontmatter 검증 통과 (${bytes} bytes, ${lines} lines)"
fi
exit "${fail}"
