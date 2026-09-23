# Source Notes

Last reviewed: 2026-09-17.

## Official Anthropic Sources

Model-specific prompting:

- [Prompting Claude Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1)
- [Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5)
- [What's new in Claude Fable 5.1](https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1)
- [Claude Fable 5.1 migration guide](https://platform.claude.com/docs/en/models/fable-5-1/migration-guide)
- [Introducing Claude Fable 5 and Claude Mythos 5](https://platform.claude.com/docs/en/models/fable-5/introducing-claude-fable-5-and-claude-mythos-5)
- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

Runtime behavior:

- [Effort](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Steering thinking](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost)
- [Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)
- [Preserved thinking](https://platform.claude.com/docs/en/build-with-claude/preserved-thinking)
- [Mid-conversation system messages](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages)
- [Refusals and fallback](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback)
- [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- [Compaction](https://platform.claude.com/docs/en/build-with-claude/compaction)
- [Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
- [Models overview](https://platform.claude.com/docs/en/models/overview)
- [Claude Code model configuration](https://code.claude.com/docs/en/model-config) for the `fable` alias and effort resolution
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

## Durable Translation

- Stronger instruction following favors short governing rules over exhaustive lists of variants.
- Fable benefits from intent and handles difficult, ambiguous, long-horizon work; test it on the actual high end of the workload.
- Higher effort can improve verification but also encourage extra exploration. Pair it with clear scope and tune it with evals. Effort level names do not correspond to the same amount of thinking across models.
- Long runs need evidence-grounded progress, durable state, suitable timeouts, and a user-communication path.
- Subagents are useful for independent work, context isolation, specialization, and fresh verification, not as a default ceremony. A non-blocking spawn tool plus a separate wait tool lets the lead keep working.
- Adaptive thinking, effort, thinking display, compaction, fallback, memory, and history handling are runtime features. Prompts should govern behavior, not imitate API settings.
- Requests to reproduce reasoning trigger the reasoning-extraction refusal category. Ask for evidence, decisions, and concise rationale instead.

## Fable 5.1 Deltas (2026-09-01 release)

Behavior that moved and now has a clause in `prompt-patterns.md`: fewer user-facing progress updates; one tool call per turn in loops with implied reads; denser prose in places; less formatting in chat; unmarked quotations in summaries; whole-file rewrites for small edits; fewer search calls at `low` effort; longer thinking before long deliverables at `xhigh` and `max`; unrequested fixes and extra test files on open-ended implementation.

API changes that are harness work, not prompt work: forced `tool_choice` returns 400; thinking blocks are bound to the producing conversation and to that model or newer, so history must be append-only (enforced for accounts created on or after 2026-08-31, with `thinking-binding-controls-2026-08-01` controls); per-message effort (beta `mid-conversation-output-config-2026-07-01`); turn-scoped system messages (beta `mid-conversation-system-clear-at-2026-08-21`); `thinking.display: "updates"` (beta `thinking-display-updates-2026-08-18`); cache reads at a quarter of the Fable 5 rate; server-side `fallbacks: "default"` (beta `server-side-fallback-2026-07-01`), whose permitted targets the Models API publishes per model as `allowed_fallback_models` (Opus 4.8 and Opus 5 on 2026-09-17). Added 2026-09-23 from the Opus 5.5 pages: on the Claude API, Fable 5.1 and Mythos 5.1 read Opus 5.5 thinking blocks, so a conversation escalated from Opus 5.5 to Fable 5.1 keeps its reasoning; Opus 5.5 does not read Fable blocks.

Unchanged from Fable 5: adaptive thinking always on, `display: "omitted"` default, no prefill, no sampling parameters, 512-token minimum cacheable prefix, same tokenizer, same base prices, 30-day data retention.

## Maintenance Notes

Recheck the Fable 5.1 prompting page, the Fable 5 prompting page, and the what's-new page together. The prompting pages own behavioral guidance; the what's-new and model pages own current API behavior such as thinking configuration, stop reasons, supported features, and availability. Keep changing parameter details in this reference and the runtime section rather than duplicating them throughout prompt examples. Official prompt snippets are copied verbatim into `prompt-patterns.md` so a reader can paste them; re-copy when the source page changes.
