# Harness Adapters

This skill should work across Codex, Claude Code, Cursor, OpenCode,
Antigravity, and similar agent harnesses. Treat this file as policy, not a list
of fixed commands.

## Universal Adapter Rule

Use the current harness' native mechanism for delegation. Prefer officially
exposed tools, thread/fork primitives, worktree tasks, or subagent APIs over
shelling out to another agent system.

If the harness exposes a tool registry or discovery mechanism, inspect it before
inventing commands. If it does not expose delegation, emulate the workflow with
sequential packets and explicit synthesis notes.

## Model And Cost Routing

Treat model assignment as part of orchestration design. Choose the model and
reasoning effort per lane before spawning workers, then include the assignment
in the packet or setup step when the harness supports it.

Keep this skill harness-neutral. Prefer the current session's defaults unless
the user, harness, or a companion skill gives a more specific routing policy.
When a companion model-routing skill is loaded, use it for exact model names and
cost preferences while this skill continues to own decomposition and synthesis
mechanics.

General policy:

- Put the strongest judgment model on framing, conflict resolution, synthesis,
  and final recommendation.
- Put long-context or cheaper workers on bounded reading, inventory, extraction,
  and source collection when they can return compact evidence packets.
- Do not spend high-value lead-agent context on raw search when a support lane
  can collect the evidence cleanly.

If a named model, plugin, or reasoning level is unavailable in the current
harness, inspect the available capabilities and use the nearest configured
equivalent. State the substitution in the final synthesis when it affects cost,
latency, confidence, or reproducibility.

## Codex

Use native subagent tools when available. Typical concepts include:

- Spawn well-scoped agents for independent tasks.
- Prefer inherited model/settings unless the user or a companion routing skill
  asks for a specific model, reasoning effort, or cost-saving lane.
- Use explorer-style agents for read-only codebase questions.
- Use worker-style agents for bounded implementation with disjoint ownership.
- Wait only when the lead agent is blocked on the result.
- Close completed agents when no longer needed.

Codex-specific caution: do not spawn subagents unless the user explicitly asked
for subagents, delegation, or parallel agent work. This skill usually triggers
only after that consent is present.

## Claude Code

Use Claude Code's native subagents, tasks, or agent-team features when present.
Prefer filesystem-backed instructions, explicit agent roles, and fresh-context
workers for isolated tasks. For team-style workflows, keep handoff artifacts
small and reviewable: spec, task, evidence, review result.

If the user supplies a companion routing skill, use it to choose exact models,
plugins, and token-saving lanes. Keep cross-harness packets small: objective,
scope, exclusions, evidence contract, and stop condition. Do not dump the whole
conversation unless the worker truly needs it.

Claude-specific caution: skills and subagents are separate concepts. A skill
can tell the lead agent how to orchestrate; it should not assume every named
agent exists.

## Cursor

Use Cursor's available agent/task primitives if exposed in the current session.
If they are not available, keep orchestration as explicit packets in the main
thread and ask the harness to run them only when the user invokes its native
multi-agent workflow.

Cursor-specific caution: editor state and user edits are easy to trample. Keep
write scopes narrow and avoid broad refactors while parallel work is in flight.

## OpenCode

Use OpenCode's native task/subagent or command integration when available.
Because installations vary, discover the local mechanism from the current tool
surface or project docs before assuming syntax.

OpenCode-specific caution: if the agent system runs in the same checkout, treat
workers as potentially conflicting unless worktrees or disjoint write scopes
are explicit.

## Antigravity

Use Antigravity's native skill/task/agent mechanism when available. Treat the
same orchestration policies as portable: independent lanes, bounded packets,
evidence-first synthesis, follow-up waves only when needed.

Antigravity-specific caution: community skill bundles can be broad and uneven.
Use installed capabilities that are visible in the current harness, not what an
online collection claims should exist.

## Fallback Mode

If no real parallel execution is available:

1. State that native parallel subagent execution is not available in the current
   harness.
2. Create the same work packets.
3. Execute them sequentially with context resets where possible.
4. Synthesize through the same gate.

Do not describe sequential work as parallel.
