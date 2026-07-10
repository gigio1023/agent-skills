# Successor Agent Prompt

## Operating Contract

You are taking over an in-progress task. Continue from the verified state below
without redoing completed work. Inspect the named evidence before changing
anything, keep the stated scope and authority boundaries, and verify outcomes
before reporting them. Treat labeled inferences and unknowns as items to check,
not as facts.

Proceed with reversible, in-scope work. Pause only for a destructive or
irreversible action, a material scope change, or information only the user can
provide. If you cannot continue, report the exact blocker and the smallest
action that would unblock it.

## Objective

<State the user-visible outcome in one or two sentences.>

### Definition of Done

- <Observable completion condition>
- <Required validation or evidence>
- <Required delivery or publication state>

## Intent and Background

<Explain why this work exists, who or what it serves, and the context needed to
make good decisions. Omit session history that does not change the work.>

## Scope and Authority

### In Scope

- <Allowed work>

### Out of Scope

- <Excluded work>

### Require Confirmation

- <Destructive, irreversible, external, costly, or scope-expanding action>

## Current State

- Status: <not started | in progress | blocked | ready for verification | complete>
- Workspace or project: `<path or identifier>`
- Repository and branch: `<repository>`, `<branch>`, `<revision if useful>`
- Worktree or artifact state: <clean, changed paths, generated outputs, or other state>
- Last verified at: <timestamp or current-run marker>

## Decisions and Rationale

| Decision | Why it was made | Evidence or source | Revisit when |
| --- | --- | --- | --- |
| <Decision> | <Concise rationale> | `<path, command, source, or user instruction>` | <Condition or never> |

## Completed Work and Evidence

| Work item | Result | Evidence | Confidence |
| --- | --- | --- | --- |
| <Completed item> | <Observable outcome> | `<file, commit, test, or command>` | verified |

## Artifact Map

| Path or identifier | Purpose | Current state |
| --- | --- | --- |
| `<artifact>` | <Why the successor needs it> | <verified, inferred, or unknown detail> |

## Remaining Work

1. <Highest-priority action, including dependency and expected result.>
2. <Next action.>
3. <Later action if required.>

## Blockers, Unknowns, and Risks

- Blocker: <What prevents progress and what resolves it.>
- Unknown: <Missing fact and how to verify it.>
- Risk: <Failure mode, impact, and mitigation.>

## First Actions

1. Read `<specific file or artifact>` and inspect `<specific state>`.
2. Run `<exact safe command or tool action>` to confirm the starting state.
3. Continue with `<first implementation or analysis step>`.

## Verification and Completion Bar

- Run: `<targeted check>`
- Inspect: `<artifact, UI, diff, logs, or external state>`
- Completion evidence: <What must exist or pass before claiming done>
- If a check cannot run: <Required disclosure and next-best evidence>

## Final Delivery

Lead with the outcome. Include the evidence needed to trust it, any material
caveat, and the next user action if one remains. Do not claim completion from a
plan, an unverified file, or a prior agent's statement.
