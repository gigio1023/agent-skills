# Context Pack Schema

Use this schema for `context-pack.json`.

## Contents

- [Status Vocabulary](#status-vocabulary-single-source-of-truth)
- [Top-Level Shape](#top-level-shape)
- [Continuation Mode](#continuation-mode-runtime-agnostic)
- [Constraints](#constraints)

## Status Vocabulary (single source of truth)

These two closed sets are the ONLY allowed status values across this skill. `handoff.md`, `context-pack.json`, both templates, and the validators all point here. Do not re-list or invent alternates elsewhere.

- Per-task status (`tasks[].status`, handoff objective rows): `not_started | in_progress | blocked | done`.
- Overall handoff status (`status` field, top-level handoff state): `complete | partial | blocked`.

Notes:

- Use `not_started` for work not yet begun. `todo` is not an allowed value (was a prior drift; standardized to `not_started`).
- The per-task set and the overall set are distinct. A handoff can be `partial` overall while individual tasks are `done`.

## Top-Level Shape

```json
{
  "session_id": "string",
  "timestamp_utc": "ISO-8601",
  "objective": "string",
  "status": "complete | partial | blocked",
  "artifacts": {
    "plan": "path-or-null",
    "progress": "path-or-null",
    "result": "path-or-null"
  },
  "tasks": [
    {
      "id": "string",
      "title": "string",
      "status": "not_started | in_progress | blocked | done",
      "owner": "string-or-null",
      "blocked_by": ["string"],
      "next_action": "string",
      "verification_refs": ["verification-id"]
    }
  ],
  "risks": [
    {
      "id": "string",
      "description": "string",
      "impact": "low | medium | high",
      "mitigation": "string"
    }
  ],
  "decisions": [
    {
      "id": "string",
      "decision": "string",
      "reason": "string",
      "date_utc": "ISO-8601"
    }
  ],
  "verification": [
    {
      "id": "string",
      "name": "string",
      "result": "pass | fail | unknown",
      "evidence": "string"
    }
  ],
  "next_actions_top3": [
    "string",
    "string",
    "string"
  ],
  "continuation": {
    "continuation_mode": "parallel_recommended | sequential_sufficient",
    "recommended_roles": ["string"],
    "writer_ownership": ["string"],
    "parallel_tracks": ["string"],
    "serialization_gates": ["string"]
  }
}
```

## Continuation Mode (runtime-agnostic)

`continuation.continuation_mode` describes the SHAPE of the remaining work, not a specific runtime feature:

- `parallel_recommended`: work splits into independent streams that benefit from parallelism. The successor should probe for the harness's native parallel-execution capability first and use it aggressively if present; if none exists, run the streams sequentially and say so.
- `sequential_sufficient`: a single linear session is the most effective path. No parallel split is needed.

This is a recommendation, not a hard requirement to spawn anything. The main
skill routes the agent to the separate continuation decision procedure.

## Constraints

1. `status` must match the handoff quality status in `handoff.md`. Both use the overall set in [Status Vocabulary](#status-vocabulary-single-source-of-truth).
2. Verification IDs are unique. Every `tasks[].verification_refs` value resolves
   to an entry in `verification`.
3. A task with `status: "done"` has at least one referenced verification whose
   result is `pass` and whose `evidence` is non-empty. The matching Completed row
   in `handoff.md` uses the same task ID and verification IDs.
4. Every substantive Completed row in `handoff.md` maps to a `done` task and one
   or more passing verification entries. A generic unrelated pass is not
   sufficient evidence for another completed claim.
5. If essential evidence is missing, do not use `complete`; downgrade to
   `partial` or `blocked`.
6. When the work is multi-track, `recommended_roles` and `writer_ownership` must be non-empty so the successor can split safely. Single-track work may leave them empty. This check keys off the actual work shape, not the `continuation_mode` value. Multi-track is detected from the data: two or more entries in `continuation.parallel_tracks`, OR two or more distinct non-null `tasks[].owner` values.
7. Keep unknowns explicit in `tasks`, `risks`, or `decisions` rather than hiding uncertainty.
