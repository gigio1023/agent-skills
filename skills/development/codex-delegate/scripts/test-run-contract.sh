#!/bin/bash
set -u

SKILL_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
RENDERER="$SKILL_DIR/scripts/render-events.mjs"
TEST_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/codex-delegate-contract.XXXXXX")
CODEX_BIN="$TEST_ROOT/codex-bin"
SETSID_BIN="$TEST_ROOT/setsid-bin"
BASE_PATH="$CODEX_BIN:/usr/bin:/bin:/usr/sbin:/sbin"
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

  mkdir -p "$workspace" "$run"
  printf '%s\npayload-token-%s\n' "$mode" "$mode" > "$run/prompt.md"
  DIR=$workspace
  SANDBOX=read-only
  RUN=$run
  export DIR SANDBOX RUN
  cat > "$RUN/run.sh" <<'EOF'
#!/bin/bash
printf 'sandbox=%s workspace=%s started=%s pgid=%s model=%s effort=%s tier=%s\n' \
  "$SANDBOX" "$DIR" "$(date -u +%FT%TZ)" "$$" gpt-5.6-sol high priority \
  > "$RUN/result.txt"
trap ':' INT
codex exec --json -C "$DIR" --sandbox "$SANDBOX" -m gpt-5.6-sol \
  -c model_reasoning_effort="high" -c service_tier="priority" \
  -o "$RUN/report.md" - < "$RUN/prompt.md" \
  > "$RUN/events.jsonl" 2> "$RUN/stderr.log"
CODEX_EXIT=$?
trap - INT
if [ "$CODEX_EXIT" -eq 0 ] && [ -s "$RUN/report.md" ]; then
  HANDOFF=ready
else
  HANDOFF=incomplete
fi
printf 'exit=%s handoff=%s finished=%s\n' \
  "$CODEX_EXIT" "$HANDOFF" "$(date -u +%FT%TZ)" >> "$RUN/result.txt"
exit "$CODEX_EXIT"
EOF
  (
    cd "$TEST_ROOT" || exit 1
    PATH=$launch_path
    export PATH
    if command -v setsid >/dev/null 2>&1; then
      setsid -f /bin/bash "$RUN/run.sh"
    else
      perl -e 'exit 0 if fork; use POSIX (); POSIX::setsid() or die; exec @ARGV or die' \
        /bin/bash "$RUN/run.sh"
    fi
  )
}

status_of() {
  node "$RENDERER" "$1/events.jsonl" --status
}

mkdir -p "$CODEX_BIN" "$SETSID_BIN"
cat > "$CODEX_BIN/codex" <<'EOF'
#!/bin/bash
output=
while [ "$#" -gt 0 ]; do
  case "$1" in
    -o|--output-last-message)
      output=$2
      shift 2
      ;;
    -C|--cd|--sandbox|-m|--model|-c|--config)
      shift 2
      ;;
    --json|exec)
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
[ ! -s "$TEST_ROOT/launch-one.stdout" ] || fail "launcher leaked stdout"
[ ! -s "$TEST_ROOT/launch-one.stderr" ] || fail "launcher leaked stderr"
grep -q '^exit=0 handoff=ready ' "$RUN_ONE/result.txt" || fail "ready marker missing"
grep -q 'payload-token-SUCCESS' "$RUN_ONE/report.md" || fail "stdin prompt did not reach report"
[ ! -e "$RUN_ONE/final.md" ] || fail "obsolete final.md was created"
status_of "$RUN_ONE" | grep -q '^state    DONE exit=0 handoff=ready' || fail "DONE status missing"
pass "Perl fallback keeps every Codex channel in files"

WORKSPACE_TWO="$TEST_ROOT/workspace 한글 [x] \$dollar \"quote\""
RUN_TWO="$WORKSPACE_TWO/.agent-runs/codex/run with spaces"
launch_run "$WORKSPACE_TWO" "$RUN_TWO" SUCCESS "$SETSID_BIN:$BASE_PATH" \
  > "$TEST_ROOT/launch-two.stdout" 2> "$TEST_ROOT/launch-two.stderr"
wait_for_terminal "$RUN_TWO"
grep -Fq "workspace=$WORKSPACE_TWO " "$RUN_TWO/result.txt" || fail "complex workspace path changed"
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
status_of "$RUN_FOUR" | grep -q '^state    EXITED exit=7 handoff=incomplete' || fail "EXITED status missing"
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

printf 'PASS: %d contract scenarios\n' "$PASS"
