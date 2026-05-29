# Orchestration Model

## Purpose
Provide a repeatable operating model for complex workspace delivery with aggressive parallelism and controlled write safety.

## Core Policy
- Team/swarm-first is mandatory for complex tasks.
- Solo mode is allowed only for simple, low-risk, single-stream work.
- Parallelize discovery, analysis, verification, and review aggressively.
- Serialize writes by ownership boundary to avoid collisions.

## Complexity Gate
Treat a task as **complex** if any condition is true:
- More than one repository, subsystem, or deliverable is affected.
- Two or more independent workstreams can run in parallel.
- Dependencies, sequencing, or cross-team coordination are required.
- Risk of semantic regression, contract drift, or rollout failure is non-trivial.

If complex, execute in swarm/team mode.

## Role Model
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

4. Parallel Execution Waves
- Run independent streams concurrently.
- Respect blocked-by relationships.

5. Integration
- Merge outputs in dependency order.
- Resolve interface or contract mismatches.

6. Verification
- Run quality gates and invariant checks.
- Record pass/fail evidence.

7. Handoff/Closure
- Publish `result.md` with outcomes, open risks, and next actions.

## Parallelism Standards
- Prefer breadth-first progress across independent streams.
- Timebox blockers and escalate quickly.
- Do not hold all streams for a single non-critical blocker.
- Keep coordination artifacts current to prevent stale assumptions.

## Minimum Done Criteria
- Objective met or explicitly re-scoped.
- Dependency and integration gates satisfied.
- Evidence recorded for key checks.
- Remaining work captured with clear ownership and next actions.
