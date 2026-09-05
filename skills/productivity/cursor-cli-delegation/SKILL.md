---
name: cursor-cli-delegation
description: >
  Use only when the user explicitly invokes or names cursor-cli-delegation to
  delegate a substantial, already-bounded mission through Cursor Agent CLI.
  Keeps planning and acceptance in the caller while Cursor executes commands,
  implementation, MCP work, testing, manipulation, and verification. Covers
  exact parent/child model selection, subagents, isolation, and evidence. NOT
  for automatic routing from Cursor, Grok, CLI, MCP, or model mentions;
  unresolved planning; plan mode; or model substitution.
---

# CLI Agent Delegation

Use the Cursor Agent CLI as an external execution lane while the calling
harness retains judgment and acceptance. The executor may do substantial
implementation, command, MCP, test, manipulation, and verification work inside
a closed mission; it does not inherit authority to redesign the mission.

## Invocation Policy

Use this skill only when the user explicitly invokes or names
`cursor-cli-delegation`. Mentioning Cursor, Grok, a model, the CLI, MCP, external
execution, or `parallel-subagents` does not invoke it. Never auto-route work to
Cursor. After explicit invocation, continue only when the mission is settled,
the external lane adds value, and the lead can inspect the result.

## Quick Path

1. Confirm the mission is ready:
   - one observable outcome;
   - fixed product and architecture decisions;
   - a named repository and revision or worktree;
   - explicit write, command, MCP, credential, and external-effect authority;
   - a deadline, preservation rules, acceptance evidence, and stop conditions.
   Fill these from the settled plan and session grants. Return only unresolved
   consequential choices to the lead; packet preparation is not another user
   approval round for decisions already made.
2. Keep planning, conflict resolution, scope changes, destructive decisions,
   integration, and final acceptance in the lead harness.
3. Read `references/cursor-agent-cli.md` and probe the installed CLI. Apply
   Model Policy below. Never infer an ID from a display name or silently
   substitute another model.
4. Choose one isolation owner. Reuse existing isolation, or create one only
   when the user or packet authorizes a new branch/worktree. Never stack
   isolation mechanisms.
5. Write one self-contained mission packet. Include only the context needed to
   execute it; point to repository sources instead of pasting the whole session.
6. Launch non-interactively in Cursor's normal execution mode with structured
   output. Do not pass `--mode plan` or `--mode ask`; this skill delegates
   execution, including read-only command and MCP work, rather than planning.
   Grant unattended writes or MCP approval only when the mission authorizes it.
7. Encourage the Cursor parent to use subagents for independent execution
   lanes. A justified per-lane model guide may differ from the parent; every
   child must still receive its exact model ID, any thinking or effort setting
   the live Task/tool schema exposes, and a lane-specific subset of authority,
   preservation, evidence, and stop rules. If Cursor cannot select and later
   expose those child settings, keep that lane in the parent instead.
8. Inspect the returned result, structured events, repository diff, generated
   artifacts, verification output, and Cursor transcript. Reject the lane if
   any child used a model or thinking setting outside the selected policy. Exit
   zero or an executor claim is not acceptance.

Finish open research or decisions in the lead first. For parallel lanes,
`orchestrate-subagents` owns decomposition and synthesis; this skill owns each
explicitly selected Cursor CLI lane.

Delegation never expands user authorization. Review-only missions stay
read-only. A change mission permits only the local edits and non-destructive
checks described in the packet.

## Model Policy

After the dated CLI reference and a live `agent models` probe:

1. An exact user-supplied model policy wins.
2. Else, when the bounded mission's dominant need is sustained context, careful
   judgment or synthesis, instruction work, or sustained subagent coordination,
   select Claude Fable 5 as a first-class option and pass an exact verified
   Fable thinking ID from the live listing.
3. Else use `cursor-grok-4.6-high-fast` for the parent and every child with no
   justified per-lane guide.

Fable is an explicit selection, not a silent fallback or substitution. If the
selected ID is absent, stop.

Enable thinking whenever the selected model and live Cursor surface support it.
Top-level: a listed thinking profile or a parameterized `--model` override
only when the live CLI documents that form. Child tasks: enable an exposed
thinking option, or set an effort control when that is the documented thinking
surface. Never invent a model ID, suffix, override, or child field. If no
supported thinking form exists, keep the exact selected ID and record that.
Dated IDs live in `references/cursor-agent-cli.md`.

