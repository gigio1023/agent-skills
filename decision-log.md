# Codex Delegate Decision Log

## 2026-07-29: Subagent observability boundary

### Intent

Keep `codex-delegate` an instruction-driven bridge from Claude Code, Cursor,
and similar hosts into `codex exec`. Codex should retain freedom to reason,
decide within the authority granted by the packet, and use internal parallel
subagents aggressively when the work benefits. The skill should not grow into
a broker, daemon, or plugin-like agent manager.

### Evidence inspected

- OpenAI Codex source at
  `/Users/gigio/git/codex`, commit
  `fe01054a28fa4bd04716d9ceadb410f2443a50ce`
- Installed CLI: `codex-cli 0.145.0`
- Core agent registry, status channels, completion mailbox, app-server
  protocol, TUI agent feed, and `codex exec --json` event projection

### Findings

1. Codex represents subagents as `CodexThread` instances in one runtime. A
   shared `AgentControl` owns their `ThreadId`, hierarchical `AgentPath`,
   parent-child registry, and per-thread status watch channel.
2. `AgentStatus` is the last lifecycle state derived from events:
   `PendingInit`, `Running`, `Interrupted`, `Completed`, `Errored`, `Shutdown`,
   or `NotFound`. It has no heartbeat, activity timestamp, or `Stalled` state.
3. The parent model learns through spawn results, explicit status tools,
   mailbox messages, and completion envelopes. It does not automatically see
   every child event.
4. App-server clients can subscribe to each child thread and therefore show
   richer per-child turn and item activity. The public repository does not
   contain the Codex Desktop frontend itself.
5. Default multi-agent V1 exposes root `spawn_agent` and `wait_agent` calls as
   `collab_tool_call` records in `codex exec --json`. These are partial,
   root-visible snapshots. Child reasoning, commands, intermediate messages,
   and descendants are filtered out.
6. Experimental multi-agent V2 currently exposes less through `codex exec`:
   spawn activity is dropped by the exec projection and wait records carry no
   child status map.
7. Codex treats a model response stream with no SSE activity for five minutes
   as a lost connection and retries. This detects a transport stall, not a
   wedged turn task or tool.

### Decisions

- Do not enable detailed reasoning summaries merely to manufacture a
  heartbeat.
- Do not add a `STALLED` state or automatic cancellation based on JSONL
  silence.
- Keep terminal record plus process-group existence as the authoritative outer
  lifecycle: `DONE`, `EXITED`, `RUNNING`, `DIED`, or `UNKNOWN`.
- Show event age as an uninterpreted observation, not a health verdict.
- Fix the disposable watcher so it wakes when either a terminal record appears
  or the recorded process group disappears.
- The renderer may recognize `collab_tool_call` and show the last
  root-observed subagent snapshot. It must label this as partial and
  version-dependent.
- Prefer lightweight prompt guidance asking the root Codex agent for sparse
  progress checkpoints after dispatch and completed work waves.
- Do not adopt `codex app-server` in the normal skill path. It provides the
  richer supervision surface but crosses the intended boundary into a
  persistent manager.

### Open investigation

Evaluate whether an established, compact Unix CLI can replace or simplify the
current `setsid` launcher and polling watcher without becoming a required
dependency or agent-management layer. Compare at least:

- ubiquitous session tools such as `tmux` or GNU Screen;
- small job queues such as Task Spooler;
- platform-native supervisors such as `systemd-run --user` and macOS
  `launchctl`;
- the current POSIX-style `setsid`/PGID/result-file baseline.

Judge each candidate by installation burden, macOS/Linux portability, detached
survival, exact exit-state recovery, concurrent job handling, log access,
machine-readable status, and whether it preserves the skill's deliberately
small scope.

## 2026-07-29: External CLI survey

### Sources

- tmux official repository and manual:
  <https://github.com/tmux/tmux>,
  <https://man.openbsd.org/tmux>
- GNU Screen manual:
  <https://www.gnu.org/software/screen/manual/screen.html>
- Task Spooler upstream and manual:
  <https://viric.name/soft/ts/>,
  <https://viric.name/soft/ts/man_ts.html>
- GNU Parallel manual and history:
  <https://www.gnu.org/software/parallel/parallel.html>,
  <https://www.gnu.org/software/parallel/history.html>
- systemd transient service documentation:
  <https://man7.org/linux/man-pages/man1/systemd-run.1.html>
- GNU `nohup` documentation:
  <https://www.gnu.org/software/coreutils/manual/html_node/nohup-invocation.html>

### Candidate findings

| Candidate | What it adds | Why it is not the default |
| --- | --- | --- |
| tmux | Detached survival, named sessions, retained pane exit code and signal, manual attach | Adds a PTY and session cleanup, is not installed by default on this Mac, and still cannot detect a hang |
| GNU Screen | Detached survival and logs; already present on macOS | macOS ships an old version, exact exit-state querying is weak, and the existing result file is still required |
| Task Spooler (`ts`/`tsp`) | Job IDs, per-user queue, slots, status, output, exit code, wait, and process-group cancellation | It is a small manager with a per-user server, has low adoption, has a `ts` name collision on Homebrew, and defaults to one slot |
| GNU Parallel | Parallel batches and an exit-bearing job log | The foreground orchestrator must still survive; it cannot reconnect to a live job |
| `systemd-run --user` | Accurate Linux service state, exit status, cgroup cancellation, journal logs | Linux-only, logout persistence can require linger, and it couples the skill to an OS service manager |
| `launchctl` | Built-in macOS detached service execution and status | macOS-only and introduces service labels and cleanup lifecycle |
| `nohup`, dtach, daemonize | Simple detachment or PID/log helpers | They do not retain enough lifecycle truth to replace the existing wrapper and result record |

