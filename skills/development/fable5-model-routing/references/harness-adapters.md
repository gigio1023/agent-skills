# Harness Adapters

The routing policy in `SKILL.md` is harness-neutral. This reference says how each harness actually sets a subagent's model and effort, what it cannot set, where the lane definitions go, and how to report what was resolved. Facts carry the date and version they were checked against; recheck them when the harness changes.

## Contents

- Generic procedure for any harness
- Claude Code
- Cursor
- Hermes Agent
- OpenCode
- Proxy-routed lanes
- Codex under a Fable lead
- Reporting and measurement

## Generic Procedure for Any Harness

Before the first spawn in an unfamiliar harness, establish four things and record them in `source-notes.md` with the date and version.

1. **Where a delegated agent's model is set.** Three places are common: an argument on the spawn call, a field in a per-agent definition file, or one global delegation setting. A harness may offer more than one, with a precedence order.
2. **Where its reasoning effort is set.** Check the same three places. Many harnesses set effort only per definition or only globally.
3. **Which lane shapes that allows.** Per-spawn control means the tier table can be applied directly and stated in the dispatch line. Per-definition control means install one definition per lane, then choose the definition. Global-only control means one lane; choose whether that lane is acceptable for the tier and state the inherited settings.
4. **Whether the runtime exposes the applied settings.** Look for a dispatch log, a hook, or a status view. If nothing exposes them, every dispatch line ends with `runtime unverified`.

If a lane cannot be given a different model or effort, the skill still governs the decision: say the inherited values, and do not spawn a below-frontier lane for judgment-adjacent work.

## Claude Code

Checked against Claude Code 2.1.278 and its documentation on 2026-09-20 (`code.claude.com/docs/en/sub-agents`, `code.claude.com/docs/en/model-config`, `code.claude.com/docs/en/agent-sdk/subagents`).

**Choosing the lane.** The Agent tool's `subagent_type` selects an agent definition; that is the primary control. Its `model` argument accepts the aliases `sonnet`, `opus`, `haiku`, and `fable`, and applies only to definitions that do not pin a model. There is no effort argument on the tool call.

**Definition fields.** A definition in `~/.claude/agents/<name>.md` (user) or `.claude/agents/<name>.md` (project) carries `model` (`sonnet`, `opus`, `haiku`, `fable`, a full model ID, or `inherit`) and `effort` (`low`, `medium`, `high`, `xhigh`, `max`; default inherits the session). Other fields such as `tools`, `disallowedTools`, `permissionMode`, and `maxTurns` bound the lane further. The Agent SDK's `AgentDefinition.effort` also accepts a number.

**Model resolution.** Per-invocation `model` → the definition's `model` (`inherit` means the main conversation's model) → `CLAUDE_CODE_SUBAGENT_MODEL` → the main conversation's model. `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` applies one model to every subagent, teammate, and workflow agent; set alone, it pins them to the main model. The env var alone does not move the built-in Explore and Plan agents.

**Effort resolution.** The session level comes from an explicit choice (`CLAUDE_CODE_EFFORT_LEVEL`, `--effort`, `/effort`), else a per-model hold that exists only for Fable 5, Opus 4.8, and Opus 4.7, else `modelSettings.<model>.effortLevel` in settings, else the model default (`high`, except Opus 4.7 at `xhigh`). A definition's `effort` overrides the session level but not the env var. `maxEffortLevel` caps every path; across settings files the lowest value wins, and `modelSettings.<model>.maxEffortLevel` replaces it per model. A definition without `effort` inherits the session level, which on a machine that saves `xhigh` for the lead model means `xhigh` for the lane.

**Aliases.** `fable` resolves to Fable 5.1 unless `ANTHROPIC_DEFAULT_FABLE_MODEL` overrides it; in Claude apps gateway sessions `fable` and `best` resolve to Fable 5. `opus` is Opus 5 and `sonnet` is Sonnet 5 on the Anthropic API; cloud providers map them differently.

**Caps and related settings.** `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` (default 20) and `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` (default 3) bound fan-out; the SDK adds `maxBudgetUsd`. `ultracode` is a setting, not an effort level: it sends `xhigh` and lets Claude orchestrate dynamic workflows. Since 2.1.277 a subagent's result reaches the lead under a header marking it as subagent output.

