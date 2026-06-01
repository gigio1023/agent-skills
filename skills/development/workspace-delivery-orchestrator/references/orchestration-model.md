# Orchestration Model

## Purpose
Provide a repeatable operating model for workspace delivery: choose the execution shape that fits the work, then parallelize only where it genuinely helps and serialize writes for safety.

## Parallelism Judgment Rule (core)
Parallelism is a judgment call, not a default mandate.
- When work splits into independent streams that benefit from parallelism, use the harness's parallel-execution capability aggressively.
- When a single linear session is more effective (a simple change, one writer, tightly coupled steps), do that. A single-session linear pass is a valid first-class choice.
- Probe for a native parallel-execution capability first. If none exists in the current harness, run sequentially and say so.
- Illustrative only (not the rule): Claude Code workflows/subagents, Codex threads. Use whatever the running harness actually provides; never hard-code one harness's mechanism.

## Independence Test (before any fan-out)
Split into parallel streams only when all hold:
- Streams touch disjoint file/path scopes (no shared writer).
- No stream is blocked-by another's output for its core work.
- Coordination overhead is lower than the time saved.
If any fails, keep those streams sequential.

## Complexity Signals
A task tends toward multi-stream orchestration when any is true:
- More than one repository, subsystem, or deliverable is affected.
- Two or more genuinely independent workstreams exist.
- Dependencies, sequencing, or cross-team coordination are required.
- Risk of semantic regression, contract drift, or rollout failure is non-trivial.

These are signals to consider fan-out, not a trigger to force it. A multi-repo change with one tightly-coupled edit path can still be a single linear session.

## Role Model (when fanning out)
These roles apply when the work is split into parallel streams. In a single linear session one operator plays all of them.
- Lead Orchestrator: Defines workstreams, dependencies, and integration gates.
- Domain Readers: Gather evidence in parallel (read-only).
- Writers: Implement changes within explicit ownership boundaries.
- Verifier/Test Runner: Executes quality checks and evidence capture.
- Reviewer: Cross-checks contract integrity and unresolved risks.

## Ownership Rules
- One writer per repository/path boundary at a time.
- No concurrent edits to the same file.
- Readers and verifiers run in parallel without write privileges.
- Integration is done only after dependency prerequisites are satisfied.

## Execution Lifecycle
1. Scope Lock
- Confirm objective, constraints, and definition of done.

2. Parallel Discovery
- Run independent read/analysis tracks simultaneously.
- Capture findings as evidence, not assumptions.

3. Intent Plan
- Produce `plan.md` with goals, workstreams, dependencies, and gates.

4. Execution
- Run independent streams concurrently when fan-out passed the independence test; otherwise execute the steps in one linear pass.
- Respect blocked-by relationships either way.

5. Integration
- Merge outputs in dependency order.
- Resolve interface or contract mismatches.

6. Verification
- Run quality gates and invariant checks.
- Record pass/fail evidence.

7. Handoff/Closure
- Publish `result.md` with outcomes, open risks, and next actions.

## Parallelism Standards (when running multiple streams)
- Prefer breadth-first progress across independent streams.
- Timebox blockers and escalate quickly.
- Do not hold all streams for a single non-critical blocker.
- Keep coordination artifacts current to prevent stale assumptions.
- If the work no longer benefits from fan-out (streams collapsed onto one scope), drop back to a single linear pass.

## Minimum Done Criteria
- Objective met or explicitly re-scoped.
- Dependency and integration gates satisfied.
- Evidence recorded for key checks.
- Remaining work captured with clear ownership and next actions.
