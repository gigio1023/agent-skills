---
name: workspace-delivery-orchestrator
description: Use when coordinating multi-repo or multi-workstream delivery that needs a real plan, parallel execution where streams are independent, and progress/closure tracking. Triggers on multi-repo work, multiple workstreams, orchestration, "여러 레포 작업", "계획 세워줘", "병렬 실행", "오케스트레이션". NOT for compiling successor handoff.md/context-pack.json after delivery (use workspace-handoff-compiler).
---

# Workspace Delivery Orchestrator

Use this skill for non-trivial delivery work that needs a decision-grade plan, coordinated execution, and progress/closure tracking. The execution shape (single linear session vs parallel fan-out) is a judgment call, not a fixed mandate.

## Produced Artifacts
- `plan.md`: decision-grade plan, written before implementation for complex work or when the user asks for a plan.
- `progress.md` (`task.md` alias): live execution state, updated on every status transition, blocker change, and milestone.
- `result.md`: closure/handoff artifact with outcomes, evidence, pending items, and next minimal actions.

## Trigger Conditions
- The user asks for orchestration, delegation, parallel execution, or planning.
- Work affects multiple repositories, subsystems, or independently shippable workstreams.
- The user asks for task/progress tracking, handoff, or closure reporting.
- The request cannot be safely completed as one short change with one quick verification.

## Procedure
1. Classify complexity and decide the execution shape using `references/orchestration-model.md`.
2. Generate `plan.md` before implementation using `references/planning-contract.md`.
3. Validate `plan.md` structure with `scripts/validate_plan.py` and revise until it passes.
4. Start execution tracking in `progress.md` (or `task.md` alias) using `references/reporting-contract.md`.
5. Execute. Fan out into parallel streams only when they pass the independence test; otherwise run a single linear pass. Then integrate and verify per `references/orchestration-model.md`.
6. Produce `result.md` for closure/handoff using `references/handoff-contract.md`.
7. Validate artifact completeness and status coherence before final handoff.

## Execution Shape (parallelism is a judgment call)
- When work splits into independent streams that benefit from parallelism, use the harness's parallel-execution capability aggressively.
- When a single linear session is more effective, do that. A single-session linear pass is a valid first-class choice.
- Probe for a native parallel-execution capability first. If none exists in the current harness, run sequentially and say so.
- Fan out only when streams touch disjoint file/path scopes, none is blocked-by another's output, and coordination overhead is below the time saved.
- One writer per repo/file scope at a time. Parallelism is safest in read, analysis, and verification streams.
- Illustrative examples only (never the rule itself): Claude Code workflows/subagents, Codex threads. Use whatever the running harness actually provides.

See `references/orchestration-model.md` for the full independence test and role model.

## Plan Depth Standard
`plan.md` must be a decision-grade plan, not a shell. The mandatory section list and depth requirements live in `references/planning-contract.md`, which is the single source of truth for plan structure (it mirrors `scripts/validate_plan.py`).

## Non-Negotiable Constraints
- `plan.md` must remain goal/intent-centric and must not include code-level implementation detail.
- One writer per repo/file scope at a time.
- If the generated `plan.md` is shallow or fails `scripts/validate_plan.py`, regenerate and refine immediately; do not proceed with a weak plan.

## Gotchas
- Shallow plan.md shells: a plan with empty section headings and no real intent, scope, or done signals is not a plan. Fill every required section with decision-grade content before executing.
- Forcing parallelism on a simple change: a 3-line edit does not need workstreams, roles, or fan-out. Match the ceremony to the work; a single linear pass is correct here.
- Multiple writers on one file scope: two streams editing the same file (or the same path boundary) will collide. Keep one writer per scope and serialize the boundary.
- Claiming parallelism without a native capability: if the harness has no parallel-execution mechanism, do not pretend to fan out. Run sequentially and say so.
- Divergent progress/task files: `progress.md` and its `task.md` alias must not hold conflicting state. Keep one authoritative copy.

## Tooling
These scripts ship with the skill. Run them from the skill directory (paths are relative).
- Initialize artifacts from templates: `scripts/init_docs.sh [target_dir]`
- Validate structure:
    - `scripts/validate_plan.py [plan.md path]`
    - `scripts/validate_progress.py [progress.md path]`
    - `scripts/validate_result.py [result.md path]`
- Smoke test (init + all three validators on generated files): `scripts/smoke_test.sh`

`init_docs.sh` and `smoke_test.sh` need `bash`; the validators need `python3`. If a tool is missing, install it first.

## References
- `references/orchestration-model.md`
- `references/planning-contract.md`
- `references/reporting-contract.md`
- `references/handoff-contract.md`
