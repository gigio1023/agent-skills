# Swarm Continuation Contract

For complex work, enforce team-first continuation instead of single-agent continuation.

## Complexity Triggers

Treat work as complex when any condition is true:

1. Multiple repositories or systems are involved.
2. More than one active owner or writer scope exists.
3. There are parallelizable tracks with dependencies.
4. High-risk changes require independent verification.
5. Remaining work cannot be completed safely by one uninterrupted linear pass.

## Continuation Mode Rules

- If complex, set mode to `swarm_required`.
- If none of the triggers apply, set mode to `single_agent_allowed`.
- If uncertain, default to `swarm_required`.

## Required Swarm Fields in Handoff

When mode is `swarm_required`, include:

1. Role map  
   - required roles (for example: steward, writer, verifier, reviewer, test runner).
2. Ownership boundaries  
   - who can write where; avoid overlapping write ownership.
3. Dependency graph  
   - blocked-by relationships and execution order.
4. Parallel opportunities  
   - read-only and validation tasks that can run concurrently.
5. Merge protocol  
   - writer serialization and final integration gate.

## Safety Rule

- Do not flatten complex outstanding work into one "next step".
- Preserve dependency and role structure so the successor AI can resume without re-discovery.
