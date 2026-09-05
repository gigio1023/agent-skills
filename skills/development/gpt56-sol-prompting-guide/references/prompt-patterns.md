# GPT-5.6 Sol Prompt Patterns

## Contents

- Prompt contract
- Outcome and stopping clauses
- Authority and collaboration
- Tool routing
- Grounding and retrieval
- Long-running state
- Runtime controls
- Migration and evaluation
- Failure diagnosis

## Prompt Contract

Start with the smallest complete contract:

```text
Goal: [user-visible outcome] Success criteria: [observable conditions] Context: [relevant facts and evidence] Constraints: [safety, business, scope, permissions] Tools: [non-obvious routing and prerequisites] Output: [required artifact or answer shape] Stop rules: [retry, fallback, ask, abstain, finish]
```

Delete any section whose content does not change behavior. Delimit untrusted or variable context so it cannot be mistaken for instructions.

## Outcome and Stopping Clauses

Use an outcome-first clause when older prompts over-prescribe process:

```text
Resolve the request end to end. Success means:
- [decision or artifact]
- [allowed action completed before responding]
- [required evidence and output fields]

Stop when these conditions are verified. If required evidence is missing, ask for the smallest missing field or return a clear blocker.
```

For tool loops:

```text
Use the fewest useful tool loops, but do not let loop minimization outrank correctness, required evidence, calculations, citations, or validation. After each result, decide whether the core request can now be completed. If yes, finish; otherwise use the smallest useful next step.
```

## Authority and Collaboration

Compact authority policy:

```text
For requests to answer, explain, review, diagnose, or plan, inspect the relevant materials and report the result. Do not implement changes unless requested.

For requests to change, build, or fix, make the requested in-scope local changes and run relevant non-destructive validation without asking first.

Require the appropriate authorization for external writes, destructive actions, purchases, or a material expansion of scope. Reuse an explicit grant already established for the same action and target; ask only for what remains missing.
```

Response prioritization:

```text
Lead with the conclusion. Include the evidence needed to support it, any material caveat, and the next action. Keep all required facts, decisions, caveats, and requested artifacts. Trim introductions, repetition, generic reassurance, and optional background first.
```

For editing tasks, state preservation explicitly:

```text
Preserve the requested artifact, factual claims, structure, genre, and required length. Improve clarity and correctness without adding unsupported claims, sections, or promotional tone.
```

## Tool Routing

A useful tool description includes:

- purpose and trigger;
- important input assumptions;
- return fields and error shape;
- side effects and approval boundary;
- when another route is better.

Prerequisite rule:

```text
Before taking an action, complete required discovery, retrieval, and validation. Do not skip a prerequisite because the intended final state seems obvious.
```

Parallelism rule:

```text
Run independent reads concurrently when safe. Keep work sequential when one result determines the next action. Synthesize parallel results before acting.
```

Programmatic Tool Calling clause:

```text
Use Programmatic Tool Calling only for [bounded reduction stage] with [eligible read-only tools]. Reduce the intermediate results to [schema] with [evidence fields]. Retry transient failures at most [count] times and stop at [condition]. Use direct calls for semantic judgment, approval, citations, native artifacts, and final validation. Do not repeat completed calls.
```

Prefer direct calls when one call is enough, outputs are already small, each result changes the next decision, approval is required, or citations and native artifacts must survive intact.

## Grounding and Retrieval

For ordinary grounded answers:

```text
Start with one broad search using short, discriminative terms. Search again only when a required fact, owner, date, identifier, source, comparison, or requested artifact is missing. Do not retrieve again only to improve wording or add nonessential detail.
```

Evidence clause:

```text
Cite only retrieved sources and attach each citation to the claim it supports. Separate inference from sourced facts and report material source conflicts. If support remains missing, narrow the answer or state the evidence gap instead of guessing. An empty result is not proof of absence.
```

For creative drafts, name which facts are fixed. Do not invent names, dates, metrics, roadmap status, customer results, or product capabilities.

## Long-Running State

User-visible update clause:

```text
Before a multi-step tool phase, send a one- or two-sentence update naming the first step. Update again only at a major phase change or when a finding changes the plan. Each update states one concrete outcome and the next step.
```

Evidence clause:

```text
Before reporting progress or completion, audit the claim against current tool results or named artifacts. State failed, skipped, and unverified checks plainly.
```

If replaying history manually, preserve assistant phase or channel semantics. Compact after meaningful milestones, keep the prompt contract stable after compaction, and treat compacted state as opaque.

Persist reasoning across turns only when goals, assumptions, and priorities are stable. Use current-turn reasoning after a material change to avoid stale anchoring.

## Runtime Controls

Keep these outside prose prompts:

- `gpt-5.6-sol` pins the flagship model; `gpt-5.6` currently aliases it.
- `reasoning.effort` supports `none`, `low`, `medium`, `high`, `xhigh`, and `max`. Use measured workload results, not prestige, to choose.
- `reasoning.mode: "pro"` is an execution mode, not a separate model slug or a prompt instruction.
- `reasoning.context` controls whether prior reasoning remains available. Pair stable multi-turn work with conversation state such as `previous_response_id`.
- Prompt caching rewards stable reusable prefixes. Use explicit breakpoints only when measured cache behavior and cost justify them.
- Programmatic Tool Calling and multi-agent coordination are tool and runtime capabilities. Expose them only when the task shape benefits.

The `instructions` parameter applies to the current response request. When a runtime continues with `previous_response_id`, ensure current instructions are sent according to the integration's state-management contract.

## Migration and Evaluation

For a requested model comparison, use this migration sequence. A static prompt review or wording migration does not require creating cases or launching model sessions; report its execution limits instead.

1. Preserve the current reasoning effort and change only the model.
2. Run two to five representative success cases and one or two near misses.
3. Remove obsolete scaffolding, repeated rules, unused examples, and tools.
4. Add one targeted behavior fix at a time.
5. Compare success, completeness, evidence, tokens, latency, and cost.

Use standard mode as the baseline. Test pro mode only where marginal quality has material value and the task is difficult enough to benefit. Test the same model and effort before varying additional parameters.

For prompt reviews, report:

- the observed or likely failure mode;
- the instruction or contradiction that causes it;
- the smallest proposed edit;
- the eval that would accept or reject that edit.

## Failure Diagnosis

| Symptom | Likely prompt cause | First intervention |
| --- | --- | --- |
| Required sections disappear | Generic brevity instruction | State preserved content and trim priority |
| Agent asks too often | Repeated approval reminders | Replace with one authority policy |
| Excessive search or validation | Heavy scaffolding or vague stop rule | Remove repetition and add observable stop condition |
| Wrong tool route | Too many tools or vague descriptions | Reduce tools and add decision rule plus return shape |
| Programmatic calls lose citations | Wrong route for native evidence | Use direct calls for citation-bearing stages |
| Multi-turn drift | Stale or missing state contract | Re-send current instructions and reset irrelevant reasoning |
| Cost rises after migration | Old prompt and tool bloat | Subtract context before raising effort |
| Output is correct but unverifiable | No evidence contract | Require named checks and source attachment |
