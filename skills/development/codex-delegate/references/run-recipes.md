# Run Recipes

Artifact contract, event vocabulary, concurrency, cancellation, and
troubleshooting for `codex exec` delegation runs.

## Contents

- [Run directory](#run-directory)
- [Sandbox by mission](#sandbox-by-mission)
- [Event vocabulary](#event-vocabulary)
- [Renderer](#renderer)
- [Run states](#run-states)
- [Concurrency](#concurrency)
- [Resume](#resume)
- [Cancel](#cancel)
- [Keeping runs out of version control](#keeping-runs-out-of-version-control)
- [Troubleshooting](#troubleshooting)

## Run directory

`<workspace>/.agent-runs/codex/<run-id>/`, run-id = UTC timestamp + random
hex (e.g. `20260726T054537Z-bd8431f2`).

| File | Content |
| --- | --- |
| `prompt.md` | The packet as submitted (write it here, don't copy a tracked file over it) |
| `events.jsonl` | The raw JSONL stream from `--json`, as received by the host |
| `stderr.log` | Full stderr |
| `final.md` | Final response written by `-o/--output-last-message` |
| `report.md` | The deliverable itself, when the packet asked for a report file |
| `run.sh` | The detached launcher, written per run: exact provenance of what ran |
| `result.txt` | Provenance line, then the terminal state |

`result.txt` line 1 records provenance —
`sandbox=… workspace=… started=… pgid=…`, plus every flag and `-c` the run
used, and `thread=… resumed_from=…` for a resume. `pgid` is what makes the
run's liveness decidable later; it is the detached session leader, so
`kill -0 -"$PGID"` answers "still alive?" and `kill -INT -"$PGID"` cancels.
The terminal state is appended after codex returns:

- `exit=N finished=…` — codex exited on its own (N is its exit code). A
  cancellation lands here too, as `exit=1`, because the wrapper outlives the
  signal.
- `cancelled=…` / `cancel_failed=…` — only written by the legacy pre-`pgid`
  cancel path below, which had to confirm death from outside.

`exit=0` means codex exited cleanly, not that the task succeeded — read
`final.md` and verify the workspace yourself.

These artifacts are evidence, not tamper-proof records. A `workspace-write`
delegate can rewrite anything under `.agent-runs/` inside its own workspace,
so a run's log cannot fully attest to that run. When a log has to hold up as
proof — a review someone else will act on, a disputed change — run the mission
`read-only`, or set `RUN` to a directory outside the delegate's workspace.
Both are judgement calls per mission, not standing requirements.

Sandbox is not the whole capability boundary either: `--sandbox` governs the
filesystem effects of shell commands, while MCP servers, network access, and
web search come from the Codex config the CLI loads. In an untrusted or
unfamiliar workspace, `--ignore-user-config` or a reviewed `-p <profile>` is
worth considering — an option to weigh, not a rule.

## Sandbox by mission

Pick the sandbox from what the mission has to produce, not from a standing
rule:

- **Context back in the reply** — a question answered, nothing written:
  `read-only`. The built-in `web_search` tool and MCP tools are not shell
  commands, so the filesystem sandbox does not gate them; whether they are
  available at all comes from the Codex config.
- **A report file** — research or analysis delivered as a document, and the
  usual shape of a delegation: `workspace-write`, with the packet naming
  `$RUN/report.md` as the deliverable. The host reads that file and delivers
  it; the final message only has to summarise and point at the path.
- **Clone, then analyze, then report** — many repositories at once:
  `workspace-write` plus `-c sandbox_workspace_write.network_access=true`,
  cloning into `$RUN/clones/` so both the inputs and `$RUN/report.md` stay
  inside the run directory.
- **`danger-full-access`** — only when the mission genuinely needs the whole
  machine and the user said so. Mass-cloning unknown repositories is not that
  case: reading unfamiliar code is peak prompt-injection surface, and it
  wants a narrower sandbox, not the widest one.

Live evidence (codex-cli 0.145.0, verified 2026-07-26): under
`--sandbox workspace-write` with the default config, `curl -sS -I
https://example.com` fails with
`curl: (6) Could not resolve host: example.com` — shell network is blocked,
DNS included. The same command with
`-c sandbox_workspace_write.network_access=true` returns `HTTP/2 200`. That
narrow override is the sanctioned way to give a workspace-write run shell
network: declare it in your reply and append it to the `result.txt`
provenance line. Exactly three `-c` keys are sanctioned — this one,
`model_reasoning_effort` for reasoning effort, and `service_tier` for the Fast
tier — declared and recorded the same way; `-c` still must never touch
`sandbox_mode` or the approval policy.

## Event vocabulary

Observed with codex-cli 0.145.0 (recheck against live output when the CLI
majors — tolerate unknown types, never hard-code an exhaustive list):

- `thread.started` — carries `thread_id`. Always the first line; this is the
  ID that `codex exec resume` needs.
- `turn.started` / `turn.completed` — `turn.completed` carries `usage`
  (input/cached/output/reasoning token counts).
- `turn.failed` — carries `error.message`.
- `item.started` / `item.updated` / `item.completed` — carry `item` with an
  item `type`:
  - `command_execution`: `command`, `exit_code`, `status`, and
    `aggregated_output` (the full command output — this payload is why raw
    logs get big).
  - `agent_message`: `text` (the same text ends up in `final.md` for the
    last message).
  - `reasoning`: summary text.
  - `file_change`, `mcp_tool_call`, `web_search`: change lists and tool/query
    metadata.
  - `error`: non-fatal warnings also arrive this way (e.g. a skills context
    budget notice) — an `error` item does not mean the run failed.

Extract the thread ID without a JSON parser:

```bash
head -n1 "$RUN/events.jsonl"
# {"type":"thread.started","thread_id":"019f9cf5-..."}
```

## Renderer

```bash
bun scripts/render-events.mjs "$RUN/events.jsonl" --tail 20   # from this skill's dir
```

`node` works identically. The renderer streams the file line by line and
keeps at most `--tail N` rendered lines, so its memory is bounded by the
longest single line, not by the file's size. A line over ~2 MB never reaches
the JSON parser at all — it degrades to `? oversized event line`. Smoke check
(also the fixture for validation):

```bash
bun scripts/render-events.mjs scripts/fixtures/sample-events.jsonl
```

Expected: one line per action — `▶`/`✓` commands with exit codes, `✉` agent
message once rather than per streamed update, `file_change` paths as
basenames, `⚠` warnings — then unknown types as bare type names, and the
degrade markers the fixture exercises: `? malformed event` for a JSON line
that is not an object (a non-object `item` degrades the same way), `×?` for a `file_change`
whose `changes` is not an array, `? unparseable line` for the garbage line.
`item.updated` renders nothing, whatever the item type: `▶` and `✓` carry the
signal, and a ✓ on an item still in progress would read as finished. The
96-char cap applies to each assembled action line (the long unknown type ends
in `…`); control characters in text are replaced with spaces, so an
`agent_message` carrying ESC/OSC sequences renders inert. The footer carries
event/command/file-change counts and the thread ID, and is not capped.

For targeted deep-dives on the raw file, grep instead of reading it whole:

```bash
grep '"type":"turn.failed"' "$RUN/events.jsonl"
grep '"exit_code":' "$RUN/events.jsonl" | grep -v '"exit_code":0'
```

## Run states

```bash
bun scripts/render-events.mjs "$RUN/events.jsonl" --status
```

Two facts decide the state: whether `result.txt` has a terminal line, and
whether the recorded process group still exists. `--status` reads the first
and probes the second with signal 0, which sends nothing.

| Terminal line | Group | State | What it means |
| --- | --- | --- | --- |
| `exit=0` | — | `DONE` | codex finished. Verify the workspace yourself. |
| `exit=N` | — | `EXITED` | codex failed, or was cancelled (`exit=1`). Read `stderr.log`. |
| none | alive | `RUNNING` | working. `last write` and `in flight` say how it is going. |
| none | gone | `DIED` | **killed, not finished.** Artifacts are partial; resume the thread. |
| none | no `pgid` | `UNKNOWN` | pre-`pgid` run, or a truncated `result.txt`. Fall back to `pgrep`. |

`DIED` is the row that did not exist before the durable template, and the
reason the state used to be unreadable: a killed run and a working run looked
identical from outside. It is also cheap to recover from, because the thread
survives — see [Resume](#resume).

**Silence is not a hang.** The event stream carries no timestamps, and a
reasoning turn emits no events at all, so a `RUNNING` run with a stale
`last write` is usually thinking. There is no outside signal that separates
deep reasoning from a wedged process. Escalate on a long gap with nothing
`in flight`, never on quiet alone; and because cancelling is now recoverable,
a wrong guess costs one resume rather than the run.

## Concurrency

- Run IDs are collision-safe; each run owns its directory and PID. Any number
  of runs can share a workspace's `.agent-runs/`.
- The **thread** is not per-run: the original run and every resume of it share
  one thread. Keep one active turn per thread — do not resume a thread whose
  earlier run is still going.
- Two concurrent runs must not **write** to the same workspace — Codex
  processes do not coordinate. Concurrent `read-only` runs are fine;
  concurrent writers belong in separate worktrees.
- Resume takes the thread ID from a specific run directory, so parallel runs
  cannot cross-resume — that is why `resume --last` is banned.

## Resume

A resume reuses the thread in a fresh run directory. It inherits the thread,
not the authority: take the original's sandbox from its `result.txt` and widen
only on new authority.

```bash
DIR="$(pwd)"; RUN="$DIR/.agent-runs/codex/ORIG_RUN_ID"   # the run being resumed
THREAD=$(sed -n '1s/.*"thread_id":"\([^"]*\)".*/\1/p' "$RUN/events.jsonl")
SANDBOX=read-only
NEW="$DIR/.agent-runs/codex/$(date -u +%Y%m%dT%H%M%SZ)-$(openssl rand -hex 4)"
mkdir -p "${NEW%/*}" && mkdir "$NEW"
# then write your follow-up packet to "$NEW/prompt.md"
cat > "$NEW/run.sh" <<EOF
#!/bin/bash
echo "sandbox=$SANDBOX workspace=$DIR started=\$(date -u +%FT%TZ) pgid=\$\$ thread=$THREAD resumed_from=${RUN##*/}" > "$NEW/result.txt"
codex exec -C "$DIR" --sandbox "$SANDBOX" resume "$THREAD" --json -m gpt-5.6-sol \\
  -c model_reasoning_effort="high" -c service_tier="priority" \\
  -o "$NEW/final.md" - < "$NEW/prompt.md" > "$NEW/events.jsonl" 2> "$NEW/stderr.log"
echo "exit=\$? finished=\$(date -u +%FT%TZ)" >> "$NEW/result.txt"
EOF
perl -e 'exit 0 if fork; use POSIX (); POSIX::setsid() or die; exec @ARGV or die' \
  /bin/bash "$NEW/run.sh"
```

Flag placement matters: `-C` and `--sandbox` belong to `exec` and precede
`resume`; `--json`, `-o`, and `-m` are accepted after it (verified on
codex-cli 0.145.0 — the wrong order exits 2). Never `resume --last`: it can
pick the wrong session during parallel work. Re-pass `-m`, the effort and tier
overrides, and `--ignore-user-config` when the original used them; `-p` cannot
carry over, because `codex exec resume` has no `--profile` — re-express it
through `-m` and config.

Resume is also the recovery path for a killed run. Verified on 0.145.0: a run
interrupted with SIGINT during a shell command resumed with its context
intact, correctly answering a question that depended on what it had been told
before the interrupt. A `DIED` run is a resume, not a restart.

## Cancel

With `pgid` on the provenance line, cancelling is one signal, from any
session:

```bash
PG=$(sed -n '1s/.*pgid=\([0-9]*\).*/\1/p' "$RUN/result.txt")
[ -n "$PG" ] && kill -INT -"$PG"
```

Verified on 0.145.0 against a live `sleep 90` turn: codex aborts the turn, its
command children are reaped with no orphans, and the wrapper still appends
`exit=1` — so a cancelled run reads as `EXITED` rather than `DIED`. Wait for
that line instead of assuming. If it never appears, escalate on the same
group with `kill -TERM -"$PG"` and then `kill -KILL -"$PG"`, and correct
`result.txt` by hand.

Signal choice still matters. SIGTERM to the codex process alone leaves its
command children running, because codex spawns them in their own process
groups; SIGINT is the graceful path, and signalling the whole session group,
which the detached launcher makes possible, reaches both.

### Pre-`pgid` runs

A run launched before the durable template has to be matched by argv instead.
The run-id reaches codex's command line through `-o "$RUN/final.md"`, so it
selects exactly one process where `codex exec` alone would match every
concurrent run:

```bash
ID="${RUN##*/}"; PIDS=$(pgrep -f "codex exec.*$ID")
[ "$(echo $PIDS | wc -w)" -eq 1 ] && kill -INT "$PIDS" || pgrep -lf "$ID"
```

Confirm with `pgrep -lf "$ID"`, then write `cancelled=` or `cancel_failed=`
into `result.txt` by hand. This matches argv rather than stored state, and
PIDs can be reused between the check and the signal — which is the whole
reason the template now records `pgid`.

## Keeping runs out of version control

```bash
EXCLUDE="$(git rev-parse --git-path info/exclude)"
grep -qxF '.agent-runs/' "$EXCLUDE" || printf '%s\n' '.agent-runs/' >> "$EXCLUDE"
```

`--git-path` resolves the real exclude file in linked worktrees, where
`--git-dir` points at `.git/worktrees/<name>/` and the append would land in a
file git never reads. The rule stays local: do not add it to the repo's
`.gitignore` unless that repo's owners asked for it.

Excluding it from git does not hide it from the repo's own tooling. A linter,
structure checker, or docs validator that walks the filesystem will descend
into `.agent-runs/` and fail on a delegate's artifacts — observed on a repo
whose checker had to add `.agent-runs` to its skip list mid-task. When a run
lands inside a repository that validates its own tree, expect to teach that
checker to skip the directory, or set `RUN` outside the repository.

## Troubleshooting

- **`codex` exits immediately, `stderr.log` mentions auth**: run
  `codex login status` in a terminal; delegation needs an authenticated CLI.
- **`Not inside a trusted directory and --skip-git-repo-check was not
  specified.`**: `-C` points somewhere that is not a git repository. A
  `trust_level = "trusted"` entry for that path in `~/.codex/config.toml` does
  not clear the check (verified on 0.145.0) — the run needs a git repo or the
  explicit flag. A multi-repo workspace root is the usual way to hit this:
  aim `-C` at the child repository the mission is really about.
- **Empty `final.md` with exit 0**: the model may have produced no final
  message (rare) — the last `agent_message` item in `events.jsonl` has the
  text.
- **Run seems hung**: `--status` first — it separates `RUNNING` from `DIED`,
  which no amount of `--tail` reading can. If it is `RUNNING`, read
  [Run states](#run-states) before cancelling: quiet usually means reasoning.
- **`--status` says `DIED`**: the run was killed, not finished. Its edits and
  `report.md` are whatever it had flushed; recover with a resume rather than a
  fresh run, and check whether the launch used the detached template.
- **Resume needs the original model**: read the original run's `result.txt`
  provenance line and re-pass what it recorded. `-m` and
  `--ignore-user-config` carry over; `-p` does not, because `codex exec
  resume` has no `--profile` — re-express the profile's restrictions through
  `-m` and config.
- **`result.txt` ends in `cancel_failed=`**: something survived. Re-run
  `pgrep -lf "$ID"`, deal with what is left, and correct the file by hand.
- **Flag errors after a CLI update**: trust `codex exec --help` over this
  document, adapt the template, and note the drift.
