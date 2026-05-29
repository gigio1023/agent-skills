---
name: workspace-handoff-compiler
version: 0.1.0
description: |
  Compile prior plan/work/result artifacts into `handoff.md` and `context-pack.json` for a successor AI.
  Triggers: handoff, context pack, session handoff, successor AI, continue across sessions, "인계", "이어서 작업", "다음 AI에게 넘겨줘", "멀티레포 핸드오프".
  Enforce source priority, explicit conflict resolution, evidence-based status downgrades (`partial` or `blocked` when proof is missing), and swarm/team-first continuation for complex work.
  NOT for: producing plan.md/progress.md/result.md during active delivery(use workspace-delivery-orchestrator).
---

# Workspace Handoff Compiler

1. Gather available artifacts for plan, execution, validation, and outcomes.
2. Apply source precedence and conflict handling from `references/handoff-source-priority.md`.
3. Evaluate completion confidence with `references/handoff-quality-gate.md`.
4. Decide continuation mode with `references/swarm-continuation-contract.md`.
5. Generate outputs:
   - `handoff.md` for human continuation.
   - `context-pack.json` following `references/context-pack-schema.md`.
6. Start from `assets/templates/handoff.template.md` and `assets/templates/context-pack.template.json` when creating new artifacts.
7. Keep facts, inferences, and unknowns separate in both outputs.
8. Do not claim `complete` without required evidence.
9. If evidence is missing or conflicting, degrade status to `partial` or `blocked` and list missing proof.

## Output Requirements

- `handoff.md` includes:
  - objective, completed work, remaining work, blockers, risks, and first next actions.
  - evidence references for every completion claim.
  - explicit continuation mode (`swarm_required` or `single_agent_allowed`).
  - per-objective task status can use `done/in_progress/blocked/not_started`; this is separate from the overall handoff status `complete/partial/blocked`.
- `context-pack.json` includes:
  - normalized machine-readable state and dependency graph.
  - ownership, constraints, and verification status.
  - status identical to `handoff.md`.

## Tooling

- `scripts/validate_handoff_md.py <handoff.md>` checks required handoff sections.
- `scripts/validate_context_pack.py <context-pack.json>` checks required keys and enum values.
- `scripts/build_handoff_index.py <artifact_dir>` builds an evidence index from delivery artifacts.
