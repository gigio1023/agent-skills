# Planning Contract (`plan.md`)

## Intent
`plan.md` defines delivery intent and execution shape. It is not an implementation script.

## Mandatory Rule
`plan.md` must be **goal/intent-centric** and must **not** include code-level implementation detail.

Disallowed examples:
- Exact file edits, function names, line-level changes, patch snippets.
- API payload literals intended as implementation instructions.
- Step-by-step coding directions.

Allowed examples:
- Business/technical objective and scope boundaries.
- Workstream intent, ownership, dependencies, and sequencing.
- Validation gates, risks, and success criteria.
- Why-now context, assumptions, and expected observable results.
- Cross-repo impact map and rollback/containment intent.

## Required Sections (single source of truth)
The heading order below is the canonical list. `scripts/validate_plan.py` enforces it, `assets/templates/plan.template.md` emits it, and `SKILL.md` points here instead of restating it. If this list changes, update the validator first, then regenerate the template and re-run `scripts/smoke_test.sh`.

1. Intent (의도)
- One-line mission and why this delivery is needed now.

2. Background (배경)
- Current state, recent change drivers, known uncertainty.

3. Goals (목표)
- 2~6 concrete goals stated as outcome targets.

4. Expected Results (결과)
- Observable end-state after delivery (what will be visibly different).

5. Scope
- In-scope and out-of-scope boundaries.

6. Constraints
- Time/scope limits, technical constraints, and do-not-touch areas. Stack-neutral; fill with whatever the repository and task impose.

7. Acceptance Criteria
- Observable and measurable completion conditions.

8. Workstreams
- Intent-level work packages with owner, output artifact, and done signal.

9. Dependency Graph
- `blocked-by` relationships and explicit parallelizable groups.

10. Validation Plan
- Required checks before integration and closure.

11. Risks and Mitigations
- High-impact failure modes and containment strategy.

12. Parallelism Strategy
- Parallelizable tracks, required sequencing, and single-writer boundaries. Use parallel fan-out only where streams are genuinely independent.

13. Rollback / Containment Intent (for medium-high risk)
- How to contain blast radius and recover if assumptions fail.

## Template
```markdown
# plan.md

## Intent (의도)
- ...

## Background (배경)
- ...

## Goals (목표)
- Goal 1: ...
- Goal 2: ...

## Expected Results (결과)
- ...

## Scope
- In scope: ...
- Out of scope: ...

## Constraints
- Time/scope limits: ...
- Technical constraints: ...
- Do-not-touch areas: ...

## Acceptance Criteria
- ...

## Workstreams
- WS1: <intent>, Owner: <role>, Output: <artifact>
- WS2: <intent>, Owner: <role>, Output: <artifact>

## Dependency Graph
- WS2 blocked-by WS1
- WS3 parallel with WS2

## Validation Plan
- Gate A: ...
- Gate B: ...

## Risks and Mitigations
- Risk: ... / Mitigation: ...

## Parallelism Strategy
- Parallelizable tracks: ...
- Required sequencing: ...
- Single-writer boundaries: ...

## Rollback / Containment Intent
- ...
```

## Quality Checklist
- No code-level directions present.
- Intent/background/goals/expected-results are all present and non-empty.
- Expected results are observable (not abstract).
- Workstreams include owner + output + done signal.
- Dependencies are explicit.
- Parallelism opportunities are explicit.
- Success criteria are measurable.
