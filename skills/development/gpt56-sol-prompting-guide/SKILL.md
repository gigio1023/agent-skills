---
name: gpt56-sol-prompting-guide
description: >
  Use when writing, reviewing, simplifying, debugging, or migrating developer
  prompts, system prompts, tool descriptions, agent instructions, or prompt
  stacks for GPT-5.6 Sol or the GPT-5.6 family. Applies current model-specific
  guidance to autonomy, tools, grounding, long runs, reasoning settings, and
  evals. NOT for choosing a model, general OpenAI API setup, or ordinary agent
  skill authoring without a GPT-5.6 prompt target.
---

# GPT-5.6 Sol Prompting Guide

Produce the smallest prompt stack that reliably delivers the required outcome
on GPT-5.6 Sol. Start with subtraction, preserve business and safety invariants,
and add model-specific instructions only for measured gaps.

## Quick Start

1. Identify the artifact: new prompt, review, migration, failure diagnosis, tool
   description, or full prompt stack. Preserve the explicitly requested model.
2. Capture the prompt contract:
   - user-visible goal and success criteria;
   - relevant context and evidence;
   - safety, business, scope, and permission boundaries;
   - tool-routing decisions and required return fields;
   - output shape, validation, fallback, and stop rules.
3. For an existing prompt, freeze representative eval cases before editing.
   Record current behavior, including a success case and the failure being fixed.
4. Remove redundant rules, generic exhortations, obsolete process steps,
   irrelevant tools, ineffective examples, and contradictions.
5. Add only the smallest instruction, schema, example, or tool rule that fixes a
   demonstrated gap. Use `references/prompt-patterns.md` for task-specific
   patterns and `assets/prompt.template.md` for a new complex prompt.
6. Keep API and harness controls outside the prose prompt. Configure model,
   reasoning effort and mode, persisted reasoning, prompt caching, and tool
   eligibility in the request or runtime.
7. Run the same evals. Accept the change only when task success and required
   evidence improve without an unjustified latency, token, or cost regression.
8. Deliver the final prompt, relevant runtime settings, and concise rationale for
   behavior-changing edits. Do not expose private reasoning.

Read `references/source-notes.md` when maintaining model-specific claims or when
the current API behavior may have changed.

## Core Prompt Shape

For a complex prompt, use only the sections that change behavior:

1. Role and operating context.
2. Goal and observable success criteria.
3. Evidence and task inputs.
4. Constraints and authority boundaries.
5. Tool routes and prerequisite retrieval.
6. Output and validation requirements.
7. Retry, fallback, abstention, and stop rules.

Describe the destination rather than scripting every intermediate thought. Let
the model choose an efficient path once the outcome and invariants are clear.

## Model-Specific Rules

### Simplify First

GPT-5.6 often performs better with shorter prompts and smaller tool sets. Remove
accumulated scaffolding before adding new guidance. Generic phrases such as “be
thorough,” “think step by step,” and repeated approval reminders can cause extra
exploration or unnecessary pauses.

Keep true invariants explicit. Replace blanket absolutes for judgment calls with
decision rules. Resolve contradictions instead of compensating with more text.

### Preserve Required Substance

Do not use generic “be concise” or “use minimal text” instructions. GPT-5.6 is
already compressed and may shorten the requested artifact. State what must stay:

- conclusion or deliverable;
- supporting evidence;
- material caveats;
- required decisions and next actions.

Trim introductions, repetition, generic reassurance, and optional background.

### Define Autonomy Once

Separate assessment from mutation. A compact authority policy should say which
requests authorize inspection only, which authorize in-scope local changes and
non-destructive validation, and which actions need confirmation. Do not repeat
“ask first” in every section.

### Route Tools by Task Shape

Expose only relevant tools. Describe what each tool does, when to use it,
important return fields, and error behavior. Require prerequisite discovery or
retrieval when correctness depends on it.

Use Programmatic Tool Calling for bounded deterministic reduction of large,
structured results. Keep direct calls for approval, semantic judgment,
citations, native artifacts, or steps where each result changes the next move.

Parallelize independent reads. Keep dependent decisions sequential. Synthesize
retrieved evidence before taking action.

### Ground Claims and Control Retrieval

State which claims require citations, what qualifies as enough evidence, and
what to do when support is missing. An empty search result is not proof of
absence. Use one or two meaningful fallbacks for partial or suspicious results,
then narrow the claim or report the evidence gap.

### Support Long Runs Without Narrating Them

Request a short preamble before the first tool call and sparse, outcome-based
updates at major phase changes. Do not narrate routine calls. Ground progress and
completion in current tool results or named artifacts.

Keep stable state available across turns. Use persisted reasoning only while the
objective, assumptions, and priorities remain relevant; stale reasoning can
anchor the model to an obsolete path.

### Tune Reasoning Last

Treat reasoning effort as a runtime setting and a last-mile tuning knob. Start
from the current workload baseline, compare the same level and one level lower,
and raise effort only when evals show a useful quality gain. Enable pro mode in
the API request, not by asking the model to “think harder.”

Request evidence, assumptions, and concise rationale. Never request a private
reasoning transcript or hidden chain of thought.

## Migration and Evaluation

For a GPT-5.5 or GPT-5.4 prompt migration:

1. Change the model while preserving the current reasoning baseline.
2. Run representative cases before prompt edits.
3. Remove obsolete scaffolding and irrelevant tools.
4. Make one targeted prompt or runtime change at a time.
5. Rerun the same cases and compare task success, completeness, evidence,
   tokens, latency, and cost.

Use two to five realistic positive cases and one or two near-miss cases that
must not trigger the behavior. A tie does not justify extra prompt text.

## Output Contract

For a new prompt, return the prompt and the runtime settings it assumes. For a
review, lead with the highest-impact finding, then provide a revised prompt or a
minimal patch. For a migration, distinguish prompt edits from API or harness
changes. Include eval evidence or state clearly which model-run validation was
not available.

## Reference Files

| File | Read when | Content |
| --- | --- | --- |
| `references/prompt-patterns.md` | Writing or revising a non-trivial prompt | Reusable prompt clauses, runtime controls, migration, and evaluation patterns |
| `references/source-notes.md` | Maintaining current model claims | Official OpenAI sources and durable translations |
| `assets/prompt.template.md` | Starting a new complex prompt | Compact fill-in prompt skeleton |

## Gotchas

- Do not make a long prompt safer by repeating the same rule.
- Do not place model, reasoning, cache, or tool-eligibility parameters inside
  prose when the runtime owns them.
- Do not enable Programmatic Tool Calling merely because several calls exist.
- Do not optimize calls or tokens at the expense of the final answer.
- Do not carry stale reasoning across a changed objective.
- Do not rewrite a working prompt stack all at once; isolate causal changes.
- Do not use examples unless they demonstrate a pattern the model otherwise
  misses or a format that must be exact.
