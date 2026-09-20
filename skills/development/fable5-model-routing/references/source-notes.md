# Source Notes

Last updated: 2026-09-20.

## Mirror Note

The `Core` section of `SKILL.md` (three signals and four tiers, effort by model class, decision rules, dispatch statement) is shared word for word with `gpt6-astra-model-routing/SKILL.md`. Change both together and record the change here and there. Everything outside the core is family- or harness-specific and may diverge.

## Sources

Anthropic model and effort guidance, fetched 2026-09-20:

- `Prompting Claude Fable 5.1`: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1
- `What's new in Claude Fable 5.1`: https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1
- `Prompting Claude Opus 5`: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
- `Effort`: https://platform.claude.com/docs/en/build-with-claude/effort
- `Optimizing for cost and intelligence`: https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence
- `Models overview`: https://platform.claude.com/docs/en/models/overview
- `Pricing`: https://platform.claude.com/docs/en/about-claude/pricing
- `How we built our multi-agent research system` (2025-06-13): https://www.anthropic.com/engineering/multi-agent-research-system
- `Building multi-agent systems: when and how to use them` (2026-01-23): https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them

Harness mechanics, fetched 2026-09-20:

- Claude Code `Create custom subagents`: https://code.claude.com/docs/en/sub-agents
- Claude Code `Model configuration`: https://code.claude.com/docs/en/model-config
- Claude Code `Changelog` (2.1.272 to 2.1.278): https://code.claude.com/docs/en/changelog
- Claude Agent SDK `Subagents`: https://code.claude.com/docs/en/agent-sdk/subagents
- Cursor `Subagents`: https://cursor.com/docs/agent/subagents
- OpenCode `Agents`: https://opencode.ai/docs/agents/
- Hermes Agent: observed configuration keys (`delegation.model`, `delegation.provider`, `agent.reasoning_effort`, `agent.reasoning_overrides`) on 2026-09-20; documentation not re-fetched.
- Per-invocation effort requests: anthropics/claude-code issues #43083 (closed completed, shipped the frontmatter `effort` field) and #72596 (closed not planned).

Routing evidence outside vendor docs:

- SWE-Router (Son et al., 2026, arXiv:2607.00053): prompt-only routing of agentic coding tasks has a Bayes-error floor; conditioning on three exploratory turns of trajectory improves routing.
- Routing collapse (Lai and Ye, 2026, arXiv:2602.03478): learned routers send nearly all near-tie queries to the strongest model.
- Self-correction illusion (Chen et al., 2026, arXiv:2606.05976): the same error relabeled as external input is corrected far more often than when it appears as the model's own thought.
- InflationAgent (Fu et al., 2026, arXiv:2608.13571): retry inflation on cheap models of roughly three to four times single-call cost.
- OpenAI Codex `Subagents`: https://learn.chatgpt.com/docs/agent-configuration/subagents (read-heavy work for subagents; role-to-model guidance for the GPT-5.6 family).
- Community packages read for patterns: matteoscurati/delegation-kit (mirrored Claude and Codex lanes with an inverted effort curve), AqueGen/model-routing (dispatch-logging hook and one-step retry rule), obra/superpowers strict-cost design spec (pre-registered failures of cheap models on judgment).

## Measured Numbers Behind the Rules

From Anthropic's cost and intelligence page, on its own benchmarks with unpublished protocols; first-party, unreplicated:

| Configuration | SWE-bench Pro solved | Cost per solved task |
|---|---|---|
| Opus 5 at `low` | 84.0% | $0.25 |
| Fable 5.1 at `low` | 88.6% | $0.54 |
| Sonnet 5 at default | 77.4% | $0.84 |
| Opus 5 at default | 91.7% | $1.01 |
| Fable 5.1 at default | 92.1% | $1.19 |

- Research and knowledge benchmarks: `medium` saved 13 to 31 percent of cost for one to three points; the default bought nothing measurable over `medium`. Long-horizon coding: `medium` cost about two points for half the spend, `low` about eight points for a quarter.
- "Sweep effort on your current model first." On one search benchmark a single model at `low` matched an orchestrator with a Sonnet 5 worker at 29 percent lower cost.
- Opus 5 at `low` with its failures re-run at default matched the default pass rate for half the cost, conditioned on a checker that does not pass bad work.
- Two of twenty problems carried 43 percent of one run's spend; compare models on the hardest tenth of tasks.
- Prices on 2026-09-20 per million tokens, input and output: Fable 5.1 $10 and $50 with cache reads at $0.25; Opus 5 $5 and $25 with cache reads at $0.50; Sonnet 5 $2 and $10; Haiku 4.5 $1 and $5 with no effort parameter and a 200K context.

Guidance statements the rules rest on:

- Effort page: `low` is for "simpler tasks that need the best speed and lowest costs, such as subagents"; `xhigh` is for long-running agentic work with token budgets in the millions.
- Fable 5.1 page: at `low` it calls search and retrieval tools less often; at `xhigh` and `max` it may think long before a long deliverable, so run those at `high`; at `low` it is often competitive on cost per task with Opus and Sonnet at higher effort.
- Opus 5 page: it delegates readily and verifies its own work unprompted; instructions to use a subagent to verify cause over-verification, and the recommended delegation line says not to use subagents to verify or double-check its own work.
- Models overview: Anthropic recommends starting with Opus 5 for most workloads and reaching for Fable 5.1 for demanding reasoning and long-horizon agentic work.
- Multi-agent posts: the 2025 post pairs an Opus lead with Sonnet workers, scales subagent count with task complexity, and reports roughly fifteen times chat token use; the 2026 post gives no model-role guidance and reports three to ten times single-agent use.

## Durable Translation

- Fable can lead difficult, long-horizon work and coordinate subagents; delegate for concurrency, isolation, fresh verification, tool fit, or a measured efficiency gain, not to keep the lead's context empty.
- Effort is the main intelligence, latency, and cost control, and level names do not transfer across models. Below the frontier the owner's policy fixes `xhigh` as the floor; the vendor numbers above show what lowering a lane would buy and are kept for that decision.
- The lane definitions exist because Claude Code sets a subagent's effort only through a definition. A skill that names efforts without shipping definitions cannot execute its own table.
- Reporting must distinguish what was read from what ran. No current harness in this reference exposes a subagent's applied effort without a hook.

## Policy History

- 2026-08-07: opened only on explicit request, because an unrequested opening meant switching the lead model.
- 2026-09-17: standing policy when Fable already leads in Claude Code or Cursor; on-request path kept for other leads.
- 2026-09-20: scope keyed to the lead model rather than the harness, with harness mechanics moved to adapters. Effort floor of `xhigh` for models below the frontier, adjustable per lane. Lane definitions shipped as assets. Verifier lane reframed as a fresh-context specification check after the Opus 5 guidance. Packet templates and the long judgment checklist removed in favor of `orchestrate-subagents` and the dispatch statement. Measurement of any of these policies on cost or quality has not been done.

## Not Verified

- Cursor's subagent definition directory and which model strings accept `effort`.
- Hermes documentation for the observed keys.
- Which effort a proxy-routed lane runs at; it is read from the route, not observed.
- The exact inheritance path for a `sonnet` or `haiku` lane on a machine that saves `modelSettings` only for other models; the documentation says a definition without `effort` inherits the session level.