No candidate distinguishes a working process from a process that is alive but
semantically wedged.

### Decision

- Keep the dependency-free run-directory, process-group, terminal-record, and
  JSONL design as the normal path.
- On systems with util-linux, prefer its `setsid -f` command for the launch.
  Retain the current Perl `POSIX::setsid()` launcher as the macOS and
  no-`setsid` fallback. Both paths preserve the same `run.sh` and evidence
  contract.
- Do not add automatic backend detection. Two status implementations would
  increase the surface area and make behavior depend on whatever happens to be
  installed. The `setsid`/Perl choice is only an equivalent launch primitive,
  not a second status backend.
- Do not integrate tmux into the normal recipe. It is the most recognizable
  mature tool and a reasonable user-controlled outer shell for interactive
  inspection, but it does not simplify the headless JSONL workflow enough.
- Keep Task Spooler as the only promising optional backend for users who
  routinely launch several independent root Codex missions. It should queue
  top-level `codex exec` runs only and never manage Codex's internal subagents.
- Do not add the Task Spooler recipe until real use shows that managing several
  outer missions is common. The intended default is one capable root Codex run
  coordinating its own internal parallel agents.
- The next justified implementation changes remain the watcher death wakeup
  and optional rendering of root-visible `collab_tool_call` events.

## 2026-07-29: Implemented minimal path

- The canonical launch now prefers util-linux `setsid -f` and falls back to
  Perl `POSIX::setsid()`. Both feed the same `run.sh`, provenance, status, and
  cancellation contract.
- Single-run and multi-run watchers now stop on either an `exit=` record or a
  vanished recorded process group.
- The renderer now recognizes `collab_tool_call`, renders root-visible state
  counts, and adds a clearly labeled partial agent snapshot to `--status`.
- The fixture covers spawn and wait records with running, completed, and
  errored child states.
- No tmux recipe was added to the deployed skill. The local machine has no
  tmux installation, so its alternate PTY and PGID behavior could not be
  verified against the existing cancellation contract. Shipping an untested
  second launcher would contradict the one-backend decision above.

## 2026-07-29: File-only handoff and cross-harness validation

### Contract change

- `codex exec -o "$RUN/report.md"` now captures the final agent response as the
  sole handoff. The delegate no longer writes a separate report and then emits
  a duplicate `final.md`.
- Prompt, JSONL stdout, stderr, report, provenance, and terminal status all stay
  in the run directory. The detached launcher emits no result to its caller.
- A terminal record now includes `handoff=ready|incomplete`. Ready requires both
  exit 0 and a non-empty report. The renderer maps clean exit with no report to
  `INCOMPLETE`, not `DONE`.
- The wrapper catches group SIGINT while Codex is running, then records Codex's
  exit before restoring the default handler. This removes dependence on
  shell-specific wait behavior during cancellation.

### Deterministic scenarios

`bash scripts/test-run-contract.sh` passes eight scenarios:

1. Perl POSIX detachment and file-only channels.
2. `setsid` branch selection through a semantics-compatible shim.
3. Spaces, Korean text, quotes, brackets, and dollar signs in paths.
4. Exit 0 with a missing report becomes `INCOMPLETE`.
5. Non-zero exit and stderr capture.
6. A quiet live group is `RUNNING`; after group death it is `DIED`.
7. Concurrent read-only runs keep separate handoffs.
8. Group SIGINT remains `EXITED` with a terminal record; missing PGID becomes
   `UNKNOWN`.

The actual GNU branch was also exercised in the locally available Linux
container image: util-linux 2.37.2 `setsid -f` produced a detached shell whose
PID equaled its PGID and which appended its terminal record.

### Live results on codex-cli 0.145.0

- Direct read-only run from a Git repository whose path contains spaces and
  Korean text: exit 0, handoff ready, exact report captured, zero launcher
  stdout/stderr, no workspace mutation beyond run artifacts.
- Live `/bin/sleep 90` cancellation: `RUNNING` with command in flight, then
  group SIGINT produced `exit=1 handoff=incomplete`; the process group and
  child disappeared.
- Resume of that cancelled thread in a fresh run directory: same thread ID,
  exit 0, handoff ready, no `final.md`.
- Forced two-agent read-only mission: both results reached one report and the
  run finished ready. The root JSONL exposed only started/completed
  `collab_tool_call` records for `wait`, with empty receiver and state maps.
  This confirms that the renderer's agent view is genuinely partial.

### Host harness results

- Cursor Agent discovered the project-local candidate from `.agents/skills`,
  launched the documented detached script, and verified a ready report.
- Claude Code first selected the stale global skill with the same name instead
  of the project symlink. That run used the old foreground and duplicate-file
  contract. An isolated temporary Claude plugin namespace then loaded the
  candidate correctly and passed the same test.
- The stale global copy remains untouched. Before normal Claude Code use, sync
  or replace `~/.agents/skills/codex-delegate` with the accepted canonical
  package; do not assume a same-name project symlink wins discovery.
