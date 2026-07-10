# Source Notes

Last updated: 2026-07-10.

Current model-generation sources:

- Anthropic, `Prompting Claude Fable 5`:
  https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5
- OpenAI, `Using GPT-5.6`:
  https://developers.openai.com/api/docs/guides/latest-model.md
- OpenAI, `Prompting guidance for GPT-5.6 Sol`:
  https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6.md

The durable translation is:

- Fable 5 can lead difficult, ambiguous, long-horizon work and dependable
  subagent coordination. Do not preserve the old assumption that it should only
  see a compact final evidence packet.
- GPT-5.6 Sol is a flagship tool-using support option, not merely a cheap raw
  search lane. Assign it bounded repository, implementation, evidence, or
  independent-review work when its harness is a better fit.
- Delegate for concurrency, context isolation, verification, specialization, or
  a measured efficiency win. Stronger default models reduce the need for
  procedural micromanagement but not the need for evidence and scope boundaries.
- Long-run status must be grounded in current tool results. Never ask Fable 5 to
  reproduce private reasoning; that can trigger reasoning-extraction safeguards.

This skill remains separate from `parallel-subagents`:

- `parallel-subagents` is harness-neutral and owns decomposition,
  packets, coordination, conflict handling, and synthesis mechanics.
- `fable5-judgment` is model-role policy. It decides when Fable 5
  should lead directly and when another configured lane has a concrete advantage.

The final answer remains the lead's synthesis, not a transcript of workers.
