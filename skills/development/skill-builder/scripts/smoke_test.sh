#!/usr/bin/env bash
# 번들된 validator(validate_skill.sh)가 자기 자신의 문서화된 호출을 통과하는지
# 확인하는 smoke test (A3: self-test discipline).
#
# 흐름:
#   1) init: 최소 스킬 한 개를 임시 디렉터리에 생성한다.
#   2) validate: 방금 생성한 스킬을 validator 에 그대로 넣어 exit 0 인지 본다.
#   3) 추가로 이 스킬 본체(상위 디렉터리)도 자기 validator 를 통과하는지 확인한다.
#
# 하나라도 exit 0 이 아니면 번들 산출물이 깨진 것이므로 smoke test 가 실패한다.
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
validator="${here}/validate_skill.sh"

tmp="$(mktemp -d)"
trap 'rm -rf "${tmp}"' EXIT

# --- 1) init: validator 가 통과하도록 만든 최소 스킬 산출물 ---
sample="${tmp}/sample-skill"
mkdir -p "${sample}"
cat > "${sample}/SKILL.md" <<'EOF'
---
name: counting-widgets
description: >
  Use when the user wants to count widgets in a directory. Triggers on
  "count widgets". NOT for editing widgets; use a different skill.
---

# Counting Widgets

## Quick Start

Count the widget files under a path and report the total.

## Gotchas

- Empty directories report zero, not an error.
EOF

# --- 2) validate: 생성한 산출물을 곧바로 검증, exit 0 단언 ---
if ! "${validator}" "${sample}"; then
  echo "smoke test FAILED: init 으로 만든 산출물이 자기 validator 를 통과하지 못함"
  exit 1
fi

# matching quote pair 안의 colon 은 유효한 단일행 scalar 로 허용한다.
quoted_sample="${tmp}/quoted-sample"
mkdir -p "${quoted_sample}"
cat > "${quoted_sample}/SKILL.md" <<'EOF'
---
name: 'quoted-sample'
description: "Use when: a quoted scalar needs a colon."
---

# Quoted Sample

## Gotchas
- Matching outer quotes must be preserved and parsed safely.
EOF

if ! "${validator}" "${quoted_sample}"; then
  echo "smoke test FAILED: 유효한 quoted scalar fixture 를 validator 가 거부함"
  exit 1
fi

# 공식 frontmatter 제약을 실제로 거부하는지도 확인한다.
invalid="${tmp}/invalid-skill"
mkdir -p "${invalid}"
cat > "${invalid}/SKILL.md" <<'EOF'
---
name: Claude Helper
description: Invalid reserved and uppercase name.
version: 1
---

# Invalid Skill

## Gotchas

- This fixture must fail validation.
EOF

if "${validator}" "${invalid}" >/dev/null 2>&1; then
  echo "smoke test FAILED: 잘못된 frontmatter fixture 를 validator 가 허용함"
  exit 1
fi

# 종료 구분선 누락, 중복 키, XML 태그도 각각 거부해야 한다.
missing_close="${tmp}/missing-close"
mkdir -p "${missing_close}"
cat > "${missing_close}/SKILL.md" <<'EOF'
---
name: missing-close
description: Use when testing malformed frontmatter.

# Missing Close

## Gotchas
- This fixture must fail.
EOF

duplicate_name="${tmp}/duplicate-name"
mkdir -p "${duplicate_name}"
cat > "${duplicate_name}/SKILL.md" <<'EOF'
---
name: duplicate-name
name: duplicate-name-again
description: Use when testing duplicate keys.
---

# Duplicate Name

## Gotchas
- This fixture must fail.
EOF

xml_description="${tmp}/xml-description"
mkdir -p "${xml_description}"
cat > "${xml_description}/SKILL.md" <<'EOF'
---
name: xml-description
description: Use when <tag>testing</tag> invalid XML in metadata.
---

# XML Description

## Gotchas
- This fixture must fail.
EOF

# 제한 YAML subset 을 우회하던 형태도 각각 거부해야 한다.
unquoted_colon="${tmp}/unquoted-colon"
mkdir -p "${unquoted_colon}"
cat > "${unquoted_colon}/SKILL.md" <<'EOF'
---
name: unquoted-colon
description: Use when: an unquoted colon appears.
---

# Unquoted Colon

## Gotchas
- This fixture must fail.
EOF

unindented_block="${tmp}/unindented-block"
mkdir -p "${unindented_block}"
cat > "${unindented_block}/SKILL.md" <<'EOF'
---
name: unindented-block
description: >
This continuation is not indented.
---

# Unindented Block

## Gotchas
- This fixture must fail.
EOF

