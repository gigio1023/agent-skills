# Harness Adapters

The routing policy in `SKILL.md` is harness-neutral. This reference says how each harness actually sets a subagent's model and effort, what it cannot set, where the role files go, and how to report what was resolved. Codex is the worked example, checked against its source at tag `rust-v0.154.0` and the installed CLI 0.154.0 on 2026-09-20; line references are into `codex-rs/`. Recheck facts when the harness changes.

## Contents

- Generic procedure for any harness
- Codex
- Hermes Agent
- OpenCode
- Claude Code or Cursor under an Astra lead
- Reporting and measurement

## Generic Procedure for Any Harness

Before the first spawn in an unfamiliar harness, establish four things and record them in `source-notes.md` with the date and version.

1. **Where a delegated agent's model is set.** Three places are common: an argument on the spawn call, a field in a per-agent definition file, or one global delegation setting. A harness may offer more than one, with a precedence order.
2. **Where its reasoning effort is set.** Check the same three places. Many harnesses set effort only per definition or only globally.
3. **Which routes that allows.** Per-spawn control means the tier table can be applied directly and stated in the dispatch line. Per-definition control means install one definition per route, then choose the definition. Global-only control means one route; decide whether it is acceptable for the tier and state the inherited settings.
4. **Whether the runtime exposes the applied settings.** Look for a dispatch log, a hook, or a status view. If nothing exposes them, every dispatch line ends with `runtime unverified`.

If a subagent cannot be given a different model or effort, the skill still governs the decision: say the inherited values, and do not send judgment-adjacent work to a below-frontier model.

## Codex

### What decides a subagent's model and effort

| Fact | Where |
|------|-------|
| Subagents inherit the lead's model and effort unless something says otherwise. The spawn tool tells the lead: "Spawned agents inherit your current model by default." | `core/src/tools/handlers/multi_agents_spec.rs:17` |
| Precedence: the spawn call's `model` and `reasoning_effort` → `[agents] default_subagent_model` and `default_subagent_reasoning_effort` in `config.toml` → inherit the parent. The defaults are read from the resolved config, so they apply even when the spawn tool hides the fields and regardless of fork mode. | `core/src/tools/handlers/multi_agents_common.rs:274-276`; `multi_agents_v2/spawn.rs:128` |
| A spawn that sets `model` without `reasoning_effort` gives the child that model's catalog `default_reasoning_level`, not the parent's effort. Sol's is `low`. | `multi_agents_common.rs:306-308` |
| A requested effort must appear in the child model's `supported_reasoning_levels`; otherwise the spawn fails with an error the lead sees. | `multi_agents_common.rs:422-442` |
| Role files outrank spawn arguments. A role that pins model or effort is advertised to the lead as locked: "These settings cannot be changed." | `core/src/agent/role.rs:185-193, 314-317` |
| The catalog's `multi_agent_version` selects V1 or V2 and beats the `multi_agent_v2` feature default. `features.multi_agent_v2.enabled = false` does not turn V2 off for a catalog-V2 model; only `agents.enabled = false` disables multi-agent tools. | `core/src/config/mod.rs:1544-1552` |
| In V2 the spawn tool exposes `model` and `reasoning_effort` when `features.multi_agent_v2.expose_spawn_agent_model_overrides` is true, and that flag defaults to true. Setting it false hides the fields and drops the override guidance from the usage hints. | `core/src/config/mod.rs:1307-1308`; `multi_agents_spec.rs:111-114`; `session/multi_agents.rs:129-131` |
| The usage hint says full-history forks (`fork_turns` omitted or `"all"`) do not accept overrides. That is prompt text only; the handler applies overrides before it reads the fork mode. What a full-history fork without `agent_type` does skip is the role, including a user-defined `default` role. | `session/multi_agents.rs:50`; `multi_agents_v2/spawn.rs:128` versus `:136-143` |
| `agent_type` appears in the spawn schema only when at least one role is configured, so a stock config cannot select the built-in `worker` or `explorer`. Those built-ins pin nothing anyway: `explorer.toml` is empty and `worker` has no config file. | `core/src/tools/spec_plan.rs:1304`; `core/assets/agent/builtins/`; `role.rs:338-403` |
| The lead's `ultra` effort switches V2 delegation to proactive mode; every other effort is explicit-request-only. Both mode texts name "the user or applicable AGENTS.md/skill instructions" as a valid explicit request. The served catalog can replace these texts. | `session/multi_agents.rs:166-199`; `context/multi_agent_mode_instructions.rs` |
| `multi_agent_reasoning_effort` in a model's catalog entry is the value sent on the wire when the selected effort is `ultra`; Astra's is `xhigh`, models without the key send `max`. It is not a subagent default. | `protocol/src/openai_models/reasoning_effort.rs:10-40`; `core/src/client.rs:877-879` |
| The root's service tier is pushed to every child; a lead in the fast tier bills every worker at the fast rate. | `core/src/agent/control/service_tier.rs`; release 0.152.0 |
| No per-child token budget exists. `[goals] max_goal_token_budget` caps a goal, and descendant usage rolls up to the root goal. | `ext/goal/src/accounting.rs:20`; `ext/goal/src/extension.rs:408` |
| V2 concurrency: slots come from `features.multi_agent_v2.max_concurrent_threads_per_session`, else `agents.max_concurrent_threads_per_session + 1`, else 4; children may use slots minus one. | `core/src/config/mod.rs:2704-2713` |
| A child whose model is catalog-V1 gets no collaboration tools and cannot spawn grandchildren. | `spec_plan.rs:655-658` |
| The spawn tool lists at most five models in its description, but any catalog model not marked disabled is accepted. | `multi_agents_common.rs:33, 400-406` |
| A skill's `SKILL.md` frontmatter is parsed for `name`, `description`, and `metadata.short-description` only. A skill cannot pin a model; it instructs the lead, and the harness treats that instruction as authorization. | `skills/src/parser.rs:6-27` |

