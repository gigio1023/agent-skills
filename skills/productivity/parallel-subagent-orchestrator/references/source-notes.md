# Source Notes

Last reviewed: 2026-07-10.

This skill reflects the user's recurring need for sustained parallel work across
coding, research, literature review, and value judgment, plus current public
guidance from the major agent ecosystems.

## Current Sources

- Anthropic, `Prompting Claude Fable 5`:
  https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5
- OpenAI, `Using GPT-5.6`:
  https://developers.openai.com/api/docs/guides/latest-model.md
- OpenAI, `Prompting guidance for GPT-5.6 Sol`:
  https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6.md
- Anthropic Agent Skills authoring guidance:
  https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- OpenAI Codex subagents:
  https://learn.chatgpt.com/docs/agent-configuration/subagents
- Anthropic Claude Code subagents:
  https://code.claude.com/docs/en/sub-agents

The model-generation update changed several defaults:

- Strong lead models can identify and sustain independent lanes more reliably.
  Parallelism may therefore be a normal execution optimization when the task
  clearly benefits; it is not limited to prompts that say "use subagents."
- Asynchronous communication and useful lead-agent work reduce blocking. Reuse
  long-lived agents for related follow-ups, but use fresh context when verifier
  independence matters.
- Programmatic tool calling is a better fit than subagents for bounded
  structured reduction with no semantic judgment between calls.
- Long-run progress must be audited against current tool results, artifacts,
  sources, or tests instead of worker self-report.
- Delegation never grants new authority for external writes, destructive work,
  purchases, or material scope expansion.

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
- Pretending sequential work was parallel when the harness has no such
  capability.
