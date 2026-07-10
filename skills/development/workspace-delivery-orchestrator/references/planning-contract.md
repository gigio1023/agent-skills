# Planning Contract (`plan.md`)

`plan.md` records delivery intent and execution shape. It is not a coding script.

## Content Boundary

Keep goals, scope, ownership, dependencies, validation, risk, and observable
outcomes. Exclude patch snippets, line-level edits, payload literals, and
step-by-step coding directions. Mention a concrete path or interface only when
it defines ownership or a contract boundary.

## Required Sections

The heading order below is canonical. The bundled validator enforces it and the
initializer supplies the compact template.

1. `Intent (의도)` - mission and why now.
2. `Background (배경)` - relevant current state and uncertainty.
3. `Goals (목표)` - concrete outcome targets.
4. `Expected Results (결과)` - observable end state.
5. `Scope` - in and out boundaries.
6. `Constraints` - limits and do-not-touch areas.
7. `Acceptance Criteria` - measurable done signals.
8. `Workstreams` - only real work packages, each with owner, output, and done signal.
9. `Dependency Graph` - blocked-by edges and independent groups.
10. `Validation Plan` - checks and evidence needed for closure.
11. `Risks and Mitigations` - material failure modes and containment.
12. `Parallelism Strategy` - sequential/parallel decision and writer boundaries.
13. `Rollback / Containment Intent` - recovery for medium/high-risk work; state
    `Not needed` with a reason for low-risk work.

## Quality Gate

- Every goal maps to an observable result or acceptance criterion.
- Every workstream has a scoped outcome, owner, output, and done signal.
- Dependencies and single-writer boundaries are explicit.
- Parallel tracks pass the independence test; otherwise the plan says
  sequential.
- Validation names the evidence to collect, not just "test it".
- Risks and rollback depth match actual impact; low-risk work stays brief.

When required headings change, update the validator and template together, then
run the bundled smoke test.
