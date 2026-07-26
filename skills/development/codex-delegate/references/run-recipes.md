# Run Recipes

Artifact contract, event vocabulary, concurrency, cancellation, and
troubleshooting for `codex exec` delegation runs.

## Contents

- [Run directory](#run-directory)
- [Sandbox by mission](#sandbox-by-mission)
- [Event vocabulary](#event-vocabulary)
- [Renderer](#renderer)
- [Concurrency](#concurrency)
- [Cancel across sessions](#cancel-across-sessions)
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
| `result.txt` | Provenance line, then the terminal state |

`result.txt` line 1 records provenance —
`sandbox=… workspace=… started=…`, plus `-m`/`-p` when the run used them, and
`thread=… resumed_from=…` for a resume. The terminal state is appended after
codex returns:

- `exit=N finished=…` — codex exited on its own (N is its exit code).
- `cancelled=…` — a cancellation was confirmed dead (see below).
- `cancel_failed=…` — the cancellation could not be confirmed; inspect.

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
provenance line. Exactly two `-c` keys are sanctioned — this one and
`model_reasoning_effort` for reasoning effort — declared and recorded the same
way; `-c` still must never touch `sandbox_mode` or the approval policy.

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

## Cancel across sessions

Within the launching session, kill the harness's background shell — then
confirm, because a harness kill does not necessarily deliver SIGINT. From a
different session, signal the codex PID with the right signal. Verified on
codex-cli 0.145.0 with a live `sleep 120` turn:

- **SIGINT**: codex aborts the turn, kills its running command children,
  exits. No orphans. This is the graceful path.
- **SIGTERM**: codex exits (143) but its running command children survive.
- **Group kill (`kill -- -PGID`)**: never reaches the commands either —
  codex spawns them in their own process groups.

Match the run, not the binary: the run-id is on codex's argv (via
`-o "$RUN/final.md"`), so it selects exactly one process where `codex exec`
alone would match every concurrent run.

```bash
RUN="$PWD/.agent-runs/codex/20260726T054537Z-bd8431f2"   # the run to cancel
ID="${RUN##*/}"
PIDS=$(pgrep -f "codex exec.*$ID")
if [ "$(echo $PIDS | wc -w)" -ne 1 ]; then
  echo "expected exactly one match — inspect before signalling:"; pgrep -lf "$ID"
else
  PID=$PIDS; CHILDREN=$(pgrep -P "$PID")  # snapshot children before signalling
  kill -INT "$PID"; sleep 5               # graceful: codex reaps its commands
  kill -0 "$PID" 2>/dev/null && { kill -TERM "$PID"; sleep 5; }
  kill -0 "$PID" 2>/dev/null && { kill -KILL "$PID"; sleep 2; }
  MYPG="$(ps -o pgid= -p $$ | tr -d ' ')" # never group-kill our own shell
  printf '%s\n' "$CHILDREN" |             # sweep anything TERM/KILL orphaned
  while read -r c; do                     # (zsh does not word-split $CHILDREN)
    [ -n "$c" ] || continue
    g="$(ps -o pgid= -p "$c" | tr -d ' ')"
    [ -n "$g" ] && [ "$g" != "$MYPG" ] || continue
    kill -TERM -- -"$g" 2>/dev/null; sleep 2
    kill -0 "$c" 2>/dev/null && kill -KILL -- -"$g" 2>/dev/null
  done
  if ! kill -0 "$PID" 2>/dev/null && [ -z "$(pgrep -f "$ID")" ]; then
    echo "cancelled=$(date -u +%FT%TZ)" >> "$RUN/result.txt"
  else
    echo "cancel_failed=$(date -u +%FT%TZ)" >> "$RUN/result.txt"; pgrep -lf "$ID"
  fi
fi
```

Honest limitations: this matches argv, not stored state, and PIDs can be
reused between the snapshot and the sweep — re-reading each child's live pgid
narrows that window but does not close it. With the canonical template one PID comes back,
because the run-id reaches only codex's own command line — the launching
shell's argv still holds the unexpanded `$(date …)-$(openssl …)`. If you
hardcoded the run directory at launch instead, that shell matches too: the
count check stops, `pgrep -lf "$ID"` shows both, and you signal the
`codex exec` PID by hand. Prefer cancelling from the launching session.

## Keeping runs out of version control

```bash
EXCLUDE="$(git rev-parse --git-path info/exclude)"
grep -qxF '.agent-runs/' "$EXCLUDE" || printf '%s\n' '.agent-runs/' >> "$EXCLUDE"
```

`--git-path` resolves the real exclude file in linked worktrees, where
`--git-dir` points at `.git/worktrees/<name>/` and the append would land in a
file git never reads. The rule stays local: do not add it to the repo's
`.gitignore` unless that repo's owners asked for it.

## Troubleshooting

- **`codex` exits immediately, `stderr.log` mentions auth**: run
  `codex login status` in a terminal; delegation needs an authenticated CLI.
- **Empty `final.md` with exit 0**: the model may have produced no final
  message (rare) — the last `agent_message` item in `events.jsonl` has the
  text.
- **Run seems hung**: render with `--tail`; a long-running command shows as
  the last `▶` line. Check `stderr.log`. Cancel with the recipe above if it
  is genuinely stuck.
- **Resume needs the original model**: read the original run's `result.txt`
  provenance line and re-pass what it recorded. `-m` and
  `--ignore-user-config` carry over; `-p` does not, because `codex exec
  resume` has no `--profile` — re-express the profile's restrictions through
  `-m` and config.
- **`result.txt` ends in `cancel_failed=`**: something survived. Re-run
  `pgrep -lf "$ID"`, deal with what is left, and correct the file by hand.
- **Flag errors after a CLI update**: trust `codex exec --help` over this
  document, adapt the template, and note the drift.
