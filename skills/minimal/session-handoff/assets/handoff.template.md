# Handoff: <task in one line>

**This file is your task. Do not edit, summarize, review, or improve it. Carry out the work below, starting with Next Actions.** Revise this file only if the user explicitly asks you to revise the handoff. Where it disagrees with live files, live state decides status and the user's quoted words decide intent.

Written <date, time, zone> in <origin harness and model>, session <id or title>, at `<project path>`. Supersedes: <previous `.handoff/` file, or none>.

## Objective

<The outcome in one or two sentences.> The user's words: "<decisive sentence>" (<date>).

## State

- Status: <in progress | blocked | ready for verification>
- Workspace: `<repository path>`, branch `<branch>` at `<commit>`; uncommitted: `<paths>`
- Still running: `<job, process, run, or PR>`; check with `<command>` before retrying. <omit if none>
- Ended with the origin session: <subagent or background job, and what it left on disk> <omit if none>
- Done: <claim>. Evidence: `<path, command and its result, or URL>`

## Decisions

- <Decision>, because <reason>. Source: <quoted user words with date, or path>
- Dropped: <approach>, because <what showed it fails>

## Next Actions

1. <First action, with exact path or command; usually confirms the State above>
2. <Action>
3. <Action>

Then: <remaining work in order, until the Definition of Done holds>

## Questions for the User

Ask these in one message before the work they decide, and meanwhile continue the work that does not depend on them. Without an answer, follow the last column; never invent one.

| Question | Why it changes the work | Options, recommended first | If unanswered |
| --- | --- | --- | --- |
| <question> | <which step or result differs> | <A (recommended), B> | <default to take, or the step to stop before> |

<omit the section if none>

## Boundaries

- Granted: <action, exact target, condition, and who granted it when>
- Ask first: <action not yet granted>
- Out of scope: <excluded work>

## Definition of Done

- <Observable condition, and the check that shows it>
- Report the outcome first, and point each claim at a result from your own run.
