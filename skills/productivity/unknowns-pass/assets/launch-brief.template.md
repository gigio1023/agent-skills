# Launch Brief: [topic]

Paste this into a fresh session to start execution.

## Starting Point

- User's familiarity: [domain and codebase/artifact familiarity in one line]
- What already exists: [files, artifacts, prior decisions, evidence]

## Confirmed Decisions

| Decision | Rationale | Source |
| --- | --- | --- |
| [decision] | [why it holds] | [user answer / technique result / inspection] |

## Resolved Unknowns

| Unknown | Resolution | Evidence |
| --- | --- | --- |
| [what was unknown] | [what was learned] | [path, reference, or artifact] |

## Open Items

| Item | Decide-later rule | Owner |
| --- | --- | --- |
| [open question] | [decide when / default if unresolved] | [user or agent] |

## Plan

Ordered with the most likely-to-change or hardest-to-reverse decisions first.

1. [step]
2. [step]

## During Execution

Keep [`implementation-notes.md` | `decision-log.md`]. When reality forces a
deviation, log: what the plan said → what reality revealed → the conservative
choice taken → when to revisit. Then keep going.

## Acceptance Criteria

[Executable work: the tests, builds, or renders that prove the result]
[Comprehension-checked work: the explainer plus scenario-based quiz the user
must pass before the irreversible step: <commit money / send / adopt / merge>]
