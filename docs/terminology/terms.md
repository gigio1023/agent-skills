# Detailed Terms

[Terminology index](../../terminology.md) · [Anti-patterns](anti-patterns.md) · [References](references.md)

## subagent

**Meaning and status:** An agent that a lead agent spawns to handle a delegated task and whose result returns to the lead. Developer usage across harnesses: Claude Code ("Subagents are specialized AI assistants"), the Claude Agent SDK, Codex ("A delegated agent that Codex starts to handle a specific task"), and Cursor. Anthropic's multi-agent engineering post uses "subagents" for the same thing and "worker" informally.

**Use and distinctions:** The running instance, as opposed to its configuration (see subagent definition). "Worker" is an acceptable informal synonym in prose about a lead and its workers; "teammate" is Claude Code's word for a peer in an agent team, not a subagent.

**Reference:** [R001](references.md#r001), [R002](references.md#r002), [R003](references.md#r003), [R005](references.md#r005), [R013](references.md#r013).

## subagent definition

**Meaning and status:** The record that configures a subagent before it runs: model, effort, tools, permissions, and instructions. The Agent SDK names the type `AgentDefinition`; Claude Code and Cursor describe it as a Markdown file with YAML frontmatter; Codex calls it a custom agent file, role, or agent type.

**Use and distinctions:** Say "subagent definition" in harness-neutral prose, "agent file" when the sentence points at a path, "role" in Codex-specific text, and `agent_type` when naming the spawn argument that selects it. The routing skills ship definitions as assets named `<model>-<role>`, such as `opus-builder` and `sol-builder`, so the name shows the cost class.

**Reference:** [R002](references.md#r002), [R004](references.md#r004), [R005](references.md#r005).

## task

**Meaning and status:** The unit of work a lead delegates to a subagent. Every harness document checked uses it: Claude Code ("a delegation message that summarizes the task"), Codex ("handle a specific task"), Cursor, Hermes ("Per-task model override"), Anthropic's research post ("research tasks").

**Use and distinctions:** Prefer "delegated task" on first use when the lead's own task is also in view. In Claude Code the historical tool name was `Task`; the tool is now `Agent`, so the noun no longer collides with a tool name.

**Reference:** [R001](references.md#r001), [R003](references.md#r003), [R005](references.md#r005), [R007](references.md#r007), [R013](references.md#r013).

## dispatch

**Meaning and status:** The act of handing a task to a subagent. Developer usage in the peer routing package AqueGen/model-routing ("Route every dispatch"); the routing skills use it for the one-line statement made before each spawn.

**Use and distinctions:** "Dispatch statement" names the line `tier | agent_type | model | effort | source | runtime status`. Do not use "dispatch" for the configured record or for the standing policy.

**Reference:** [R010](references.md#r010), [R011](references.md#r011).

## route

**Meaning and status:** A standing assignment of a class of work to a model at an effort. Research usage in the LLM routing literature (RouteLLM, Hybrid LLM), where a router assigns queries to models.

**Use and distinctions:** "The reviewer route runs Fable at `high`" describes policy; "this spawn's assignment" describes one decision. A proxy's "route string" (for example an opencodex `ocx-route`) is that product's identifier for a pinned model and effort, so name it "route string" when both senses are near.

**Reference:** [R008](references.md#r008), [R009](references.md#r009).

## tier

**Meaning and status:** One of four difficulty classes used by the routing skills to place a delegated task: mechanical collection, bounded execution, judgment-adjacent support, judgment core. Developer usage in AqueGen/model-routing for the same idea ("Think in tiers, not model names").

**Use and distinctions:** Reserved for difficulty. Do not use "tier" for a model class or a service tier; say "model class" and "service tier" in full.

**Reference:** [R010](references.md#r010), [R011](references.md#r011).

## role

**Meaning and status:** Codex's noun for a named subagent configuration: a `[agents.<name>]` table with a `config_file`, or a standalone role file under `agents/` that carries `name`, `description`, `developer_instructions`, and any `config.toml` key such as `model` and `model_reasoning_effort`. Source-specific to Codex.

**Use and distinctions:** Use in Codex-specific sections and asset names. Outside Codex, "subagent definition" is the neutral noun. CrewAI's `role` is a persona field and unrelated.

**Reference:** [R004](references.md#r004).

## effort floor

**Meaning and status:** Internal name for this pack's routing policy: every model below the frontier lead class runs at reasoning effort `xhigh` by default, and a route is lowered only per definition or spawn argument with a recorded reason. Frontier lead models vary effort by task shape. Confirmed as the maintainer's policy on 2026-09-20.

**Use and distinctions:** A local policy name, not an industry term. Anthropic's cost measurements show what lowering a route would buy; they do not define the floor.

**Reference:** [R011](references.md#r011).
