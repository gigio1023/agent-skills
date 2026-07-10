# Reporting Contract (`progress.md` / `task.md`)

Track current execution state without turning each tool call into a diary.

## File and Status Rules

`progress.md` is preferred. If the workspace uses `task.md`, treat it as the
same artifact and keep only one authoritative copy.

Workstream status is one of:

- `todo`: defined but not started;
- `in_progress`: active work with a next action;
- `blocked`: cannot proceed until a named condition changes;
- `done`: completed with verification evidence.

## Update Triggers

Update when execution starts, a status or blocker changes, a milestone lands,
scope/priority changes, or immediately before closure. Do not update only to
record routine reads or commands that did not change state.

Each update records UTC timestamp, workstream, owner, status, meaningful delta,
blocker if any, evidence, and next action. Use the compact initialized template.

## Consistency Gate

- One current row exists per workstream.
- `done` rows cite inspectable evidence.
- Dependency changes are reflected before dependent work starts.
- The final progress state and `result.md` do not conflict.
