# Source Notes

Prompting sources reviewed on 2026-09-14. Runtime references retain their 2026-09-05 snapshot and were not reverified for this instruction-design revision.

## Prompting Sources

| Source | Sections checked | Package coverage |
| --- | --- | --- |
| [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), Eric Provencher, September 11, 2026 | Better skills; Up-to-date AGENTS.md; Decision boundaries; Persistence | Short task-specific descriptions, progressive disclosure, reconsidering recipes, conditional repository reading, permission and completion boundaries |
| [Using GPT-6 Astra](https://developers.openai.com/api/docs/guides/latest-model/gpt-6-astra.md#prompting-best-practices) | Prompting best practices | Initiative, instruction following, writing style, subagent delegation, proportional verification |

The article informs both the advice this skill produces and the package's own design:

| Article guidance | Application in this package |
| --- | --- |
| Short descriptions with clear applicability; excessive descriptions can be shortened by Codex | The description leads with the Astra instruction task and omits the behavior inventory |
| Use progressive disclosure for multiple workflows | The entry point routes to instruction design, prompt patterns, the template, runtime notes, or sources by need |
| Reconsider elaborate itineraries and model-specific assumptions | The working path uses outcome and constraints; the template has no compulsory plan, delegation phase, or first-pass review gate |
| Read repository documents when the task needs them | Instruction design uses conditional links and distinguishes narrow edits from requested stack audits |
| Revisit ask-first boundaries and redundant test encouragement | Prompt patterns reuse existing authorization and tie further checks to changed behavior or unresolved evidence |
| Define completion before stopping | The template and persistence pattern include the requested execution, inspection, repair, and observable stopping condition |

## Runtime And Foundational Sources

The following supporting material was recorded as verified on 2026-09-05. Reopen the relevant source before changing an integration; this table does not mark the entire runtime current.

| Source | Recorded coverage |
| --- | --- |
| [Astra migration quickstart](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra#migration-quickstart) | API compatibility checklist |
| [GPT-6 Astra model](https://developers.openai.com/api/docs/models/gpt-6-astra) | Model identity and supported reasoning effort |
| [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering) | Message authority, context separation, instruction continuity, evaluation advice |
| [Reasoning models](https://developers.openai.com/api/docs/guides/reasoning#change-reasoning-mid-conversation) | Configuration updates and compatibility limits |
| [Async tool calling](https://developers.openai.com/api/docs/guides/async-tool-calling) | Application ownership and result correlation |
| [Mid-turn steering](https://developers.openai.com/api/docs/guides/steering) | WebSocket transport and limits on already-started actions |

## Interpretation Limits

The two prompting sources describe tendencies and authoring recommendations. They do not demonstrate that this package improves performance. The task workflow, original examples, template, worker ownership fields, and validation policy are practical adaptations, not OpenAI-certified prompts.

The article gives no universal description-length limit, skill-count cap, instruction-reduction target, or guarantee of safe execution. Preserve real boundaries and task-specific domain knowledge. Its warning about instructions shared across models is a reason to scope Astra tuning, not to transfer Astra claims to Sol, Luna, or another model.

The official user-over-skill guideline concerns skill guidance; it does not reverse system and developer authority or override application permissions. Likewise, a prompt clause cannot create async execution, API steering, or collaboration tools. The Sol skill supplies a related package layout, not evidence for Astra compression, tool-count, or reasoning defaults.

## Maintenance

Fetch the exact model-specific guide and confirm its body identifies Astra. The unqualified `latest-model` route can change models. If a route moves or returns an incomplete body, search official OpenAI documentation for the exact target and fetch the matching page rather than guessing a new slug.

Recheck sources relevant to the claim being changed. If retrieval is unavailable, identify the dated fallback and unresolved claim. Record the pages and sections actually reviewed; updating a document does not refresh every citation. Retain evidence for important workarounds so a later model or tool change can justify revising them.
