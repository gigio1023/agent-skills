# Cursor Agent CLI Reference

Local syntax and model listing checked 2026-09-09. Initial preflight reported `2026.09.02-c22c1a3`; a post-smoke probe reported `2026.09.08-6caf4ff` with the required flags and exact default still present. No install/update command was invoked; the cause and exact transition time were not established, so the individual smoke launches cannot be pinned conclusively to one version. Installed help and live account availability govern launch syntax; this snapshot is not a permanent model alias or security guarantee.

## Contents

- Preflight and exact models
- Runner invocation
- Evidence and exit semantics
- Permissions and isolation
- Follow-ups and cancellation
- Verified scope and sources

## Preflight And Exact Models

Run from the intended workspace, without changing configuration:

```bash
command -v agent
agent --version
agent status
agent --help
agent models
```

Stop for missing executable, authentication, required flags, or selected model. Do not install, log in, update, or substitute a model without authorization. Preserve the version and relevant model-list entry in private task evidence; avoid publishing account details from status output. The runner deliberately does not redo these service probes on every turn.

The verified default ID is `cursor-grok-4.6-xhigh-fast`, listed as `Cursor Grok 4.6 Extra High Fast`; a live initialization event reported that same display label. The request's exact model wins. There is no automatic Fable route and no fallback to `auto`. Do not normalize a malformed identifier into a guessed valid model. No standalone `--thinking` flag was exposed: the exact default already chooses the xhigh profile. Use another documented profile or bracket override only when requested and verified for that model, not an invented thinking suffix.

Top-level `--model` selects the Cursor parent. Internal subagent models and effort need explicit enforcement only when the user imposes such a policy; then inspect the current child tool schema and transcript, and report unsupported controls or missing evidence rather than asserting compliance.

## Runner Invocation

Execute `scripts/cursor_run.py` with Python 3.9+ on macOS/Linux. Resolve paths from the directory containing this skill's `SKILL.md`, not a caller-specific installation path. The packet and state directory must be outside the skill package; prefer a private state location outside the target repository too.

Prepare a UTF-8, secret-free packet describing the authorized task, sources, allowed effects, preservation rules, and expected evidence. Then, from the skill directory:

```bash
python3 -B scripts/cursor_run.py \
  --workspace /absolute/path/to/existing-workspace \
  --prompt-file /absolute/private/path/mission.txt
```

This translates to an argument array, never a shell string:

```text
agent --print --output-format stream-json --model cursor-grok-4.6-xhigh-fast --workspace /absolute/path/to/existing-workspace --yolo -- <packet as one argument>
```

The end-of-options delimiter protects a packet beginning with a flag; quotes, newlines, shell substitutions, and metacharacters remain literal text. It does not make secrets safe in argv. The CLI has no verified prompt-file flag; the runner reads the file and passes its contents positionally. There is no `eval`, shell interpolation, or arbitrary extra-flags forwarding. `--agent` accepts one executable name/path, not a compound command.

Options that change the invocation:

| Runner option | Meaning |
| --- | --- |
| `--model EXACT_ID` | Request-specific parent model; verify it with `agent models` first |
| `--resume EXACT_SESSION_ID` | Resume this session, including an ordinary related follow-up |
| `--mode ask` / `--mode plan` | Explicitly requested native read-only mode; default `agent` omits the CLI mode flag |
| `--no-yolo` | Omit broad unattended approval when the request/host requires a narrower lane |
| `--timeout SECONDS` | Optional positive finite wall-clock budget; omitted means no runner-imposed deadline |
| `--state-dir PATH` | Private runtime root; default `~/.local/state/cursor-cli-delegation` |
| `--agent PATH` | Installed executable; useful for multiple installations, not model fallback |

The runner creates no worktree, queue, database, daemon, retry policy, ACP bridge, or model-routing layer. It preserves sandbox configuration and never passes `--sandbox disabled`. It is an evidence/process helper, not a permission enforcement system.

## Evidence And Exit Semantics

Each invocation creates a unique `run-*` directory (mode 0700), with files created under umask 077 (mode 0600):

- `stdout.log`: raw stream saved during execution; inspect this for live progress if needed.
- `stderr.log`: separate raw diagnostics.
- `events.jsonl`: valid object events parsed line by line after process termination, without retaining the full transcript. Memory tracks the largest event, initialization, and latest result; malformed lines remain in stdout and produce one bounded issue per category.
- `receipt.json`: sanitized launch argv (packet omitted), requested model, reported initialization label, workspace, PID, process exit, stop reason, session/resumed session, terminal result, issues, timing, and evidence directory.

The runner prints a JSON object containing the receipt path. It retains raw output rather than guessing a service response. Logs may contain the echoed packet, sensitive tool output, and thinking events; keep them private, review before sharing, and do not reproduce hidden reasoning as acceptance evidence. The packet is omitted only from receipt argv, not guaranteed absent from logs or result text. Cursor's own session persistence is separate from these files.

`transport_status: complete` is an evidence check, not task acceptance. `task_status` stays `unverified`; the calling workflow must inspect actual sources, artifacts, checks, diffs, and external-state readbacks. A success event or prose assertion does not establish that code works, sources are sound, scope was respected, or child models matched a policy.