**Cost note.** Fable 5.1 cache reads cost half of Opus 5's per token, and cached input is the largest term in an agent loop. In a Fable-led session, escalating a lane to `fable` at `low` can cost less than escalating to `opus`.

**Installing the lanes.** Copy the files from `assets/agents/claude-code/` into `~/.claude/agents/` or the project's `.claude/agents/` after the user approves, then spawn with `subagent_type` set to the lane name. Edit a lane's `effort` line to lower it; add a definition rather than editing a shared one when a project needs a different floor.

**Measuring what ran.** Nothing in the Agent tool's result reports the applied effort. A `PostToolUse` hook matched on the `Agent` tool receives the call's input on stdin and can append it to a log; a command as small as `cat >> ~/.claude/dispatch-log.jsonl` records every dispatch with its `subagent_type` and `model`. Propose the hook; do not install it unasked. Without it, dispatch lines end with `runtime unverified`.

## Cursor

Checked against `cursor.com/docs/agent/subagents` on 2026-09-20.

A subagent file carries `name`, `description`, `model` (default `inherit`), `readonly`, and `is_background`. Model and effort travel together in the model string: `model: "claude-opus-5[effort=high]"`, with further options such as `context=300k` and `fast=false` combinable as `[effort=high,context=300k]`. An empty bracket pair such as `composer-2.5[]` selects the standard variant instead of the fast one, which is a cost difference. Options depend on the model and use the SDK's parameter names; the page does not enumerate which models accept `effort`, so confirm a Fable model string against a live `agent models` listing before relying on it. There is no per-invocation choice: the lane is which definition runs. The documentation fetched did not state the definition directory; verify it before installing.

## Hermes Agent

Observed in a local Hermes configuration on 2026-09-20; confirm against the current Hermes documentation before relying on key names.

`delegation.model` and `delegation.provider` set one model for every delegated agent, so Hermes offers a single delegation lane per configuration. Effort is set per model rather than per lane: `agent.reasoning_effort` is the lead's level, and `agent.reasoning_overrides` maps a model name to an effort, which is how the effort floor is expressed there, for example `gpt-5.6-terra: xhigh` beside `gpt-6-astra: high`. With this shape, the routing decision is whether the configured delegation model fits the tier of the work being delegated; when it does not, keep the work with the lead or ask the user to change `delegation.model` for the session, and state the inherited lane in the dispatch line.

## OpenCode

Checked against `opencode.ai/docs/agents/` on 2026-09-20.

Agents are defined in `opencode.json` under `agent.<name>` or as Markdown agent files, with `mode: subagent` for lanes. Each agent carries its own `model`, and unrecognized keys pass through to the provider, so `reasoningEffort` sets the lane's effort where the provider supports it. `permission.task` controls which agents may be spawned. Lanes are therefore per definition, as in Claude Code.

## Proxy-Routed Lanes

A proxy such as opencodex can expose second-family models as Claude Code agent definitions. Those definitions pin their model, ignore the Agent tool's `model` argument, and carry no `effort` field; the effort is fixed by the proxy's route, which typically names it, as in a `gpt-5.6-luna-medium` route. Treat them as fixed lanes: read the route's effort from the proxy's configuration or dashboard before claiming the floor holds, and until then report the lane's effort as unconfirmed. Such lanes are the practical way to give a Fable lead a GPT-5.6 worker for repository-heavy or high-volume work.

## Codex Under a Fable Lead

A Fable lead inside Codex is possible only through a proxy. If it occurs, the mechanics are Codex's: spawn arguments, `[agents]` defaults, and role files, documented with verified line references in `gpt6-astra-model-routing`'s adapter reference. The routing policy is unchanged.

## Reporting and Measurement

State one line per lane before spawning: tier, lane, resolved model, resolved effort, where the value was read, and `runtime confirmed` or `runtime unverified`. "Where the value was read" is a file path, a settings key, a proxy route, or the word `inherited` followed by the inherited value. Never describe the intended configuration as the one that ran.
