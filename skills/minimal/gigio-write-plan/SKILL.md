---
name: gigio-write-plan
description: >
  Use only when asked to write or revise a plan file for chosen project work.
  Keeps the overall goal and current understanding while detailing only the
  work needed for the next decision, including research and experiments.
  NOT for execution, ordinary task tracking, or reopening settled intent.
---

# Gigio Write Plan

Create a plan a later session can use to make the next useful advance. Keep the overall direction visible; detail the next analysis, experiment, review, or implementation whose result changes the next decision. Do not manufacture a complete sequence when later steps depend on findings.

## Establish the basis

Read PROJECT.md or the existing intent document, current user instructions, and relevant results. Identify the next decision or desired result and why it matters. Recover facts before asking questions. Settle the questions whose answers would change the plan before detailing work, including consequential unknowns nobody has noticed yet, and ask them together rather than one at a time. Use find-unknowns when a bounded discovery pass or option map fits, and deep-interview only when the user wants sustained interviewing. Open empirical questions can be the work itself.

Preserve accepted goals and limits in recognizable user wording. Label a planner's new proposal only where it could change intent or authority. An unanswered question is not approval, but sufficient existing direction does not need another confirmation.

## Detail the next work

Use assets/plan-template.md under the user's chosen root, defaulting to .plans/<topic>.md. The root can be a research workspace, vault, or several repositories. Follow its established storage and visibility policy; do not silently add a Git exclusion or a competing tracking system.

Bound the current round by the next decision. State the question, relevant known facts, important assumptions, selected action, expected information, how to assess the result, and when to reconsider. Later possibilities can remain short alternatives or open questions rather than scheduled tasks.

A result can justify proceeding, reject an explanation, reveal insufficient information, or require a change in direction. Make that distinction visible before execution. Do not demand a predicted finding, code output, or pass/fail command when the work calls for judgment.

For implementation, dependencies and checks may be known in advance. For research, record dependencies that are real now. Use task IDs when actions need separate ownership; preserve existing IDs. Stage numbers are optional scheduling aids. Resolve shared-write conflicts before simultaneous execution, rather than assigning all future findings at planning time.

Name paths or resources to be changed where ownership matters. A read-only comparison can name its sources and result location; it needs no artificial edit. A run names inputs, resource limits, and existing output records. Do not copy code bodies, raw logs, or an entire literature collection into a plan.

## Carry authority and continuity

Record existing grants for targets, data, compute, budget, publication, and consequential actions. Fast follow-up checks within the same question and permitted resources may be chosen during execution. Ask before a direction change or a long new activity, such as work expected to take two to three days or more, unless that exact activity was already authorized. Short duration alone does not authorize paid services, private-data transfer, or a new external write. Apply tighter project limits when present; consider cost and disruption as well as elapsed time.

Link source records and versions whose changes would invalidate this round. A commit, dataset revision, model checkpoint, document version, or observed live state may be appropriate. Do not require hashes or rerunning every historical check when they cannot affect the current action.

Use existing experiment and research records. The plan coordinates work and decisions; it is not the only permissible place for state.

## Deliver

Provide the saved path, first useful action, and any material proposed intent awaiting a decision. A planning-only request ends at the plan. If execution was requested too, continue through gigio-execute-plan under the same grant.

When revising a plan, preserve earlier results and the reason for a changed action while updating upcoming work. The next session should see the current plan immediately without reconstructing it from an append-only history.
