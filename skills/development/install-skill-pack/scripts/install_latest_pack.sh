#!/usr/bin/env bash

set -euo pipefail

source_ref="gigio1023/agent-skills#main"
agents=()
skills=()
self_test=false

usage() {
  cat <<'EOF'
Usage: install_latest_pack.sh --agent <id> [--agent <id> ...] [--skill <name> ...]
       install_latest_pack.sh --self-test

Resolves skills@latest once, performs a disposable audited preflight, and asks
for the literal confirmation INSTALL before modifying global skill directories.
EOF
}

fail() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

security_table_from_log() {
  awk '
    /Security Risk Assessments/ { capture = 1 }
    capture { print }
    capture && /Details:/ { exit }
  ' "$1"
}

validate_security_table() {
  local table="$1"

  [[ "$table" == *"Security Risk Assessments"* ]] || {
    printf 'latest CLI did not emit a security assessment table'
    return 1
  }
  for provider in Gen Socket Snyk; do
    [[ "$table" == *"$provider"* ]] || {
      printf 'security assessment is missing the %s column' "$provider"
      return 1
    }
  done
  if grep -Fq -- "--" <<<"$table"; then
    printf 'security assessment contains an unverified -- result'
    return 1
  fi
  if grep -Eq '(^|[^0-9])[1-9][0-9]* alerts?([^[:alpha:]]|$)' <<<"$table"; then
    printf 'Socket reported one or more alerts; global installation is blocked'
    return 1
  fi
  if grep -Eq '(High|Critical)[[:space:]]+Risk[[:space:]]+[0-9]+[[:space:]]+alerts?' <<<"$table"; then
    printf 'Gen reported high or critical risk; global installation is blocked'
    return 1
  fi
}

expect_valid_table() {
  local name="$1"
  local table="$2"
  local message=""

  if ! message="$(validate_security_table "$table")"; then
    fail "self-test $name unexpectedly failed: $message"
  fi
}

expect_invalid_table() {
  local name="$1"
  local expected="$2"
  local table="$3"
  local message=""

  if message="$(validate_security_table "$table")"; then
    fail "self-test $name unexpectedly passed"
  fi
  [[ "$message" == *"$expected"* ]] ||
    fail "self-test $name returned an unexpected error: $message"
}

run_self_test() {
  local valid_table=$'Security Risk Assessments\n  Gen  Socket  Snyk\n  sample  Safe  0 alerts  Med Risk\n  Details: https://skills.sh/example/repo'
  local snyk_high_table=$'Security Risk Assessments\n  Gen  Socket  Snyk\n  sample  Safe  0 alerts  High Risk\n  Details: https://skills.sh/example/repo'
  local socket_alert_table=$'Security Risk Assessments\n  Gen  Socket  Snyk\n  sample  Safe  1 alert  Low Risk\n  Details: https://skills.sh/example/repo'
  local missing_result_table=$'Security Risk Assessments\n  Gen  Socket  Snyk\n  sample  Safe  --  Low Risk\n  Details: https://skills.sh/example/repo'
  local gen_high_table=$'Security Risk Assessments\n  Gen  Socket  Snyk\n  sample  High Risk  0 alerts  Low Risk\n  Details: https://skills.sh/example/repo'
  local missing_provider_table=$'Security Risk Assessments\n  Gen  Socket\n  sample  Safe  0 alerts\n  Details: https://skills.sh/example/repo'

  expect_valid_table "valid table" "$valid_table"
  expect_valid_table "reviewable Snyk high result" "$snyk_high_table"
  expect_invalid_table "singular Socket alert" "Socket reported" "$socket_alert_table"
  expect_invalid_table "missing provider result" "unverified" "$missing_result_table"
  expect_invalid_table "Gen high risk" "Gen reported" "$gen_high_table"
  expect_invalid_table "missing provider column" "missing the Snyk" "$missing_provider_table"
  printf 'OK: install_latest_pack security-table self-test passed\n'
}

while (($# > 0)); do
  case "$1" in
    --agent)
      (($# >= 2)) || fail "--agent requires a value"
      agents+=("$2")
      shift 2
      ;;
    --skill)
      (($# >= 2)) || fail "--skill requires a value"
      skills+=("$2")
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --self-test)
      self_test=true
      shift
      ;;
    *)
      fail "unknown argument: $1"
      ;;
  esac
done

if [[ "$self_test" == true ]]; then
  ((${#agents[@]} == 0 && ${#skills[@]} == 0)) ||
    fail "--self-test does not accept --agent or --skill"
  run_self_test
  exit 0
fi

((${#agents[@]} > 0)) || fail "at least one --agent is required"
((${#skills[@]} > 0)) || skills=("*")

command -v npm >/dev/null 2>&1 || fail "npm is required"
command -v npx >/dev/null 2>&1 || fail "npx is required"

cli_version="$(npm view skills@latest version)"
[[ "$cli_version" =~ ^[0-9]+\.[0-9]+\.[0-9]+([-.+][0-9A-Za-z.-]+)?$ ]] ||
  fail "npm returned an invalid skills@latest version: $cli_version"

cli=(npx --yes "skills@$cli_version")
reported_version="$("${cli[@]}" --version | tr -d '[:space:]')"
[[ "$reported_version" == "$cli_version" ]] ||
  fail "resolved skills@$cli_version but CLI reported $reported_version"

printf 'Resolved Skills CLI: %s\n' "$cli_version"
printf 'Published source: %s\n' "$source_ref"

tmp_root="$(mktemp -d "${TMPDIR:-/tmp}/install-skill-pack.XXXXXX")"
cleanup() {
  rm -rf "$tmp_root"
}
trap cleanup EXIT

mkdir -p "$tmp_root/npm-cache" "$tmp_root/project"
preflight_log="$tmp_root/preflight.log"

printf '\nRunning disposable security preflight...\n'
(
  cd "$tmp_root/project"
  npm_config_cache="$tmp_root/npm-cache" NO_COLOR=1 \
    "${cli[@]}" add "$source_ref" \
    --agent codex \
    --skill "${skills[@]}" \
    --yes </dev/null
) 2>&1 | tee "$preflight_log"

audit_table="$(security_table_from_log "$preflight_log")"
audit_error=""
if ! audit_error="$(validate_security_table "$audit_table")"; then
  fail "$audit_error"
fi

printf '\nReview the security table and any medium/high/critical detail pages.\n'
printf 'Type INSTALL to modify global skill directories; anything else cancels: '
confirmation=""
IFS= read -r confirmation || true

if [[ "$confirmation" != "INSTALL" ]]; then
  printf 'Installation cancelled; global skill directories were not modified.\n'
  exit 0
fi

printf '\nInstalling with the reviewed skills@%s...\n' "$cli_version"
"${cli[@]}" add "$source_ref" \
  --global \
  --agent "${agents[@]}" \
  --skill "${skills[@]}" \
  --yes

printf '\nGlobal discovery after installation:\n'
"${cli[@]}" list --global --json
