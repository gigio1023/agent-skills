# Handoff Quality Gate

Use this gate before publishing `handoff.md` and `context-pack.json`.

## Required Checks

1. Objective clarity  
   - primary objective and success criteria are explicit.
2. Evidence coverage  
   - each completed row names its `task_id` and one or more verification IDs.
   - the same task is `done` in `context-pack.json`, and each referenced
     verification is `pass` with non-empty evidence.
3. Remaining scope  
   - open tasks are actionable and ordered.
4. Dependency and blocker visibility  
   - external dependencies and blockers are listed with owner.
5. Continuation readiness  
   - first executable next action is present.
6. Status consistency  
   - `handoff.md` and `context-pack.json` status match.

## Status Rules

- `complete`:
  - all required checks pass.
  - no unresolved conflicts affecting outcome.
  - no missing evidence for completion claims.
- `partial`:
  - useful progress exists, but at least one required check fails.
  - or evidence is missing for one or more completion claims.
  - or unresolved conflicts exist without hard stop.
- `blocked`:
  - continuation cannot proceed due to hard dependency or unresolved critical conflict.
  - required next action depends on unavailable external input or access.

## Anti-Fabrication Rule

- Never output `complete` based on assumption, memory, or inferred success.
- If proof is missing, downgrade to `partial` or `blocked` and enumerate missing evidence.
- An unrelated passing check does not prove another task. Keep verification IDs
  claim-specific in both output files.
