---
name: codex-delegate
description: >
  Use only when the user explicitly invokes or names codex-delegate to
  delegate a packaged, bounded task from a Claude Code or Cursor main session
  to the Codex CLI through codex exec, or to resume, follow, or cancel such a
  run. Provides a prompt-packet checklist, model, effort and speed routing, a
  durable detached run template with explicit sandbox, a four-state run status
  check, thread-ID resume and cancellation recipes, and a read-only event
  renderer. NOT for automatic routing from mere mentions of Codex or GPT, not
  for use from inside the Codex harness itself, and not for the official
  Codex plugin commands, general multi-agent orchestration, or delegating to
  Cursor (cursor-cli-delegation).
---

# Codex Delegate

Delegate a complete, bounded task from the main session to the Codex CLI with
`codex exec --json`. No plugin, broker, or daemon: the host packages intent,
launches one detached `codex` run that outlives the command that started it,
checks it through a read-only renderer, and verifies the outcome.

Requirements: `codex` CLI ≥ 0.145, logged in; `openssl` for run IDs; `perl`
for the detached launch (system perl is enough, and macOS has no `setsid`);
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
summary plus that path, which you read and deliver. What the mission covers,
judgment and opinion included, is the main session's call written into the
packet. Template and worked example:
[references/prompt-packet.md](references/prompt-packet.md).

## 2. Launch — durable run template

Copy as-is; adjust `$DIR`, `$SANDBOX`, and the flags inside `run.sh`:

```bash
DIR="$(pwd)"              # target workspace
SANDBOX=workspace-write   # see the mission mapping below
RUN="$DIR/.agent-runs/codex/$(date -u +%Y%m%dT%H%M%SZ)-$(openssl rand -hex 4)"
mkdir -p "${RUN%/*}" && mkdir "$RUN"
# then write your mission packet to "$RUN/prompt.md"
cat > "$RUN/run.sh" <<EOF
#!/bin/bash
echo "sandbox=$SANDBOX workspace=$DIR started=\$(date -u +%FT%TZ) pgid=\$\$ -m gpt-5.6-sol -c model_reasoning_effort=\"high\" -c service_tier=\"priority\"" > "$RUN/result.txt"
codex exec --json -C "$DIR" --sandbox "$SANDBOX" -m gpt-5.6-sol \\
  -c model_reasoning_effort="high" -c service_tier="priority" \\
  -o "$RUN/final.md" - < "$RUN/prompt.md" > "$RUN/events.jsonl" 2> "$RUN/stderr.log"
echo "exit=\$? finished=\$(date -u +%FT%TZ)" >> "$RUN/result.txt"
EOF
perl -e 'exit 0 if fork; use POSIX (); POSIX::setsid() or die; exec @ARGV or die' \
  /bin/bash "$RUN/run.sh"
```

Then arm one disposable watcher, as a background shell in the launching
session, so its exit is the completion signal:

```bash
until grep -q '^exit=' "$RUN/result.txt"; do sleep 10; done
```

Detachment is the whole point: the harness kills a command's process group, so
`&` and `nohup` both die with the launcher (measured), while a forked `setsid`
run lands under pid 1 and always records its own terminal state.

Non-negotiable rules:

- `--sandbox` is always explicit, and one `$SANDBOX` feeds both the flag and
  `result.txt`. Pick it from what the mission must produce — reply-only →
  `read-only`; a report file, the usual case → `workspace-write`;
  `danger-full-access` only when the user said so. Mapping and the network
  override: [references/run-recipes.md](references/run-recipes.md).
- Never pass `--dangerously-bypass-approvals-and-sandbox`, and never use `-c`
  to change `sandbox_mode` or the approval policy. Exactly three overrides are
  sanctioned: `model_reasoning_effort="…"`, `service_tier="priority"`, and
  `sandbox_workspace_write.network_access=true` — declare each visibly.
- The prompt travels as a file through stdin, never as an argv argument.
- Fine to add: `-m`, `-p`, `--output-schema`. Every flag and override belongs
  on the `result.txt` line so a resume can match them.

## Model and dispatch

