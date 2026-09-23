# Source Notes

Prompting sources reviewed on 2026-09-14 and re-read on 2026-09-23, when the package became the GPT-6 family guide. Runtime references were reverified on 2026-09-23.

## Prompting Sources

| Source | Sections checked | Package coverage |
| --- | --- | --- |
| [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), Eric Provencher, September 11, 2026 | Better skills; Up-to-date AGENTS.md; Decision boundaries; Persistence | Short task-specific descriptions, progressive disclosure, reconsidering recipes, conditional repository reading, permission and completion boundaries |
| [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model/gpt-6-astra.md#prompting-best-practices), formerly titled "Using GPT-6 Astra" | Introduction; Limitations; Prompting best practices; Migration quickstart | Family scope, Astra and Sol runtime differences, initiative, instruction following, writing style, subagent delegation, proportional verification |

The article informs both the advice this skill produces and the package's own design:

| Article guidance | Application in this package |
| --- | --- |
| Short descriptions with clear applicability; excessive descriptions can be shortened by Codex | The description leads with the GPT-6 instruction task and omits the behavior inventory |
| Use progressive disclosure for multiple workflows | The entry point routes to instruction design, prompt patterns, the template, runtime notes, or sources by need |
| Reconsider elaborate itineraries and model-specific assumptions | The working path uses outcome and constraints; the template has no compulsory plan, delegation phase, or first-pass review gate |
| Read repository documents when the task needs them | Instruction design uses conditional links and distinguishes narrow edits from requested stack audits |
| Revisit ask-first boundaries and redundant test encouragement | Prompt patterns reuse existing authorization and tie further checks to changed behavior or unresolved evidence |
| Define completion before stopping | The template and persistence pattern include the requested execution, inspection, repair, and observable stopping condition |

## Runtime And Foundational Sources

Verified on 2026-09-23. Reopen the relevant source before changing an integration; this table does not mark the entire runtime current.

| Source | Recorded coverage |
| --- | --- |
| [GPT-6 migration quickstart](https://developers.openai.com/api/docs/guides/latest-model/gpt-6-astra.md#migration-quickstart) | API compatibility checklist for Astra, Sol, and Luna |
| [GPT-6 Astra model](https://developers.openai.com/api/docs/models/gpt-6-astra) and [GPT-6 Sol model](https://developers.openai.com/api/docs/models/gpt-6-sol) | Model identity, supported reasoning effort, and defaults |
| [API changelog](https://developers.openai.com/api/docs/changelog), Sep 22 entry | GPT-6 Sol and Luna release |
| Codex `codex-rs/models-manager/models.json` at tags `rust-v0.156.0` and `rust-v0.156.1` | Codex catalog entries for `gpt-6-sol` |
| [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering) | Message authority, context separation, instruction continuity, evaluation advice |
| [Reasoning models](https://developers.openai.com/api/docs/guides/reasoning#change-reasoning-mid-conversation) | Configuration updates for the GPT-6 family, reasoning mode, reasoning context |
| [Async tool calling](https://developers.openai.com/api/docs/guides/async-tool-calling) | Application ownership and result correlation |
| [Mid-turn steering](https://developers.openai.com/api/docs/guides/steering) | WebSocket transport for the GPT-6 family and limits on already-started actions |

## Interpretation Limits

The two prompting sources describe tendencies and authoring recommendations. They do not demonstrate that this package improves performance. The task workflow, original examples, template, worker ownership fields, and validation policy are practical adaptations, not OpenAI-certified prompts.

The prompting guidance comes from behavior observed with Astra. OpenAI offers it as a starting point for the GPT-6 family and asks for evaluation on the chosen model, so it is not evidence about Sol's behavior. The article gives no universal description-length limit, skill-count cap, instruction-reduction target, or guarantee of safe execution. Preserve real boundaries and task-specific domain knowledge. Its warning about instructions shared across models is a reason to scope GPT-6 tuning and to confirm an Astra-derived clause on Sol before adding it.

The official user-over-skill guideline concerns skill guidance; it does not reverse system and developer authority or override application permissions. Likewise, a prompt clause cannot create async execution, API steering, or collaboration tools.

## Package History

- 2026-09-05: created as `gpt6-astra-prompting-guide`.
- 2026-09-14: redesigned for focused context after the skills and prompts article.
- 2026-09-23: renamed `gpt6-prompting-guide` and extended to GPT-6 Sol after the owner stopped using GPT-5.6 models. `gpt56-sol-prompting-guide` was removed rather than converted, because OpenAI publishes one prompting guide for the GPT-6 family and its GPT-5.6 behavioral claims do not transfer; the API capabilities GPT-6 keeps from GPT-5.6 moved to the runtime notes.

## Maintenance

The unqualified `latest-model` route served "Using GPT-6" on 2026-09-23 and can change when a new model ships. Fetch the exact page and confirm its body names the GPT-6 family. If a route moves or returns an incomplete body, search official OpenAI documentation for the exact target and fetch the matching page rather than guessing a new slug.

Recheck sources relevant to the claim being changed. If retrieval is unavailable, identify the dated fallback and unresolved claim. Record the pages and sections actually reviewed; updating a document does not refresh every citation. Retain evidence for important workarounds so a later model or tool change can justify revising them.