### The served catalog moves

The bundled catalog (`codex debug models --bundled`) and the served catalog (`codex debug models`) differ, and the served one changed within one day during this skill's authoring: Luna moved from V1 to V2 and gained `ultra`, and Astra's default effort read `medium` where the bundle says `low`. Read the catalog at install time, record the values in `source-notes.md` with the date, and never hard-code them in instructions.

### Installing the routes

1. Read `codex debug models` and note each candidate model's `default_reasoning_level`, `supported_reasoning_levels`, and `multi_agent_version`.
2. After approval, merge `assets/codex/config.snippet.toml` into `~/.codex/config.toml`. Its `[agents]` block sends every unnamed worker to Terra at `xhigh`; always set model and effort together there.
3. Copy `assets/codex/agents/*.toml` into `~/.codex/agents/` (or a project's `.codex/agents/`). Standalone role files are discovered from that directory and need a `name` and a non-blank `developer_instructions`, or they are skipped with a startup warning. A role file accepts any `config.toml` key, so `model` and `model_reasoning_effort` live at its top level.
4. Leave `expose_spawn_agent_model_overrides` at its default so the lead can still choose a model and effort per spawn on this skill's instruction. Set it to false only when the user wants the `[agents]` defaults to be the sole author.
5. In the first session, spawn once and confirm the spawn tool shows `model` and `reasoning_effort`; `codex debug prompt-input` renders the prompt but not the tool schemas, so this cannot be checked statically.

### Spawn argument shape (V2)

```json
{"task_name": "scan_callers", "message": "...", "agent_type": "terra-scout"}
{"task_name": "impl_parser", "message": "...", "model": "gpt-5.6-sol", "reasoning_effort": "xhigh", "fork_turns": "none"}
```

Use `agent_type` for a pinned role and `model` plus `reasoning_effort` together for an ad-hoc assignment. `fork_turns` is `"none"`, `"all"`, or a positive integer string; a fresh-context worker uses `"none"`.

### Under codex-delegate

When another host launches a Codex run through `codex-delegate`, that skill owns the mission's model and effort. This skill applies inside the run only if the mission's lead is Astra and the packet allows internal subagents.

## Hermes Agent

Observed in a local Hermes configuration on 2026-09-20; confirm against the current Hermes documentation before relying on key names.

`delegation.model` and `delegation.provider` set one model for every delegated agent, so Hermes offers one delegated-agent model per configuration. Effort is per model: `agent.reasoning_effort` is the lead's level, and `agent.reasoning_overrides` maps a model name to an effort, for example `gpt-6-astra: high` beside `gpt-5.6-terra: xhigh`, which is the effort floor expressed in Hermes terms. The routing decision is therefore whether the configured delegation model fits the tier; when it does not, keep the work with the lead or ask the user to change `delegation.model` for the session, and state the inherited settings.

## OpenCode

Checked against `opencode.ai/docs/agents/` on 2026-09-20. Agents are defined under `agent.<name>` with their own `model`; unrecognized keys pass through to the provider, so `reasoningEffort` sets a subagent's effort where the provider supports it. `mode: subagent` marks a delegated agent and `permission.task` controls which agents may be spawned. Routes are per definition.

## Claude Code or Cursor Under an Astra Lead

An Astra lead in Claude Code or Cursor requires a proxy that exposes Astra as the session model; the proxy configuration observed for this pack exposed only GPT-5.6 models as subagent definitions. If such a session exists, the mechanics are those harnesses' and are documented in `fable5-model-routing`'s adapter reference; the routing policy is unchanged.

## Reporting and Measurement

State one line per task before spawning: tier, `agent_type`, resolved model, resolved effort, where the value was read, and `runtime confirmed` or `runtime unverified`. In Codex, "where the value was read" is the role file path, the `[agents]` key, or the spawn argument; a pinned role's advertisement in the tool description counts as confirmation of the pin, while an inherited effort stays unverified because nothing reports the child's applied level back to the lead.
