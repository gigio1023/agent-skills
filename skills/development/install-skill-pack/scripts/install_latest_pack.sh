#!/usr/bin/env bash

set -euo pipefail

source_ref="gigio1023/agent-skills#main"
agents=()
skills=()

usage() {
  cat <<'EOF'
Usage: install_latest_pack.sh --agent <id> [--agent <id> ...] [--skill <name> ...]

Resolves skills@latest once, performs a disposable audited preflight, and asks
for the literal confirmation INSTALL before modifying global skill directories.
EOF
}

fail() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
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
    *)
      fail "unknown argument: $1"
      ;;
  esac
done

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

grep -Fq "Security Risk Assessments" "$preflight_log" ||
  fail "latest CLI did not emit a security assessment table"
for provider in Gen Socket Snyk; do
  grep -Fq "$provider" "$preflight_log" ||
    fail "security assessment is missing the $provider column"
done
if grep -Eq '[1-9][0-9]* alerts' "$preflight_log"; then
  fail "Socket reported one or more alerts; global installation is blocked"
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
