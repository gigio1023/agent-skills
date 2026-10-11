---
name: gigio-execute-plan
description: >
  Use only when asked to execute or continue a plan file or a named part of it.
  Carries out the next useful work, interprets results, and updates the plan
  within the user's direction and resource limits. Supports research,
  experiments, datasets, documents, and implementation.
  NOT for starting work merely because a plan exists.
---

# Gigio Execute Plan

Advance the objective using the plan's current understanding and next decision. Execute, inspect the result, and choose the next bounded action within established scope. A plan guides the work; it does not make a contradicted assumption true.

## Re-enter from actual state

Read the goal, existing grants, current work, sources, and project context. Inspect relevant actual state before acting: results, data and model versions, changed files, or active jobs. A named task narrows this to the task and genuine prerequisites.

Older plans may use stage, needs, owns, acceptance, check, Results, and Run log. Read their meaning and preserve completed records. Use known dependencies for current execution; do not insist on rewriting a usable old plan or treating speculative later stages as settled research decisions.

Resolve discrepancies that can be checked. Preserve unrelated work. An unavailable checker remains unverified, and a missing input blocks the work that needs it. Do not substitute another dataset, model, or environment and present it as the named one. Before retrying a remote or long-running action, establish whether the original is still active.

## Execute and interpret

Perform the next analysis, experiment, review, or implementation. Use the relevant specialist's method: research-credo covers research questions, data, experiments, and evaluation; agent-skills covers implementation and harness tools. Load only the capability needed now. Do not prohibit a worker from reading relevant skills or sources.

Check the actual result rather than accepting a worker's completion claim. Record the finding and what it changes. A negative result, an excluded explanation, or a supported statement that available data cannot distinguish alternatives can complete an investigation. An input-format check does not establish that a model evaluation ran, and an inconclusive comparison does not establish equivalence.

Within the same question and permitted resources, perform quick diagnostics or follow-up work without asking for every small choice. Update the current plan and project understanding so the next session inherits the revised state. Keep earlier results and the reason for a changed action.

Bring a proposed change of research question, project goal, success criterion, or consequential scope to the user before acting on it. Present the observation, why the old approach is doubtful, the proposed next work, and expected cost or duration. Pause affected work; continue independent authorized work if useful. Do not defer a known direction problem to a final review while consuming resources on its invalid premise.

Ask before a long new activity, such as two to three days or more, unless the user already authorized that activity and its bounds. Also respect narrower project limits and material cost, shared-resource, or external-effect constraints. A fast action is not automatically authorized if it changes those boundaries.

## Coordinate workers

An explicit user choice about delegation governs, including whether to delegate, how many workers, and the budget. Without one, the lead decides. Once the direction is settled and the questions that would change the work are answered, dispatch the ready independent tasks through orchestrate-subagents, which carries the dispatch defaults and their limits. Keep work sequential where each step depends on the previous result. Give workers the objective, sources, task boundaries, relevant skills, expected result, existing grants, and the decisions already made, so they finish without routing routine questions back. Name project and plan paths without copying whole records. Delegation adds no authority beyond the existing grants.

Partition shared writes and live-job ownership before parallel work. Read-only workers can examine the same sources. Do not duplicate a running experiment because its original session lost a handle. The lead integrates findings and owns project digest and plan updates unless another owner is established.

Use git-worktree-setup for requested implementation isolation and the selected harness's real runtime mechanisms. These helpers live in agent-skills; their absence is not a reason to invent a framework. Use a supported direct route when sufficient.

## Verify progress and continue

Match verification to the claim. Use tests for implemented behavior, actual logs and outputs for run completion, source inspection for a review finding, and justified comparison for an interpretation. A read-only review needs no changed source file. A command exit code is not a substitute for interpreting its output.

Keep execution failures distinct from unwelcome research results. Retry only after a concrete correction or new information makes it useful, within remaining limits. Repeated identical failure calls for diagnosis or stopping, not spending the budget unchanged. Do not change the question merely to obtain a passing result.

Update existing records proportionally: what happened, what was learned, sources needed to check it, and the next decision. Keep raw attempts and operational state in their established records rather than duplicating them in the plan.

Continue in-scope work until the requested outcome, decision point, limit, or real blocker is reached. When requested, use gigio-review-results for review and the appropriate publication skill for delivery. Do not commit, publish, install, or start another workstream simply because a round finished.

Finish with the result, its support, any material unresolved question, and the next useful action. The whole project is not complete merely because the current round is complete.
