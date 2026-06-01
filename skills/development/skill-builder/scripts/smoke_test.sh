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

# --- 3) 이 스킬 본체도 자기 규칙을 통과하는지 (dogfooding) ---
self_dir="$(cd "${here}/.." && pwd)"
if ! "${validator}" "${self_dir}"; then
  echo "smoke test FAILED: skill-builder 본체가 자기 validator 를 통과하지 못함"
  exit 1
fi

echo "smoke test passed: init -> validate exit 0, self-check exit 0"
