#!/bin/bash
set -u

SKILL_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
RENDERER="$SKILL_DIR/scripts/render-events.mjs"
LAUNCHER="$SKILL_DIR/scripts/launch-run.sh"
TEST_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/codex-delegate-contract.XXXXXX")
CODEX_BIN="$TEST_ROOT/codex-bin"
SETSID_BIN="$TEST_ROOT/setsid-bin"
BASE_PATH="$CODEX_BIN:/usr/bin:/bin:/usr/sbin:/sbin"
CODEX_CALL_LOG="$TEST_ROOT/codex-calls.log"
export CODEX_CALL_LOG
PASS=0

cleanup() {
  rm -rf -- "$TEST_ROOT"
}
trap cleanup EXIT

fail() {
  printf 'FAIL: %s\n' "$*" >&2
  exit 1
}

pass() {
  PASS=$((PASS + 1))
  printf 'ok %d - %s\n' "$PASS" "$1"
}

wait_for_terminal() {
  local run=$1
  local tries=0
  while ! grep -q '^exit=' "$run/result.txt" 2>/dev/null; do
    tries=$((tries + 1))
    [ "$tries" -lt 200 ] || fail "terminal record timeout: $run"
    sleep 0.05
  done
}

wait_for_provenance() {
  local run=$1
  local tries=0
  while ! grep -q 'pgid=' "$run/result.txt" 2>/dev/null; do
    tries=$((tries + 1))
    [ "$tries" -lt 200 ] || fail "provenance timeout: $run"
    sleep 0.05
  done
}

watch_terminal_or_death() {
  local run=$1
  local tries=0
  local pg
  while :; do
    grep -q '^exit=' "$run/result.txt" 2>/dev/null && return 0
    pg=$(sed -n '1s/.*pgid=\([0-9]*\).*/\1/p' "$run/result.txt" 2>/dev/null)
    [ -n "$pg" ] && ! kill -0 -"$pg" 2>/dev/null && return 0
    tries=$((tries + 1))
    [ "$tries" -lt 200 ] || return 1
    sleep 0.05
  done
}

launch_run() {
  local workspace=$1
  local run=$2
  local mode=$3
  local launch_path=$4
  local model=${5:-gpt-5.6-sol}
  local effort=${6:-xhigh}
  local fast_requested=${7:-no}
  local ignore_user_config=${8:-no}
  local skip_git_repo_check=${9:-no}
  local host_route=${10:-launcher-subagent}
  local host_model=${11:-claude-sonnet-5}
  local routing_reason=${12:-default}
  local packet="$run.packet.md"
  local manifest="$run.manifest"

  mkdir -p "$workspace" "$(dirname "$run")"
  printf '%s\npayload-token-%s\n' "$mode" "$mode" > "$packet"
  (
    cd "$TEST_ROOT" || exit 1
    PATH=$launch_path
    export PATH
    /bin/bash "$LAUNCHER" --workspace "$workspace" --sandbox read-only \
      --packet "$packet" --run-dir "$run" --model "$model" --effort "$effort" \
      --fast-requested "$fast_requested" \
      --ignore-user-config "$ignore_user_config" \
      --skip-git-repo-check "$skip_git_repo_check" \
      --host-route "$host_route" --host-model "$host_model" \
      --routing-reason "$routing_reason" > "$manifest"
  ) || fail "launcher script failed: $run"
}

status_of() {
  node "$RENDERER" "$1/events.jsonl" --status
}

mkdir -p "$CODEX_BIN" "$SETSID_BIN"
cat > "$CODEX_BIN/codex" <<'EOF'
#!/bin/bash
output=
model=
effort=
service_tier=
ignore_user_config=no
skip_git_repo_check=no
printf 'call\n' >> "$CODEX_CALL_LOG"
while [ "$#" -gt 0 ]; do
  case "$1" in
    -o|--output-last-message)
      output=$2
      shift 2
      ;;
    -m|--model)
      model=$2
      shift 2
      ;;
    -c|--config)
      case "$2" in
        model_reasoning_effort=*) effort=${2#*=} ;;
        service_tier=*) service_tier=${2#*=} ;;
      esac
      shift 2
      ;;
    -C|--cd|--sandbox)
      shift 2
      ;;
    --json|exec)
      shift
      ;;
    --ignore-user-config)
      ignore_user_config=yes
      shift
      ;;
    --skip-git-repo-check)
      skip_git_repo_check=yes
      shift
      ;;
    -)
      shift
      break
      ;;
    *)
      shift
      ;;
  esac
