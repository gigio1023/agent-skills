# Anti-Patterns

[Terminology index](../../terminology.md) · [Detailed terms](terms.md) · [References](references.md)

## "lane" for a subagent, its definition, or a route

**Problematic use:** "the cheaper lane", "lane definitions", "open a lane for every independent task", "judgment lane". The routing skills and several orchestration skills in this pack used one word for three different things: the subagent doing delegated work, the configured record that pins its model and effort, and the standing assignment of a class of work to a model.

**Replacement:** subagent (or worker) for the agent; task for the unit of work and dispatch for the act; subagent definition, agent file, or Codex role for the configured record, and `agent_type` in a dispatch line; route for the standing assignment and assignment for one spawn's decision. Keep tier for difficulty.

**Why the original misleads:** None of the harness documents checked on 2026-09-20 uses "lane" for any of these senses (Claude Code, Agent SDK, Codex subagents and config reference, Cursor, OpenCode, OpenAI Agents SDK), and the routing literature says model, router, route, and cascade. Hermes uses "worker lane" only in its Kanban feature, for a class of process a dispatcher routes tasks to, and still calls the configured agent a profile. The word is a partition metaphor borrowed from swimlanes and SIMD lanes and stretched across referents, which made sentences ambiguous about whether they described an agent, a file, or a policy. The closest human-maintained peer package uses "tier" and "dispatch" and never "lane"; the package that does use it carries model-authorship trailers on much of its history.

**Scope:** Editorial decision by the maintainer on 2026-09-20 for this pack's reader-facing prose, applied to `fable5-model-routing` and `gpt6-astra-model-routing`, then across `orchestrate-subagents`, `codex-delegate`, `english-prompt-review`, `cursor-cli-delegation`, `pr-review-comment`, `mermaid-diagrams`, and `docs/finding-unknowns-workflow.md`, where the same word also stood for a review pass, a restricted execution mode, a parallel Codex run, and a domain's dedicated skill set. In `mermaid-diagrams` the diagram sense is written out as "swimlane", and the `subgraph lane` syntax stays as the renderer spells it. This is a preference about precision, not a claim that "lane" is incorrect in other fields.

**Exceptions:** Quoted source text, such as Hermes's "worker lane"; product syntax, such as Mermaid's `subgraph lane` and `swimlane-beta`; and literal uses in fields that own the word, such as SIMD or GPU lanes, CI lanes in Fastlane, and BPMN swimlanes.

**Reference:** [R001](references.md#r001) through [R007](references.md#r007), [R013](references.md#r013), and [R014](references.md#r014) for the absence in harness and SDK documentation, [R008](references.md#r008) and [R009](references.md#r009) for the literature nouns, [R010](references.md#r010) and [R012](references.md#r012) for community usage, [R011](references.md#r011) for the decision.
