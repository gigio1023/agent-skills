---
name: codex-delegate
description: >
  Use only from Claude Code, Cursor, or another non-Codex host harness when the
  user explicitly invokes or names codex-delegate to delegate a packaged,
  bounded task to the Codex CLI, or to resume, follow, or cancel such a run.
  Runs the designated highest-capability Codex model in Fast mode by default,
  lets Codex freely coordinate internal parallel subagents, and lets the host
  set Codex's judgment authority in the packet. Provides a durable detached run,
  file-only handoff, explicit sandbox, status, resume, cancellation, and a
  read-only renderer.
  NOT for automatic routing from mere mentions of Codex or GPT, use from inside
  Codex itself, official Codex plugin commands, general multi-agent
  orchestration, or delegating to Cursor (cursor-cli-delegation).
---

# Codex Delegate

Delegate a complete, bounded task from the main session to the Codex CLI with
`codex exec --json`. No plugin, broker, or daemon: the host packages intent,
launches one detached `codex` run that outlives the command that started it,
checks it through a read-only renderer, and verifies the outcome.

Execution boundary: the host is Claude Code, Cursor, or another non-Codex
harness. If this skill is invoked from inside Codex, stop instead of launching
Codex recursively. The boundary is instruction-driven; do not add harness
detection or a plugin-like management layer to enforce it.

Requirements: `codex` CLI ≥ 0.145, logged in; `openssl` for run IDs;
util-linux `setsid` when available, otherwise `perl` with POSIX support for the
detached launch (macOS has system Perl but no `setsid` command); `bun`
(preferred) or Node ≥ 18 for the renderer.

## 1. Package the mission

Codex sees the packet plus whatever it discovers in the workspace. Write the
smallest complete set of:

- objective and an observable definition of done;
- intent, context, and decisions that exist only in the host conversation,
  plus the paths, plans, or artifacts Codex cannot discover;
- scope in and out, plus how much investigation, judgment, and decision-making
  Codex owns;
- authority boundaries and pause conditions, including intended external
  effects (network, MCP tools, credentials);
- freedom to coordinate internal subagents: encouraged by default, with Codex
  choosing their number, split, and sequencing;
- verification commands and the final response contract.

The handoff is always a file. Ask Codex to return the complete report as its
final response; `-o "$RUN/report.md"` captures that response without sending
the result through the host conversation or terminal. The JSON event stream
and stderr also go only to files. The host waits for `handoff=ready`, then
reads `report.md`; no material result may exist only in a progress event.

The host may reserve consequential decisions, grant bounded judgment, or give
Codex end-to-end ownership of the mission. It need not enumerate every minor
choice: unless the packet says otherwise, Codex may make ordinary reversible
decisions inside the granted scope and pauses only when a choice crosses a
stated boundary or materially changes the mission. Template and worked example:
[references/prompt-packet.md](references/prompt-packet.md).

## 2. Launch — durable run template

Copy as-is; adjust `$DIR`, `$SANDBOX`, and the flags inside `run.sh`:

```bash
DIR="$(pwd)"              # target workspace
SANDBOX=workspace-write   # see the mission mapping below
RUN="$DIR/.agent-runs/codex/$(date -u +%Y%m%dT%H%M%SZ)-$(openssl rand -hex 4)"
mkdir -p "${RUN%/*}" && mkdir "$RUN"
# then write your mission packet to "$RUN/prompt.md"
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
if command -v setsid >/dev/null 2>&1; then
  setsid -f /bin/bash "$RUN/run.sh"
else
  perl -e 'exit 0 if fork; use POSIX (); POSIX::setsid() or die; exec @ARGV or die' \
    /bin/bash "$RUN/run.sh"
fi
```

Then arm one disposable watcher, as a background shell in the launching
session, so its exit is the completion signal:

```bash
while :; do
  grep -q '^exit=' "$RUN/result.txt" 2>/dev/null && break
  PG=$(sed -n '1s/.*pgid=\([0-9]*\).*/\1/p' "$RUN/result.txt" 2>/dev/null)
  [ -n "$PG" ] && ! kill -0 -"$PG" 2>/dev/null && break
  sleep 10
done
```

Detachment is the whole point: the harness kills a command's process group, so
`&` and `nohup` both die with the launcher (measured), while either detached
launch branch creates a new session. The watcher exits on a terminal line or a
vanished process group; in the latter case `--status` reports `DIED`.

