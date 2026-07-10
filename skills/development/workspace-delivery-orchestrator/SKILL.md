---
name: workspace-delivery-orchestrator
description: >
  Use when the user explicitly wants durable `plan.md`, `progress.md`, and
  `result.md` artifacts for non-trivial delivery, or when work spans multiple
  repositories or independent workstreams and needs ownership, dependencies,
  execution coordination, and closure evidence. Triggers on multi-repo delivery,
  multiple workstreams, orchestration, "여러 레포 작업", "병렬 실행", and
  explicit progress/result tracking. NOT for a simple single-scope change, an
  ordinary conversational plan with no artifact requirement, or compiling a
  successor handoff (use workspace-handoff-compiler).
---

# Workspace Delivery Orchestrator

Coordinate non-trivial delivery through three compact, evidence-backed
artifacts. Match ceremony to actual complexity: one sequential workstream is a
valid plan, and parallel tracks exist only when they pass the independence test.

## Quick Start

1. Confirm the trigger: durable delivery artifacts are requested or the work
   genuinely needs cross-repo/workstream coordination. Do not create these files
   for a routine change merely because planning could be useful.
2. Inspect workspace instructions and existing `plan.md`, `progress.md` or
   `task.md`, and `result.md`. Preserve user-authored content and select one
   authoritative progress artifact.
3. Classify the execution shape with `references/orchestration-model.md`.
   Default to sequential when streams share writes, depend on unfinished
   outputs, or would cost more to coordinate than they save.
4. Initialize missing artifacts when useful:

   ```bash
   scripts/init_docs.sh <target_dir>
   ```

   Fill `plan.md` from `references/planning-contract.md`, then validate it
   before implementation:

   ```bash
   python3 scripts/validate_plan.py <plan.md>
   ```

5. Execute only the scoped workstreams. Update `progress.md` on status,
   blocker, scope, or milestone changes, not after every tool call. Back `done`
   states with inspectable tool results.
6. Integrate in dependency order, run the planned checks, and write
   `result.md` from `references/handoff-contract.md`.
7. Validate closure artifacts and fix failures before reporting:

   ```bash
   python3 scripts/validate_progress.py <progress.md>
   python3 scripts/validate_result.py <result.md>
   ```

8. Lead the final response with delivery status and outcomes, then link the
   artifacts, verification evidence, residual risks, and next minimal action.

## Artifact Contract

The references are the single source of truth for required sections and status
semantics:

| Artifact | Purpose | Contract |
| --- | --- | --- |
| `plan.md` | Outcome, boundaries, execution shape, and done signals before implementation | `references/planning-contract.md` |
| `progress.md` (`task.md` alias) | Current workstream state and blockers during execution | `references/reporting-contract.md` |
| `result.md` | Outcome, evidence, remaining work, and closure status | `references/handoff-contract.md` |

Keep required facts, decisions, caveats, ownership, and actions. Trim generic
process narration, placeholder workstreams, repeated background, and
implementation detail better represented by the diff.

## Execution Boundaries

- One writer owns a repository or file scope at a time. Parallel reads and
  verification may proceed independently; overlapping writes are serialized.
- Do not create extra roles, workstreams, refactors, or deliverables to make the
  plan look complete. Every stream needs a scoped outcome and done signal.
- A plan does not authorize work outside the user's request. Record out-of-scope
  opportunities instead of implementing them.
- If evidence changes scope, dependencies, or acceptance criteria, update the
  plan/progress artifact before continuing.
- If a required decision or external dependency blocks safe progress, mark the
  affected stream blocked and state the smallest unblock action.

## Tooling

Run scripts from this skill directory; paths above are relative to it.

- `scripts/init_docs.sh [target_dir]` copies missing templates and never
  overwrites existing artifacts.
- `scripts/validate_plan.py [path]` checks required H2 sections, canonical order,
  and duplicates. `validate_progress.py [path]` and `validate_result.py [path]`
  check their required structure.
- `scripts/smoke_test.sh` initializes a temporary artifact set and runs all
  validators plus out-of-order and duplicate-plan negative fixtures. It requires
  Bash and Python 3.

## Output Contract

`result.md` and the final response must agree on `complete`, `partial`, or
`blocked`. Completion claims cite commands, files, logs, or other inspectable
evidence. Include what was not verified only when it materially limits
confidence. Do not present a passing structural validator as proof that the
delivery objective itself succeeded.

## Gotchas

- A shallow template with headings but no outcomes, boundaries, owners, or done
  signals is not a valid plan even if the structure validator passes.
- Do not force parallelism onto tightly coupled or single-writer work. Revert to
  sequential execution when tracks converge on one scope.
- `progress.md` and `task.md` are aliases, not two status sources. Never let them
  diverge.
- Update progress from tool-backed state. Do not mark `done` because an agent
  reported intent or because a patch was merely attempted.
- Keep artifact files in the target workspace, not in this skill directory.

## Reference Files

| File | Read when | Content |
| --- | --- | --- |
| `references/orchestration-model.md` | Choosing or changing execution shape | Independence, ownership, integration, and done rules |
| `references/planning-contract.md` | Creating or revising `plan.md` | Required headings and content boundaries |
| `references/reporting-contract.md` | Tracking active execution | Statuses, update triggers, and consistency rules |
| `references/handoff-contract.md` | Closing or pausing delivery | Result sections, evidence, and status rules |