done
printf 'model=%s effort=%s tier=%s ignore_user_config=%s skip_git_repo_check=%s\n' \
  "$model" "$effort" "$service_tier" "$ignore_user_config" \
  "$skip_git_repo_check" >&2
prompt=$(cat)
mode=${prompt%%$'\n'*}
printf '%s\n' '{"type":"thread.started","thread_id":"mock-thread"}'
case "$mode" in
  SUCCESS)
    printf 'captured:%s\n' "$prompt" > "$output"
    printf '%s\n' '{"type":"item.completed","item":{"id":"a","type":"agent_message","text":"mock complete"}}'
    printf '%s\n' '{"type":"turn.completed","usage":{"input_tokens":1,"output_tokens":1}}'
    exit 0
    ;;
  MISSING)
    printf '%s\n' '{"type":"turn.completed","usage":{"input_tokens":1,"output_tokens":0}}'
    exit 0
    ;;
  FAIL)
    printf 'simulated failure\n' >&2
    printf '%s\n' '{"type":"turn.failed","error":{"message":"simulated failure"}}'
    exit 7
    ;;
  SLEEP)
    trap 'exit 1' INT
    while :; do sleep 1; done
    ;;
  *)
    printf 'unknown mode: %s\n' "$mode" >&2
    exit 9
    ;;
esac
EOF
chmod +x "$CODEX_BIN/codex"

cat > "$SETSID_BIN/setsid" <<'EOF'
#!/bin/bash
[ "${1:-}" = "-f" ] || exit 64
shift
exec perl -e 'exit 0 if fork; use POSIX (); POSIX::setsid() or die; exec @ARGV or die' "$@"
EOF
chmod +x "$SETSID_BIN/setsid"

WORKSPACE_ONE="$TEST_ROOT/plain-workspace"
RUN_ONE="$TEST_ROOT/plain-run"
launch_run "$WORKSPACE_ONE" "$RUN_ONE" SUCCESS "$BASE_PATH" \
  > "$TEST_ROOT/launch-one.stdout" 2> "$TEST_ROOT/launch-one.stderr"
wait_for_terminal "$RUN_ONE"
RESOLVED_RUN_ONE="$(cd "$(dirname "$RUN_ONE")" && pwd -P)/$(basename "$RUN_ONE")"
[ ! -s "$TEST_ROOT/launch-one.stdout" ] || fail "launcher leaked stdout"
[ ! -s "$TEST_ROOT/launch-one.stderr" ] || fail "launcher leaked stderr"
grep -Fq "run=$RESOLVED_RUN_ONE" "$RUN_ONE.manifest" || fail "launch manifest has no run path"
grep -Fq "report=$RESOLVED_RUN_ONE/report.md" "$RUN_ONE.manifest" || fail "launch manifest has no report path"
grep -q '^thread=mock-thread$' "$RUN_ONE.manifest" || fail "launch manifest has no thread ID"
grep -q '^provenance=' "$RUN_ONE.manifest" || fail "launch manifest has no provenance"
grep -q 'payload-token' "$RUN_ONE.manifest" && fail "launch manifest leaked prompt content"
grep -q '^exit=0 handoff=ready ' "$RUN_ONE/result.txt" || fail "ready marker missing"
grep -q 'model=gpt-5.6-sol effort=xhigh fast_requested=no tier=default network=no ignore_user_config=no skip_git_repo_check=no' "$RUN_ONE/result.txt" || fail "default provenance drifted"
EXPECTED_PACKET_SHA=$(openssl dgst -sha256 -r "$RUN_ONE/prompt.md" | awk '{print $1}')
grep -q "host_route=launcher-subagent host_model=claude-sonnet-5 routing_reason=default packet_sha256=$EXPECTED_PACKET_SHA" "$RUN_ONE/result.txt" || fail "host provenance or packet hash drifted"
grep -q 'model=gpt-5.6-sol effort=xhigh tier=default ignore_user_config=no skip_git_repo_check=no' "$RUN_ONE/stderr.log" || fail "default model settings did not reach codex"
grep -q 'payload-token-SUCCESS' "$RUN_ONE/report.md" || fail "stdin prompt did not reach report"
[ ! -e "$RUN_ONE/final.md" ] || fail "obsolete final.md was created"
status_of "$RUN_ONE" | grep -q '^state    DONE exit=0 handoff=ready' || fail "DONE status missing"
pass "Perl fallback keeps every Codex channel in files"

