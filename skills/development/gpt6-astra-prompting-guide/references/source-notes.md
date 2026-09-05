# Source Notes

Last reviewed: 2026-09-05.

## Official Sources And Coverage

| Source | Sections used | Package coverage |
| --- | --- | --- |
| [Using GPT-6 Astra](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra) | Prompting best practices; migration quickstart | Five behavior tendencies; autonomy, loaded instructions, style, delegation, verification; compatibility checklist |
| [GPT-6 Astra model](https://developers.openai.com/api/docs/models/gpt-6-astra) | Model identity and supported reasoning effort | Exact API model and effort values |
| [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering) | Message roles and instruction following; message formatting; evaluation advice | Authority boundaries, context separation, instruction continuity, behavior validation |
| [Reasoning models](https://developers.openai.com/api/docs/guides/reasoning#change-reasoning-mid-conversation) | Change reasoning mid-conversation | Configuration updates and their compatibility limits |
| [Async tool calling](https://developers.openai.com/api/docs/guides/async-tool-calling) | How async tools work | Tool definition, application ownership, result correlation |
| [Mid-turn steering](https://developers.openai.com/api/docs/guides/steering) | Send a steering message; return tool results or approval; handle failures | WebSocket requirement and limits on already-started work |

## Interpretation Boundary

The main guide's five tendencies are official observations. The diagnostic
workflow, prompt clauses, template, worker ownership fields, and validation
reporting rules are this package's operational adaptations. They are not
OpenAI-certified prompts or independently measured performance improvements.

The Sol skill supplies a familiar package layout, not evidence for Astra
behavior. In particular, do not carry its compression, tool-count, or reasoning
defaults forward without Astra-specific support.

The user-over-skill guideline in the Astra guide concerns skill guidance; it
does not reverse the API instruction hierarchy. Apply message authority and
application permission boundaries when adapting that advice.

## Maintenance

Open the model-specific guide and confirm that its body identifies Astra.
The unqualified `latest-model` route can change to a different model. Search
official OpenAI documentation for the exact model if the recorded route moves
or returns an incomplete body; do not infer a new slug from an old pattern.

Recheck runtime claims before an API migration. If sources conflict, report
the exact disagreement and avoid an unsupported example. If live retrieval is
unavailable, label this dated snapshot as the fallback. Record the review date
after checking the pages, not merely after editing this file.
