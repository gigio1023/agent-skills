---
name: prompting-guide
description: >
  Write, review, simplify, debug, or migrate system prompts, agent instructions, CLAUDE.md, AGENTS.md, skills, subagent definitions, tool descriptions, or long-run prompt stacks for a specific target model: Claude Fable 5 or 5.1 (also Mythos), Claude Opus 5 or 5.5, or GPT-6 Astra or GPT-6.1 Sol, including migration between versions. Also explains, drafts, reviews, or translates a Codex Goal mode or Claude Code /goal prompt. Use for "write the system prompt for Opus", "review this CLAUDE.md for Fable", "migrate this prompt to GPT-6", "goal prompt 써줘", "프롬프트 고쳐줘". NOT for choosing a model or effort for a run or subagent (model-routing), API code migration or general API setup, or skill packaging without a target model (skill-builder).
---

# Prompting Guide

Each supported model family has its own guide. Identify the family that will run the instructions, read that guide, and follow its routing to its own references and template. Do not preload the other guides.

| Target model | Read |
| --- | --- |
| Claude Fable 5 or Fable 5.1, including Mythos 5 and 5.1 | [Fable guide](references/fable/guide.md) |
| Claude Opus 5 or Opus 5.5, including migration from Opus 5 | [Opus guide](references/opus/guide.md) |
| GPT-6 Astra or GPT-6.1 Sol, including migration from legacy GPT-6 Sol or GPT-5.6 | [GPT guide](references/gpt/guide.md) |

The target is the model that will execute the prompt, not the model doing the editing. Take it from the request, a model ID in the integration or configuration, a `model` field in the agent or skill definition, or the host's documented default. Ask only when it cannot be determined and the answer changes the advice.

For a Codex Goal mode or Claude Code `/goal` prompt, whether to explain, draft, review, translate between the two harnesses, or activate one, read the [Goal mode guide](references/goal-mode/guide.md) together with the target family's guide. It carries the goal contract, the harness differences that change how a goal is written or judged, and the activation rules.

When an artifact will run on more than one family, such as a skill shared by Claude Code and Codex, apply each family's guide to that family's behavior and keep the clauses distinguishable. When migrating from one family to another, follow the target family's guide; the source family's guide only helps identify scaffolding written for the old model.

## Keep Families Separate

Do not port guidance between families without measurement. The model lines changed in different directions, and effort level names do not mean the same amount of thinking across models. A clause, effort setting, or workaround that one guide recommends is evidence about that family only. The Fable and Opus guides share some Anthropic runtime facts; when maintaining one of them, update the other as listed in [Opus source notes](references/opus/source-notes.md#shared-with-the-fable-guide).

A model outside these families has no guide here. Say so and work from that model's official prompting documentation rather than borrowing a family guide's model-specific clauses.
