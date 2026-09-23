# GPT-6 Runtime Notes

Verified against official OpenAI documentation and the Codex source on 2026-09-23. Recheck these settings before changing an integration. They describe the public API and Codex; other harnesses need their own documentation.

## Models And Effort

The [Astra model page](https://developers.openai.com/api/docs/models/gpt-6-astra) lists `gpt-6-astra` with reasoning efforts `low`, `medium`, `high`, `xhigh`, and `max`. The [Sol model page](https://developers.openai.com/api/docs/models/gpt-6-sol) lists `gpt-6-sol` with `none` through `max` and a default of `medium`. Do not infer `minimal` for either model, or `none` for Astra.

Codex reads its own catalog. The bundled catalog at CLI 0.156.1 lists `gpt-6-sol` with default `medium` and levels `low` through `ultra`; the 0.156.0 catalog lists only `gpt-6-astra`. A Codex `ultra` level is a harness setting, not an API effort.

## Migration Compatibility

The [GPT-6 migration quickstart](https://developers.openai.com/api/docs/guides/latest-model/gpt-6-astra.md#migration-quickstart) covers Astra, Sol, and Luna:

- Preserve the current effective effort where the model supports it. Astra has no `none`; use `low`. Sol supports `none`. A `minimal` baseline starts at `low`.
- Use Responses for tools. Astra supports Chat Completions but its tool calling requires Responses. Sol calls functions in Chat Completions only with `reasoning_effort: "none"`; use Responses for reasoning with tools.
- When effort is not `none`, remove `temperature`, `top_p`, and `top_logprobs`; also remove Chat Completions `logprobs` or Responses `include: ["message.output_text.logprobs"]` entries.
- For EU data residency, use Standard processing. Fast mode for Astra carries no latency SLA.
- From GPT-5.5 or earlier, migrate `prompt_cache_retention` to `prompt_cache_options.ttl: "30m"` and review cache behavior and billing.

Keep these compatibility changes distinct from edits to the prose prompt. The checklist is not a complete deployment configuration.

## Moving From GPT-5.6

This pack stopped using GPT-5.6 on 2026-09-23 and routes that work to Sol. OpenAI documented GPT-5.6's prompt tendencies, such as preferring shorter prompts and compressing output under generic brevity instructions, for GPT-5.6 only; do not carry them to GPT-6 unmeasured. Start from this package's patterns and evaluate on the Sol workload.

[Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model/gpt-6-astra.md) keeps the API capabilities GPT-5.6 had, including Programmatic Tool Calling, multi-agent orchestration, persisted reasoning, compaction, pro mode, and prompt caching. They stay runtime settings:

- `reasoning.mode: "pro"` selects pro execution for difficult tasks that tolerate latency; it is independent of `reasoning.effort` and is not a prompt instruction ([reasoning guide](https://developers.openai.com/api/docs/guides/reasoning#reasoning-mode)).
- `reasoning.context` selects whether earlier turns' reasoning is rendered into the next sample on supported models. Carry reasoning only while the objective and assumptions still hold; stale reasoning can anchor the model to an obsolete path.
- Programmatic Tool Calling fits bounded, deterministic reduction of large structured results. Keep direct calls for approvals, citations, semantic judgment, and steps where each result changes the next move.

## Changing Effort During A Conversation

The [reasoning guide](https://developers.openai.com/api/docs/guides/reasoning#change-reasoning-mid-conversation) supports `configuration_update` for the GPT-6 family in standard, single-agent mode. Insert the item before the next user message while retaining the original request-level `reasoning.effort` to preserve the cacheable prompt prefix. The updated effort persists until another update, and two updates may not sit next to each other. This changes effort only; check the current compatibility section before combining it with other modes.

The [prompt engineering guide](https://developers.openai.com/api/docs/guides/prompt-engineering#message-roles-and-instruction-following) also notes that `instructions` from a previous response are not inherited merely by passing `previous_response_id`. The integration must supply applicable instructions on the next request.

## Async Tools

With [async tool calling](https://developers.openai.com/api/docs/guides/async-tool-calling), set `async: true` on a function or custom tool definition. The application executes the tool and returns its eventual output with the original `call_id`. The model can work on independent steps in the meantime. This feature does not host the job or replace application state management.

Before adopting it, identify the result consumer, failure path, and completion condition. Keep dependent actions behind the actual result. Do not equate an async call with a completed action or with background response generation.

## Mid-Turn Steering

[Steering](https://developers.openai.com/api/docs/guides/steering) is available for the GPT-6 family over a Responses WebSocket connection. Send `response.steer` after `response.created`, identifying the original response with `previous_response_id`. Acceptance queues the input; it does not establish that the change has taken effect.

Steering does not retract emitted output, undo earlier actions, or cancel started tools. Track continuation and failure events, and return outstanding tool results or approvals required by the API. A prompt cannot supply this transport behavior on its own.
