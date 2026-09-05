# Claude Code Goals

Use this reference when the target is Claude Code or when translating a goal into or out of Claude Code.

## Current Contract

Claude Code's `/goal` sets one completion condition for the current session and starts a turn immediately. After each turn, a separate small evaluator model reads the condition and conversation. A negative decision starts another turn; a positive decision clears the goal as achieved.

The command requires Claude Code v2.1.139 or later. It is user-entered session input rather than an agent-callable goal-state API. When another agent authors a Claude Code goal, it should return a ready-to-submit `/goal` command and must not claim that the target session changed.

The evaluator does not run commands or read files. It can judge only evidence that Claude has surfaced in the conversation. Write completion conditions so the transcript can demonstrate them.

An effective condition normally includes:

- one measurable end state;
- a stated check and expected signal;
- constraints that must remain true.

The condition may be up to 4,000 characters. A turn or time clause can bound the run, such as `or stop after 20 turns`, but a bound is optional rather than a universal completion criterion.

## Draft Shape

```text
/goal <measurable end state>, proven by <command or observable check and its expected signal>, while preserving <critical constraints>. Report the actual evidence in the conversation. Stop and ask if <real blocker or approval gate>.
```

Keep the condition falsifiable. Pin a command or path only after confirming it is appropriate for the project. For qualitative work, define an inspectable rubric or human approval gate instead of pretending subjective quality is a binary command result.

## Evaluator Visibility

A plan, issue, or goal file can guide the worker but the evaluator cannot open it independently. If the goal references a file:

- require Claude to read it as execution context;
- keep the terminal condition in the direct goal text;
- require the final response to surface the acceptance checklist and observed evidence;
- never claim that the evaluator “re-reads the file.”

The same rule applies to tests and builds: the evaluator sees reported command and output evidence in the conversation, not the workspace or process itself.

## Operating Boundaries

Goal mode does not grant additional tool permissions. Default permission rules still apply. Unattended operation may require separately configured permission behavior, which a goal prompt must not assume or authorize.

An active goal can be inspected or cleared with the native command. An active goal restored with a resumed session keeps its condition, while turn, timer, and token-spend baselines reset. Goal mode also depends on the trusted-workspace and hooks configuration documented by Claude Code.

## Claude-Specific Checks

- Could a convincing summary pass without the underlying work? Require the actual command name, result signal, artifact, or review evidence.
- Could the named check be gamed by weakening the exact test, benchmark, or source set? Add only the relevant preservation clause.
- Can the evaluator distinguish partial progress from the terminal outcome?
- Does an optional bound stop the run honestly without being mistaken for successful completion?
- Are approvals and blockers allowed to interrupt “autonomous” work?

## Translation From Codex

Preserve outcome, context, constraints, and verification. Rewrite verification so the worker must surface the evidence in the conversation. Remove Codex goal state, token-budget, and completion-status assumptions. Add a turn or time bound only when the user wants one or the risk calls for a proposed bound.
