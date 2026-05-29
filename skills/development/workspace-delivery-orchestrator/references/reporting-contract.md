# Reporting Contract (`progress.md` / `task.md` alias)

## Intent
Track active execution state with low-latency updates so parallel streams stay coordinated.

## File Alias Policy
- Preferred file: `progress.md`.
- If the workspace uses `task.md`, treat `task.md` as an alias for the same artifact.
- Do not maintain divergent state across both names.

## Trigger Rules
Create or update the artifact when any event occurs:
- Execution starts.
- Status transition (`todo` -> `in_progress` -> `done`, or `blocked`).
- New blocker discovered or blocker resolved.
- Milestone completed.
- Scope or priority changes.
- Pre-handoff final status sync.

## Entry Requirements
Each update entry must include:
- Timestamp (UTC)
- Workstream ID/name
- Owner
- Status
- Brief delta (what changed)
- Blockers (if any)
- Next action

## Status Vocabulary
- `todo`: Defined but not started.
- `in_progress`: Actively being executed.
- `blocked`: Cannot proceed due to dependency or constraint.
- `done`: Completed and verified for this stream.

## Template
```markdown
# progress.md

## Current Snapshot
- Objective: ...
- Overall status: in_progress
- Last updated (UTC): 2026-01-01T12:00:00Z

## Workstreams
| Stream | Owner | Status | Blocked By | Next Action |
|---|---|---|---|---|
| WS1 | ... | in_progress | none | ... |
| WS2 | ... | blocked | WS1 | ... |

## Update Log
- 2026-01-01T12:00:00Z | WS1 | Owner: ... | Status: in_progress | Delta: ... | Blockers: none | Next: ...
- 2026-01-01T12:15:00Z | WS2 | Owner: ... | Status: blocked | Delta: ... | Blockers: WS1 | Next: ...
```

## Consistency Rules
- Keep one authoritative state per workstream.
- Reflect dependency changes immediately.
- Ensure `progress.md`/`task.md` and `result.md` do not conflict at handoff.