- Default `gpt-5.6-sol` at `high` effort with `service_tier="priority"`, the
  tier Codex calls Fast (1.5× speed, heavier quota). `codex exec` has a flag
  for neither; both ride sanctioned `-c` overrides.
- Two separate dials. Effort follows the mission — `medium` mechanical,
  `high` implementation or investigation, `xhigh` adversarial review. Speed
  does not: leave Fast on unless the run is long and unhurried and quota
  matters more than the wait.
- Sol-family packets: shape with the sibling `gpt56-sol-prompting-guide`, and
  grant Codex internal subagents when subtasks are parallel.
- Dispatch: one run is the template above, owned by the main session. Give
  several runs to a subagent on the host's light tier to keep the launch
  mechanics out of the main context; it relays and manages, judgment stays
  with the main session.
  [references/model-and-dispatch.md](references/model-and-dispatch.md).

## 3. Observe

```bash
bun scripts/render-events.mjs "$RUN/events.jsonl" --status    # is it alive?
bun scripts/render-events.mjs "$RUN/events.jsonl" --tail 20   # what has it done?
```

(`scripts/` is relative to this skill's dir; `node` works too.) `--status`
reads `result.txt` and probes the recorded `pgid` with signal 0, yielding
DONE/EXITED, RUNNING, DIED, or UNKNOWN. **DIED** is the state that did not
exist before: no terminal line and no process group means killed rather than
finished, so resume the thread instead of starting over. `--tail` prints one
capped line per action, dropping command output, diffs, and deltas;
`events.jsonl` keeps the raw stream, so grep it rather than read it whole.
States, thresholds, and why silence is not a hang:
[references/run-recipes.md](references/run-recipes.md).

Artifacts are evidence, not proof: a `workspace-write` delegate can rewrite its
own run directory, so go `read-only` or move `RUN` outside it when a log must
hold up.

## 4. Verify — output is input, not proof

After a delegated write, inspect the workspace yourself: `git diff`, run the
packet's verification commands, then report. Never forward `report.md` or the
final message as the outcome, unverified.

## 5. Resume — explicit thread ID only

The thread ID is on line 1 of `events.jsonl`. A resume reruns the durable
template in a fresh run directory with the original's sandbox, inheriting the
thread but not the authority, and it recovers a run killed mid-turn (verified:
context survived a SIGINT during a command). Never `resume --last`. Recipe and
flag ordering: [references/run-recipes.md](references/run-recipes.md).

## 6. Cancel

`result.txt` carries the `pgid`, so one signal to the group cancels a run from
any session:

```bash
PG=$(sed -n '1s/.*pgid=\([0-9]*\).*/\1/p' "$RUN/result.txt")
[ -n "$PG" ] && kill -INT -"$PG"
```

Verified on 0.145.0: the turn aborts, command children are reaped with no
orphans, and the wrapper still appends `exit=1`, so a cancelled run stays
distinguishable from a killed one. Escalation:
[references/run-recipes.md](references/run-recipes.md).

## Scope guard

A guide plus one read-only renderer. No daemons, brokers, background managers,
or wrapper CLI; the per-run `run.sh` is provenance, written once and gone with
the run directory. If the contract fails in real use, report the failure
instead of growing the tooling.

## Gotchas

- An `error` item is not a failed run — non-fatal warnings arrive the same way,
  an unsupported `service_tier` among them, so its absence is how you know Fast
  applied. `turn.failed` or a non-zero exit is the failure signal.
- `exit=0` means codex exited cleanly, not that the task succeeded: judge it
  from the report plus your own workspace checks.
- The user's global Codex config may be more permissive or on another model
  than you expect (e.g. `danger-full-access`) — hence the explicit `--sandbox`
  and `-m`.
- Concurrent runs must not write to one workspace; `read-only` runs may share
  it, writers belong in separate worktrees.
- A non-git workspace refuses the launch until `--skip-git-repo-check` is
  added; a config `trust_level` entry does not substitute.
- `.agent-runs/` belongs in the repo's local `git info/exclude`, never its
  `.gitignore`, and tree-walking repo tooling may need to skip it too —
  [references/run-recipes.md](references/run-recipes.md).
