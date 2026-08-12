---
name: codex-delegate
description: >
  Use only from Claude Code, Cursor, or another non-Codex host harness when the
  user explicitly invokes or names codex-delegate to delegate a packaged,
  bounded task to the Codex CLI, or to resume, follow, or cancel such a run.
  Defaults to gpt-5.6-sol at xhigh effort on the standard non-Fast tier, with
  task-shaped routing to Terra or another model and effort when justified. Fast
  mode requires an explicit user request. Lets the host set Codex's judgment and
  internal-subagent authority in the packet. Uses a host-side launcher subagent
  as the default execution path when the harness supports one while the main
  host retains lifecycle ownership. Provides a durable detached run, file-only
  handoff, explicit sandbox, status, resume, cancellation, and a read-only
  renderer.
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
- whether internal subagents are useful: allow Codex to choose their number and
  topology when the mission has genuinely independent branches;
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

## 2. Launch through a host-side launcher subagent

The main host writes the final immutable packet to a file and resolves the
workspace, sandbox, model, effort, Fast assertion, and network grant. When the
host harness exposes native subagents, give those fixed inputs to a host-side
launcher subagent. It invokes the bundled deterministic launcher and returns
its stdout unchanged as the launch manifest. When model pinning is available,
use the harness's reliable lightweight model for this mechanical role; in
Claude Code the intended route is Sonnet-class. Escalate only after
unavailability or a manifest-contract failure. `SKILL_DIR` below means the
directory containing this active `SKILL.md`:

```bash
bash "$SKILL_DIR/scripts/launch-run.sh" \
  --workspace "$DIR" \
  --sandbox "$SANDBOX" \
  --packet "$PACKET" \
  --model gpt-5.6-sol \
  --effort xhigh \
  --fast-requested no \
  --network-access no \
  --ignore-user-config no \
  --skip-git-repo-check no
```

`--fast-requested=yes` is valid only after an explicit user Fast request. The
script derives `service_tier=priority`; every other run records and passes
`service_tier=default`. Use `--run-dir` only when the main host deliberately
chooses an external evidence location or stable run ID.

The manifest contains `run`, `result`, `events`, `report`, `thread`, and the
exact provenance line. `thread=pending` is valid when Codex has not emitted its
first event within the launch script's bounded wait. The launcher subagent checks
the manifest and provenance, returns them to the main host, and stops. It never
waits for task completion or reads `report.md`.

The main host owns the watcher. Arm it after receiving the manifest so its exit
can wake the session that will verify the result:

```bash
while :; do
  grep -q '^exit=' "$RUN/result.txt" 2>/dev/null && break
  PG=$(sed -n '1s/.*pgid=\([0-9]*\).*/\1/p' "$RUN/result.txt" 2>/dev/null)
  [ -n "$PG" ] && ! kill -0 -"$PG" 2>/dev/null && break
  sleep 10
done
```

If native subagents are unavailable, the launcher subagent fails, or its
manifest is incomplete, the main host calls the same script directly. Do not
reconstruct the launch shell from memory. Detachment remains inside the script:
the durable run survives the short-lived launcher subagent or main-host command.
The watcher exits on a terminal line or vanished process group; in the latter
case `--status` reports `DIED`.

Non-negotiable rules:

- `--sandbox` is always explicit, and one `$SANDBOX` feeds both the flag and
  `result.txt`. Pick it from workspace effects: investigation with no workspace
  edits → `read-only`; local edits → `workspace-write`; `danger-full-access`
  only when the user said so. The CLI writes `report.md` in every mode.
  Mapping and the network override:
  [references/run-recipes.md](references/run-recipes.md).
- Never pass `--dangerously-bypass-approvals-and-sandbox`, and never change
  `sandbox_mode` or approval policy through config. The launcher exposes only
  model effort, the derived service tier, and the narrow workspace-write network
  override. It records all three in provenance.
- The launcher copies the immutable packet to `prompt.md`. The Codex result
  travels as `report.md` through `-o`; events and stderr stay in their files.
  Only the bounded launch manifest reaches the launcher subagent or main host.

## Model and dispatch

- Start every new run from `gpt-5.6-sol` at `xhigh` effort with
  `service_tier="default"`. An explicit user choice wins. Otherwise use Terra
  at `xhigh`, another supported model, or another effort only when task shape or
  availability gives a concrete reason. Record the resolved values and the
  reason for any deviation from the default.
- Fast is a separate dial. Set `service_tier="priority"` only when the user
  explicitly asks for Fast; urgency inferred from the task is not enough.
- Shape GPT-5.6-family packets with the sibling `gpt56-sol-prompting-guide`.
  Allow internal subagents when independent branches justify them; keep small,
  dependent, or conflicting work sequential.
- Judgment ownership comes from the packet. Codex may execute fixed decisions,
  decide within named bounds, or own the mission's investigation, judgment,
  and decisions end to end. Do not force decisions back to the host when the
  packet already granted them.
- Dispatch: the host main session owns the packet, routing decisions, watcher,
  result verification, resume decision, and cancellation. A host-side launcher
  subagent is the default execution path for one or many fixed packets. This
  role is distinct from the per-run `run.sh` wrapper and Codex's internal
  subagents. It starts each run through `launch-run.sh`, verifies initial
  provenance, returns a manifest, and stops. Main-host launch through the same
  script remains the failure fallback.
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

The main host authorizes and writes the follow-up packet, then sends its path
and the exact source run directory through the same launcher-subagent path. The
launcher calls `launch-run.sh --resume-from "$RUN"`; the script refuses an
active source run and inherits its recorded thread and launch settings into a
fresh run directory. A resume recovers a run killed mid-turn (verified: context
survived a SIGINT during a command). Never `resume --last`. Recipe and contract:
[references/run-recipes.md](references/run-recipes.md).

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

An instruction-driven guide plus one deterministic launch script and one
read-only renderer. No harness detection, daemons, brokers, background managers,
automatic retries, or activity heuristics. The script creates one durable run,
emits one manifest, and exits; the per-run `run.sh` remains exact provenance.
Keep routing, collaboration, and judgment boundaries in the description and
packet. Report a contract failure instead of silently growing the launcher's
authority.

## Gotchas

- An `error` item is not a failed run — non-fatal warnings arrive the same way,
  including an unsupported `service_tier`. Such a warning means the requested
  tier was not applied; `turn.failed` or a non-zero exit is the failure signal.
- `exit=0 handoff=ready` means Codex exited cleanly and produced a non-empty
  report. It does not prove the task succeeded: judge the report plus your own
  workspace checks.
- The user's global Codex config may be more permissive or on another model
  than you expect (e.g. `danger-full-access`) — hence the explicit `--sandbox`
  and `-m`.
- Concurrent runs must not write to one workspace; `read-only` runs may share
  it, writers belong in separate worktrees.
- A non-git workspace refuses the launch until `--skip-git-repo-check yes` is
  added; a config `trust_level` entry does not substitute.
- `.agent-runs/` belongs in the repo's local `git info/exclude`, never its
  `.gitignore`, and tree-walking repo tooling may need to skip it too —
  [references/run-recipes.md](references/run-recipes.md).
