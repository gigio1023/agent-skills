---
name: work-plan
description: >
  Use only when the user explicitly asks to write or revise a plan file for chosen work, to execute or continue a plan file or a named part, to review project work against its intent, or to record or audit a project's durable context such as PROJECT.md: "write a plan file for this", "run the plan", "continue the plan", "review this against the plan", "계획 파일 써줘", "계획 이어서 해줘", "계획대로 됐는지 봐줘". Plans through the next decision for research, experiments, datasets, documents, and implementation. NOT for starting because a plan file exists or work looks large, automatic end-of-task review, ordinary task tracking, discovery before the goal is clear (find-unknowns, interview), session transfer files (session-handoff), design documents (design-doc), or worktree isolation (git-worktree-setup).
---

# Work Plan

A plan file carries chosen work across sessions: the user's goal and limits, what is currently understood, the next decision, and the work whose result informs it. This skill writes that file, advances the work, and reviews the result against the user's intent. Each mode opens only on its own explicit request, because an unwanted opening lands on disk or on the bill.

## Choose the mode

| Request | Mode | Read |
| --- | --- | --- |
| Write or revise a plan; names `gigio-write-plan` | write | [references/write.md](references/write.md) |
| Execute or continue a plan or a named part; names `gigio-execute-plan` | execute | [references/execute.md](references/execute.md) |
| Review work against its intent; names `gigio-review-results` | review | [references/review.md](references/review.md) |
| Record or audit durable project context without planning; names `gigio-project-setup` | context | [references/project-context.md](references/project-context.md) |

Load only the reference for the requested mode. A request for two modes, such as "plan this and run it", runs them in order under the same grant without asking for the second half again. Finishing one mode does not open the next: a planning request ends at the plan, and a finished round does not start a review, a commit, or a publication.

Plan files written from earlier templates name `gigio-execute-plan` or `gigio-write-plan` in their header; those names mean execute and write mode here, and the file needs no rewrite to be usable. The header line is not itself a request: a plan file starts nothing until the user asks to execute, revise, or review it.

## Rules every mode keeps

- **The user owns direction; the agent maintains understanding.** Keep accepted goals and limits in recognizable user wording, separate from the agent's observations and interpretations. Label a planner proposal that could change intent or authority until the user accepts it; work resting on it stays visibly unconfirmed.
- **Plan to the next decision.** Detail the work whose result changes the next decision. Later possibilities stay short alternatives or open questions; known implementation dependencies remain valid.
- **Raise direction problems when they appear.** A finding that challenges the goal, question, success criterion, or consequential scope goes to the user promptly, with the observation and the proposed change, before any work follows a different direction. Work that does not depend on it continues.
- **Ask before long new work.** Fast follow-up within the same question and permitted resources proceeds. A long new activity, such as two to three days or more, needs the user's decision unless that activity was already authorized. Duration does not replace limits on cost, data, external writes, or shared resources.
- **Inspect the sources the current action depends on.** Check the actual state of results, data and model versions, changed files, and live jobs before acting on them. A named input is not replaced by a similar one, and rerunning historical checks that cannot affect the current action is not required.
- **Match verification to the claim.** A run of the real entry point on fixed input, plus the tests the project keeps, for implemented behavior, logs and outputs for run completion, source inspection for a review finding, justified comparison for an interpretation. A negative or inconclusive result can finish a bounded investigation, and an unavailable check leaves a result unverified.
- **Partition shared writes before parallel work.** Settle who writes which files, output locations, or shared resources, and who owns each live job, before work runs in parallel.
- **Delegation follows the user's choice.** An explicit user choice about delegation governs; without one, the lead decides. Delegation adds no authority beyond the existing grants.

Read [references/project-context.md](references/project-context.md) when the work spans repositories or sessions and no instruction file or maintained intent document already carries the project's purpose, direction, constraints, current understanding, next question, and resource locations, or when the user asks to record or audit that context.

## Neighbors

Use `find-unknowns` to surface the problems, goals, and constraints neither side has noticed before the goal is clear, and `interview` when the user wants sustained questioning. `design-doc` owns research and system design documents; a plan that serves a design links it instead of copying it. `session-handoff` writes a transfer file a successor executes; the plan file stays the durable record of the work. `orchestrate-subagents` carries dispatch defaults for parallel workers, `git-worktree-setup` isolates implementation checkouts, and `small-model-handoff`, when installed, bounds a weaker executor on an approved plan.
