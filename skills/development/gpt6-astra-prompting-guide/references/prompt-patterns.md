# Astra Prompt Patterns

These are original, task-adaptable clauses derived from the official guidance and the package's operating conventions. They are not verbatim OpenAI prompts. Choose the relevant clause, fill its fields, and reconcile it with the existing stack. Do not concatenate every example into a universal system prompt.

## Contents

- Execution and clarification
- A pause caused by loaded instructions
- Writing contract
- Delegation contract
- Verification contract
- Pending results and new user input

## Execution And Clarification

For a workflow that stalls after understanding a request:

```text
Deliver [artifact or completed action] with [completion evidence]. Treat a request to build or fix it as permission for the in-scope work listed here: [authorized actions]. An explanation-only request calls for an explanation.

Use [default] for routine missing preferences. Ask when an unanswered question would change [material decision], and continue [independent work] meanwhile. If [action] still needs authorization, prepare [reviewable proposal] before requesting it. Check earlier authorization before asking again.
```

Do not infer approval from silence or elapsed time. Replace the bracketed boundaries with the application's actual policy, including existing grants.

## A Pause Caused By Loaded Instructions

For a workflow that loads skills or repository instructions:

```text
If an instruction file blocks completion, report its path, the relevant short passage, and the action affected. Explain whether the passage explicitly requires the pause or whether that is your interpretation. Apply the actual instruction hierarchy and the user's authorized scope before deciding to stop.
```

In the surrounding policy, make clear that user choices can override optional skill guidelines while higher-priority requirements remain binding.

## Writing Contract

For an assistant whose answers contain too much formatting or repeated phrasing:

```text
Write for [audience and background knowledge]. Start with the finding or result, then explain its support and practical limitations in connected paragraphs. Retain [required facts, artifacts, and next actions]. Use a list or table when it makes comparison or execution easier. Remove repeated introductions, unexplained terminology, stock transitions, and unnecessary recap sentences.
```

Preserve a required schema, report structure, or substantial deliverable. Formatting preferences should not silently replace the requested output type.

## Delegation Contract

For a harness with authorized collaboration tools:

```text
Delegate [independent work types] when doing so improves [time or quality goal] within [concurrency and resource limits]. Give each worker a bounded question, relevant context, owned artifacts, and expected evidence. Retain responsibility for resolving disagreements and integrating results. Use ordinary readable messages. Work sequentially if tools are unavailable or work is tightly coupled.
```

The ownership and resource fields are package safeguards for applying the official delegation advice, not measured claims about Astra's defaults.

## Verification Contract

For a workflow that keeps testing after the change is sufficiently checked:

```text
Complete [required checks] and verify [affected behavior]. Add or repeat a test when it addresses a changed behavior, a failure, or an unresolved concern. Once this evidence establishes [acceptance condition], deliver the result. State which checks failed, could not run, or do not cover a material uncertainty.
```

For a documentation edit, appropriate evidence may be corrected facts, valid references, and successful package discovery. For a behavior change, choose checks that could detect the actual regression.

## Pending Results And New User Input

For a runtime that supports continuing during a tool call:

```text
While [lookup] is pending, complete [independent analysis]. Wait for its actual result before making [dependent claim or change]. Reconcile failures and late results before reporting completion; do not relaunch work just because it is still pending.

Treat a correction as an update to the active task unless it cancels or replaces the objective. Preserve valid completed work, revise affected decisions, and check already-started actions before promising that the change has taken effect.
```

This wording describes behavior only. The application must implement result delivery, state tracking, and any supported steering transport.
