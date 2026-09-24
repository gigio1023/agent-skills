# Source Notes

Last reviewed: 2026-07-10; Claude Opus guidance and GPT-6 sources added 2026-09-23.

This skill reflects the user's recurring need for sustained parallel work across coding, research, literature review, and value judgment, plus current public guidance from the major agent ecosystems.

## Current Sources

- Anthropic, `Prompting Claude Fable 5`: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5, and `Prompting Claude Fable 5.1`: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1
- Anthropic, `Prompting Claude Opus 5`: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
- Anthropic, `Prompting Claude Opus 5.5`: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5
- OpenAI, `Using GPT-6` (Astra, Sol, and Luna): https://developers.openai.com/api/docs/guides/latest-model/gpt-6-astra.md. The 2026-07-10 review read `Using GPT-5.6` and the GPT-5.6 Sol prompting guidance; this pack stopped using GPT-5.6 on 2026-09-23. GPT-6's guide notes that Astra may delegate less often than a workflow wants, so a packet or skill should say when to delegate.
- Anthropic Agent Skills authoring guidance: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- OpenAI Codex subagents: https://learn.chatgpt.com/docs/agent-configuration/subagents
- Anthropic Claude Code subagents: https://code.claude.com/docs/en/sub-agents

The model-generation update changed several defaults:

- Strong lead models can identify and sustain independent subagents more reliably. Parallelism may therefore be a normal execution optimization when the task clearly benefits; it is not limited to prompts that say "use subagents."
- 2026-09-25, owner decision: explicit user instructions about delegation still govern, and the lead's own decision to delegate is valued rather than gated. The description now also opens when the lead has decided on a multi-agent wave, and "the size of the fan-out is the user's call" became "an explicit user choice governs; without one, the lead decides". It still does not open merely because workstreams are independent, which keeps the 2026-08-07 lesson that situation-shaped descriptions over-trigger.
- Asynchronous communication and useful lead-agent work reduce blocking. Reuse long-lived agents for related follow-ups, but use fresh context when verifier independence matters.
- Programmatic tool calling is a better fit than subagents for bounded structured reduction with no semantic judgment between calls.
- Long-run progress must be audited against current tool results, artifacts, sources, or tests instead of worker self-report.
- Delegation never grants new authority for external writes, destructive work, purchases, or material scope expansion.

Claude Opus guidance, read 2026-09-23 (Opus 5.5 keeps the Opus 5 patterns as its starting point):

- Opus delegates readily, which multiplies cost and time on small tasks. Give delegation criteria or use the harness's deterministic caps; do not use subagents to verify or double-check the lead's own work, because the model already verifies and extra verification compounds cost. The Gotchas bullet on re-checking comes from this.
- On long multi-part tasks, Opus 5.5 can end a turn with a progress update instead of a tool call. A subagent's last message is its result, so such a turn can hand the lead a plan instead of an outcome. The duty to treat an announced next step as unfinished, and the packet rule on stop conditions, follow from this; the subagent case is an inference from the documented behavior, not an observed failure.
- Anthropic reports that small Opus 5.5 teams finish sooner when the harness appends elapsed time against a budget to each message it returns to the model, and that a tighter budget mainly keeps more agents working in parallel. That lever belongs to whoever builds the harness; a lead running inside Claude Code or Codex cannot append those lines, so this skill does not prescribe it.

## Patterns Kept

- One portable orchestration skill instead of separate harness-specific skills.
- Companion routing skills may provide exact model and cost preferences.
- Small first waves followed by narrower evidence-driven follow-ups.
- Explicit objective, scope, evidence, output, and stop contracts.
- Claim/evidence/confidence synthesis instead of summary concatenation.
- Disjoint ownership for parallel edits and fresh-context review where useful.

## Patterns Rejected

- Large catalogs of named specialist agents as a default interface.
- User-specific model policy inside this harness-neutral skill.
- Spawning agents for tiny sequential work or deterministic data reduction.
- Popularity or worker confidence as a substitute for direct evidence.
- Automatic background skill rewriting without deliberate evaluation.
- Pretending sequential work was parallel when the harness has no such capability.
