# Source Notes

Last reviewed: 2026-07-10.

## Official OpenAI Sources

- [Using GPT-5.6](https://developers.openai.com/api/docs/guides/latest-model.md)
- [Prompting guidance for GPT-5.6 Sol](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6.md)
- [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)
- [Programmatic Tool Calling](https://developers.openai.com/api/docs/guides/tools-programmatic-tool-calling)
- [Multi-agent](https://developers.openai.com/api/docs/guides/tools-multi-agent)
- [Reasoning](https://developers.openai.com/api/docs/guides/reasoning)
- [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)
- [Conversation state](https://developers.openai.com/api/docs/guides/conversation-state)
- [OpenAI Model Spec: chain of command](https://model-spec.openai.com/2025-02-12.html#chain_of_command)

## Durable Translation

- GPT-5.6 Sol benefits from outcome, constraints, evidence, and completion bars more than accumulated procedural scaffolding.
- Shorter prompts and smaller tool sets are the default hypothesis; retain extra instructions only when representative evals show they add value.
- Generic brevity can suppress required artifacts. Prioritize content instead.
- Autonomy and permission boundaries should be compact and non-repetitive.
- Programmatic Tool Calling is for bounded deterministic reduction, not a default for every multi-call workflow.
- Reasoning effort, pro mode, persisted reasoning, cache policy, and tool eligibility are runtime controls. Prompts should state the task contract.
- Optimize the final user-visible result. Fewer calls, turns, or tokens are not improvements when required evidence or completeness regresses.

## Maintenance Notes

Fetch the latest model guide first. It declares the current model alias and the canonical migration and prompting guides. Recheck API parameters and deprecation timelines before changing runtime examples; keep time-sensitive facts in this reference rather than duplicating them throughout the skill.
