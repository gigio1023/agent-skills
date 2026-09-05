# Run Recipes

Artifact contract, event vocabulary, concurrency, cancellation, and troubleshooting for `codex exec` delegation runs.

## Contents

- [Run directory](#run-directory)
- [Launch manifest](#launch-manifest)
- [Sandbox by mission](#sandbox-by-mission)
- [Event vocabulary](#event-vocabulary)
- [Renderer](#renderer)
- [Contract smoke test](#contract-smoke-test)
- [Run states](#run-states)
- [Concurrency](#concurrency)
- [Resume](#resume)
- [Cancel](#cancel)
- [Keeping runs out of version control](#keeping-runs-out-of-version-control)
- [Troubleshooting](#troubleshooting)

## Run directory

`<workspace>/.agent-runs/codex/<run-id>/`, run-id = UTC timestamp + random hex (e.g. `20260726T054537Z-bd8431f2`).

| File | Content |
| --- | --- |
| `prompt.md` | The immutable packet copied by `scripts/launch-run.sh` |
| `events.jsonl` | The raw JSONL stream from `--json`, as received by the host |
| `stderr.log` | Full stderr |
| `report.md` | The only handoff: the final response captured by `-o/--output-last-message` |
| `run.sh` | The detached per-run wrapper: exact executable provenance |
| `result.txt` | Provenance line, then the terminal state |

`report.md` is the only consumer-facing handoff. The JSON protocol repeats the last agent message inside `events.jsonl`; keep that raw file for diagnostics, but the host reads and verifies `report.md`. The run directory's `report.md` is reserved for `-o/--output-last-message`. Never use it as a task deliverable path. Put generated artifacts in a named workspace location and identify them in the final response.

`result.txt` line 1 records provenance — `sandbox=… workspace=… started=… pgid=… model=… effort=… fast_requested=… tier=… network=… ignore_user_config=… skip_git_repo_check=… host_route=… host_model=… routing_reason=… packet_sha256=…`, plus `thread=… resumed_from=…` for a resume. `fast_requested` is `no` unless the user explicitly requested Fast; the launch script derives `tier=default|priority` from it. `host_route` is `launcher-subagent|direct-main`. `host_model` is the exact host model ID or `unavailable`. `routing_reason` records the selected model or fallback reason. `packet_sha256` binds provenance to the copied immutable packet. `pgid` is what makes the run's liveness decidable later; it is the detached session leader, so `kill -0 -"$PGID"` answers "still alive?" and `kill -INT -"$PGID"` cancels. The terminal state is appended after codex returns:

- `exit=N handoff=ready|incomplete finished=…` — codex exited on its own. `ready` requires exit 0 and a non-empty `report.md`; all other outcomes are `incomplete`. A cancellation lands here as `exit=1 handoff=incomplete`, because the wrapper outlives the signal.
- `cancelled=…` / `cancel_failed=…` — only written by the legacy pre-`pgid` cancel path below, which had to confirm death from outside.

`exit=0 handoff=ready` means Codex exited cleanly and produced a non-empty handoff. It does not mean the task succeeded: read `report.md` and verify the workspace yourself.

These artifacts are evidence, not tamper-proof records. A `workspace-write` delegate can rewrite anything under `.agent-runs/` inside its own workspace, so a run's log cannot fully attest to that run. When a log has to hold up as proof — a review someone else will act on, a disputed change — run the mission `read-only`, or set `RUN` to a directory outside the delegate's workspace. Both are judgement calls per mission, not standing requirements.

Sandbox is not the whole capability boundary either: `--sandbox` governs the filesystem effects of shell commands, while MCP servers, network access, and web search come from the Codex config the CLI loads. In an untrusted or unfamiliar workspace, `--ignore-user-config yes` is worth considering. It keeps authentication but excludes the user's Codex configuration.

## Launch manifest

`scripts/launch-run.sh` is the only normal initial-run and resume entry point. The main host first chooses an absolute run path that does not exist. The script validates the fixed launch inputs, creates that path, copies the packet, writes the per-run wrapper, detaches the Codex process, waits only for initial provenance and a bounded thread-ID probe, then prints exactly six `key=value` lines:

```text
run=/absolute/run/directory
result=/absolute/run/directory/result.txt
events=/absolute/run/directory/events.jsonl
report=/absolute/run/directory/report.md
thread=<thread-id|pending>
provenance=<exact first result.txt line>
```

This manifest is safe to return through the launcher subagent because it has no prompt, event, stderr, or report content. `thread=pending` means startup exceeded the bounded probe; it does not mean the run failed. The main host uses `run` to arm the watcher and reads the thread ID from the first event when needed.

The script's documented invocation is from the skill root:

```bash
bash scripts/launch-run.sh \
  --workspace /absolute/workspace \
  --sandbox read-only \
  --packet /absolute/packet.md \
  --run-dir /absolute/workspace/.agent-runs/codex/20260813T010203Z-a1b2c3d4 \
  --model gpt-5.6-sol \
  --effort xhigh \
  --fast-requested no \
  --network-access no \
  --ignore-user-config no \
  --skip-git-repo-check no \
  --host-route launcher-subagent \
  --host-model claude-sonnet-5 \
  --routing-reason default
```

`--network-access=yes` requires `workspace-write`. `--ignore-user-config=yes` keeps CLI authentication while excluding the user's Codex config. `--skip-git-repo-check=yes` is required for a non-git workspace. `--run-dir` is required and may place artifacts outside the workspace. Its target directory must not already exist. Input or validation failures return nonzero before a Codex process starts.

If launcher output is lost, do not assume the launch failed. Check the exact preselected path. When it exists, recover the same six-field manifest without starting Codex:

```bash
bash scripts/launch-run.sh \
  --recover-manifest \
  --run-dir /absolute/preselected/run \
  --packet /absolute/packet.md
```

Recovery compares the supplied packet with `prompt.md`, recomputes its SHA-256, and requires matching packet and host provenance. Use the recovered run when it passes. An existing path that fails recovery is a contract failure. Only an absent path permits one direct-main launch through the normal command with the same `--run-dir`. Never retry merely because a manifest did not arrive.

## Sandbox by mission

Pick the sandbox from the workspace effects the mission needs. The CLI writes `report.md` through `-o`, outside the model's shell sandbox:

- **Investigation or review** — no workspace edits: `read-only`. The complete final response still lands in `report.md`. Built-in web search and MCP tools are not shell commands, so the filesystem sandbox does not gate them; availability comes from the Codex config.
- **Implementation or generated files** — intended workspace edits: `workspace-write`. The report remains a CLI capture, not a model-written artifact.
- **Clone, then analyze, then report** — many repositories at once: `workspace-write` plus `-c sandbox_workspace_write.network_access=true`, cloning into `$RUN/clones/`; the final response still lands in `$RUN/report.md`.
- **`danger-full-access`** — only when the mission genuinely needs the whole machine and the user said so. Mass-cloning unknown repositories is not that case: reading unfamiliar code is peak prompt-injection surface, and it wants a narrower sandbox, not the widest one.

Live evidence (codex-cli 0.145.0, verified 2026-07-26): under `--sandbox workspace-write` with the default config, `curl -sS -I https://example.com` fails with `curl: (6) Could not resolve host: example.com` — shell network is blocked, DNS included. The same command with `-c sandbox_workspace_write.network_access=true` returns `HTTP/2 200`. That narrow override is the sanctioned way to give a workspace-write run shell network: declare it in your reply and append it to the `result.txt` provenance line. Exactly three `-c` keys are sanctioned — this one, `model_reasoning_effort` for reasoning effort, and `service_tier` (`default` normally, `priority` only on an explicit Fast request) — declared and recorded the same way; `-c` still must never touch `sandbox_mode` or the approval policy.

## Event vocabulary

Observed with codex-cli 0.145.0 (recheck against live output when the CLI majors — tolerate unknown types, never hard-code an exhaustive list):

- `thread.started` — carries `thread_id`. Always the first line; this is the ID that `codex exec resume` needs.
- `turn.started` / `turn.completed` — `turn.completed` carries `usage` (input/cached/output/reasoning token counts).
- `turn.failed` — carries `error.message`.
- `item.started` / `item.updated` / `item.completed` — carry `item` with an item `type`:
  - `command_execution`: `command`, `exit_code`, `status`, and `aggregated_output` (the full command output — this payload is why raw logs get big).
  - `agent_message`: `text` (the last one ends up in `report.md` for the last message).
  - `reasoning`: summary text.
  - `file_change`, `mcp_tool_call`, `web_search`: change lists and tool/query metadata.
  - `collab_tool_call`: a root-visible internal-subagent action. It may carry receiver thread IDs and their last states, but not the children's own reasoning, commands, intermediate messages, or complete descendant tree. Treat it as a partial, version-dependent snapshot.
  - `error`: non-fatal warnings also arrive this way (e.g. a skills context budget notice) — an `error` item does not mean the run failed.

Extract the thread ID without a JSON parser:

```bash
head -n1 "$RUN/events.jsonl"
# {"type":"thread.started","thread_id":"019f9cf5-..."}
```

## Renderer

```bash
bun scripts/render-events.mjs "$RUN/events.jsonl" --tail 20   # from this skill's dir
```

`node` works identically. The renderer streams the file line by line and keeps at most `--tail N` rendered lines, so its memory is bounded by the longest single line, not by the file's size. A line over ~2 MB never reaches the JSON parser at all — it degrades to `? oversized event line`. Smoke check (also the fixture for validation):

```bash
bun scripts/render-events.mjs scripts/fixtures/sample-events.jsonl
```

Expected: one line per action — `▶`/`✓` commands with exit codes, `✉` agent message once rather than per streamed update, `file_change` paths as basenames, `⚠` warnings, and `collab` actions with any root-observed agent state counts — then unknown types as bare type names, and the degrade markers the fixture exercises: `? malformed event` for a JSON line that is not an object (a non-object `item` degrades the same way), `×?` for a `file_change` whose `changes` is not an array, `? unparseable line` for the garbage line. `item.updated` renders nothing, whatever the item type: `▶` and `✓` carry the signal, and a ✓ on an item still in progress would read as finished. The 96-char cap applies to each assembled action line (the long unknown type ends in `…`); control characters in text are replaced with spaces, so an `agent_message` carrying ESC/OSC sequences renders inert. The footer carries event/command/file-change counts and the thread ID, and is not capped.

For targeted deep-dives on the raw file, grep instead of reading it whole:

```bash
grep '"type":"turn.failed"' "$RUN/events.jsonl"
grep '"exit_code":' "$RUN/events.jsonl" | grep -v '"exit_code":0'
```

## Contract smoke test

From the skill root:

```bash
bash scripts/test-run-contract.sh
```

This uses a fake `codex` executable, makes no model or network call, and checks the complete shell contract: manifest-only launcher output; packet copying; file-only Codex stdout, stderr, event, and report channels; non-empty handoff gating; non-zero exit; process-group death; graceful group cancellation; missing provenance; concurrent read-only runs; complex paths; the native Perl fallback; and `setsid` branch selection through a local semantics-compatible shim. It also checks Sol/xhigh/non-Fast defaults, contextual Terra routing, explicit Fast provenance, optional config and git-check flags, resume inheritance, and rejection of an invalid Fast assertion. It also verifies packet-bound host provenance, manifest recovery without a second Codex launch, rejection of an invalid existing run, a recorded direct-main fallback, and the required preselected run path. Sixteen scenarios currently pass. It does not claim to test GNU util-linux itself.

## Run states

```bash
bun scripts/render-events.mjs "$RUN/events.jsonl" --status
```

Two facts decide the state: whether `result.txt` has a terminal line, and whether the recorded process group still exists. `--status` reads the first and probes the second with signal 0, which sends nothing.

| Terminal line | Group | State | What it means |
| --- | --- | --- | --- |
| `exit=0 handoff=ready` | — | `DONE` | Codex finished and `report.md` is non-empty. Verify the result yourself. |
| `exit=0 handoff=incomplete` | — | `INCOMPLETE` | Codex exited cleanly but produced no handoff. Inspect the event log, then resume. |
| `exit=N` | — | `EXITED` | Codex failed, or was cancelled (`exit=1`). Read `stderr.log`. |
| none | alive | `RUNNING` | Working. `last write` and `in flight` say how it is going. |
| none | gone | `DIED` | **Killed, not finished.** Artifacts are partial; resume the thread. |
| none | no `pgid` | `UNKNOWN` | Pre-`pgid` run, or a truncated `result.txt`. Fall back to `pgrep`. |

When `collab_tool_call` records expose receiver IDs or states, `--status` adds an `agents` line with the last states visible to the root exec stream. An empty receiver/state map still renders the collab action but cannot produce an agent summary. This is not a current census: children do not stream their own activity through `codex exec`, and some multi-agent versions emit no usable state map.

`DIED` is the row that did not exist before the durable template, and the reason the state used to be unreadable: a killed run and a working run looked identical from outside. It is also cheap to recover from, because the thread survives — see [Resume](#resume).

**Silence is not a hang.** The event stream carries no timestamps, and model work may emit no root-visible events, so a `RUNNING` run with a stale `last write` is usually thinking or waiting on an internal child. There is no outside signal that separates deep reasoning from a wedged process. Escalate on a long gap with nothing `in flight`, never on quiet alone; and because cancelling is now recoverable, a wrong guess costs one resume rather than the run.

## Concurrency

- Run IDs are collision-safe; each run owns its directory and PID. Any number of runs can share a workspace's `.agent-runs/`.
- The **thread** is not per-run: the original run and every resume of it share one thread. Keep one active turn per thread — do not resume a thread whose earlier run is still going.
- Two concurrent runs must not **write** to the same workspace — Codex processes do not coordinate. Concurrent `read-only` runs are fine; concurrent writers belong in separate worktrees.
- Resume takes the thread ID from a specific run directory, so parallel runs cannot cross-resume — that is why `resume --last` is banned.

## Resume

A resume reuses the thread in a fresh run directory. It inherits the recorded sandbox, model, effort, Fast assertion, and network grant from the original run. It does not inherit new authority: widen any capability only after the user grants it.

```bash
bash scripts/launch-run.sh \
  --workspace "$DIR" \
  --packet "$FOLLOWUP_PACKET" \
  --resume-from "$RUN" \
  --run-dir "$NEW_RUN" \
  --host-route launcher-subagent \
  --host-model "$HOST_MODEL" \
  --routing-reason resume-inherited
```

`RUN` names one exact source run directory and `FOLLOWUP_PACKET` is the new immutable packet. The script refuses to resume while that source run's process group is alive. It extracts the explicit thread ID and provenance, creates a fresh run directory, and returns the same six-field launch manifest as a new thread. The main host must select `NEW_RUN` before dispatch so a lost resume manifest can be recovered by exact path. Never `resume --last`: parallel work can make it select the wrong thread.

Model or effort may change when the resumed work or current availability gives a concrete reason. Update the packet and record the reason when overriding the inherited route. A legacy run without `fast_requested` resumes with `no`; Fast may remain `yes` only when the original explicit request still covers the same mission or the user asks again. The launch script owns the verified CLI flag ordering and provenance so the host does not reconstruct them from memory.

Resume is also the recovery path for a killed run. Verified on 0.145.0: a run interrupted with SIGINT during a shell command resumed with its context intact, correctly answering a question that depended on what it had been told before the interrupt. A `DIED` run is a resume, not a restart.

## Cancel

With `pgid` on the provenance line, cancelling is one signal, from any session:

```bash
PG=$(sed -n '1s/.*pgid=\([0-9]*\).*/\1/p' "$RUN/result.txt")
[ -n "$PG" ] && kill -INT -"$PG"
```

Verified on 0.145.0 against a live `sleep 90` turn: codex aborts the turn, its command children are reaped with no orphans, and the wrapper still appends `exit=1` — so a cancelled run reads as `EXITED` rather than `DIED`. Wait for that line instead of assuming. The wrapper's temporary `trap ':' INT` keeps the group signal from killing the recorder while the Codex child receives its normal SIGINT disposition; the trap is restored immediately after Codex returns. If the terminal line never appears, escalate on the same group with `kill -TERM -"$PG"` and then `kill -KILL -"$PG"`, and correct `result.txt` by hand.

Signal choice still matters. SIGTERM to the codex process alone leaves its command children running, because codex spawns them in their own process groups; SIGINT is the graceful path, and signalling the whole session group, which the detached launcher makes possible, reaches both.

### Pre-`pgid` runs

A run launched before the durable template has to be matched by argv instead. The run-id reaches codex's command line through `-o "$RUN/report.md"`, so it selects exactly one process where `codex exec` alone would match every concurrent run:

```bash
ID="${RUN##*/}"; PIDS=$(pgrep -f "codex exec.*$ID")
[ "$(echo $PIDS | wc -w)" -eq 1 ] && kill -INT "$PIDS" || pgrep -lf "$ID"
```

Confirm with `pgrep -lf "$ID"`, then write `cancelled=` or `cancel_failed=` into `result.txt` by hand. This matches argv rather than stored state, and PIDs can be reused between the check and the signal — which is the whole reason the template now records `pgid`.

## Keeping runs out of version control

```bash
EXCLUDE="$(git rev-parse --git-path info/exclude)"
grep -qxF '.agent-runs/' "$EXCLUDE" || printf '%s\n' '.agent-runs/' >> "$EXCLUDE"
```

`--git-path` resolves the real exclude file in linked worktrees, where `--git-dir` points at `.git/worktrees/<name>/` and the append would land in a file git never reads. The rule stays local: do not add it to the repo's `.gitignore` unless that repo's owners asked for it.

Excluding it from git does not hide it from the repo's own tooling. A linter, structure checker, or docs validator that walks the filesystem will descend into `.agent-runs/` and fail on a delegate's artifacts — observed on a repo whose checker had to add `.agent-runs` to its skip list mid-task. When a run lands inside a repository that validates its own tree, expect to teach that checker to skip the directory, or set `RUN` outside the repository.

## Troubleshooting

- **`codex` exits immediately, `stderr.log` mentions auth**: run `codex login status` in a terminal; delegation needs an authenticated CLI.
- **`Not inside a trusted directory and --skip-git-repo-check was not specified.`**: `-C` points somewhere that is not a git repository. A `trust_level = "trusted"` entry for that path in `~/.codex/config.toml` does not clear the check (verified on 0.145.0) — the run needs a git repo or the explicit flag. A multi-repo workspace root is the usual way to hit this: aim `-C` at the child repository the mission is really about.
- **`INCOMPLETE exit=0`**: Codex returned no non-empty final response. Inspect the last `agent_message` in `events.jsonl`; if it contains the result, resume and ask Codex to return that complete result as its final response.
- **Launcher returned no manifest**: inspect the exact preselected run path. Recover the manifest when it exists and matches the packet. Launch directly only when the path is absent. An existing invalid path is a contract failure, not permission to overwrite or retry.
- **The task wrote a deliverable to `$RUN/report.md`**: the CLI final capture may have replaced it. Inspect the workspace and event log before resuming. Keep future deliverables outside the run directory.
- **Run seems hung**: `--status` first — it separates `RUNNING` from `DIED`, which no amount of `--tail` reading can. If it is `RUNNING`, read [Run states](#run-states) before cancelling: quiet usually means reasoning.
- **`--status` says `DIED`**: the run was killed, not finished. Its edits and `report.md` are whatever it had flushed; recover with a resume rather than a fresh run, and check whether the launch used the detached template.
- **Resume needs the original launch settings**: `launch-run.sh --resume-from` reads them from `result.txt` and records them in the new run. Legacy records without the optional config and git-check fields inherit `no`.
- **`result.txt` ends in `cancel_failed=`**: something survived. Re-run `pgrep -lf "$ID"`, deal with what is left, and correct the file by hand.
- **Flag errors after a CLI update**: trust `codex exec --help` over this document, adapt the template, and note the drift.
