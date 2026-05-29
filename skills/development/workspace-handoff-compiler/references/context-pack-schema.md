# Context Pack Schema

Use this schema for `context-pack.json`.

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
      "status": "todo | in_progress | blocked | done",
      "owner": "string-or-null",
      "blocked_by": ["string"],
      "next_action": "string"
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
  "swarm_continuation": {
    "mode": "swarm_required | single_agent_allowed",
    "recommended_roles": ["string"],
    "writer_ownership": ["string"],
    "parallel_tracks": ["string"],
    "serialization_gates": ["string"]
  }
}
```

## Constraints

1. `status` must match the handoff quality status in `handoff.md`.
2. If a claim is completed in `handoff.md`, there should be a related entry in `verification`.
3. If essential evidence is missing, do not use `complete`; downgrade to `partial` or `blocked`.
4. If mode is `swarm_required`, role and ownership arrays must be non-empty.
5. Keep unknowns explicit in `tasks`, `risks`, or `decisions` rather than hiding uncertainty.
