---
name: workspace-handoff-compiler
description: >-
  Use when a work session is ending and a successor agent must continue it, or
  when the user asks for a handoff, context pack, session handoff, "continue
  across sessions", "인계", "이어서 작업", or "다음 AI에게 넘겨줘". Compiles
  prior artifacts and live repository evidence into `handoff.md` plus
  `context-pack.json`, resolving conflicts by source priority and refusing
  unsupported completion claims. NOT for producing plan/progress/result
  artifacts during active delivery (use workspace-delivery-orchestrator).
---

# Workspace Handoff Compiler

Produce a successor-ready `handoff.md` and `context-pack.json` that agree on
status, distinguish evidence from inference, and identify the first executable
next actions. Do not turn the handoff into a session transcript.

## Quick Start

1. Gather `plan.md`, `progress.md` or `task.md`, `result.md`, relevant logs, and
   current repository state. Use `scripts/build_handoff_index.py <artifact_dir>`
   when the artifact set is not obvious. If both status aliases exist, the index
   surfaces both with hashes and timestamps and leaves progress unselected until
   you resolve authority; never treat its readiness hint as true in that state.
2. Resolve discrepancies with `references/handoff-source-priority.md`. Record a
   conflict only when the precedence and tie-break rules cannot resolve it.
3. Apply `references/handoff-quality-gate.md`. A completion claim needs a file,
   command, test, or other inspectable evidence reference.
4. Choose continuation shape with `references/continuation-mode.md`. Default to
   one sequential path unless multiple remaining tracks are genuinely
   independent and parallel work would save more than it costs.
5. Fill both templates:
   - `assets/templates/handoff.template.md`
   - `assets/templates/context-pack.template.json`
6. Run all three validators. Fix the artifacts until every command exits 0:

   ```bash
   python3 scripts/validate_handoff_md.py <handoff.md>
   python3 scripts/validate_context_pack.py <context-pack.json>
   python3 scripts/validate_handoff_parity.py <handoff.md> <context-pack.json>
   ```

7. Deliver both paths, overall status, evidence gaps, and the first next action.

## Evidence and Status Contract

The only status vocabularies and the JSON shape live in
`references/context-pack-schema.md`. Do not invent synonyms or duplicate the
sets elsewhere. The overall status in both outputs must match.

- Facts cite their source.
- Inferences are labeled and include the evidence that supports them.
- Unknowns state what proof is missing and whether it blocks continuation.
- A completed task and its handoff Completed row share the same task ID and
  verification IDs; at least one referenced verification passes with non-empty
  evidence.
- Missing or conflicting decisive evidence lowers the overall status; prose
  confidence cannot substitute for proof.

When no delivery artifacts exist, compile from live repository evidence such
as `git status`, `git diff`, commit history, and changed files. Conversation
memory may fill context only when labeled unverified. A cold handoff cannot be
`complete` until evidence supports it.

## Continuation Contract

`continuation_mode` describes the remaining work, not a required agent or
runtime mechanism. For multi-track work, include independent tracks,
dependencies, writer ownership, serialization gates, and recommended roles.
For single-track work, keep those fields minimal or empty.

If the recommended execution capability is unavailable, preserve the same
dependency and ownership map and execute the tracks sequentially. Do not add
model-specific routing advice to this skill.

## Output Contract

`handoff.md` must make the objective, completed and remaining work, blockers,
risks, evidence, and next actions understandable without the prior conversation.
`context-pack.json` must encode the same state, ownership, dependencies,
verification, and continuation shape using the schema reference.

Keep required facts, caveats, ownership, and actions; trim exhaustive history,
generic encouragement, and duplicate summaries. A successor should be able to
start the first action without re-investigating the entire session.

## Tooling

All scripts use Python 3 standard library only and paths are relative to this
skill directory:

- `scripts/build_handoff_index.py <artifact_dir>` summarizes available delivery
  artifacts; `--dir <artifact_dir>` is also accepted. It reports both status
  candidates and a conflict/selection flag instead of silently preferring one.
- `scripts/validate_handoff_md.py <handoff.md>` checks required sections.
- `scripts/validate_context_pack.py <context-pack.json>` checks keys, types, and
  enums.
- `scripts/validate_handoff_parity.py <handoff.md> <context-pack.json>` checks
  status parity and task-specific evidence for completed claims.
- `scripts/smoke_test.sh` exercises valid output plus unsupported-claim and
  divergent-status negative fixtures.

## Reference Files

| File | Read when | Content |
| --- | --- | --- |
| `references/handoff-source-priority.md` | Gathering or reconciling sources | Evidence precedence and conflict resolution |
| `references/handoff-quality-gate.md` | Assigning overall status | Required checks and anti-fabrication rule |
| `references/context-pack-schema.md` | Creating or validating either output | Canonical statuses, JSON shape, and constraints |
| `references/continuation-mode.md` | Describing remaining execution shape | Independence test, ownership fields, and sequential fallback |

## Gotchas

- Do not paste contradictory documents side by side. Resolve them or surface
  the specific unresolved conflict and its consequence.
- Do not mark work done from a hopeful plan, memory, or the presence of changed
  files. Cite outcome evidence.
- A validator passing proves structure, not factual truth. Recheck decisive
  claims against source evidence.
- Do not default the template to parallel work. Use `parallel_recommended` only
  after the remaining tracks pass the independence test.
- Never let `progress.md` and `task.md` silently represent different states;
  select the authoritative source and record the conflict if needed.
