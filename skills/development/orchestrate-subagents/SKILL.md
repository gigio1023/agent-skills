---
name: orchestrate-subagents
description: >
  Use when the user asks for parallel subagents, delegated agents, agent
  teams, or competing research tracks, names orchestrate-subagents, or when
  the lead has itself decided to run a multi-agent wave. Orchestrates coding,
  research, judgment, review, planning, and synthesis across Codex, Claude
  Code, Cursor, OpenCode, Antigravity, and similar harnesses. NOT for small or
  tightly sequential tasks, and not opened merely because a task has
  independent workstreams; an agent or two inline needs no skill. An explicit
  user choice about delegation governs; without one, the lead decides.
---

# Orchestrate Subagents

## Purpose

Lead parallel work to improve judgment, coverage, and execution while keeping the user's objective intact.

Use the native delegation, task, thread, worktree, or subagent mechanism provided by the current environment. If no such mechanism is available, emulate the same discipline with explicit work packets, local notes, and sequential passes rather than pretending parallel execution happened.

## Quick Start

1. Restate the user's objective, decision pressure, and expected output.
2. Decide whether parallelization is actually useful. Prefer parallel work when the task has independent sources, perspectives, files, modules, hypotheses, or independent verifications.
3. Read `references/delegation-patterns.md` for the task type.
4. Read `references/harness-adapters.md` and use the current harness' native delegation mechanism, model policy, and cost-routing options without hardcoding commands from another environment.
5. Size the first wave deliberately. Spawn the smallest useful wave while the decomposition is still uncertain; spawn a subagent for every genuinely independent task when the split is already clear or the user asks for maximum parallelism. Each subagent receives a self-contained packet: objective, scope, exclusions, output contract, evidence requirements, and stop condition.
6. Prefer asynchronous updates and reuse a long-lived agent for related follow-up work when retained context is valuable. While agents run, advance a disjoint lead-agent slice instead of blocking on the slowest subagent. When a worker finishes and independent work remains queued, dispatch its next packet right away — a wave is a starting shape, not a barrier.
7. Before reporting progress, tie each claim to a worker artifact, tool result, source, or test from the current run.
8. Read results, then synthesize. Do not concatenate summaries. Use `references/synthesis-gate.md` to merge claims, evidence, confidence, conflicts, and remaining gaps.
9. If gaps remain and the user goal still needs it, launch a targeted follow-up wave. Otherwise finish with a decision, implementation, or research answer.
10. Close completed workflow-owned subagents when their results are integrated. Preserve user tasks and worktrees unless their cleanup was explicitly authorized; ending worker execution does not authorize deleting its files.

## Operating Philosophy

Parallel agents are not a brainstorming trick. They are context isolation, coverage expansion, adversarial checking, and throughput. Use them when those properties matter.

Orchestration intensity is a dial the lead keeps adjusting, not a shape chosen once. The same discipline covers a single scoped helper, one bounded wave, and a sustained worker pool that the lead keeps saturated by re-dispatching queued tasks as workers finish. Set the intensity from how much genuinely independent work exists, the task's stakes, and the user's budget — then revise it mid-run as results reveal more or less independence than expected.

Subagent count follows independent ownership, the user's budget, and the available concurrency limit. Queue excess work and reuse finished workers; do not treat a clear decomposition as unlimited spending authority. Surplus agents duplicate effort and add noise. Fewer is not safer — too few subagents serialize independent work. The right number changes with the kind of work, so decide it by planning the split, not by defaulting to a familiar count.

Not every multi-call workflow needs an agent. Use a deterministic or programmatic tool path for bounded structured reduction that needs no semantic judgment between calls; keep sequential work direct when each result determines the next move.

An explicit user instruction about delegation governs: whether to delegate, how many subagents, which models, and the budget. Without one, deciding to delegate and sizing the wave are the lead's calls, and making them is expected rather than exceptional; do not stop to ask for permission the user did not ask to give. That autonomy covers the fan-out only. Delegation never grants new authority for external writes, destructive work, purchases, or material scope expansion.

The lead keeps ownership. Subagents may investigate, implement bounded slices, critique, verify, or argue from a perspective, but the lead agent owns task framing, conflict resolution, final judgment, and user communication.

