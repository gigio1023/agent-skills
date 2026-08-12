#!/bin/bash
set -u

usage() {
  cat >&2 <<'EOF'
usage: launch-run.sh --workspace DIR --packet FILE (--sandbox MODE | --resume-from RUN) [options]

Options:
  --model MODEL              new-thread default: gpt-5.6-sol
  --effort EFFORT            new-thread default: xhigh
  --fast-requested yes|no    new-thread default: no
  --network-access yes|no    new-thread default: no; yes requires workspace-write
  --ignore-user-config yes|no
                              new-thread default: no
  --skip-git-repo-check yes|no
                              new-thread default: no
  --resume-from RUN          inherit a prior run's thread and launch settings
  --run-dir DIR              default: WORKSPACE/.agent-runs/codex/<generated-id>
EOF
}

fail() {
  printf 'launch-run: %s\n' "$*" >&2
  exit 64
}

WORKSPACE=
SANDBOX=
SANDBOX_SET=no
PACKET=
MODEL=
MODEL_SET=no
EFFORT=
EFFORT_SET=no
FAST_REQUESTED=
FAST_REQUESTED_SET=no
NETWORK_ACCESS=
NETWORK_ACCESS_SET=no
IGNORE_USER_CONFIG=
IGNORE_USER_CONFIG_SET=no
SKIP_GIT_REPO_CHECK=
SKIP_GIT_REPO_CHECK_SET=no
RESUME_FROM=
RESUME_THREAD=
RESUMED_FROM=
RUN=

while [ "$#" -gt 0 ]; do
  case "$1" in
    --workspace|--sandbox|--packet|--model|--effort|--fast-requested|--network-access|--ignore-user-config|--skip-git-repo-check|--resume-from|--run-dir)
      [ "$#" -ge 2 ] || fail "$1 requires a value"
      case "$1" in
        --workspace) WORKSPACE=$2 ;;
        --sandbox) SANDBOX=$2; SANDBOX_SET=yes ;;
        --packet) PACKET=$2 ;;
        --model) MODEL=$2; MODEL_SET=yes ;;
        --effort) EFFORT=$2; EFFORT_SET=yes ;;
        --fast-requested) FAST_REQUESTED=$2; FAST_REQUESTED_SET=yes ;;
        --network-access) NETWORK_ACCESS=$2; NETWORK_ACCESS_SET=yes ;;
        --ignore-user-config) IGNORE_USER_CONFIG=$2; IGNORE_USER_CONFIG_SET=yes ;;
        --skip-git-repo-check) SKIP_GIT_REPO_CHECK=$2; SKIP_GIT_REPO_CHECK_SET=yes ;;
        --resume-from) RESUME_FROM=$2 ;;
        --run-dir) RUN=$2 ;;
      esac
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *) fail "unknown argument: $1" ;;
  esac
done

[ -n "$WORKSPACE" ] || fail "--workspace is required"
[ -d "$WORKSPACE" ] || fail "workspace does not exist: $WORKSPACE"
[ -s "$PACKET" ] || fail "packet is missing or empty: $PACKET"

