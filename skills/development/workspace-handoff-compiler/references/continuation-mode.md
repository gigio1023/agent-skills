# Continuation Mode (runtime-agnostic)

Decide how the successor should resume the remaining work. The two modes describe the SHAPE of the work, not any specific harness feature.

## Modes

- `parallel_recommended`: remaining work splits into independent streams that benefit from parallelism.
- `sequential_sufficient`: a single linear session is the most effective path.

## Universal Judgment Rule (parallelism)

When work splits into independent streams that benefit from parallelism, use the harness's parallel-execution capability aggressively. When a single linear session is more effective, do that.

Always probe for a native parallel-execution capability first. If none exists, run the streams sequentially and say so explicitly in the handoff (sequential fallback). Parallelism is never an unconditional requirement, and it is never tied to one specific runtime.

Illustrative examples only (not the rule itself): Claude Code workflows or subagents, Codex threads. Any of these, or none, may be available. Detect, then decide.

## When to recommend `parallel_recommended`

Recommend parallel continuation when any of these hold:

1. Multiple repositories or systems are involved.
2. More than one independent owner or writer scope exists.
3. There are independent tracks that can progress without waiting on each other.
4. High-risk changes need verification independent of the change author.
5. Remaining work cannot be completed safely by one uninterrupted linear pass.

If none hold, recommend `sequential_sufficient`. If uncertain, prefer `sequential_sufficient` and note what would tip it toward parallel.

## Sequential Fallback (must document)

Even when `parallel_recommended` is set, the successor may have no parallel capability. In that case:

1. Run the streams in dependency order in one session.
2. Record in `handoff.md` that parallelism was recommended but executed sequentially, and why.
3. Keep the role map and ownership boundaries as a serialization guide, so a single agent still respects write boundaries one stream at a time.

## Multi-track fields

When the work is multi-track (more than one independent stream, owner, or repository), include in `handoff.md` and `context-pack.json`:

1. Role map: required roles (for example reader, writer, verifier, reviewer).
2. Ownership boundaries: who writes where, with no overlapping write ownership.
3. Dependency graph: blocked-by relationships and execution order.
4. Parallel opportunities: read-only and validation tasks that can run concurrently.
5. Merge protocol: writer serialization and final integration gate.

Single-track work may leave the role and ownership arrays empty.

## Safety Rule

Do not flatten complex outstanding work into a single "next step". Preserve dependency and role structure so the successor can resume without re-discovering it.