WORKSPACE_TWO="$TEST_ROOT/workspace 한글 [x] \$dollar \"quote\""
RUN_TWO="$WORKSPACE_TWO/.agent-runs/codex/run with spaces"
launch_run "$WORKSPACE_TWO" "$RUN_TWO" SUCCESS "$SETSID_BIN:$BASE_PATH" \
  > "$TEST_ROOT/launch-two.stdout" 2> "$TEST_ROOT/launch-two.stderr"
wait_for_terminal "$RUN_TWO"
RESOLVED_WORKSPACE_TWO=$(cd "$WORKSPACE_TWO" && pwd -P)
grep -Fq "workspace=$RESOLVED_WORKSPACE_TWO " "$RUN_TWO/result.txt" || fail "complex workspace path changed"
grep -q '^exit=0 handoff=ready ' "$RUN_TWO/result.txt" || fail "setsid branch did not finish"
[ ! -s "$TEST_ROOT/launch-two.stdout" ] || fail "setsid branch leaked stdout"
[ ! -s "$TEST_ROOT/launch-two.stderr" ] || fail "setsid branch leaked stderr"
pass "setsid selection preserves spaces, Unicode, quotes, and dollar signs"

RUN_THREE="$TEST_ROOT/missing-run"
launch_run "$WORKSPACE_ONE" "$RUN_THREE" MISSING "$BASE_PATH"
wait_for_terminal "$RUN_THREE"
grep -q '^exit=0 handoff=incomplete ' "$RUN_THREE/result.txt" || fail "missing handoff marker absent"
status_of "$RUN_THREE" | grep -q '^state    INCOMPLETE exit=0 handoff=incomplete' || fail "INCOMPLETE status missing"
pass "clean exit without report is not reported as DONE"

RUN_FOUR="$TEST_ROOT/failing-run"
launch_run "$WORKSPACE_ONE" "$RUN_FOUR" FAIL "$BASE_PATH"
wait_for_terminal "$RUN_FOUR"
grep -q '^exit=7 handoff=incomplete ' "$RUN_FOUR/result.txt" || fail "failure terminal record absent"
grep -q 'simulated failure' "$RUN_FOUR/stderr.log" || fail "stderr was not captured"
STATUS_FOUR=$(status_of "$RUN_FOUR")
printf '%s\n' "$STATUS_FOUR" | grep -q '^state    EXITED exit=7 handoff=incomplete' || fail "EXITED status missing"
printf '%s\n' "$STATUS_FOUR" | grep -q 'do not retry automatically' || fail "EXITED hint encouraged an unclassified retry"
pass "non-zero exit and stderr remain file-backed"

RUN_FIVE="$TEST_ROOT/died-run"
launch_run "$WORKSPACE_ONE" "$RUN_FIVE" SLEEP "$BASE_PATH"
wait_for_provenance "$RUN_FIVE"
status_of "$RUN_FIVE" | grep -q '^state    RUNNING' || fail "live group was not RUNNING"
watch_terminal_or_death "$RUN_FIVE" &
WATCHER=$!
PG=$(sed -n '1s/.*pgid=\([0-9]*\).*/\1/p' "$RUN_FIVE/result.txt")
[ -n "$PG" ] || fail "died run has no pgid"
kill -KILL -"$PG"
wait "$WATCHER" || fail "watcher did not wake after death"
grep -q '^exit=' "$RUN_FIVE/result.txt" 2>/dev/null && fail "killed wrapper wrote a false terminal record"
status_of "$RUN_FIVE" | grep -q '^state    DIED' || fail "DIED status missing"
pass "the same quiet run moves from RUNNING to DIED only after group death"

RUN_SIX_A="$TEST_ROOT/concurrent-a"
RUN_SIX_B="$TEST_ROOT/concurrent-b"
launch_run "$WORKSPACE_ONE" "$RUN_SIX_A" SUCCESS "$BASE_PATH"
launch_run "$WORKSPACE_ONE" "$RUN_SIX_B" SUCCESS "$SETSID_BIN:$BASE_PATH"
wait_for_terminal "$RUN_SIX_A"
wait_for_terminal "$RUN_SIX_B"
grep -q '^exit=0 handoff=ready ' "$RUN_SIX_A/result.txt" || fail "concurrent run A failed"
grep -q '^exit=0 handoff=ready ' "$RUN_SIX_B/result.txt" || fail "concurrent run B failed"
pass "independent read-only runs keep separate handoffs"