if [ -n "$RESUME_FROM" ]; then
  [ -f "$RESUME_FROM/result.txt" ] || fail "resume source has no result.txt: $RESUME_FROM"
  [ -s "$RESUME_FROM/events.jsonl" ] || fail "resume source has no events.jsonl: $RESUME_FROM"
  ORIGINAL_PROVENANCE=$(sed -n '1p' "$RESUME_FROM/result.txt")
  RESUME_THREAD=$(sed -n '1s/.*"thread_id":"\([^"]*\)".*/\1/p' "$RESUME_FROM/events.jsonl")
  [ -n "$RESUME_THREAD" ] || fail "resume source has no thread ID: $RESUME_FROM"
  if ! grep -q '^exit=' "$RESUME_FROM/result.txt"; then
    ORIGINAL_PG=$(printf '%s\n' "$ORIGINAL_PROVENANCE" | sed -n 's/.* pgid=\([0-9]*\).*/\1/p')
    if [ -n "$ORIGINAL_PG" ] && kill -0 -"$ORIGINAL_PG" 2>/dev/null; then
      fail "resume source is still running: $RESUME_FROM"
    fi
  fi
  [ "$SANDBOX_SET" = yes ] ||
    SANDBOX=$(printf '%s\n' "$ORIGINAL_PROVENANCE" | sed -n 's/^sandbox=\([^ ]*\).*/\1/p')
  [ "$MODEL_SET" = yes ] ||
    MODEL=$(printf '%s\n' "$ORIGINAL_PROVENANCE" | sed -n 's/.* model=\([^ ]*\).*/\1/p')
  [ "$EFFORT_SET" = yes ] ||
    EFFORT=$(printf '%s\n' "$ORIGINAL_PROVENANCE" | sed -n 's/.* effort=\([^ ]*\).*/\1/p')
  if [ "$FAST_REQUESTED_SET" = no ]; then
    FAST_REQUESTED=$(printf '%s\n' "$ORIGINAL_PROVENANCE" |
      sed -n 's/.* fast_requested=\([^ ]*\).*/\1/p')
    FAST_REQUESTED=${FAST_REQUESTED:-no}
  fi
  if [ "$NETWORK_ACCESS_SET" = no ]; then
    NETWORK_ACCESS=$(printf '%s\n' "$ORIGINAL_PROVENANCE" |
      sed -n 's/.* network=\([^ ]*\).*/\1/p')
    case "${NETWORK_ACCESS:-no}" in
      yes|true|on|enabled) NETWORK_ACCESS=yes ;;
      no|false|off|disabled) NETWORK_ACCESS=no ;;
      *) fail "resume source has invalid network provenance: $NETWORK_ACCESS" ;;
    esac
  fi
  if [ "$IGNORE_USER_CONFIG_SET" = no ]; then
    IGNORE_USER_CONFIG=$(printf '%s\n' "$ORIGINAL_PROVENANCE" |
      sed -n 's/.* ignore_user_config=\([^ ]*\).*/\1/p')
    IGNORE_USER_CONFIG=${IGNORE_USER_CONFIG:-no}
  fi
  if [ "$SKIP_GIT_REPO_CHECK_SET" = no ]; then
    SKIP_GIT_REPO_CHECK=$(printf '%s\n' "$ORIGINAL_PROVENANCE" |
      sed -n 's/.* skip_git_repo_check=\([^ ]*\).*/\1/p')
    SKIP_GIT_REPO_CHECK=${SKIP_GIT_REPO_CHECK:-no}
  fi
  RESUMED_FROM=$(basename "$RESUME_FROM")
else
  [ "$SANDBOX_SET" = yes ] || fail "--sandbox is required for a new thread"
  [ "$MODEL_SET" = yes ] || MODEL=gpt-5.6-sol
  [ "$EFFORT_SET" = yes ] || EFFORT=xhigh
  [ "$FAST_REQUESTED_SET" = yes ] || FAST_REQUESTED=no
  [ "$NETWORK_ACCESS_SET" = yes ] || NETWORK_ACCESS=no
  [ "$IGNORE_USER_CONFIG_SET" = yes ] || IGNORE_USER_CONFIG=no
  [ "$SKIP_GIT_REPO_CHECK_SET" = yes ] || SKIP_GIT_REPO_CHECK=no
fi

[ -n "$SANDBOX" ] || fail "sandbox provenance is missing"
[ -n "$MODEL" ] || fail "model must not be empty"
[ -n "$EFFORT" ] || fail "effort must not be empty"

case "$SANDBOX" in
  read-only|workspace-write|danger-full-access) ;;
  *) fail "sandbox must be read-only, workspace-write, or danger-full-access" ;;
esac

case "$FAST_REQUESTED" in
  yes) SERVICE_TIER=priority ;;
  no) SERVICE_TIER=default ;;
  *) fail "--fast-requested must be yes or no" ;;
esac

case "$NETWORK_ACCESS" in
  yes)
    [ "$SANDBOX" = workspace-write ] ||
      fail "--network-access=yes requires --sandbox=workspace-write"
    ;;
  no) ;;
  *) fail "--network-access must be yes or no" ;;
esac

case "$IGNORE_USER_CONFIG" in
  yes|no) ;;
  *) fail "--ignore-user-config must be yes or no" ;;
esac

case "$SKIP_GIT_REPO_CHECK" in
  yes|no) ;;
  *) fail "--skip-git-repo-check must be yes or no" ;;
esac

DIR=$(cd "$WORKSPACE" && pwd -P) || exit 64
if [ -z "$RUN" ]; then
  RUN_PARENT="$DIR/.agent-runs/codex"
  mkdir -p "$RUN_PARENT" || exit 1
  RUN="$RUN_PARENT/$(date -u +%Y%m%dT%H%M%SZ)-$(openssl rand -hex 4)"
else
  RUN_PARENT=$(dirname "$RUN")
  mkdir -p "$RUN_PARENT" || exit 1
  RUN_PARENT=$(cd "$RUN_PARENT" && pwd -P) || exit 1
  RUN="$RUN_PARENT/$(basename "$RUN")"
