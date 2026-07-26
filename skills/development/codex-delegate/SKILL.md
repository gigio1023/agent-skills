---
name: codex-delegate
description: >
  Use when a Claude Code or Cursor main session should delegate a packaged,
  bounded task to the Codex CLI — implementation, investigation, or review —
  through codex exec, or when a delegated run must be resumed, followed, or
  cancelled. Provides a prompt-packet checklist, model and effort routing,
  dispatch patterns, a canonical run template with explicit sandbox, thread-ID
  resume and cancellation recipes, and a read-only event renderer. NOT for the
  official Codex plugin commands, general multi-agent orchestration, or
  delegating to Cursor (cursor-cli-delegation).
---

# Codex Delegate

Delegate a complete, bounded task from the main session to the Codex CLI with
`codex exec --json`. No plugin, broker, or daemon: the host packages intent,
launches one `codex` child, watches it through a read-only renderer, and
verifies the outcome.

Requirements: `codex` CLI ≥ 0.145, logged in; `openssl` for run IDs;
`bun` (preferred) or Node ≥ 18 for the renderer.

## 1. Package the mission

Codex sees the packet plus whatever it discovers in the workspace. Write the
smallest complete set of:

- objective and an observable definition of done;
- intent, context, and decisions that exist only in the host conversation,
  plus the paths, plans, or artifacts Codex cannot discover;
- scope in and out, and the decisions Codex may make alone;
- authority boundaries and pause conditions, including intended external
  effects (network, MCP tools, credentials);
- verification commands and the final response contract.

Normally the deliverable is a file: have Codex write its report to
`$RUN/report.md` (expand the path in the packet); the final message is a short
summary plus that path, which you read and deliver. Template and worked
example: [references/prompt-packet.md](references/prompt-packet.md).

## 2. Launch — canonical run template

Copy as-is; adjust `$DIR`, `$SANDBOX`, and optional flags:

```bash
DIR="$(pwd)"              # target workspace
SANDBOX=workspace-write   # see the mission mapping below
RUN="$DIR/.agent-runs/codex/$(date -u +%Y%m%dT%H%M%SZ)-$(openssl rand -hex 4)"
mkdir -p "${RUN%/*}" && mkdir "$RUN" &&
  echo "sandbox=$SANDBOX workspace=$DIR started=$(date -u +%FT%TZ)" > "$RUN/result.txt"
# then write your mission packet to "$RUN/prompt.md"
codex exec --json -C "$DIR" --sandbox "$SANDBOX" -o "$RUN/final.md" - \
  < "$RUN/prompt.md" > "$RUN/events.jsonl" 2> "$RUN/stderr.log"
echo "exit=$? finished=$(date -u +%FT%TZ)" >> "$RUN/result.txt"
```

The final `mkdir` is non-`-p`: a run-ID collision must fail, not merge into a
live run.

Non-negotiable rules:

- `--sandbox` is always explicit; one `$SANDBOX` feeds the flag and
  `result.txt`. Pick it from what the mission must produce: context back in
  the reply → `read-only`; a report file, the usual case → `workspace-write`
  with the report at `$RUN/report.md`; shell network (mass-clone, then
  analyze) → add the network override below and clone inside the workspace;
  `danger-full-access` only when the mission needs the whole machine and the
  user said so — never to mass-clone unknown repos, peak prompt-injection
  surface. Full mapping: [references/run-recipes.md](references/run-recipes.md).
- Never pass `--dangerously-bypass-approvals-and-sandbox`, and never use `-c`
  to change `sandbox_mode` or the approval policy. Exactly two overrides are
  sanctioned: `sandbox_workspace_write.network_access=true` for shell network
  and `model_reasoning_effort="…"` for effort — declare either visibly.
- The prompt travels as a file through stdin, never as an argv argument.
- Fine to add: `-m`, `-p`, `--output-schema`. Append every flag and override
  you use to the `result.txt` line so a resume can match them.

## Model and dispatch

- Default `gpt-5.6-sol` at `high` effort; pass `-m gpt-5.6-sol` when the
  environment default is unknown. `codex exec` has no effort flag — effort
  rides the second sanctioned `-c`: `-c model_reasoning_effort="high"`.
