# Model Prompting Contract

Use this reference to translate GPT-6 Astra, GPT-5.6-series, and Claude Fable guidance
into one portable filesystem skill. This is a dated maintenance reference, not a
reason to put model names into every domain skill.

## Contents

- Official sources
- Shared behavior
- Differences to preserve
- Portable prompt pattern
- Tools and parallel work
- Long runs and communication
- Model-era migration

## Official Sources

Sol/Fable snapshot reviewed 2026-07-10; Astra addition reviewed 2026-09-05.

- OpenAI, [Using GPT-6 Astra](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra).
  Keep its clarification, loaded-instruction, style, delegation, and testing
  observations distinct from the older model comparison below.

- OpenAI, `Using GPT-5.6`:
  https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6
- OpenAI, `Prompting guidance for GPT-5.6 Sol`:
  https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6.md
- OpenAI, `Build skills`:
  https://learn.chatgpt.com/docs/build-skills
- Anthropic, `Prompting Claude Fable 5`:
  https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5
- Anthropic, `Prompting best practices`:
  https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Anthropic, `Skill authoring best practices`:
  https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Anthropic, `Extend Claude with skills`:
  https://code.claude.com/docs/en/skills

Refresh these sources before relying on current model, effort, API, metadata, or
harness availability details.

## Shared Behavior

Both model families now reward a smaller, clearer contract:

- State the result and completion bar instead of narrating ordinary reasoning or
  implementation steps.
- Keep important constraints, authority, evidence, output, and stop conditions.
- Delete repeated rules, obsolete weaker-model compensation, irrelevant tools,
  and examples that do not change behavior.
- Match degrees of freedom to risk: contextual heuristics for open work,
  parameterized patterns for preferred approaches, exact gates for fragile work.
- Define the difference between assessment and mutation. Both families can take
  useful initiative, but can also over-act when boundaries are implicit.
- Validate against tool results or artifacts and report failures faithfully.
- Do not ask for private reasoning, chain-of-thought, scratchpads, or reflection
  transcripts.

The portable writing rule is:

> Lead with the outcome. Keep required facts, decisions, artifacts, evidence,
> caveats, and next actions. Remove introductions, repetition, generic
> reassurance, and options not pursued first.

This avoids GPT-5.6's over-compression under generic brevity instructions and
Fable 5's tendency at high effort to elaborate or survey unused alternatives.

## Differences To Preserve

| Topic | GPT-5.6 series | Claude Fable | Portable treatment |
| --- | --- | --- | --- |
| Prompt size | Shorter prompts and smaller tool sets often improve quality and efficiency | Brief steering can replace enumerated behavior; older prescriptive skills can degrade output | Start small, retain only evaluated task deltas |
| Long work | Supports persisted reasoning, pro mode, and sparse phase updates | Designed for long-horizon autonomy; can run longer and occasionally stop early or overplan | Define done state, grounded phase updates, and genuine blockers; configure runtime outside the domain skill |
| Brevity | Generic “be concise” can suppress required artifacts | Outcome-first selective brevity works; readability must beat shorthand | State what must remain and what to trim |
| Tools | Programmatic Tool Calling helps bounded structured reduction | Strong direct tool use and asynchronous subagent coordination | Route by task shape; do not require a provider-specific mechanism |
| Parallelism | Multi-agent and Codex subagents help independent work | Fable dispatches and sustains subagents readily | Make independence the rule and keep a sequential fallback |
| Effort | Preserve baseline, test same and one level lower; raise only on measured gain | Effort is a major latency/cost control and high can over-explore routine work | Record effort in evaluations; do not hard-code it in portable domain skills |
| Prompt structure | Lightweight task sections are sufficient | XML tags help complex mixed-content API prompts | Use plain Markdown for normal skills; reserve XML for adapter templates with a measured need |
| Memory | Persisted reasoning and harness memory require freshness discipline | Explicit lesson memory can improve long-running agents | Store durable state outside upgradeable skill folders and only when the workflow needs it |

Do not average away these differences. The shared core states intent and
contract; a model or harness adapter selects runtime controls.

## Portable Prompt Pattern

Use only the fields that change behavior:

```text
Outcome: <user-visible artifact or decision>

Context: <why this matters and source material that changes the work>

Success: <required facts, files, states, evidence, or validation>

Authority: <assessment-only vs local change; actions still requiring approval>

Constraints: <invariants, preservation rules, exclusions, safety boundaries>

Routing: <capability decision rules, prerequisites, parallel/sequential rule>

Output: <reader-facing shape and facts that must remain>

Stop/fallback: <done condition, bounded retries, real blocker>
```

For a simple task, collapse this to a paragraph and a short checklist. A fixed
template that adds empty headings is legacy scaffolding, not portability.

Personality belongs here only when tone is part of the product or artifact.
Otherwise let the harness's global style own it. Explain intent when it affects
judgment, especially for long work, but do not add a generic role paragraph to
every skill.

## Tools And Parallel Work

Tool descriptions or skill instructions should communicate:

- the capability and prerequisite;
- when the route is appropriate;
- important return fields and error states;
- allowed side effects;
- retry and stop behavior when non-obvious.

Prefer direct calls when one result is small, approval-sensitive, citation-bearing,
native-artifact producing, or semantically changes the next action. Prefer a
deterministic script or programmatic reduction for large structured filtering,
joining, ranking, aggregation, or repeated validation. Prefer parallel workers
for independent work, isolated context, specialized access, or fresh review.

Parallel calls alone do not justify a programmatic layer. Parallel workers alone
do not justify coordination overhead. The core workflow must still work in one
context when the harness lacks either mechanism.

## Long Runs And Communication

For multi-step tasks, allow a short user-visible preamble and sparse updates at
major phase changes. Each progress claim must point to a current result or named
artifact. Do not request narration of every tool call.

The final response re-grounds the reader: outcome first, decisive evidence,
material caveat, and any action needed from them. Avoid private shorthand or
terms invented during the work unless they are reintroduced.

Provider-specific send-to-user tools and Codex progress surfaces are harness
features. A portable skill specifies the communication outcome, not either
mechanism.

## Model-Era Migration

Inspect existing instructions and relevant resources before adding a new model
clause. An Astra refresh should resolve unnecessary pauses and contradictory
files at their source, preserve session grants, and bound checks by the changed
artifact. These are authoring adaptations, not measured cross-model results.

The comparison sequence below applies only when model evaluation is requested.
Otherwise deliver the static patch and report the untested model behavior.

1. Freeze representative tasks and success criteria.
2. Run each primary model/harness pair without the skill and with the current
   skill before editing.
3. Remove redundant scaffolding, contradictions, irrelevant tools, and generic
   style rules.
4. Add the smallest instruction that fixes a reproduced failure.
5. Re-run the same tasks after each bounded edit group.
6. Report untested models, harnesses, effort settings, and side-effect modes.

Do not change the model, effort, prompt, tools, and evaluator simultaneously; a
passing result would not identify which change helped.
