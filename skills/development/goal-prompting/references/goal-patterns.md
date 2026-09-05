# Goal Patterns

Use this reference when the goal needs domain-specific completion evidence or a file-backed contract.

## Match Proof To The Claim

- Bug: reproduce the failure, apply the fix, then show the same check passing and a relevant regression check.
- Tests or build: name the focused command and required exit or summary signal.
- Performance: name metric, threshold, method, environment, and run count.
- Migration: name the required new state, the absence check for legacy state, and behavior-preserving validation.
- UI: combine a feature checklist with rendered evidence at named states or viewports and a human gate when visual judgment remains subjective.
- Research: name the decision the work must enable, source scope, evidence standard, citations, and the final artifact.
- Operations: name healthy state, observation window, failure threshold, rollback boundary, and escalation trigger.

Do not use `git status is clean`, the entire test suite, a fixed number of checks, or a universal anti-cheat list by default. Add a preservation clause only for a shortcut that could plausibly fake this task's success, such as weakening the exact tests used as proof.

## File-Backed Contracts

Keep the direct goal concise. When necessary detail would exceed the target's limit or the task benefits from a reviewable spec, place details in a user-owned plan or goal file and make the direct payload point to it.

Write or modify that file only when the user explicitly requested a file artifact or authorized local changes. Otherwise return proposed contents for the user to place in a file, or reference an existing file without changing it.

The direct payload must still state the terminal outcome, decisive evidence, and critical boundaries. A referenced file supplies execution context; it does not prove completion. Require the worker to surface the final checks and results in the conversation so the completion decision has visible evidence.

Add a progress ledger, per-item statuses, checkpoints, or a resume protocol only when the task is large enough to benefit. Do not manufacture a project-management system for a bounded goal.

For a finite collection, use a source of truth and terminal states only when they make the stop condition easier to judge. Define how unknown items are discovered before execution if the collection is not yet enumerable. Do not let “deferred” count as completed work unless the user explicitly accepts it as a terminal outcome.

## Research And Subjective Work

Research goals should end in a decision, comparison, or evidence-backed artifact rather than “research thoroughly.” State the current-source requirement when facts may change and distinguish reported facts, inference, and unknowns.

For design, writing, or other taste-shaped work, combine objective requirements with a reference, rubric, rendered artifact, or user review gate. Do not invent a numeric score or refuse all qualitative goals merely because one command cannot judge the whole result.
