# Continuation Mode

Choose the continuation value already defined by the compiler's context-pack
contract. It describes the shape of remaining work, not a required runtime or
model.

## Decision Rule

Use the parallel recommendation only when all of these hold:

- At least two remaining tracks can make useful progress independently.
- Writer scopes are disjoint, or shared writes have an explicit serialization
  gate.
- No track needs another track's unfinished core output to begin.
- Coordination overhead is lower than the expected time or quality benefit.

Otherwise use the sequential recommendation. When uncertain, prefer sequential
and record what future condition would make a split worthwhile.

## Multi-Track Fields

For multi-track work, preserve:

- role map and writer ownership;
- blocked-by relationships and execution order;
- independent read or verification tracks;
- integration and final verification gates.

Single-track work may leave role, ownership, and parallel-track arrays empty.

## Sequential Fallback

If parallel execution is recommended but unavailable, run the same tracks in
dependency order. Retain ownership boundaries as serialization rules and note
that execution was sequential; do not redesign the work around a named harness
or model.

## Safety Rule

Do not flatten complex outstanding work into one vague next step. Preserve the
dependencies and first executable action even when execution is sequential.