Non-negotiable rules:

- `--sandbox` is always explicit, and one `$SANDBOX` feeds both the flag and
  `result.txt`. Pick it from workspace effects: investigation with no workspace
  edits → `read-only`; local edits → `workspace-write`; `danger-full-access`
  only when the user said so. The CLI writes `report.md` in every mode.
  Mapping and the network override:
  [references/run-recipes.md](references/run-recipes.md).
- Never pass `--dangerously-bypass-approvals-and-sandbox`, and never use `-c`
  to change `sandbox_mode` or the approval policy. Exactly three overrides are
  sanctioned: `model_reasoning_effort="…"`, `service_tier="priority"`, and
  `sandbox_workspace_write.network_access=true` — declare each visibly.
- The prompt travels as `prompt.md` through stdin. The result travels as
  `report.md` through `-o`; stdout and stderr are redirected before launch, so
  no Codex result channel reaches the caller or host conversation.
- Fine to add: `-m`, `-p`, `--output-schema`. Every flag and override belongs
  on the `result.txt` line so a resume can match them.

## Model and dispatch

- Default `gpt-5.6-sol` at `high` effort with `service_tier="priority"`, the
  tier Codex calls Fast (1.5× speed, heavier quota). `codex exec` has a flag
  for neither; both ride sanctioned `-c` overrides.
- Two separate dials. Effort follows the mission — `medium` mechanical,
  `high` implementation or investigation, `xhigh` adversarial review. Speed
  does not: leave Fast on unless the user explicitly asks otherwise. Never
  silently downgrade the model or omit Fast; report unavailability or drift.
- Sol-family packets: shape with the sibling `gpt56-sol-prompting-guide`, and
  strongly encourage internal subagents. Codex decides whether to spawn them,
  how many to use, and how to coordinate them; independent branches should run
  in parallel, while dependent work and conflicting writes stay sequential.
- Judgment ownership comes from the packet. Codex may execute fixed decisions,
  decide within named bounds, or own the mission's investigation, judgment,
  and decisions end to end. Do not force decisions back to the host when the
  packet already granted them.
- Dispatch: one run is the template above, owned by the main session. Give
  several runs to a subagent on the host's light tier to keep the launch
  mechanics out of the main context; it relays and manages, while each
  packet's judgment grant remains intact.
  [references/model-and-dispatch.md](references/model-and-dispatch.md).

## 3. Observe

```bash
bun scripts/render-events.mjs "$RUN/events.jsonl" --status    # is it alive?
bun scripts/render-events.mjs "$RUN/events.jsonl" --tail 20   # what has it done?
```

(`scripts/` is relative to this skill's dir; `node` works too.) `--status`
reads `result.txt` and probes the recorded `pgid` with signal 0, yielding
DONE/INCOMPLETE/EXITED, RUNNING, DIED, or UNKNOWN. `DONE` requires both
`exit=0` and a non-empty captured report. **DIED** means no terminal line and
no process group, so resume the thread instead of starting over. `--tail`
prints one capped line per action, dropping command output, diffs, and deltas;
`events.jsonl` keeps the raw stream, so grep it rather than read it whole.
States, thresholds, and why silence is not a hang:
[references/run-recipes.md](references/run-recipes.md).

Artifacts are evidence, not proof: a `workspace-write` delegate can rewrite its
own run directory, so go `read-only` or move `RUN` outside it when a log must
hold up.

## 4. Verify — output is input, not proof

After a delegated write, inspect the workspace yourself: `git diff`, run the
packet's verification commands, then report. Treat `report.md` as the only
handoff and as input, not proof; never forward it unverified.

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

An instruction-driven guide plus one read-only renderer. No harness detection,
daemons, brokers, background managers, automatic retries, activity heuristics,
or wrapper CLI; the per-run `run.sh` is provenance, written once and gone with
the run directory. Keep model, collaboration, and judgment boundaries in the
description, packet, and canonical command. If the contract fails in real use,
report the failure instead of growing the tooling.

## Gotchas

- An `error` item is not a failed run — non-fatal warnings arrive the same way,
  an unsupported `service_tier` among them, so its absence is how you know Fast
  applied. `turn.failed` or a non-zero exit is the failure signal.
- `exit=0 handoff=ready` means Codex exited cleanly and produced a non-empty
  report. It does not prove the task succeeded: judge the report plus your own
  workspace checks.
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