## Mission Packet

Write one packet containing:

- one observable outcome and the fixed decisions;
- workspace, revision, isolation owner, instructions, and sources of truth;
- authorized files, commands, MCPs, credentials, network or external effects,
  retries, artifacts, subagents, and the exact model and available thinking
  setting each child must use;
- preserved behavior and explicit non-goals;
- required checks, observable acceptance, and returned evidence;
- a wall-clock deadline and scoped cancellation owner;
- stop conditions for state mismatch, missing model/tool/auth, user-change
  overlap, out-of-scope work, missing decisions, or unprovable acceptance; and
- a final report covering session/model evidence, changed files, diff, commands,
  results, deviations, unknowns, and the smallest blocker.

The packet is closed but not blind. The executor must read enough surrounding
code to find the real flow and root cause. It may make ordinary tactical choices
inside the fixed scope, but must stop before a new product, architecture,
recovery, or authority decision.

## Minimal-Implementation Rule

Understand the affected flow, then skip unnecessary work, reuse repository or
native facilities, and make the shortest correct root-cause change. Add no
speculative abstraction, dependency, document, or tooling. Preserve validation,
security, accessibility, data-loss protection, calibration, and explicit
requirements. Non-trivial logic leaves the narrowest runnable check protecting
the visible consequence.

## Isolation and Parallelism

For writes, prefer lead-owned isolation when the lead will inspect or integrate
in place. Use Cursor worktrees only when no outer worktree exists. Parallel
writers need distinct worktrees or mechanically disjoint ownership. Creating a
branch or worktree requires explicit user or mission-packet authority.

Cursor may create internal subagents for independent exploration,
implementation, or verification. Restate the outcome, scope, authority,
evidence, and stop conditions to every child, narrowing authority to that
child's lane. Pass each child's exact model and any available thinking
setting in the child task; do not use a convenience or fallback model.
Require transcript or tool-call evidence of those settings. Missing
evidence makes that child's result unverified.

## MCP and Permission Boundary

Inspect configured MCP servers first. Approve all only when every server is
required and trusted. Unattended writes are a broad grant; use them only for a
closed mission in isolation. A read-only mission still uses Cursor's normal
execution mode; enforce no-mutation authority in the packet, avoid unnecessary
broad grants, and audit the workspace and external state afterward.

Never place secrets in the mission packet or captured output. Refer to existing
environment or credential mechanisms without printing their values.

## Acceptance Gate

The lead accepts the mission only after checking:

- CLI version, exact requested model ID and mapping, thinking form or recorded
  lack of support, launch arguments, and the service-reported initialization
  label;
- every Cursor child task's explicit model argument, available thinking
  setting, and transcript evidence;
- process status, terminal result, and session identity when supplied;
- changed files and external effects stayed inside authority;
- the diff is the smallest correct root-cause implementation;
- observed checks support the claim;
- user changes, safety boundaries, and fixed decisions remain intact;
- manual or rendered evidence gaps are named honestly.

A missing terminal event, nonzero process status, malformed structured output,
unexpected diff, or unverifiable acceptance claim is a failed or incomplete
mission. Preserve its evidence and return the decision to the lead.

## Gotchas

- Do not silently substitute a model, mode, worktree, or MCP permission.
- Do not use `--mode plan` or `--mode ask`; return unfinished planning to the
  lead and execute settled work in normal mode.
- Do not let an internal Task choose its own default model or thinking setting.
- Do not invent a model ID, thinking suffix, parameterized override, or child
  thinking field.
- Do not treat `--force` as local-write permission; it is a broad trust grant.
- Do not run concurrent writers in one checkout.
- Do not ask the executor that made a diff to provide final acceptance.
- Do not turn a failed check into permission for adjacent fixes.
- Do not confuse the top-level model event with proof of every child model;
  inspect Task/subagent records and reject mixed-model execution.

## Reference

Read `references/cursor-agent-cli.md` immediately before launch for the dated
commands, model mapping, permissions, evidence, failure handling, and sources.
