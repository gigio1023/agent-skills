# Source Notes

Last reviewed: 2026-07-10.

## Official Anthropic Sources

- [Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5)
- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Introducing Claude Fable 5 and Claude Mythos 5](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5)
- [Effort](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking)
- [Refusals and fallback](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback)
- [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- [Compaction](https://platform.claude.com/docs/en/build-with-claude/compaction)
- [Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

## Durable Translation

- Stronger instruction following favors short governing rules over exhaustive
  lists of variants.
- Fable 5 benefits from intent and handles difficult, ambiguous, long-horizon
  work; test it on the actual high end of the workload.
- Higher effort can improve verification but also encourage extra exploration.
  Pair it with clear scope and tune it with evals.
- Long runs need evidence-grounded progress, durable state, suitable timeouts,
  and a user-communication path.
- Subagents are useful for independent work, context isolation, specialization,
  and fresh verification, not as a default ceremony.
- Adaptive thinking, effort, thinking display, compaction, fallback, and memory
  are runtime features. Prompts should govern behavior, not imitate API settings.
- Requests to reproduce reasoning can trigger reasoning-extraction safeguards.
  Ask for evidence, decisions, and concise rationale instead.

## Maintenance Notes

Recheck the model introduction and prompting page together. The prompting page
owns behavioral guidance; the model page owns current API behavior such as
thinking configuration, stop reasons, supported features, and availability.
Keep changing parameter details in this reference and the runtime section rather
than duplicating them throughout prompt examples.