Favor policies over brittle mechanics. A portable orchestration skill should describe what good delegation means and let each harness choose how to spawn, wait, message, fork, or isolate work.

## When To Parallelize

Parallelize when at least one is true:

- Independent evidence sources exist: official docs, academic papers, GitHub repos, market data, codebase areas, user files, or competing product examples.
- Multiple expert lenses would improve judgment: supporter, skeptic, operator, historian, implementer, reviewer, security, accessibility, performance.
- Implementation can be split by disjoint ownership: modules, packages, screens, scripts, tests, docs, migration, verification.
- Verification can run while implementation continues.
- The task is large enough that context isolation reduces drift.

Stay single-agent when the task is tiny, highly sequential, privacy-sensitive without need, or when coordination overhead would exceed the benefit.

## Reference Files

| File | Read when | Content |
|------|-----------|---------|
| `references/delegation-patterns.md` | Before first wave | Patterns for research, value judgment, coding, review, verification, and long-running work |
| `references/synthesis-gate.md` | Before merging results | Evidence matrix, conflict handling, gap analysis, follow-up wave rules |
| `references/harness-adapters.md` | Before spawning or emulating agents | Harness-neutral mapping for Codex, Claude Code, Cursor, OpenCode, Antigravity |
| `references/scenario-catalog.md` | When deciding whether this skill fits or explaining expected use cases | Expanded scenario catalog and model-routing examples |
| `references/anti-slop-research.md` | For web, GitHub, literature, market, or tool research | Filters for AI slop, fake popularity, weak sources, and shallow agent-skill collections |
| `references/prompt-packets.md` | When writing subagent prompts | Reusable packet shapes for delegation |
| `references/source-notes.md` | When maintaining or explaining this skill | Research basis and design trade-offs |

## Lead Agent Duties

- Respect the current work boundary. When a plan already assigns dependencies and ownership, use them for the current round; do not require a stage field or a fully specified project. Reconcile stale assumptions and changed evidence with the lead before dispatch. Workers may use relevant domain skills within their packet, and must return findings that invalidate the basis promptly. Running a requested plan belongs to `gigio-execute-plan`, which can draw on this skill for orchestration mechanics.
- Design non-overlapping work. If two subagents would answer the same question, split by source, method, perspective, or output responsibility.
- Preserve provenance. Every important claim should say where it came from and whether it is direct evidence, inference, taste, or speculation.
- Track state explicitly. Know which agents are running, what each owns, what is blocked, and what output is expected next.
- Ground progress claims in current-run evidence. A worker saying it is done is not proof; inspect its artifact, cited source, diff, or test result.
- Treat a worker result that announces its next step as unfinished. A subagent's last message is its result, and some models, Claude Opus 5.5 among them, can end a turn on a progress note; resume the worker with the open items instead of accepting the note.
- Re-anchor follow-up waves. Every new wave should include what is already known and what remains uncertain, not the whole conversation dump.
- Protect the worktree. For code edits, assign disjoint write scopes and remind workers that other agents may be editing nearby files.
- Close the loop. A parallel run is not done until results are synthesized, contradictions are handled, and the user gets a clear answer or artifact.
- When the user corrects the task, update affected packets and inspect active worker state before redispatching. A sent correction is not proof that a worker received it or stopped an already-started action.

## Gotchas

- More agents can make the answer worse. If agents duplicate effort, inherit the same bad premise, or produce unranked summaries, parallelism creates noise.
- Do not use subagents for structured filtering, joining, ranking, or aggregation when a bounded deterministic reduction is clearer and cheaper.
- Do not outsource the core decision. Subagents provide evidence and arguments; the lead agent decides.
- Do not spawn a subagent to re-check the lead's own reasoning. A reviewer earns its cost through fresh context on the specification and artifact; models that already verify their own work, such as Claude Opus, over-verify when told to.
- Do not let star counts or popularity replace quality judgment. Use popularity as one weak signal, then inspect substance.
- Do not force code-edit workers into overlapping files unless the user accepts merge risk or the harness provides clean worktree isolation.
- Do not wait idly. Once agents are running, advance non-overlapping work.
- Do not bury uncertainty. If sources conflict or evidence is thin, say so and decide whether another wave is worth the cost.
