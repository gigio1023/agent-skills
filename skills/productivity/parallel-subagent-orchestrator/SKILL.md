---
name: parallel-subagent-orchestrator
description: >
  Use when the user asks for parallel subagents, delegated agents, agent teams,
  competing research tracks, or when a large task has independent workstreams
  where parallel execution would materially improve speed, coverage, or
  verification. Orchestrates coding, research, judgment, review, planning, and
  synthesis across Codex, Claude Code, Cursor, OpenCode, Antigravity, and similar
  harnesses. NOT for small or tightly sequential tasks.
---

# Parallel Subagent Orchestrator

## Purpose

Lead parallel work to improve judgment, coverage, and execution while keeping
the user's objective intact.

Use the native delegation, task, thread, worktree, or subagent mechanism provided
by the current environment.
If no such mechanism is available, emulate the same discipline with explicit
work packets, local notes, and sequential passes rather than pretending
parallel execution happened.

## Quick Start

1. Restate the user's objective, decision pressure, and expected output.
2. Decide whether parallelization is actually useful. Prefer parallel work when
   the task has independent sources, perspectives, files, modules, hypotheses,
   or verification lanes.
3. Read `references/delegation-patterns.md` for the task type.
4. Read `references/harness-adapters.md` and use the current harness' native
   delegation mechanism, model policy, and cost-routing options without
   hardcoding commands from another environment.
5. Spawn the smallest useful first wave. Each subagent receives a
   self-contained packet: objective, scope, exclusions, output contract,
   evidence requirements, and stop condition.
6. Prefer asynchronous updates and reuse a long-lived agent for related follow-up
   work when retained context is valuable. While agents run, advance a disjoint
   lead-agent slice instead of blocking on the slowest lane.
7. Before reporting progress, tie each claim to a worker artifact, tool result,
   source, or test from the current run.
8. Read results, then synthesize. Do not concatenate summaries. Use
   `references/synthesis-gate.md` to merge claims, evidence, confidence,
   conflicts, and remaining gaps.
9. If gaps remain and the user goal still needs it, launch a targeted follow-up
   wave. Otherwise finish with a decision, implementation, or research answer.
10. Close or retire subagents/threads/worktrees that are no longer needed.

## Operating Philosophy

Parallel agents are not a brainstorming trick. They are context isolation,
coverage expansion, adversarial checking, and throughput. Use them when those
properties matter.

Not every multi-call workflow needs an agent. Use a deterministic or
programmatic tool path for bounded structured reduction that needs no semantic
judgment between calls; keep sequential work direct when each result determines
the next move.

The lead keeps ownership. Subagents may investigate, implement bounded
slices, critique, verify, or argue from a perspective, but the lead agent owns
task framing, conflict resolution, final judgment, and user communication.

Favor policies over brittle mechanics. A portable orchestration skill should
describe what good delegation means and let each harness choose how to spawn,
wait, message, fork, or isolate work.

## When To Parallelize

Parallelize when at least one is true:

- Independent evidence lanes exist: official docs, academic papers, GitHub
  repos, market data, codebase areas, user files, or competing product examples.
- Multiple expert lenses would improve judgment: supporter, skeptic, operator,
  historian, implementer, reviewer, security, accessibility, performance.
- Implementation can be split by disjoint ownership: modules, packages,
  screens, scripts, tests, docs, migration, verification.
- Verification can run while implementation continues.
- The task is large enough that context isolation reduces drift.

Stay single-agent when the task is tiny, highly sequential, privacy-sensitive
without need, or when coordination overhead would exceed the benefit.

## Common Scenarios

This skill is especially useful for:

- Breadth research: ecosystem scans, tool selection, GitHub/package review, and
  market maps where independent source lanes reduce slop.
- Evidence review: papers, laws, standards, policies, and high-impact claims
  where source quality matters more than summary volume.
- Strategy or value judgment: apply/skip, buy/wait, path selection, relocation,
  architecture, or product choices under uncertainty.
- Codebase exploration: architecture, tests, and risk discovery before changing
  unfamiliar or cross-cutting code.
- Parallel implementation: disjoint modules, screens, scripts, tests, docs, or
  verification lanes that can proceed without write conflicts.
- Adversarial review: correctness, security, user-fit, maintainability,
  evidence quality, accessibility, performance, or design critique.
- Long-running work: multi-wave research, implementation, review, and
  verification where each wave should be re-anchored from accepted evidence.

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

- Design non-overlapping work. If two subagents would answer the same question,
  split by source, method, perspective, or output responsibility.
- Preserve provenance. Every important claim should say where it came from and
  whether it is direct evidence, inference, taste, or speculation.
- Track state explicitly. Know which agents are running, what each owns, what is
  blocked, and what output is expected next.
- Ground progress claims in current-run evidence. A worker saying it is done is
  not proof; inspect its artifact, cited source, diff, or test result.
- Re-anchor follow-up waves. Every new wave should include what is already known
  and what remains uncertain, not the whole conversation dump.
- Protect the worktree. For code edits, assign disjoint write scopes and remind
  workers that other agents may be editing nearby files.
- Close the loop. A parallel run is not done until results are synthesized,
  contradictions are handled, and the user gets a clear answer or artifact.

## Gotchas

- More agents can make the answer worse. If agents duplicate effort, inherit the
  same bad premise, or produce unranked summaries, parallelism creates noise.
- Do not use subagents for structured filtering, joining, ranking, or aggregation
  when a bounded deterministic reduction is clearer and cheaper.
- Do not outsource the core decision. Subagents provide evidence and arguments;
  the lead agent decides.
- Do not let star counts or popularity replace quality judgment. Use popularity
  as one weak signal, then inspect substance.
- Do not force code-edit workers into overlapping files unless the user accepts
  merge risk or the harness provides clean worktree isolation.
- Do not wait idly. Once agents are running, advance non-overlapping work.
- Do not bury uncertainty. If sources conflict or evidence is thin, say so and
  decide whether another wave is worth the cost.
