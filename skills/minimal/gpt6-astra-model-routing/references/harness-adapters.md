# Harness Adapters

Apply the GPT routing policy through the active harness's supported controls. Use its current tool schema and model catalog; implementation behavior that contradicts the exposed contract is not permission to bypass it.

## Capability Check

Before a spawn in an unfamiliar surface, establish:

1. Whether model and effort are set per call, per role, or globally.
2. Which model IDs and effort levels the surface accepts.
3. Which fork modes, role pins, and override rules apply.
4. Whether the result exposes the child's applied settings.

Record the selected settings and their source in the dispatch. Record runtime confirmation separately. If only one delegation model is available, use Astra for general GPT work. A global Sol setting is suitable only when every delegated packet is mechanical.

## Codex

The [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) documents `agents.default_subagent_model` and `agents.default_subagent_reasoning_effort`. Explicit spawn values take precedence over those defaults. The [subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents) documents custom TOML agents with `name`, `description`, and `developer_instructions`, plus supported configuration fields such as `model` and `model_reasoning_effort`.

Read the active spawn tool before dispatch. A role that locks settings must be used with those settings; select another role or a supported explicit override when the task needs different settings. Do not assume `agent_type` exists on every Codex surface.

When the current tool says a full-history fork inherits settings and rejects overrides, follow that contract. For an override, use `fork_turns: "none"` or a supported positive integer string and supply the context the worker needs. For a full-history fork, omit overrides and use it only when the inherited model and effort fit the task. Historical handler behavior does not change this rule.

### Explicit Spawn

For a surface exposing the native `spawn_agent` fields below:

```json
{"task_name":"implement_parser","message":"Implement the assigned parser change within the supplied scope and return the diff and verification evidence.","model":"gpt-6-astra","reasoning_effort":"xhigh","fork_turns":"none"}
```

A mechanical collection packet may set `model: "gpt-6.1-sol"` with an explicit supported effort. The packet must contain fixed inputs, commands or transforms, output shape, and mechanical acceptance checks. Sol does not choose what the output means or what to do next.

### Optional Role Installation

1. Confirm the target CLI and account expose `gpt-6-astra` and, if needed, `gpt-6.1-sol`. Inspect the current catalog; a bundled entry does not establish account access.
2. Under the user's installation grant, merge `assets/codex/config.snippet.toml` into the chosen user or project configuration. Unnamed workers default to Astra at `xhigh`.
3. Copy the role files into the supported agent directory, conventionally `~/.codex/agents/` or the project's `.codex/agents/`. Inspect existing files before replacing any.
4. When migrating this pack's earlier roles, replace references to `sol-scout` and `sol-builder` with `astra-scout` and `astra-builder`. Retire old installed files only within the installation grant. Do not leave the old roles selectable as normal routes.
5. Validate configuration and role discovery through the target harness. A live model call runs only when the task requests or requires it; report untested runtime application otherwise.

Set model and effort together in explicit defaults. The assets use `xhigh`; preserve an explicitly selected effort by choosing a compatible role or supported explicit spawn instead of silently using a conflicting pin. Do not change service tier, concurrency, or the lead model as a side effect of installing worker roles.

### Delegated Missions

`codex-delegate` owns the external mission's launch, model, effort, grant, and evidence. This routing skill applies to GPT children inside that mission whenever the packet and harness allow internal subagents. It applies again to permitted descendants. The mission's scope and budget remain binding.

## Hermes Agent

The Hermes v0.21.3 source inspected on 2026-09-23 uses `delegation.model`, `delegation.provider`, and `delegation.reasoning_effort` as shared child settings. An empty child effort inherits the parent's resolved effort; `agent.reasoning_overrides` does not set the child effort in that version. These are dated findings. Recheck the current version before configuring it.

With a single child model, use `delegation.model: gpt-6-astra` and the selected supported effort for general work. Do not set Sol as a shared default and then send it diagnosis or research. If per-task selection is unavailable, keep a mechanical task on Astra or execute its fixed procedure directly.

## OpenCode

The agent documentation inspected on 2026-09-20 used per-agent `model` and `mode: subagent`, with provider-specific effort fields. Recheck the installed provider and [agent documentation](https://opencode.ai/docs/agents/) before installation. Express Astra as the general route and Sol 6.1 only as a mechanical role; do not infer API support from a display name.

## Claude Code And Cursor

Use the current native or proxy adapter for GPT access. The harness reference in the companion `fable5-model-routing` skill describes the separately maintained Claude and Cursor mechanics. Confirm the exact GPT model ID, effort, tool support, and override behavior before dispatch. A proxy alias is not proof that it resolves to Astra or Sol 6.1.

## API Boundary

GPT-6.1 Sol is `gpt-6.1-sol`, distinct from legacy `gpt-6-sol`. Its public API accepts `low`, `medium`, `high`, `xhigh`, and `max`; `none` and `minimal` are unsupported. Tool calling requires Responses. Codex's catalog and modes are separate from this API contract. For migration details, discover the companion `gpt6-prompting-guide` skill and read its runtime notes.
