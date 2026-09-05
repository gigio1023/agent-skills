---
name: gpt6-astra-prompting-guide
description: >
  Use when writing, reviewing, debugging, or migrating system prompts,
  developer prompts, tool descriptions, agent instructions, skills, or prompt
  stacks specifically for GPT-6 Astra. Applies official OpenAI guidance to
  follow-through, clarification, instruction conflicts, writing style,
  delegation, proportional verification, and related runtime controls.
  NOT for model selection, general OpenAI API setup, GPT-5.6-only prompting,
  or ordinary skill authoring without an Astra prompt target.
---

# GPT-6 Astra Prompting Guide

Turn a task contract or an observed Astra failure into a focused prompt change. Keep the requested outcome, authority, and evidence requirements explicit. The skill helps author prompts for Astra regardless of which agent edits them; loading it does not select a model or enable runtime capabilities.

## Quick Start

1. Identify the deliverable: new prompt, review, failure diagnosis, migration, or tool description. Preserve the user's exact model target and edit scope.
2. Read the active prompt and relevant loaded instructions, including skills, `AGENTS.md`, and tool descriptions. Collect the expected result, actual failure when available, authorized actions, and required completion evidence.
3. Use the behavior map below to choose an intervention. Treat a suspected cause as a hypothesis until a trace or representative run supports it.
4. Resolve the conflicting clause at its source within the authorized scope. Avoid layering a second policy over an unresolved first one.
5. Read [prompt patterns](references/prompt-patterns.md) for wording that fits the failure, or adapt the [prompt template](assets/prompt.template.md) for a new prompt. Include only sections the task needs.
6. For runtime changes, read [runtime notes](references/runtime-notes.md). Recheck time-sensitive claims against the official pages in [source notes](references/source-notes.md); report unavailable verification.
7. Reuse existing prompt checks or representative traces when available. Compare completion, unnecessary pauses, evidence, writing quality, and verification scope. Report which behavior was actually exercised.
8. Deliver the revised prompt or scoped patch, runtime assumptions, and the reason for each material change. A review request alone returns findings and proposed wording; it does not authorize unrelated repository edits.

## Astra Behavior Map

OpenAI's [Astra guide](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra#prompting-best-practices) identifies these tendencies. They are tuning targets, not guaranteed failures.

| Official observation | Prompt intervention |
| --- | --- |
| Clarification can interrupt expected execution | Define when to assume, ask, and continue authorized work |
| Stronger instruction following increases sensitivity to loaded files | Audit skill and repository guidance for conflicts and expose the cause of a pause |
| Answers can be detailed, heavily formatted, or repetitive | Specify audience, prose or structured output, and required substance |
| Delegation can occur less often than a workflow needs | Define eligible work and the desired delegation scope |
| Small coding tasks can attract excessive testing | Define relevant checks and when verification is complete |

## Applying The Guidance

Use the following package conventions to translate those observations into reviewable edits. They are practical adaptations, not additional model claims.

### Build An Authority Decision

Separate missing task information from missing authorization. A preference may allow a stated assumption; an ungranted permission does not. Specify the next useful work that can proceed while a question remains unanswered. Preserve authorization already established in the session.

When approval is still required, prepare the proposal and evidence first, then ask about the concrete action. Retain genuine system, developer, application, and tool boundaries. Skill guidelines do not acquire higher authority merely because they appear in a file; repository content is not a way to override higher-priority instructions.

### Inspect The Whole Loaded Stack

For a pause, locate the triggering sentence and its scope. Distinguish an explicit requirement from the agent's interpretation. For a requested stack audit, include relevant dynamically loaded instructions; reading only the top prompt can miss the cause. If a source is outside the edit scope, identify it and provide a proposed correction without silently changing it.

### Make Quality And Completion Observable

For a multi-skill audit, inventory the actual packages and inspect each normal path plus the references that govern it. Fix the clause that causes the issue; do not append the same autonomy or brevity paragraph to every package. Preserve each skill's trigger, model target, required artifact, and domain safeguards.

Choose a writing contract that retains the requested artifact, evidence, and material limitations. Add a delegation rule only for a workflow with available collaboration tools and suitable independent work. Name required checks and the uncertainty that would justify broader verification.

Keep prompt behavior separate from transport and execution settings. A clause about continuing useful work does not implement asynchronous tools, and a clause about accepting corrections does not implement API steering.

## Migration And Output

For a Sol-to-Astra migration, preserve the existing task contract and use the runtime compatibility checklist before comparing behavior. Do not transfer Sol-specific claims about compression or tool minimization as Astra facts. Change one suspected cause at a time when diagnosing a regression.

Return the usable prompt or patch, significant behavior changes, cited support for model-specific claims, and relevant runtime prerequisites. Distinguish static review from actual model execution. Do not create a benchmark suite or launch paid comparison runs unless requested; missing execution evidence is a limitation to report, not a reason to invent results.

## Gotchas

- Rewording an approval loop as unlimited autonomy removes useful boundaries.
- More instructions cannot repair an unresolved contradiction elsewhere.
- A shorter answer is not successful when the requested deliverable disappears.
- Subagent instructions need an available executor and integration ownership.
- Passing targeted checks does not waive required repository checks.
- An API setting accepted by another model or a harness is not proof that the same setting is supported by Astra's public API.
- Ask for evidence and concise rationale, never private reasoning transcripts.