internal_quote_name="${tmp}/internal-quote-name"
mkdir -p "${internal_quote_name}"
cat > "${internal_quote_name}/SKILL.md" <<'EOF'
---
name: "foo'bar"
description: Use when testing internal quote preservation.
---

# Internal Quote Name

## Gotchas
- This fixture must fail.
EOF

inconsistent_block_indent="${tmp}/inconsistent-block-indent"
mkdir -p "${inconsistent_block_indent}"
cat > "${inconsistent_block_indent}/SKILL.md" <<'EOF'
---
name: inconsistent-block-indent
description: >
    First continuation establishes four-space indentation.
  This continuation illegally reduces it to two spaces.
---

# Inconsistent Block Indent

## Gotchas
- This fixture must fail.
EOF

metadata_fixtures=()

make_invalid_description_fixture() {
  local label="$1"
  local raw_value="$2"
  local fixture="${tmp}/${label}"
  mkdir -p "${fixture}"
  printf '%s\n' \
    '---' \
    "name: ${label}" \
    "description: ${raw_value}" \
    '---' \
    '' \
    "# ${label}" \
    '' \
    '## Gotchas' \
    '- This fixture must fail.' > "${fixture}/SKILL.md"
  metadata_fixtures+=("${fixture}")
}

make_invalid_name_fixture() {
  local label="$1"
  local raw_value="$2"
  local fixture="${tmp}/${label}"
  mkdir -p "${fixture}"
  printf '%s\n' \
    '---' \
    "name: ${raw_value}" \
    'description: Use when testing an implicit YAML name scalar.' \
    '---' \
    '' \
    "# ${label}" \
    '' \
    '## Gotchas' \
    '- This fixture must fail.' > "${fixture}/SKILL.md"
  metadata_fixtures+=("${fixture}")
}

make_invalid_description_fixture "flow-sequence-description" "[invalid"
make_invalid_description_fixture "flow-map-description" "{invalid"
make_invalid_description_fixture "alias-description" "*missing-alias"
make_invalid_description_fixture "anchor-description" "&anchor"
make_invalid_description_fixture "null-description" "null"
make_invalid_description_fixture "boolean-description" "true"
make_invalid_description_fixture "number-description" "123"
make_invalid_description_fixture "tilde-description" "~"
make_invalid_description_fixture "reserved-indicator-description" "@invalid"
make_invalid_description_fixture "invalid-double-escape" '"Use when \q is invalid."'
make_invalid_description_fixture "invalid-single-quote" "'Use when it's broken.'"
make_invalid_name_fixture "implicit-null-name" "null"
make_invalid_name_fixture "implicit-number-name" "123"

for malformed in \
  "${missing_close}" \
  "${duplicate_name}" \
  "${xml_description}" \
  "${unquoted_colon}" \
  "${unindented_block}" \
  "${internal_quote_name}" \
  "${inconsistent_block_indent}" \
  "${metadata_fixtures[@]}"
do
  if "${validator}" "${malformed}" >/dev/null 2>&1; then
    echo "smoke test FAILED: malformed fixture 를 validator 가 허용함: ${malformed}"
    exit 1
  fi
done

# 루트 Markdown 누락과 reference-to-reference 체인도 거부해야 한다.
missing_reference="${tmp}/missing-reference"
mkdir -p "${missing_reference}"
cat > "${missing_reference}/SKILL.md" <<'EOF'
---
name: missing-reference
description: Use when testing a missing root Markdown reference.
---

# Missing Reference

Read [GUIDE.md](GUIDE.md).

## Gotchas
- This fixture must fail.
EOF

chained="${tmp}/chained-reference"
mkdir -p "${chained}/references"
cat > "${chained}/SKILL.md" <<'EOF'
---
name: chained-reference
description: Use when testing a chained Markdown reference.
---

# Chained Reference

Read [first.md](references/first.md).

## Gotchas
- This fixture must fail.
EOF
cat > "${chained}/references/first.md" <<'EOF'
# First Reference

Continue to [second.md](second.md).
EOF
cat > "${chained}/references/second.md" <<'EOF'
# Second Reference
EOF

for bad_reference in "${missing_reference}" "${chained}"; do
  if "${validator}" "${bad_reference}" >/dev/null 2>&1; then
    echo "smoke test FAILED: 잘못된 reference fixture 를 validator 가 허용함: ${bad_reference}"
    exit 1
  fi
done

# --- 3) 이 스킬 본체도 자기 규칙을 통과하는지 (dogfooding) ---
self_dir="$(cd "${here}/.." && pwd)"
if ! "${validator}" "${self_dir}"; then
  echo "smoke test FAILED: skill-builder 본체가 자기 validator 를 통과하지 못함"
  exit 1
fi

echo "smoke test passed: valid fixtures/self-check exit 0, malformed fixtures rejected"
