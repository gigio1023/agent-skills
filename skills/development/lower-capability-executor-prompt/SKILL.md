---
name: lower-capability-executor-prompt
description: >
  Use only when the user explicitly invokes lower-capability-executor-prompt to
  turn an already researched and approved plan into a bounded prompt for
  an executor less capable than the planner. Covers scoped changes, test, build,
  and check runs, reproductions, and read-only evidence collection. Requires
  exact scope, actions, authority, capability assumptions, evidence, and stop
  rules. NOT for automatic invocation, model/cost/executor recommendations,
  peer or high-capability executors, discovery, planning, open-ended work, or
  general session handoffs.
---

# Lower-Capability Executor Prompt

Turn a finished plan into a narrow execution contract for a model that is less
reliable than the planner at task execution, recovery, context handling, or scope
control. Reduce its judgment surface; keep unresolved decisions with the planner.

## Invocation Policy

Use this skill only when the user explicitly invokes it to build the bounded
prompt. Model names, cost preferences, executor recommendations, and discussion
or edits to this skill do not invoke it. Do not auto-apply it to a handoff. Do
not use it for a peer or high-capability executor that can safely
inherit open judgment. Use `handoff-prompt` for successor-ready session
transfers.

## Quick Path

1. Require the planner to supply:
   - one observable outcome and task mode;
   - the approved procedure and supporting evidence or prerequisites;
   - exact files, commands, inputs, sources, and working locations in scope;
   - permitted mutations, external effects, generated artifacts, and retries;
   - invariants and facts that must remain unchanged;
   - the executor's known limits and decisions it may make independently;
   - expected evidence, acceptance criteria, and stop conditions.
2. If a field is missing or contradictory, return a short missing-information
   list. Do not guess, broaden scope, or delegate unfinished investigation.
3. Select `change`, `run`, `inspect`, or an explicitly ordered `mixed` mode.
4. Write one prompt from `assets/execution-prompt.template.md`; remove sections
   that do not apply instead of leaving empty placeholders.
5. Resolve every choice the executor cannot handle reliably. It may check the
   packet against current reality but must not reopen the plan.
6. Separate preflight, execution, evidence collection, and final reporting. If
   preflight matches, continue without a routine approval pause.
7. Return the copy-ready prompt plus only the assumptions the planner must
   resolve before use.

Read `references/prompt-patterns.md` for mode-specific scope patterns, stop
reports, and examples.

## Handoff Gate

A valid packet answers these without new product, architecture, or recovery
judgment:

| Field | Required content |
| --- | --- |
| Outcome | One observable result, artifact, or evidence packet |
| Mode | `change`, `run`, `inspect`, or an ordered combination |
| Basis | Approved decision, procedure, reproduction, or named prerequisite |
| Scope | Exact files, symbols, commands, inputs, sources, and locations |
| Authority | Permitted writes, side effects, retries, credentials, and external actions |
| Procedure | Ordered actions and the choices already resolved by the planner |
| Preservation | Contracts, state, data, formatting, or environment to keep unchanged |
| Executor profile | Relevant limits in execution, recovery, context, or scope control |
| Evidence | Expected outputs, exit states, artifacts, diffs, or cited observations |
| Stop conditions | Mismatches that must return to the planner |

“Investigate and handle it” is not a packet. If the executor must discover the
procedure, choose the fix, or decide how to recover, planning is unfinished.

## Task Modes

| Mode | Scope contract | Completion evidence |
| --- | --- | --- |
| `change` | Allowed files and symbols, exact edits, permitted generated files | Diff, changed-file audit, supplied checks |
| `run` | Exact commands, working directory, inputs, environment assumptions, retries | Command, exit status, relevant output, artifacts |
| `inspect` | Named sources and questions, read-only boundary, evidence format | Cited observations and explicit unknowns |
| `mixed` | Ordered modes with a separate authority boundary for each phase | Evidence from every phase and cumulative side effects |

For `run`, a failed test or check is a result, not permission to diagnose or edit.
For `inspect`, no mutation is allowed unless a later phase grants it explicitly.

## Prompt Rules

### Lead With the Optimization Target

For changes, open with:

```text
Do not optimize for completing the request as broadly as possible.
Optimize for the smallest correct and verifiable change.
```

For non-mutating work, replace the second line with:

```text
Optimize for the smallest authorized execution that produces the required evidence.
```

Then state one outcome. Do not repeat it later.

### Make Scope and Authority Mechanical

- For `change`, provide exclusive file and symbol allowlists.
- For `run`, provide exact commands, working directory, allowed retries, and
  whether generated artifacts may remain.
- For `inspect`, name allowed sources, questions, and the read-only boundary.
- For `mixed`, state where each phase begins and whether its authority changes.

Write operational limits, not model stereotypes. Prohibit only relevant failure
modes: unplanned edits, extra commands, dependency or configuration changes,
test weakening, destructive actions, secret access, or external writes.

### Treat the Plan as Fixed Input

Require a preflight consistency check against named evidence and prerequisites.
If it matches, continue. Do not ask the executor to redesign, investigate adjacent
issues, choose alternatives, or improvise recovery. Unexpected results belong in
the report unless a supplied branch or bounded retry covers them.

### Use One Short Execution Loop

1. Preflight: confirm prerequisites, scope, authority, and current state.
2. Execute: perform only the supplied actions.
3. Collect evidence: capture the required outputs, artifacts, diffs, or findings.
4. Report: show results, side effects, assumptions, deviations, and unknowns.

If a required tool or check is unavailable, report it. Do not install packages,
change configuration, access new credentials, or invent infrastructure unless the
packet explicitly authorizes that action.

### Stop on Authority or Plan Mismatches

Stop before the affected action when:

- a prerequisite or approved basis contradicts current reality;
- completion requires a file, command, source, credential, or side effect outside
  the stated scope;
- a destructive or external action lacks explicit authority;
- an unexpected mutation or overlapping user change cannot be preserved;
- the supplied procedure has no defined branch for a result requiring judgment.

Name the mismatch, evidence, work already performed, and smallest missing
decision or authority expansion.

## Output Contract

Return one copy-ready execution prompt containing the outcome, mode, approved
basis and procedure, scope, authority, preservation rules, preflight, evidence,
stop conditions, and final report fields. Do not execute the task, rank models,
add alternative plans, or create a synthetic evaluation.

## Reference Files

| File | Read when | Content |
| --- | --- | --- |
| `references/prompt-patterns.md` | Building or reviewing a bounded handoff | Packet, mode scopes, stop report, examples, and failure patterns |
| `assets/execution-prompt.template.md` | Producing the final prompt | Copy-ready multi-mode execution template |

## Gotchas

- Do not call the executor “stupid” or “weak”; state task-relevant limits.
- Do not infer lower capability from model size, speed, or price alone.
- Do not use this skill for a peer or high-capability executor merely because a
  handoff is occurring.
- Do not turn a failing test run into an unauthorized bug-fix task.
- Do not treat command completion as success when exit status, evidence, or
  expected artifacts are missing.
- Do not let the executor expand its own scope to make recovery easier.
