# Astra Prompt Patterns

These original examples adapt [OpenAI's Astra guidance](https://developers.openai.com/api/docs/guides/latest-model/gpt-6-astra.md#prompting-best-practices) and its [skills and prompts article](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra). Read the section matching the problem, fill the relevant fields, and reconcile it with the existing instructions. They are options, not a universal prompt to concatenate.

## Contents

- [Completion and persistence](#completion-and-persistence)
- [Clarification and permission](#clarification-and-permission)
- [Conflicting loaded instructions](#conflicting-loaded-instructions)
- [Writing contract](#writing-contract)
- [Tool descriptions](#tool-descriptions)
- [Delegation](#delegation)
- [Verification](#verification)
- [Pending results and corrections](#pending-results-and-corrections)

## Completion And Persistence

When the agent returns after a first implementation while requested work remains:

```text
Deliver [outcome]. Completion includes [running the implementation, inspecting the result, and repairing failures within scope], with [observable acceptance evidence]. Continue until those conditions and the required checks are met. If a blocker prevents completion, identify it and report the work completed.
```

Include only the actions the task calls for. For exploration, specify the question and stopping evidence or scope limit. Reconcile any existing first-pass review gate instead of adding an instruction that contradicts it.

## Clarification And Permission

When routine omissions or repeated approvals interrupt authorized work:

```text
Use [default] for [routine missing preference]. Ask when the answer would change [material decision], and continue [independent work] while waiting. The task already authorizes [actions within scope]; do not ask again for those actions. Before requesting any still-ungranted approval for [action], prepare [reviewable proposal and evidence].
```

Keep missing information distinct from missing authorization. Silence or elapsed time does not grant permission. An early clarification is appropriate when its answer is needed to prepare the right result.

## Conflicting Loaded Instructions

When a skill or repository rule appears to cause an unexplained stop:

```text
If loaded guidance prevents the requested action, identify the file, quote the relevant passage, and explain whether it explicitly requires the pause or that is your interpretation. Apply the governing instruction hierarchy and existing session authorization. Continue work that remains authorized.
```

Fix the conflicting source when edits to it are in scope. The official user-over-skill advice concerns skill guidelines; system and developer instructions and application or tool permission boundaries remain binding. Ask for supporting evidence and a concise rationale, never private reasoning transcripts.

## Writing Contract

When repeated framing or excessive formatting obscures the deliverable:

```text
Write for [audience and background knowledge]. Start with the result and explain its support and practical limitations in connected paragraphs. Retain [required facts, artifacts, and next actions]. Use lists or tables when they make comparison or execution easier. Remove repeated introductions, stock transitions, and unnecessary recaps.
```

Preserve required schemas and report structure. A brevity preference must leave enough substance to complete the requested artifact.

## Tool Descriptions

When a tool contract is missing information the caller needs, describe its purpose, meaningful inputs, decisive result fields, side effects, and useful failure handling. Keep exact syntax and ordering where the API requires them; omit a prescribed call sequence when several approaches are valid.

```text
Use [tool] to [specific operation]. [Input] selects [scope]. The call [side effect, if any] and returns [result fields]. [Pending state] means work is still in progress; [completion field] establishes completion. On [recoverable error], use [supported recovery].
```

This is a package authoring pattern, not an official Astra tool schema. Verify capabilities in the actual tool or runtime documentation; prose does not implement them.

## Delegation

When the workflow needs parallel work and the harness provides authorized collaboration tools:

```text
Delegate [independent work types] when it improves [time or quality goal] within [resource limits]. Give workers the relevant context, owned artifacts, and expected evidence. Retain responsibility for resolving disagreements and integrating results. Keep messages readable. Continue sequentially when the work is tightly coupled or tools are unavailable.
```

Add this only when delegation serves the task. Loading a prompting guide does not authorize spawning workers or select their models.

## Verification

When repeated checks continue after sufficient evidence is available:

```text
Complete [required checks] and verify [affected behavior]. Add or repeat checks for a changed behavior, a failure, or an unresolved concern. When the acceptance condition is established, deliver the result. Report checks that failed or could not run and any material coverage limit.
```

Documentation changes may need fact, link, and package checks. Behavior changes need checks that could detect the actual regression. Preserve required repository checks; avoid generic demands to test everything or create tests that only mirror the implementation.

## Pending Results And Corrections

When the runtime supports work during a pending tool call:

```text
While [lookup] is pending, complete [independent work]. Wait for its result before [dependent claim or action]. Reconcile failures and late results before reporting completion.

Treat a correction as an update to the active task unless it cancels or replaces the objective. Preserve valid completed work and check already-started actions before claiming that the correction has taken effect.
```

The application must implement result delivery, state tracking, and any steering transport. Read [runtime notes](runtime-notes.md) when changing that implementation. A pending call is not a completed action.
