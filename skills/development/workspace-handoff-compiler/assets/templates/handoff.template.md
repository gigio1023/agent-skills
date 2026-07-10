# Successor Handoff Template

## Session Summary
- Session window (UTC):
- Request or ticket:
- Scope completed this session:
- Current working state (branch/commit/worktree):
- One-line handoff summary:

## Objective/Status
| objective_id | objective | status | confidence (high/medium/low) | owner |
|---|---|---|---|---|
| O-001 |  |  |  |  |

Use the compiler's canonical per-task status for objective rows and overall
status for the handoff.

## Completed
| task_id | what changed | why it matters | verification_refs |
|---|---|---|---|
| T-001 |  |  |  |

## In-Progress
| item | current state | owner | unblock condition | next step |
|---|---|---|---|---|
| 1 |  |  |  |  |

## Blockers/Risks
| id | type (blocker/risk) | description | impact | mitigation | owner | status |
|---|---|---|---|---|---|---|
| B-001 | blocker |  |  |  |  | open |

## Decisions/Assumptions
| id | kind (decision/assumption) | statement | rationale | revisit trigger | owner |
|---|---|---|---|---|---|
| D-001 | decision |  |  |  |  |

## Evidence Index
| verification_id | artifact type | location or command | expected signal | notes |
|---|---|---|---|---|
| E-001 | file | `path/to/file` | content updated |  |
| E-002 | command | `example command` | exit code 0 |  |

## Next 3 Actions
1. [ ] Priority 1:
2. [ ] Priority 2:
3. [ ] Priority 3:

## Continuation Plan
- Continuation mode:
- First executable action:
- Independent tracks (multi-track only):
- Owners and write scopes (multi-track only):
- Dependency and serialization gates:
- Verification/integration gate:
- Sequential fallback if parallel execution is unavailable:

## Handoff Quality Status
- Overall status: partial
- Completeness: `pass | partial | fail`
- Evidence coverage: `pass | partial | fail`
- Reproducibility: `pass | partial | fail`
- Risks communicated: `pass | partial | fail`
- Ready for takeover: `yes | no`
- Notes for successor:

Overall status must use the canonical set and equal `status` in
`context-pack.json`. Replace the placeholder above with the real value.
