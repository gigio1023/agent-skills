# Source Notes

Created: 2026-09-20. Updated 2026-09-23 for GPT-6 Sol.

## Mirror Note

The `Core` section of `SKILL.md` (three signals and four tiers, effort by model class, decision rules, dispatch statement) is shared word for word with `fable5-model-routing/SKILL.md`. Change both together and record the change here and there. Everything outside the core is family- or harness-specific and may diverge.

## Sources

OpenAI model and guidance pages, fetched 2026-09-20:

- `GPT-6 Astra` model page: https://developers.openai.com/api/docs/models/gpt-6-astra
- `GPT-5.6 Sol`, `Terra`, `Luna` model pages: https://developers.openai.com/api/docs/models/gpt-5.6-sol , https://developers.openai.com/api/docs/models/gpt-5.6-terra , https://developers.openai.com/api/docs/models/gpt-5.6-luna
- `Pricing`: https://developers.openai.com/api/docs/pricing
- `Using GPT-6 Astra` (retitled `Using GPT-6` by 2026-09-23): https://developers.openai.com/api/docs/guides/latest-model/gpt-6-astra.md (the subagent section tunes how much to delegate and names no worker model)
- `Rethinking skills and prompts for GPT-6 Astra`: https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra
- Codex `Subagents`: https://learn.chatgpt.com/docs/agent-configuration/subagents (on 2026-09-20, role-to-model guidance for the GPT-5.6 family: the flagship for ambiguous multi-step work, Terra for exploration and read-heavy scans, Luna for clear, repeatable, high-volume work; a warning about parallel write-heavy workflows. On 2026-09-23 the page said to start most tasks with `gpt-6-sol`, use `gpt-6-luna` for fast, narrowly scoped work, and start explicit settings at `medium` for Sol)
- Codex `Config reference`: https://learn.chatgpt.com/docs/config-file/config-reference
- Codex `Build skills`: https://learn.chatgpt.com/docs/build-skills.md

Fetched 2026-09-23 for the GPT-6 Sol move:

- `GPT-6 Sol` model page: https://developers.openai.com/api/docs/models/gpt-6-sol (efforts `none` through `max`, default `medium`)
- API changelog, Sep 22 entry: https://developers.openai.com/api/docs/changelog (GPT-6 Sol and Luna released)
- Codex `codex-rs/models-manager/models.json` at `rust-v0.156.0` (only `gpt-6-astra`) and `rust-v0.156.1` (adds `gpt-6-sol`, default `medium`, levels `low` through `ultra`, V2)
- Hermes Agent v0.21.3 source: `tools/delegate_tool_config.py` lines 494-507 (child effort from `delegation.reasoning_effort`, else the parent's resolved effort) and `hermes_cli/config_defaults.py`

Codex source, read at tag `rust-v0.154.0` on 2026-09-20 (the installed CLI was 0.154.0):

- `codex-rs/core/src/tools/handlers/multi_agents_spec.rs` (spawn tool schemas, V1 and V2, the override exposure gate at lines 111-114)
- `codex-rs/core/src/tools/handlers/multi_agents_common.rs` (precedence at 274-276, catalog default fallback at 306-308, effort validation at 422-442, model lookup at 400-406)
- `codex-rs/core/src/tools/handlers/multi_agents_v2/spawn.rs` (override application at 128 before fork handling at 136-143)
- `codex-rs/core/src/config/mod.rs` (V2 config defaults at 1307-1308, version resolution at 1544-1552, concurrency at 2704-2713)
- `codex-rs/core/src/session/multi_agents.rs` (usage hints and the delegation mode at 166-199)
- `codex-rs/core/src/agent/role.rs` (role application at 185-193, lock advertisement at 314-317, built-ins at 338-403)
- `codex-rs/agent-roles/src/agent_role_config.rs` and `loader.rs` (role file shape and discovery)
- `codex-rs/protocol/src/openai_models/reasoning_effort.rs` (the `ultra` wire rewrite)
- `codex-rs/core/src/agent/control/service_tier.rs`, `codex-rs/ext/goal/src/accounting.rs`, `codex-rs/ext/goal/src/extension.rs`
- `codex-rs/skills/src/parser.rs` (skill frontmatter fields)

Runtime checks on the authoring machine, 2026-09-20: `codex debug models` and `codex debug models --bundled` (catalog values), `codex features list` (`multi_agent` on, `multi_agent_v2` off), `codex debug prompt-input` (prompt text only; a V1 model rendered without the multi-agent role block, V2 models with it and with the override guidance present at default settings).

Other harnesses:

- Hermes Agent: configuration keys (`delegation.model`, `delegation.provider`, `agent.reasoning_effort`, `agent.reasoning_overrides`) observed in a local configuration on 2026-09-20. The delegation and Kanban documentation pages were read the same day for vocabulary, not for a key-by-key check of that configuration. The source check on 2026-09-23 (above) showed that children take `delegation.reasoning_effort`, not the per-model overrides.
- OpenCode `Agents`: https://opencode.ai/docs/agents/

Community packages read for patterns: matteoscurati/delegation-kit (Codex role files `astra-judge`, `terra-builder`, `luna-clerk` with the inverted effort curve and a Sol lead that consults Astra), AqueGen/model-routing (dispatch logging and the one-step retry rule), obra/superpowers strict-cost design spec (pre-registered failures of cheap models on judgment).

## Values as Read on 2026-09-20

Prices per million tokens, standard tier, input and output: Astra $10 and $50 with cache reads at $1; Sol $4 and $20; Terra $2 and $12; Luna $0.20 and $1.20. Fast mode is twice standard on every line; batch and flex are half. Requests over 272K input tokens bill input at twice and output at one and a half times. No `-pro` model IDs exist; pro mode is a reasoning mode.

Served Codex catalog (`codex debug models`, afternoon): Astra default `medium`, levels `low` through `ultra`, V2, `multi_agent_reasoning_effort: xhigh`; Sol default `low`, V2; Terra default `medium`, V2; Luna default `medium`, V2, `multi_agent_reasoning_effort: xhigh`. The same file read that morning had Luna at V1 without `ultra`, and the bundled catalog has Astra's default at `low`. Codex reports a 272K context window with an 872K opt-in; the API pages list 1,050,000.

## Values as Read on 2026-09-23

Prices per million tokens, standard tier: GPT-6 Sol $2 input, $0.20 cached input, $2.50 cache writes, $10 output; Astra unchanged at $10, $1, $12.50, and $50. GPT-6 Luna ($0.10 and $0.50) is listed but not used by this pack. The served catalog on Codex 0.154.0 had Luna back at V1 without `ultra`; Astra `medium`, GPT-5.6 Sol `low`, and Terra `medium` were unchanged.

## Durable Translation

- Inheritance is the default in every surface checked, so an Astra lead's cost problem is solved by naming the worker, not by tuning the lead.
- Under the owner's effort floor, workers below the frontier run at `xhigh`; the choice that saves money is GPT-6 Sol instead of Astra, and Astra at `high` instead of the session effort when Astra is the worker.
- Codex offers per-spawn, per-role, and per-session control, so it can execute the tier table directly. The two silent failures to guard are model-without-effort and trusting the fork sentence.
- Skill text is authorization in Codex: the spawn tool and the delegation mode both accept "skill instructions" as the explicit request they require. The `When It Applies` section exists to supply that request only after the lead has decided to delegate.

## Policy History

- 2026-09-23: the owner stopped using GPT-5.6 models. Every worker route now runs GPT-6 Sol at `xhigh`, GPT-6 Luna is not used, and the roles `terra-scout` and `luna-clerk` became `sol-scout` and `sol-clerk`; `sol-builder` keeps its name on the new model. The `[agents]` default moved to `gpt-6-sol`, which needs Codex CLI 0.156.1 or later. The shared core's below-frontier list now reads Opus 5.5 and Opus 5, Sonnet 5, and GPT-6 Sol (edited in both routing skills). The Hermes effort mechanism was corrected from source.
- 2026-09-23: the shared core's below-frontier list names Claude Opus 5.5 and Opus 5, mirroring the Opus refresh recorded in `fable5-model-routing`'s source notes.
- 2026-09-20: created as the GPT-family sibling of `fable5-model-routing`, keyed to the lead model rather than a harness, with the shared core mirrored and Codex as the verified adapter. Measurement of the default routes on cost or quality has not been done. Vocabulary follows the repository's `terminology.md`: subagent, subagent definition or role, task, dispatch, route, tier; "lane" is not used.

## Not Verified

- The live spawn tool schema under an Astra lead; inferred from source defaults and the rendered usage hint, not observed.
- Whether the served catalog's `model_messages.multi_agent` replaces the delegation-mode texts on a given machine.
- Whether a managed or enterprise configuration layer overrides the `[agents]` keys.
- A live spawn of `gpt-6-sol` in Codex; the installed CLI on 2026-09-23 was 0.154.0, which does not list the model.
- Any effect of these defaults on cost or quality.
