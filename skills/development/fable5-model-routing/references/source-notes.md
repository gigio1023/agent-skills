# Source Notes

Last updated: 2026-09-17.

## Sources

Model-generation guidance:

- Anthropic, `Prompting Claude Fable 5.1`: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1
- Anthropic, `What's new in Claude Fable 5.1`: https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1
- Anthropic, `Prompting Claude Fable 5`: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5
- Anthropic, `Effort`: https://platform.claude.com/docs/en/build-with-claude/effort
- Anthropic, `Steering thinking`: https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost
- Anthropic, `Models overview`: https://platform.claude.com/docs/en/models/overview
- OpenAI, `Using GPT-5.6`: https://developers.openai.com/api/docs/guides/latest-model.md
- OpenAI, `Prompting guidance for GPT-5.6 Sol`: https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6.md

Harness mechanics for per-subagent model and effort:

- Claude Code, `Create custom subagents` (frontmatter `model` and `effort`, Agent tool `model` argument, `CLAUDE_CODE_SUBAGENT_MODEL`): https://code.claude.com/docs/en/sub-agents
- Claude Code, `Model configuration` (the `fable` alias, effort resolution order, frontmatter effort overrides the session level): https://code.claude.com/docs/en/model-config
- Cursor, `Subagents` (`model: inherit` or `<id>[effort=...]`): https://cursor.com/docs/agent/subagents

## Durable Translation

- Fable can lead difficult, ambiguous, long-horizon work and dependable subagent coordination. Do not preserve the old assumption that it should only see a compact final evidence packet.
- GPT-5.6 Sol is a flagship tool-using support option, not merely a cheap raw search lane. Assign it bounded repository, implementation, evidence, or independent-review work when its harness is a better fit.
- Delegate for concurrency, context isolation, verification, specialization, or a measured efficiency win. Stronger default models reduce the need for procedural micromanagement but not the need for evidence and scope boundaries.
- Effort is the primary intelligence, latency, and cost control on Fable, and its level names do not mean the same amount of thinking across models. `high` is the default wherever effort is supported (Haiku 4.5 has no effort parameter); `low` is documented as the setting for subagents and simpler tasks; `xhigh` is for long agentic runs; `max` is prone to overthinking. At `low`, Fable 5.1 searches less. Fable 5.1 at `low` is often competitive on cost per task with Opus- and Sonnet-class models at higher effort.
- Claude Code sets a subagent's model per invocation but, as of v2.1.271, its effort only through an agent definition's `effort` field. Cursor sets both through the definition's `model` string. The skill therefore says what to choose and requires the lead to report what the harness actually applied.
- Long-run status must be grounded in current tool results. Never ask Fable to reproduce private reasoning; that triggers the reasoning-extraction refusal category.

## Policy Change on 2026-09-17

Until 2026-09-17 the skill opened only on an explicit request ("put Fable on the judgment"), a policy set on 2026-08-07 while the skill lived in gigio-pack, where an unrequested opening meant switching the lead model. The owner changed the policy on 2026-09-17: when Fable is already the main session model in Claude Code or Cursor, the skill is a standing policy, and every subagent dispatch carries a model and effort chosen for its difficulty. The reasoning is that under a Fable lead the costly action, changing who leads, has already happened by the user's choice; what remained unmanaged was lanes inheriting the lead's model and effort by omission. The on-request entry is kept for sessions led by another model, where opening a Fable lane still lands on the bill.

The skill does not decide whether to delegate; `orchestrate-subagents` and the lead's own judgment do. Measurement of the standing policy's effect on cost and quality has not been done; revisit after real sessions show whether the stated assignments drew corrections.

## Separation From Neighbors

- `orchestrate-subagents` is harness-neutral and owns decomposition, packets, coordination, conflict handling, and synthesis mechanics. It consumes this skill as the companion routing policy for exact model names and effort.
- `small-model-handoff` owns the bounded prompt when the chosen lane is a weaker executor.
- `fable5-model-routing` is model-role and effort policy. It decides which lane owns which work and at what setting.

The final answer remains the lead's synthesis, not a transcript of workers.