fi

mkdir "$RUN" || fail "run directory already exists or cannot be created: $RUN"
cp "$PACKET" "$RUN/prompt.md" || exit 1

export DIR SANDBOX MODEL EFFORT FAST_REQUESTED SERVICE_TIER NETWORK_ACCESS RUN
export IGNORE_USER_CONFIG SKIP_GIT_REPO_CHECK RESUME_THREAD RESUMED_FROM
cat > "$RUN/run.sh" <<'EOF'
#!/bin/bash
if [ -n "$RESUME_THREAD" ]; then
  printf 'sandbox=%s workspace=%s started=%s pgid=%s thread=%s resumed_from=%s model=%s effort=%s fast_requested=%s tier=%s network=%s ignore_user_config=%s skip_git_repo_check=%s\n' \
    "$SANDBOX" "$DIR" "$(date -u +%FT%TZ)" "$$" "$RESUME_THREAD" \
    "$RESUMED_FROM" "$MODEL" "$EFFORT" "$FAST_REQUESTED" "$SERVICE_TIER" \
    "$NETWORK_ACCESS" "$IGNORE_USER_CONFIG" "$SKIP_GIT_REPO_CHECK" \
    > "$RUN/result.txt"
else
  printf 'sandbox=%s workspace=%s started=%s pgid=%s model=%s effort=%s fast_requested=%s tier=%s network=%s ignore_user_config=%s skip_git_repo_check=%s\n' \
    "$SANDBOX" "$DIR" "$(date -u +%FT%TZ)" "$$" "$MODEL" "$EFFORT" \
    "$FAST_REQUESTED" "$SERVICE_TIER" "$NETWORK_ACCESS" \
    "$IGNORE_USER_CONFIG" "$SKIP_GIT_REPO_CHECK" > "$RUN/result.txt"
fi
trap ':' INT
if [ -n "$RESUME_THREAD" ]; then
  CODEX_ARGS=(exec -C "$DIR" --sandbox "$SANDBOX" resume "$RESUME_THREAD"
    --json -m "$MODEL" -c "model_reasoning_effort=$EFFORT"
    -c "service_tier=$SERVICE_TIER")
else
  CODEX_ARGS=(exec --json -C "$DIR" --sandbox "$SANDBOX" -m "$MODEL"
    -c "model_reasoning_effort=$EFFORT" -c "service_tier=$SERVICE_TIER")
fi
if [ "$NETWORK_ACCESS" = yes ]; then
  CODEX_ARGS+=(-c sandbox_workspace_write.network_access=true)
fi
if [ "$IGNORE_USER_CONFIG" = yes ]; then
  CODEX_ARGS+=(--ignore-user-config)
fi
if [ "$SKIP_GIT_REPO_CHECK" = yes ]; then
  CODEX_ARGS+=(--skip-git-repo-check)
fi
codex "${CODEX_ARGS[@]}" -o "$RUN/report.md" - < "$RUN/prompt.md" \
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
chmod +x "$RUN/run.sh"

if command -v setsid >/dev/null 2>&1; then
  setsid -f /bin/bash "$RUN/run.sh"
else
  perl -e 'exit 0 if fork; use POSIX (); POSIX::setsid() or die; exec @ARGV or die' \
    /bin/bash "$RUN/run.sh"
fi

TRIES=0
while [ ! -s "$RUN/result.txt" ]; do
  TRIES=$((TRIES + 1))
  [ "$TRIES" -lt 100 ] || fail "run launched but provenance did not appear: $RUN"
  sleep 0.05
done

if [ -n "$RESUME_THREAD" ]; then
  THREAD=$RESUME_THREAD
else
  THREAD=pending
  TRIES=0
  while [ "$THREAD" = pending ] && [ "$TRIES" -lt 100 ]; do
    if [ -s "$RUN/events.jsonl" ]; then
      THREAD=$(sed -n '1s/.*"thread_id":"\([^"]*\)".*/\1/p' "$RUN/events.jsonl")
      [ -n "$THREAD" ] || THREAD=pending
    fi
    TRIES=$((TRIES + 1))
    [ "$THREAD" != pending ] || sleep 0.05
  done
fi

printf 'run=%s\n' "$RUN"
printf 'result=%s\n' "$RUN/result.txt"
printf 'events=%s\n' "$RUN/events.jsonl"
printf 'report=%s\n' "$RUN/report.md"
printf 'thread=%s\n' "$THREAD"
printf 'provenance=%s\n' "$(sed -n '1p' "$RUN/result.txt")"