| Runner exit | Meaning |
| --- | --- |
| `0` | Process exited zero and structured completion/session evidence passed; task still requires acceptance |
| `1` | Process exited zero but structured evidence was incomplete or erroneous |
| `2` | Invalid runner input; no launch |
| `124` | Runner deadline; owned process group cancellation attempted |
| `127` | Executable could not launch; receipt preserves the failure |
| Other positive process exit | Preserved as returned by Cursor |
| `128 + signal` | Child signal exit or runner SIGINT/SIGTERM cancellation |

The receipt distinguishes overlapping numeric meanings, such as a child itself returning 124. Nonzero exits, missing initialization/model evidence, missing/error terminal results, malformed structured output, and missing/conflicting session IDs make the transport incomplete. Every supplied session ID must be a nonempty string and agree across events, including initialization and result, and with an explicit resume ID. Preserve absent fields as unknown, not invented evidence. Disk failure or forcible runner SIGKILL can prevent a final receipt; raw logs are the fallback, not a success claim.

## Permissions And Isolation

The verified help calls `--yolo` an alias for `--force` (“Run Everything”), and `--force` allows commands unless explicitly denied. Treat it as a broad trust grant that can bypass prompts for workspace/tools; it does not authorize otherwise forbidden effects. It is the requested default, not a reason to add `--approve-mcps`, `--trust`, `--add-dir`, or sandbox overrides.

Inspect repository and user Cursor MCP/plugin/rule configuration before launch, without printing credentials. Discovery of a tool or source does not authorize using it. A server may write external state or control another process. If a required boundary cannot be enforced with the available lane, stop rather than relying on prompt wording as a sandbox. `--no-yolo` may encounter approval stops in headless mode; do not treat that as permission to broaden access.

Record canonical workspace, revision/status when applicable, and preexisting user changes. Reuse outer isolation and omit Cursor worktree flags. If worktree creation is separately authorized, choose one owner and inspect `.cursor/worktrees.json` setup commands before using native creation; setup itself can have command/network effects. The helper never creates worktrees. Parallel writers need distinct workspaces or disjoint ownership.

## Follow-ups And Cancellation

For any related continuation, use the exact session returned in the receipt:

```bash
python3 -B scripts/cursor_run.py \
  --workspace /absolute/path/to/same-workspace \
  --prompt-file /absolute/private/path/followup.txt \
  --resume EXACT_SESSION_ID
```

Replace the placeholder with the actual ID; do not use `--continue`, bare `--resume`, or “latest” when multiple sessions may exist. Include the next objective plus relevant preserved constraints/authority, not only a failed criterion. Check workspace state before continuing, and avoid simultaneous continuations of one session. An independent mission should start fresh.

The runner owns one POSIX session/process group. Timeout or SIGINT/SIGTERM sends TERM and then KILL only while its leader remains unreaped, then waits for the leader; it does not search by process name or signal the caller's group. If polling already reaped the leader, cancellation skips group signals to avoid a reused ID and records that cleanup limitation in the receipt. Send SIGINT/SIGTERM to the active runner through the host's scoped process handle for manual cancellation; do not send signals to stale receipt PIDs. The PID is historical evidence, not a persistent cancellation API.

Children that detach into another group and remote/MCP jobs may outlive this cancellation. Descendants can also remain when cleanup is skipped after the leader was reaped. Group signals do not prove every effect stopped. Inspect relevant external state and remaining owned work before accepting or resuming. A force-killed runner cannot guarantee cleanup. No automatic retry or resume occurs; choose the next action from evidence and existing authority.

## Verified Scope And Sources

A live authorized transport smoke used the exact Grok default, YOLO, a temporary empty workspace, and a no-tools/no-writes packet. A fresh response and ordinary exact-session follow-up both returned terminal success and process exit zero, with the expected tokens and unchanged empty workspace. This checks prompt transport, structured evidence, and resume—not research quality, implementation, child model controls, or cross-harness behavior. Local sandbox configuration was already disabled; the helper did not change it or pass a disable flag. Therefore the smoke establishes no sandbox-enforcement claim. Per-run IDs and private logs stay in external task evidence rather than the installed package.

Primary maintenance sources:

- [CLI overview](https://cursor.com/docs/cli/overview)
- [Headless CLI](https://cursor.com/docs/cli/headless)
- [CLI parameters](https://cursor.com/docs/cli/reference/parameters)
- [Output format](https://cursor.com/docs/cli/reference/output-format)
- [Rules and MCP](https://cursor.com/docs/cli/using)
- [CLI permission history](https://cursor.com/changelog/page/9)
- [CLI subagents and skills](https://cursor.com/changelog/2-4)
- [Asynchronous and nested subagents](https://cursor.com/changelog/2-5)

The installed help/model list and actual stream were rechecked for this revision; those web pages were not all refreshed. Recheck the relevant surface after a CLI change or observed drift. Do not promote a dated display name, permission behavior, or child schema into an unsupported current guarantee.
