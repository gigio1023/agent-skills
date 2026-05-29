# Handoff Contract (`result.md`)

## Intent
`result.md` is the closure and transfer artifact for completed or paused delivery sessions.

## When Required
- Session completion.
- Ownership transfer to another worker/team.
- Planned pause with remaining actionable work.

## Required Sections
1. Summary
- One-paragraph outcome statement against the objective.

2. Completed Outcomes
- What is fully delivered and accepted.

3. Evidence
- Commands, checks, or artifacts that support completion claims.

4. Pending Items
- Unfinished work with explicit owner and priority.

5. Risks and Decisions
- Active risks, accepted tradeoffs, and decisions made.

6. Next Minimal Actions
- Smallest actionable next steps for the next operator.

7. Handoff Status
- `complete`, `partial`, or `blocked` with reason.

## Template
```markdown
# result.md

## Summary
- ...

## Completed Outcomes
- ...

## Evidence
- ...

## Pending Items
- Item: ... | Owner: ... | Priority: ...

## Risks and Decisions
- Risk: ...
- Decision: ...

## Next Minimal Actions
1. ...
2. ...

## Handoff Status
- partial (reason: ...)
```

## Quality Checklist
- Claims are backed by evidence.
- Pending work has explicit ownership.
- Next actions are minimal and executable.
- Status label matches actual completion level.
