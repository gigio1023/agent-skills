# Source Notes

Last reviewed: 2026-07-10.

## Primary Sources

- Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Anthropic, [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Anthropic, [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- OpenAI Agents SDK, [Handoffs](https://openai.github.io/openai-agents-js/guides/handoffs/)
- OpenAI Agents SDK, [Handoff prompt](https://openai.github.io/openai-agents-python/ref/extensions/handoff_prompt/)
- LangGraph, [Multi-agent collaboration](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/multi-agent-collaboration/)
- Microsoft AutoGen, [Handoffs](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/design-patterns/handoffs.html)

## Durable Translation

- A handoff is a state transfer, not a transcript. The next agent needs the
  current objective, decisions, artifacts, evidence, and next actions.
- Long-running work benefits from durable state artifacts alongside repository
  history. Conversation compaction alone may not preserve enough operational
  detail for a fresh session.
- Context is finite. Point to high-signal artifacts and let the successor fetch
  detail on demand instead of embedding every log and file.
- Runtime handoffs often transfer conversation context automatically. A file
  handoff must make that state explicit and portable across harnesses.
- The receiving agent needs a clear operating contract, authority boundary,
  stopping condition, and verification bar, not only a description of past work.

## Maintenance Notes

Recheck these sources when agent runtimes materially change their session state,
compaction, memory, or handoff behavior. Keep runtime-specific tool names out of
the portable prompt unless the generated handoff targets that exact runtime.