- Effort by mission: mechanical edits `medium`, implementation or
  investigation `high`, adversarial review or hard debugging `xhigh`. A fast
  variant or lower effort only when the user asks.
- Sol-family packets: shape with the sibling `gpt56-sol-prompting-guide`, and
  grant Codex internal subagents when subtasks are parallel.
- Dispatch: a courier subagent on the host's light tier by default, background
  shell for trivial runs, never a polling wrapper. Both:
  [references/model-and-dispatch.md](references/model-and-dispatch.md).

## 3. Observe

```bash
bun scripts/render-events.mjs "$RUN/events.jsonl" --tail 20
```

(`scripts/` is relative to this skill's dir; `node` works too.) One capped
line per action; command output, diffs, and deltas are dropped.
`events.jsonl` keeps the raw stream — grep it selectively rather than reading
it whole.

Artifacts are evidence, not proof: a `workspace-write` delegate can rewrite
its own run directory — go `read-only` or move `RUN` outside it when a log
must hold up.

## 4. Verify — output is input, not proof

After a delegated write, inspect the workspace yourself: `git diff`, run the
packet's verification commands, then report. Never forward `report.md` or the
final message as the outcome, unverified.

## 5. Resume — explicit thread ID only

```bash
DIR="$(pwd)"; RUN="$DIR/.agent-runs/codex/ORIG_RUN_ID"  # the run being resumed
head -n1 "$RUN/events.jsonl"   # thread_id is on line 1
SANDBOX=read-only              # reuse the original's sandbox (its result.txt);
                               # widen only on new authority
NEW="$DIR/.agent-runs/codex/$(date -u +%Y%m%dT%H%M%SZ)-$(openssl rand -hex 4)"
mkdir -p "${NEW%/*}" && mkdir "$NEW" &&
  echo "sandbox=$SANDBOX workspace=$DIR started=$(date -u +%FT%TZ) thread=THREAD_ID resumed_from=${RUN##*/}" > "$NEW/result.txt"
# then write your follow-up packet to "$NEW/prompt.md"
codex exec -C "$DIR" --sandbox "$SANDBOX" resume THREAD_ID --json \
  -o "$NEW/final.md" - < "$NEW/prompt.md" > "$NEW/events.jsonl" 2> "$NEW/stderr.log"
echo "exit=$? finished=$(date -u +%FT%TZ)" >> "$NEW/result.txt"
```

A resume inherits the thread, not the authority.

Flag placement matters: `-C` and `--sandbox` belong to `exec` and precede
`resume`; `--json`, `-o`, and `-m` are accepted after it (verified on
codex-cli 0.145.0 — the wrong order exits 2). Never `resume --last`: it can
pick the wrong session during parallel work. Re-pass `-m`, the effort `-c`,
and `--ignore-user-config` when the original used them; `-p` cannot carry over
(resume has no `--profile`) — re-express it through `-m` and config.

## 6. Cancel

Same session: kill the background shell through the harness — that may not
deliver SIGINT, so confirm with `pgrep -f "codex exec.*<run-id>"`. Across
sessions: send **SIGINT** to the codex PID first — codex aborts the turn and
cleans up its command children (verified on 0.145.0). SIGTERM and group kills
orphan them: codex spawns commands in their own process groups. Escalation,
concurrency, troubleshooting: [references/run-recipes.md](references/run-recipes.md).

## Keep runs out of version control

`.agent-runs/` goes in the repo's local `git info/exclude`, never its
`.gitignore` — recipe in [references/run-recipes.md](references/run-recipes.md).

## Scope guard

A guide plus one read-only renderer. No daemons, brokers, background managers,
or wrapper CLI. If the contract fails in real use, report the observed failure
instead of growing the tooling.

## Gotchas

- An `error` item in `events.jsonl` is not a failed run — non-fatal warnings
  arrive the same way; `turn.failed` or a non-zero exit is the failure signal.
- `exit=0` means codex exited cleanly, not that the task succeeded: judge it
  from the report plus your own workspace checks.
- The user's global Codex config may be more permissive, or on another model
  and effort, than you expect (e.g. `danger-full-access` by default) — hence
  the explicit `--sandbox`, and `-m` when the default is unknown.
- Concurrent runs must not write to one workspace; `read-only` runs may share
  it, writers belong in separate worktrees.
