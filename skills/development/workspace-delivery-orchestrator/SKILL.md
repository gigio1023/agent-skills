---
name: workspace-delivery-orchestrator
version: 0.1.0
description: |
  Coordinate complex workspace delivery with swarm/team-first aggressive parallelism.
  Triggers: multi-repo work, multiple workstreams, orchestration, swarm/team parallelism, "여러 레포 작업", "계획 세워줘", "병렬 실행", "오케스트레이션".
  Produces and maintains plan.md, progress.md (task.md alias), and result.md during delivery.
  NOT for: compiling successor handoff.md/context-pack.json after delivery(use workspace-handoff-compiler).
---

# Workspace Delivery Orchestrator

Use this skill for non-trivial delivery work. For complex tasks, swarm/team execution is the default; solo execution is an exception.

## Trigger Conditions
- The user asks for orchestration, delegation, swarm/team operation, or aggressive parallel execution.
- Work affects multiple repositories, subsystems, or independently shippable workstreams.
- The user asks for planning, task/progress tracking, handoff, or closure reporting.
- The request cannot be safely completed as one short change with one quick verification.

## Procedure
1. Classify complexity and choose mode using `references/orchestration-model.md`.
2. If complex, establish swarm/team roles first and enforce writer ownership boundaries.
3. Generate `plan.md` before implementation using `references/planning-contract.md`.
4. Validate `plan.md` depth/structure and revise until it satisfies the planning contract.
5. Start execution tracking in `progress.md` (or `task.md` alias) using `references/reporting-contract.md`.
6. Execute in parallel waves, then integrate and verify using `references/orchestration-model.md`.
7. Produce `result.md` for closure/handoff using `references/handoff-contract.md`.
8. Validate artifact completeness and status coherence before final handoff.

## Artifact Rules
- `plan.md`: Required before implementation for any complex task, or when the user asks for a plan.
- `progress.md` / `task.md`: Required when execution starts; update on every status transition, blocker change, and milestone.
- `result.md`: Required at completion or handoff; include outcomes, evidence, pending items, and next minimal actions.

## Plan Depth Standard (Mandatory)
`plan.md` must be a decision-grade plan, not a shell. Use the mandatory section list in `references/planning-contract.md` as the source of truth.
- `Risks and Mitigations`
- `Execution Waves/Order`

Depth requirements:
- Must explain why now, what changed, and what uncertainty exists.
- Must include explicit cross-repo impact mapping when multiple repos are in scope.
- Must define measurable completion signals and evidence collection method.
- Must include parallel execution design (what is parallel vs serialized and why).
- Must include rollback/containment intent for high-risk work.

## Non-Negotiable Constraints
- `plan.md` must remain goal/intent-centric and must not include code-level implementation detail.
- Complex work must use swarm/team-first aggressive parallelism.
- One writer per repo/file scope at a time; parallelism is maximized in read/analysis/verification streams.
- If the generated `plan.md` is shallow, regenerate and refine immediately; do not proceed with a weak plan.

## Tooling (Optional)
- Initialize artifacts from templates:
  - `scripts/init_docs.sh [target_dir]`
- Validate structure:
  - `scripts/validate_plan.py [plan.md path]`
  - `scripts/validate_progress.py [progress.md path]`
  - `scripts/validate_result.py [result.md path]`

## References
- `references/orchestration-model.md`
- `references/planning-contract.md`
- `references/reporting-contract.md`
- `references/handoff-contract.md`
