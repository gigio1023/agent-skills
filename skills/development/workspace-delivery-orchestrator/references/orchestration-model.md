# Orchestration Model

Choose the smallest execution shape that delivers the outcome safely.

## Independence Test

Run streams in parallel only when all hold:

- each stream has a distinct outcome and can make useful progress now;
- writer paths are disjoint, or a serialization gate protects shared writes;
- no stream needs another stream's unfinished core output to begin;
- coordination overhead is lower than the expected speed or quality benefit.

Otherwise run the coupled streams sequentially. Parallel execution is an
optimization, not a completion requirement.

## Complexity Signals

Multi-stream coordination is more likely to help when the task spans multiple
repositories, independently shippable deliverables, distinct owners, or an
independent high-risk verification lane. These are signals, not automatic
reasons to fan out.

## Ownership and Integration

- One writer owns each repository/path boundary at a time.
- Reads and verification may proceed independently when they do not mutate the
  writer's inputs.
- Record blocked-by relationships before execution.
- Integrate outputs in dependency order and resolve contract mismatches before
  final verification.
- Collapse back to sequential execution if streams converge on one writer scope.

## Evidence Lifecycle

1. Lock objective, scope, constraints, and done signals.
2. Gather only evidence needed to decide the execution shape and plan.
3. Execute scoped streams and update status on meaningful transitions.
4. Integrate, verify, and record command/file evidence.
5. Close with outcomes, remaining risk, and minimal next actions.

## Minimum Done Criteria

- Objective is met or explicitly re-scoped.
- Dependencies and integration gates are satisfied.
- Key acceptance checks have inspectable evidence.
- Remaining work has an owner or a clear unblock action.
