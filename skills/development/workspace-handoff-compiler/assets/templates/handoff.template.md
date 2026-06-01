# AI Handoff Template

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

Status values come from the single source in `references/context-pack-schema.md` (Status Vocabulary). Objective rows use the per-task set (`not_started/in_progress/blocked/done`); the overall handoff uses the overall set (`complete/partial/blocked`).

## Completed
| item | what changed | why it matters | evidence_ref |
|---|---|---|---|
| 1 |  |  |  |

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
| ref_id | artifact type | location or command | expected signal | notes |
|---|---|---|---|---|
| E-001 | file | `path/to/file` | content updated |  |
| E-002 | command | `example command` | exit code 0 |  |

## Next 3 Actions
1. [ ] Priority 1:
2. [ ] Priority 2:
3. [ ] Priority 3:

## Continuation Plan
See `references/continuation-mode.md` for the judgment rule and sequential fallback.
- Continuation mode (`parallel_recommended` or `sequential_sufficient`):
- If parallel_recommended, probe for a native parallel-execution capability first; if none, run sequentially and note it here:
- Owners and write scopes (multi-track only):
- Single-writer locks:
- Task dependency order:
- Parallelizable reads/verifications:
- Coordination checkpoint (time or trigger):
- Escalation rule if blocked:

## Handoff Quality Status
- Overall status: partial
- Completeness: `pass | partial | fail`
- Evidence coverage: `pass | partial | fail`
- Reproducibility: `pass | partial | fail`
- Risks communicated: `pass | partial | fail`
- Ready for takeover: `yes | no`
- Notes for next AI:

Overall status must be one of `complete/partial/blocked` and must equal the `status` in `context-pack.json`. Replace the placeholder above with the real value.
