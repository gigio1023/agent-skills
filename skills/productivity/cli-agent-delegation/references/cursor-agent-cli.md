# Cursor Agent CLI Contract

Verified against the local Cursor Agent CLI on 2026-07-23. The installed
executable is the source of truth because flags and model IDs can change.

## Contents

- Preflight
- Model resolution
- Non-interactive launch
- Prompt transport
- Workspace isolation
- Permissions and MCP
- Structured evidence
- Sessions and follow-ups
- Parallel and nested agents
- Failure handling
- Maintenance sources

## Preflight

Run these read-only checks from the target repository:

```bash
command -v agent
agent --version
agent status
agent --help
agent models
```

Stop when the executable, authentication, requested model, or required current
flag is unavailable. Do not log in, update the CLI, change configuration, or
select a substitute model unless the user authorized that action.

On the verified installation:

```text
agent version: 2026.07.20-8cc9c0b
agent models display name: Cursor Grok 4.5 Fast
requested model ID: cursor-grok-4.5-high-fast
initialization event model: Cursor Grok 4.5 High Fast
```

Treat this as a dated observation, not a permanent alias.

## Model Resolution

Resolve the model at launch time:

```bash
agent models
```

Match the exact requested profile and pass its ID with `--model`. A display name
such as “High Fast” is not a CLI contract. If the requested ID is absent, stop
and report the available relevant entries. Never silently fall back to `auto`
or a different model.

The selected top-level model should appear in the `stream-json` initialization
event. The display label may differ from `agent models`; match the requested ID
before launch, then retain the emitted label as run evidence. If no model event
appears, report model identity as unverified.

## Non-Interactive Launch

Read-only inspection:

```bash
packet_path=/absolute/path/to/mission.md
packet="$(<"$packet_path")"
agent \
  --print \
  --mode plan \
  --model cursor-grok-4.5-high-fast \
  --workspace /absolute/path/to/workspace \
  --output-format stream-json \
  --trust \
  "$packet"
```

Authorized change mission:

```bash
packet_path=/absolute/path/to/mission.md
packet="$(<"$packet_path")"
agent \
  --print \
  --model cursor-grok-4.5-high-fast \
  --workspace /absolute/path/to/workspace \
  --output-format stream-json \
  --sandbox enabled \
  --force \
  --trust \
  "$packet"
```

`--print` is the scripting and non-interactive surface. The verified help states
that it retains write and shell tools; read-only behavior therefore comes from
the selected read-only mode and packet, not from `--print` itself.

`--force` auto-allows commands unless explicitly denied. Use it only for an
already-authorized closed change mission. `--trust` suppresses the workspace
trust prompt; use it only after the lead verifies the exact workspace.

The sandbox is a useful default for local implementation but may block a task
whose explicit requirements cross its boundary. Do not disable it merely to
make a failed run continue. Return that boundary to the lead.

## Prompt Transport

The verified help exposes the prompt as positional arguments and does not expose
a prompt-file flag. Put a long packet in a file for review, read it into one
quoted shell variable, and pass that variable as one argument.

Do not use `eval`, interpolate the packet into executable shell source, or place
secrets in it. When the calling harness has a subprocess API that accepts an
argument array, prefer that API over composing a shell string.

Keep the packet as a temporary or ignored artifact unless the repository asks
for tracked task documents. Do not create a standing report or tracker merely
to transport the prompt.

## Workspace Isolation

The verified CLI supports:

```text
--workspace <path-or-name>
--add-dir <path>
--worktree [name]
--worktree-base <branch>
--skip-worktree-setup
```

Use one isolation owner:

- If the lead or harness already created a worktree, pass its absolute path with
  `--workspace` and omit Cursor worktree flags.
- Otherwise Cursor may create one with `--worktree <name>` and an explicit
  `--worktree-base <ref>`.
- Never create a Cursor worktree inside a lead-owned worktree.

Record the canonical workspace path, base revision, and pre-run status. After
the run, compare the same workspace and inspect its diff.

## Permissions and MCP

The verified CLI separates command auto-approval, sandbox mode, workspace trust,
and MCP approval:

```text
--force
--sandbox enabled|disabled
--trust
--approve-mcps
```