RUN_SEVEN="$TEST_ROOT/cancelled-run"
launch_run "$WORKSPACE_ONE" "$RUN_SEVEN" SLEEP "$BASE_PATH"
wait_for_provenance "$RUN_SEVEN"
PG=$(sed -n '1s/.*pgid=\([0-9]*\).*/\1/p' "$RUN_SEVEN/result.txt")
[ -n "$PG" ] || fail "cancelled run has no pgid"
kill -INT -"$PG"
wait_for_terminal "$RUN_SEVEN"
status_of "$RUN_SEVEN" | grep -q '^state    EXITED exit=' || fail "cancelled run did not retain terminal state"
grep -q 'handoff=incomplete' "$RUN_SEVEN/result.txt" || fail "cancelled run claimed a ready handoff"
pass "graceful group cancellation stays EXITED rather than DIED"

RUN_EIGHT="$TEST_ROOT/unknown-run"
mkdir -p "$RUN_EIGHT"
: > "$RUN_EIGHT/events.jsonl"
printf 'sandbox=read-only workspace=%s started=%s\n' \
  "$WORKSPACE_ONE" "$(date -u +%FT%TZ)" > "$RUN_EIGHT/result.txt"
status_of "$RUN_EIGHT" | grep -q '^state    UNKNOWN' || fail "missing pgid did not degrade to UNKNOWN"
pass "truncated provenance degrades to UNKNOWN without guessing"

RUN_NINE="$TEST_ROOT/terra-run"
launch_run "$WORKSPACE_ONE" "$RUN_NINE" SUCCESS "$BASE_PATH" \
  gpt-5.6-terra xhigh no yes yes
wait_for_terminal "$RUN_NINE"
grep -q 'model=gpt-5.6-terra effort=xhigh fast_requested=no tier=default' "$RUN_NINE/result.txt" || fail "Terra provenance drifted"
grep -q 'model=gpt-5.6-terra effort=xhigh tier=default' "$RUN_NINE/stderr.log" || fail "Terra settings did not reach codex"
grep -q 'ignore_user_config=yes skip_git_repo_check=yes' "$RUN_NINE/result.txt" || fail "explicit safety flags were not recorded"
grep -q 'ignore_user_config=yes skip_git_repo_check=yes' "$RUN_NINE/stderr.log" || fail "explicit safety flags did not reach codex"
pass "contextual Terra routing stays xhigh and non-Fast with explicit safety flags"

RUN_TEN="$TEST_ROOT/explicit-fast-run"
launch_run "$WORKSPACE_ONE" "$RUN_TEN" SUCCESS "$BASE_PATH" gpt-5.6-sol xhigh yes
wait_for_terminal "$RUN_TEN"
grep -q 'model=gpt-5.6-sol effort=xhigh fast_requested=yes tier=priority' "$RUN_TEN/result.txt" || fail "Fast provenance drifted"
grep -q 'model=gpt-5.6-sol effort=xhigh tier=priority' "$RUN_TEN/stderr.log" || fail "explicit Fast setting did not reach codex"
pass "explicit Fast request is represented separately from effort"

RUN_ELEVEN="$TEST_ROOT/invalid-fast-run"
PACKET_ELEVEN="$TEST_ROOT/invalid-fast-packet.md"
printf 'SUCCESS\n' > "$PACKET_ELEVEN"
if PATH="$BASE_PATH" /bin/bash "$LAUNCHER" --workspace "$WORKSPACE_ONE" \
  --sandbox read-only --packet "$PACKET_ELEVEN" --run-dir "$RUN_ELEVEN" \
  --fast-requested inferred --host-route direct-main --host-model unavailable \
  --routing-reason default > "$TEST_ROOT/invalid-fast.stdout" \
  2> "$TEST_ROOT/invalid-fast.stderr"; then
  fail "invalid Fast assertion was accepted"
fi
[ ! -e "$RUN_ELEVEN" ] || fail "invalid Fast assertion created a run"
grep -q -- '--fast-requested must be yes or no' "$TEST_ROOT/invalid-fast.stderr" ||
  fail "invalid Fast assertion did not explain the failure"
pass "invalid Fast assertions fail before run creation"

RUN_TWELVE="$TEST_ROOT/resumed-run"
PACKET_TWELVE="$TEST_ROOT/resumed-packet.md"
printf 'SUCCESS\npayload-token-RESUME\n' > "$PACKET_TWELVE"
PATH="$BASE_PATH" /bin/bash "$LAUNCHER" --workspace "$WORKSPACE_ONE" \
  --packet "$PACKET_TWELVE" --resume-from "$RUN_ONE" --run-dir "$RUN_TWELVE" \
  --host-route launcher-subagent --host-model claude-sonnet-5 \
  --routing-reason resume-inherited \
  > "$RUN_TWELVE.manifest" 2> "$TEST_ROOT/resumed-launch.stderr"
