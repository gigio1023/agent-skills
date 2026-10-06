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
4. Read `references/harness-adapters.md` and use the current native delegation mechanism. For GPT workers, apply `gpt6-astra-model-routing`: Astra by default, Sol 6.1 only for very easy deterministic execution. For Anthropic workers, keep the applicable Anthropic routing policy.
5. Map the work before sizing it. List each packet with the inputs it needs before it can start. Spawn the smallest useful first set while the decomposition is still uncertain. When the split is already clear or the user asks for maximum parallelism, spawn a subagent for every ready packet. Each subagent receives a self-contained packet: objective, scope, exclusions, output contract, evidence requirements, expected duration, progress artifact, and stop condition.
6. Run the [dispatch loop](#dispatch-loop) until the map is done. Dispatch each packet as soon as its own inputs exist, check live workers for stalls, and advance a disjoint lead slice while they run. Reuse a long-lived agent for related follow-up work when its retained context is valuable.
7. Before reporting progress, tie each claim to a worker artifact, tool result, source, or test from the current run.
8. Read results, then synthesize. Do not concatenate summaries. Use `references/synthesis-gate.md` to merge claims, evidence, confidence, conflicts, and remaining gaps.
9. If gaps remain and the user goal still needs it, launch a targeted follow-up wave. Otherwise finish with a decision, implementation, or research answer.
10. Close completed workflow-owned subagents when their results are integrated. Preserve user tasks and worktrees unless their cleanup was explicitly authorized; ending worker execution does not authorize deleting its files.

## Dispatch Loop

Plan the run as a dependency map rather than as waves. Each packet names what it needs before it can start: another packet's artifact, a lead decision, or nothing. A packet whose inputs exist is ready. A wave is only the shape of the map at the start, so a ready packet never waits for an unrelated worker in the same wave.

Keep a ledger of live workers. Record each worker's packet, write scope, start time, expected duration, progress artifact, and the packets that wait on its output. The expected duration is an estimate from the packet's size. Write it down so that a stall becomes visible.

On every event (a worker finishes, a scheduled check fires, the user writes), do the following in order:

1. Integrate finished results that unblock other packets.
2. Dispatch every ready packet while running workers stay below the concurrency limit and the budget allows.
3. Check each live worker against its expected duration, as described under liveness below.
4. Take a lead slice that does not overlap any worker's write scope.

Before you end a turn to wait, count the ready packets and the running workers. Dispatch the ready packets first if the limit allows.

**Sequential chains.** Some work is a chain in which each step builds on the previous one, such as stacked branches, ordered migrations, or a rebase series. Keep only the chain's order serial and give the chain to one integrator. Take out every node that does not depend on that order and give it its own packet. Examples are a fix that can target the base branch, a standalone tool, a review of a link that is already final, or documentation that needs only names. Start the integrator when the inputs of the first links exist. Do not wait until every review finishes.

**Verification lanes.** Size review and verification by independently checkable units, such as one lane per branch, module, or claim group, up to the concurrency limit. If a few reviewers cover many units, the final and slowest phase runs serially.

**Liveness.** Many harnesses report a background worker only when it stops, so a stalled worker and a working worker look the same. Each packet therefore names a progress artifact the lead can inspect. Examples are incremental writes to the report file, a growing diff or commits in the worker's own worktree, or a short progress note. Use these checks:

- Check the artifacts at about a third of the expected duration and again when the expected duration ends. Set the check time from the packet. A generic long fallback timer can hide a stall for an hour.
- Judge progress by artifacts in the worker's write scope and by its running processes. Transcript and log timestamps can lag behind a worker that is still active.
- A worker is stalled when nothing in its scope changed for a large part of its expected duration and none of its commands are running. Send it one message that asks for its result or blocker. If the next check still shows no change, stop the worker. Then dispatch a replacement packet that starts from the partial artifacts and states what is already done.

## Operating Philosophy

Parallel agents are not a brainstorming trick. They are context isolation, coverage expansion, adversarial checking, and throughput. Use them when those properties matter.

Orchestration intensity is a dial the lead keeps adjusting, not a shape chosen once. The same discipline covers a single scoped helper, one bounded wave, and a sustained worker pool that the lead keeps saturated by re-dispatching queued tasks as workers finish. Set the intensity from how much genuinely independent work exists, the task's stakes, and the user's budget — then revise it mid-run as results reveal more or less independence than expected.

Subagent count follows independent ownership, the user's budget, and the available concurrency limit. Queue excess work and reuse finished workers; do not treat a clear decomposition as unlimited spending authority. Surplus agents duplicate effort and add noise. Fewer is not safer — too few subagents serialize independent work. The right number changes with the kind of work, so decide it by planning the split, not by defaulting to a familiar count.

Not every multi-call workflow needs an agent. Use a deterministic or programmatic tool path for bounded structured reduction that needs no semantic judgment between calls. Distinguish fetching named sources from selecting sources, extracting meaningful claims, summarizing conflicts, or choosing follow-up queries. Those latter tasks require judgment, even when they are read-only or cover many inputs. Keep sequential work direct when each result determines the next move.

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
- Track state explicitly in the [dispatch ledger](#dispatch-loop): which agents are running, what each owns, when each should finish, what shows its progress, and which packets wait on it.
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
- A downstream phase whose inputs are ready can still end up waiting for one slow reviewer in the previous wave. Read readiness from each packet's own inputs, not from the wave.
- A whole phase given to one worker turns parallel work into serial work, for example review plus port plus a standalone tool plus documentation in one packet. Split the phase into the chain and its independent nodes before you dispatch it.
- A completion-only notification combined with a long fallback timer lets a stalled worker sit unnoticed. Check progress artifacts on the packet's own schedule.
- Do not bury uncertainty. If sources conflict or evidence is thin, say so and decide whether another wave is worth the cost.
