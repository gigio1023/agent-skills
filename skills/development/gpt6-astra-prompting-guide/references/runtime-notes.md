# Astra Runtime Notes

Verified against official OpenAI documentation on 2026-09-05. Recheck these
settings before changing an integration. They describe the public API;
harness-specific options require that harness's own documentation.

## Migration Compatibility

The [model page](https://developers.openai.com/api/docs/models/gpt-6-astra)
lists `gpt-6-astra` and reasoning efforts `low`, `medium`, `high`, `xhigh`,
and `max`. Do not infer support for `minimal`, `none`, or a harness's `ultra`.

The [Astra migration checklist](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra#migration-quickstart)
specifies:

- Move a `none` or `minimal` baseline to `low`; otherwise retain effective effort.
- Use Responses for tools. Chat Completions supports Astra but not tool calling.
- Remove `temperature`, `top_p`, and `top_logprobs`; also remove Chat Completions
  `logprobs` or Responses `include: ["message.output_text.logprobs"]` entries.
- For EU data residency, use Standard processing; Astra Fast mode is unavailable.
- From GPT-5.5 or earlier, migrate `prompt_cache_retention` to
  `prompt_cache_options.ttl: "30m"` and review cache behavior and billing.

Keep these compatibility changes distinct from edits to the prose prompt.
The checklist is not a complete deployment configuration.

## Changing Effort During A Conversation

The [reasoning guide](https://developers.openai.com/api/docs/guides/reasoning#change-reasoning-mid-conversation)
supports `configuration_update` for Astra in standard, single-agent mode.
Insert the item before the next user message while retaining the original
request-level `reasoning.effort` to preserve the cacheable prompt prefix.
The updated effort persists until another update. This changes effort only;
check the current compatibility section before combining it with other modes.

The [prompt engineering guide](https://developers.openai.com/api/docs/guides/prompt-engineering#message-roles-and-instruction-following)
also notes that `instructions` from a previous response are not inherited merely
by passing `previous_response_id`. The integration must supply applicable
instructions on the next request.

## Async Tools

With [async tool calling](https://developers.openai.com/api/docs/guides/async-tool-calling),
set `async: true` on a function or custom tool definition. The application
executes the tool and returns its eventual output with the original `call_id`.
The model can work on independent steps in the meantime. This feature does not
host the job or replace application state management.

Before adopting it, identify the result consumer, failure path, and completion
condition. Keep dependent actions behind the actual result. Do not equate an
async call with a completed action or with background response generation.

## Mid-Turn Steering

[Steering](https://developers.openai.com/api/docs/guides/steering) is available
for Astra over a Responses WebSocket connection. Send `response.steer` after
`response.created`, identifying the original response with
`previous_response_id`. Acceptance queues the input; it does not establish
that the change has taken effect.

Steering does not retract emitted output, undo earlier actions, or cancel
started tools. Track continuation and failure events, and return outstanding
tool results or approvals required by the API. A prompt cannot supply this
transport behavior on its own.
