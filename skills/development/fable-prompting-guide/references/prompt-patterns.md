# Claude Fable 5 Prompt Patterns

## Contents

- Prompt contract
- Intent and action
- Scope and authority
- Progress and long runs
- Tools and subagents
- Memory and context
- Output and readability
- Runtime controls
- Migration and evaluation
- Failure diagnosis

## Prompt Contract

Start with:

```text
Purpose: [larger task, audience, and why this work matters]
Goal: [user-visible outcome]
Done: [observable completion conditions]
Context: [relevant evidence and inputs]
Authority: [allowed work, excluded work, pause conditions]
Tools and state: [non-obvious routing, delegation, memory]
Output: [artifact or answer shape]
Validation and stop: [checks, fallbacks, finish condition]
```

Keep each section at the right altitude. Fable 5 generally needs the governing
decision rule, not every behavioral variant the rule implies.

## Intent and Action

Give the reason:

```text
This work supports [larger objective] for [audience]. They need [what the output
enables]. With that in mind, [request].
```

Prevent overplanning:

```text
When you have enough information to act, act. Do not re-derive established
facts, reopen settled decisions, or narrate options you will not pursue. When a
choice is needed, make a recommendation and state what evidence would change it.
```

Autonomous completion clause:

```text
Before ending, inspect your final paragraph. If it promises work that can be
done now with the available tools, do that work. End only when the task is
complete or blocked on information or authority only the user can provide.
```

Use the autonomous clause only for workflows where the user will not be present
to answer mid-run. Interactive sessions can use a lighter pause rule.

## Scope and Authority

Assessment boundary:

```text
When the user asks a question, describes a problem, or requests diagnosis, the
deliverable is the assessment. Report findings and stop. Implement a change only
when the request authorizes it.
```

Scope boundary for high effort:

```text
Do not add features, refactor, or introduce abstractions beyond the task. Choose
the simplest complete change for current requirements. Validate at user input,
external APIs, and other real system boundaries; do not add defensive machinery
for impossible internal states.
```

Pause rule:

```text
Pause only for a destructive or irreversible action, a real scope change, or
input only the user can provide. Otherwise continue with reversible in-scope work.
```

## Progress and Long Runs

Evidence rule:

```text
Before reporting progress, audit each claim against a tool result or named
artifact from this run. State failed, skipped, and unverified checks plainly.
Report verified completion without hedging.
```

Sparse update rule:

```text
Before the first multi-step tool phase, state the first step in one or two
sentences. Update only when a major phase begins or a finding changes the plan.
Each update includes one concrete outcome and the next step.
```

The harness should provide long timeouts, streaming, asynchronous monitoring,
and resumability. Do not solve runtime timeouts with more prompt text.

If exact user-facing content must arrive without ending the turn, define a
dedicated tool with a single message field. Pair it with:

```text
Use the send-to-user tool for partial deliverables, direct replies, or progress
facts the user must receive verbatim. Do not use it for narration or reasoning.
```

## Tools and Subagents

Tool descriptions should make triggers and boundaries clear without aggressive
“always use” language. Include decisive return fields and error behavior.

Delegation clause:

```text
Delegate independent subtasks and continue non-overlapping work while they run.
Give each subagent a bounded question, evidence requirement, and stop condition.
Intervene when a subagent lacks context or leaves scope. Synthesize results
before acting; do not concatenate reports.
```

Use a fresh-context verifier for consequential long runs or subjective quality
gates. Do not require a committee for routine bounded work.

## Memory and Context

Memory clause:

```text
Store one durable lesson or decision per record with a one-line summary. Record
confirmed approaches and corrections with why they mattered. Do not copy facts
already available in the repository or conversation. Update duplicates and
delete records that become wrong.
```

Choose the context mechanism by purpose:

| Mechanism | Use for |
| --- | --- |
| Active context | Current task instructions and high-signal evidence |
| Compaction | In-session continuity after history grows |
| Tool-result clearing | Old results that can be fetched again |
| Memory or state artifact | Decisions and progress that must survive sessions |
| Subagent context | Isolated independent work or fresh verification |

For long documents, place source material before the query. Wrap multiple
documents and metadata in clear XML tags such as `<documents>`, `<document>`,
`<source>`, and `<document_content>`. Ask the model to cite or quote the relevant
passages before synthesizing when traceability matters.

Use three to five diverse examples only when format, tone, or edge behavior
needs demonstration. Wrap examples in `<examples>` and `<example>` tags.

## Output and Readability

Outcome-first final response:

```text
Open with what happened or what you found. Then provide the evidence that
matters, the main caveat, and any action the user must take. Drop tool-loop
shorthand and write for a reader who did not watch the work.
```

Keep complete sentences. Avoid dense arrow chains, unexplained internal labels,
and references to analysis the user never saw. Choose clarity over compressed
fragments.

## Runtime Controls

Keep these outside the prompt:

- Fable 5 uses adaptive thinking at all times; disabling thinking is unsupported.
- Use `effort` to tune depth. Start with `high` for substantial work, reserve
  `xhigh` for capability-sensitive cases, and test `medium` or `low` for routine
  or interactive work.
- Manual extended-thinking `budget_tokens` is unsupported for Fable 5.
- `thinking.display` controls summarized or omitted thinking output. Raw
  reasoning is not returned.
- Long tasks need appropriate client timeouts, streaming, and asynchronous UX.
- Compaction, context editing, memory, task budgets, and fallback are API or
  harness capabilities.
- A refusal arrives as API state and must be handled by the integration.

Do not prompt the model to expose or reproduce reasoning. Ask for concise
rationale, evidence, assumptions, and decision criteria.

## Migration and Evaluation

Migration sequence:

1. Run the current prompt and tools on representative cases.
2. Remove old response-length taxonomies, aggressive tool triggers, manual
   thinking budgets, repeated rules, and unnecessary orchestration.
3. Add only measured Fable-specific controls for scope, progress evidence,
   long-run communication, memory, or early stopping.
4. Set the intended effort and harness controls outside the prompt.
5. Rerun the same cases and compare outcomes, evidence, scope, latency, tokens,
   and cost.

Include a difficult case near the top of the workload range. Simple tests alone
can hide the model behaviors the prompt is meant to govern.

Grade the environment or artifact when possible. A polished transcript is not
proof that a code change, external action, or generated file is correct.

## Failure Diagnosis

| Symptom | Likely cause | First intervention |
| --- | --- | --- |
| Overplanning | Ambiguous goal or legacy exhaustive process | Add reason, outcome, and action threshold |
| Unrequested cleanup | High effort without scope boundary | Add one explicit scope clause |
| False progress | No evidence contract | Require claims to cite current tool results |
| Text-only promise to act | Long-run early stopping | Add autonomous completion clause |
| Premature handoff | Exposed context countdown or anxiety | Hide countdown and use durable state |
| Excessive subagents | Blanket delegation instruction | Delegate only independent bounded work |
| Dense final summary | Tool-loop language leaked to user output | Add reader re-grounding clause |
| Refusal after reasoning request | Reasoning-extraction instruction | Remove transcript request; use evidence and summaries |
| Slow routine task | Effort too high or prompt too heavy | Lower effort and remove stale scaffolding |
| Cross-session drift | No durable state artifact | Pair compaction with maintained memory or handoff state |
