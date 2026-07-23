---
name: cursor-cli-delegation
description: >
  Use only when the user explicitly invokes or names cursor-cli-delegation to
  delegate a substantial, already-bounded mission through Cursor Agent CLI.
  Covers closed packets, exact model selection, non-interactive launch,
  isolation, optional Cursor subagents and MCP use, evidence capture, and
  lead-side acceptance. NOT for automatic routing from Cursor, Grok, CLI, MCP,
  or model mentions; unresolved planning; model substitution; or shell commands.
---

# CLI Agent Delegation

Use the Cursor Agent CLI as an external execution lane while the calling
harness retains judgment and acceptance. The executor may do substantial
implementation and tool work inside a closed mission; it does not inherit
authority to redesign the mission.

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
2. Keep planning, conflict resolution, scope changes, destructive decisions,
   integration, and final acceptance in the lead harness.
3. Read `references/cursor-agent-cli.md` and probe the installed CLI. Resolve
   the requested model from `agent models`; never infer an ID from its display
   name or silently substitute another model.
4. Choose one isolation owner. Reuse existing isolation, or create one only
   when the user or packet authorizes a new branch/worktree. Never stack
   isolation mechanisms.
5. Write one self-contained mission packet. Include only the context needed to
   execute it; point to repository sources instead of pasting the whole session.
6. Launch non-interactively with structured output. Grant unattended writes or
   MCP approval only when the mission explicitly authorizes them.
7. Let the Cursor parent use its own subagents when the mission contains
   independent lanes and the packet permits them. Each child receives a
   lane-specific subset of authority plus the shared preservation and stop rules.
8. Inspect the returned result, structured events, repository diff, generated
   artifacts, and verification output. Exit zero or an executor claim is not
   acceptance.

Finish open research or decisions in the lead first. For parallel lanes,
`parallel-subagents` owns decomposition and synthesis; this skill owns each
explicitly selected Cursor CLI lane.

## Authority Split

| Lead harness owns | Cursor executor owns inside the packet |
| --- | --- |
| Objective, decisions, scope, non-goals | Trace the named flow and callers |
| Model and fallback policy | Choose the smallest correct tactic |
| Worktree and concurrency topology | Make authorized edits and tool calls |
| Destructive, credential, MCP, external-write authority | Bounded diagnosis inside the fixed decision |
| Conflict resolution, acceptance, integration, user report | Evidence and an honest completion or blocker report |

Delegation never expands user authorization. Review-only missions stay
read-only. A change mission permits only the local edits and non-destructive
checks described in the packet.

## Mission Packet

Write the packet in this order:

```text
Outcome
- One observable result.

Fixed decisions
- Choices that must not be reopened.

Repository state
- Workspace, revision, branch/worktree owner, instructions, sources of truth.

Scope
- Authorized files, systems, commands, non-goals, and preserved behavior.

Authority
- Writes, commands, artifacts, network, MCPs, credentials, external effects,
  retries, and subagent use.

Execution rules
- Trace the affected flow and callers before editing.
- Reuse existing/native facilities; make the smallest root-cause diff.
- Add no speculative abstraction, dependency, document, or tooling.
- Preserve safety boundaries and every explicit requirement.

Verification
- Required checks, observable acceptance, and returned evidence.

Deadline
- Wall-clock limit and what the lead terminates and inspects after a stall.

Stop conditions
- Mismatch, unavailable model/tool/auth, user-change overlap, out-of-scope need,
  missing decision, or acceptance that cannot be demonstrated.

Final report
- Model/session evidence, changed files, diff summary, commands and observed
  results, deviations, unverified claims, and the smallest blocker.
```

The packet is closed but not blind. The executor must read enough surrounding
code to find the real flow and root cause. It may make ordinary tactical choices
inside the fixed scope, but must stop before a new product, architecture,
recovery, or authority decision.

## Minimal-Implementation Rule

Within the locked decisions, use this order:

1. Skip work that the requested outcome does not need.
2. Reuse an existing code path or repository pattern.
3. Use the standard library or native platform.
4. Reuse an already-installed dependency.
5. Make the shortest correct root-cause change.

Minimize only after understanding the flow. Do not patch the named symptom if a
shared routing point is the actual fix. Preserve validation, security,
accessibility, data-loss protection, calibration, and explicit requirements.
Non-trivial logic leaves the narrowest runnable check that protects the visible
consequence.

## Isolation and Parallelism

For writes, prefer lead-owned isolation when the lead will inspect or integrate
in place. Use Cursor worktrees only when no outer worktree exists. Parallel
writers need distinct worktrees or mechanically disjoint ownership. Creating a
branch or worktree requires explicit user or mission-packet authority.

Cursor may create internal subagents for independent exploration,
implementation, or verification. Restate the outcome, scope, authority,
evidence, and stop conditions to every child, narrowing authority to that
child's lane. Do not assume a child used the parent's model without direct
evidence.

## MCP and Permission Boundary

Inspect configured MCP servers first. Approve all only when every server is
required and trusted. Unattended writes are a broad grant; use them only for a
closed mission in isolation. Read-only missions use a read-only Cursor mode.

Never place secrets in the mission packet or captured output. Refer to existing
environment or credential mechanisms without printing their values.

## Acceptance Gate

The lead accepts the mission only after checking:

- CLI version, exact requested model ID and mapping, launch arguments, and the
  service-reported initialization label;
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
- Do not treat `--force` as local-write permission; it is a broad trust grant.
- Do not run concurrent writers in one checkout.
- Do not ask the executor that made a diff to provide final acceptance.
- Do not turn a failed check into permission for adjacent fixes.
- Do not confuse the top-level model event with proof of every child model.

## Reference

Read `references/cursor-agent-cli.md` immediately before launch for the dated
commands, model mapping, permissions, evidence, failure handling, and sources.