Do not collapse them into one “unattended” switch. For an MCP mission:

1. Inspect repository and user Cursor MCP configuration.
2. Confirm every automatically approved server is trusted and in scope.
3. Add `--approve-mcps` only when blanket approval of that configured set is
   acceptable.
4. State tool-specific authority in the mission packet.

The CLI can discover repository rules and MCP configuration, but discovery does
not grant new authority. A configured server may still perform external writes,
open windows, or control another process.

## Structured Evidence

Prefer:

```text
--output-format stream-json
```

Capture the host process status and parse the stream. The documented stream
includes an initialization event with fields such as workspace/model/permission
mode and a terminal result event. Current documented terminal JSON includes
result state, error state, duration, response text, and session ID.

On the verified version, `--mode ask` still emitted
`"permissionMode":"default"` in the initialization event. Do not use that field
alone to prove read-only mode; retain the exact launch arguments and inspect the
workspace afterward.

Require all of:

- process exit status;
- initialization event and selected model when emitted;
- terminal result event;
- session ID when emitted;
- executor response;
- independent workspace status and diff;
- required command outputs and generated artifacts.

Do not treat prose such as “all tests pass” as test evidence. Do not treat exit
zero as proof that the requested outcome or authorized scope was satisfied.
Thinking or partial deltas are transport noise, not acceptance evidence; do not
surface them as hidden reasoning.

`--stream-partial-output` is optional and only applies to `--print` with
`stream-json`. Use it for live progress only when the calling harness can absorb
the additional event volume.

## Sessions and Follow-ups

The verified CLI supports:

```text
--resume [chatId]
--continue
agent ls
agent resume
agent create-chat
```

Prefer a fresh mission for independent work. Resume the exact returned session
only for a narrow correction that depends on its context. Never use a vague
“continue previous” in parallel orchestration, where the previous session may
belong to another lane.

A follow-up packet should state:

- accepted evidence from the prior run;
- the one failed criterion;
- the exact correction authority;
- unchanged non-goals and stop conditions.

Do not ask the same executor to self-approve its first result.

## Parallel and Nested Agents

The verified top-level help has no general `--parallel` flag for launching
independent local missions. The outer harness owns process concurrency,
worktrees, timeouts, cancellation, and synthesis.

Cursor officially supports subagents in the CLI, including parallel specialized
contexts. Current Cursor releases also describe asynchronous and nested
subagents. Treat that as agent capability, not a stable top-level command-line
API.

The mission may tell the Cursor parent to use subagents when:

- lanes are independent;
- write ownership is disjoint;
- each child receives a complete bounded packet;
- the parent integrates and reports their evidence.

The top-level `--model` proves only the parent selection. Do not claim that every
child used the same model unless direct run evidence or an explicit custom
subagent configuration proves it.

## Failure Handling

Return control to the lead when:

- the requested model is unavailable;
- authentication or required MCP routing is unavailable;
- the process exits nonzero or emits no terminal result;
- the workspace or base revision differs from the packet;
- a user change overlaps the authorized edit;
- the executor requests destructive, credential, network, or external-write
  authority not already granted;
- required acceptance cannot be demonstrated;
- another product or architecture decision is needed.

Preserve structured output and the resulting diff. One bounded retry is
reasonable only when the packet already defines the recovery, such as a
transient transport retry or a corrected exact command. Otherwise the lead
decides the next step.

## Maintenance Sources

Primary sources:

- [Cursor CLI overview](https://docs.cursor.com/en/cli/overview)
- [Headless CLI](https://docs.cursor.com/en/cli/headless)
- [CLI parameters](https://docs.cursor.com/en/cli/reference/parameters)
- [CLI output format](https://docs.cursor.com/en/cli/reference/output-format)
- [Using the CLI, including rules and MCP](https://docs.cursor.com/en/cli/using)
- [Cursor 2.4: CLI subagents and skills](https://cursor.com/changelog/2-4)
- [Cursor 2.5: asynchronous and nested subagents](https://cursor.com/changelog/2-5)

Re-run the preflight after a CLI update. Update this dated reference when local
help, structured events, permission behavior, model IDs, or official subagent
contracts change.