wait_for_terminal "$RUN_TWELVE"
[ ! -s "$TEST_ROOT/resumed-launch.stderr" ] || fail "resume launcher leaked stderr"
grep -q 'thread=mock-thread resumed_from=plain-run' "$RUN_TWELVE/result.txt" || fail "resume provenance lost its source"
grep -q 'model=gpt-5.6-sol effort=xhigh fast_requested=no tier=default' "$RUN_TWELVE/result.txt" || fail "resume did not inherit route"
grep -q 'ignore_user_config=no skip_git_repo_check=no' "$RUN_TWELVE/result.txt" || fail "resume did not inherit safety flags"
grep -q 'host_route=launcher-subagent host_model=claude-sonnet-5 routing_reason=resume-inherited packet_sha256=' "$RUN_TWELVE/result.txt" || fail "resume lost current host provenance"
grep -q '^thread=mock-thread$' "$RUN_TWELVE.manifest" || fail "resume manifest lost its thread"
grep -q 'payload-token-RESUME' "$RUN_TWELVE/report.md" || fail "resume packet did not reach Codex"
pass "resume inherits explicit provenance through the same launcher"

RECOVERED_MANIFEST="$TEST_ROOT/recovered.manifest"
CALLS_BEFORE_RECOVERY=$(wc -l < "$CODEX_CALL_LOG" | tr -d ' ')
PATH="$BASE_PATH" /bin/bash "$LAUNCHER" --recover-manifest \
  --run-dir "$RUN_ONE" --packet "$RUN_ONE.packet.md" > "$RECOVERED_MANIFEST"
CALLS_AFTER_RECOVERY=$(wc -l < "$CODEX_CALL_LOG" | tr -d ' ')
cmp -s "$RUN_ONE.manifest" "$RECOVERED_MANIFEST" || fail "recovered manifest differs from launch manifest"
[ "$CALLS_BEFORE_RECOVERY" = "$CALLS_AFTER_RECOVERY" ] || fail "manifest recovery launched Codex again"
pass "lost launcher output is recovered from the preselected run without relaunch"

RUN_FOURTEEN="$TEST_ROOT/bad-recovery-run"
mkdir -p "$RUN_FOURTEEN"
cp "$RUN_ONE.packet.md" "$RUN_FOURTEEN/prompt.md"
cp "$RUN_ONE/run.sh" "$RUN_FOURTEEN/run.sh"
printf 'sandbox=read-only host_route=launcher-subagent host_model=claude-sonnet-5 routing_reason=default packet_sha256=wrong\n' \
  > "$RUN_FOURTEEN/result.txt"
if PATH="$BASE_PATH" /bin/bash "$LAUNCHER" --recover-manifest \
  --run-dir "$RUN_FOURTEEN" --packet "$RUN_ONE.packet.md" \
  > "$TEST_ROOT/bad-recovery.stdout" 2> "$TEST_ROOT/bad-recovery.stderr"; then
  fail "invalid existing run was adopted"
fi
grep -q 'recovery provenance does not match packet hash' "$TEST_ROOT/bad-recovery.stderr" ||
  fail "invalid recovery did not explain the provenance failure"
pass "an existing path without matching provenance is a contract failure"

RUN_FIFTEEN="$TEST_ROOT/direct-fallback-run"
launch_run "$WORKSPACE_ONE" "$RUN_FIFTEEN" SUCCESS "$BASE_PATH" \
  gpt-5.6-sol xhigh no no no direct-main unavailable manifest-delivery-failure
wait_for_terminal "$RUN_FIFTEEN"
grep -q 'host_route=direct-main host_model=unavailable routing_reason=manifest-delivery-failure' "$RUN_FIFTEEN/result.txt" || fail "direct fallback route was not recorded"
pass "direct fallback through an absent preselected path records its route"

PACKET_SIXTEEN="$TEST_ROOT/no-run-dir.packet.md"
printf 'SUCCESS\n' > "$PACKET_SIXTEEN"
if PATH="$BASE_PATH" /bin/bash "$LAUNCHER" --workspace "$WORKSPACE_ONE" \
  --sandbox read-only --packet "$PACKET_SIXTEEN" --host-route direct-main \
  --host-model unavailable --routing-reason default \
  > "$TEST_ROOT/no-run-dir.stdout" 2> "$TEST_ROOT/no-run-dir.stderr"; then
  fail "launch without a preselected run path succeeded"
fi
grep -q -- '--run-dir is required' "$TEST_ROOT/no-run-dir.stderr" ||
  fail "missing run path did not explain the failure"
pass "every launch requires a main-selected absent run path"

printf 'PASS: %d contract scenarios\n' "$PASS"
