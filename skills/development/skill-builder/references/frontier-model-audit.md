# Frontier-Model Skill Audit

Use this reference when a skill was built around limitations of an older model
generation and must be retuned for GPT-5.6 Sol, Claude Fable 5, or another
frontier model.

## Contents

- Current evidence
- Three-way baseline
- Instruction classification
- Subtractive audit
- Autonomy, tools, and multi-agent routing
- Validation matrix
- Acceptance rules

## Current Evidence

Sources reviewed on 2026-07-10:

- OpenAI, `Using GPT-5.6`:
  https://developers.openai.com/api/docs/guides/latest-model.md
- OpenAI, `Prompting guidance for GPT-5.6 Sol`:
  https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6.md
- Anthropic, `Prompting Claude Fable 5`:
  https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5
- Anthropic, `Skill authoring best practices`:
  https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- OpenAI, `Build skills`:
  https://learn.chatgpt.com/docs/build-skills
- Anthropic, `Extend Claude with skills`:
  https://code.claude.com/docs/en/skills

Durable findings:

- Stronger models need less generic scaffolding. OpenAI reports better quality
  and large token reductions from shorter prompts; Anthropic warns that
  prescriptive older skills can degrade Fable 5 output.
- State the outcome, non-obvious constraints, authority, evidence bar, output,
  and stop conditions. Let the model choose ordinary implementation steps.
- Strong instruction following makes contradictions and repeated rules more
  harmful, not less.
- GPT-5.6 is already compressed; generic brevity can remove required content.
  Prioritize required facts and artifacts instead of asking for minimal text.
- Fable 5 sustains long runs and delegation well. Its progress claims should be
  grounded in current tool results, and it should not be asked to reproduce
  private reasoning.

## Three-Way Baseline

Keep the target model, harness, tool surface, reasoning or effort setting,
prompts, and evaluator fixed. Run:

| Condition | Purpose |
|-----------|---------|
| Target model, no skill | Measures the frontier default and reveals unnecessary instructions |
| Target model, current skill | Measures benefit or regression from legacy scaffolding |
| Target model, candidate skill | Measures whether the edit adds verified leverage |

Use representative tasks, not only examples copied from the skill. Include
near-miss prompts to test discovery. When both GPT-5.6 Sol and Fable 5 are target
runtimes, test both if available; a pass on one is not proof for the other.

## Instruction Classification

Tag each meaningful block before editing:

- `domain invariant`: private schema, policy, vocabulary, format, or safety rule.
- `fragile procedure`: exact order or command where deviation is risky.
- `tool contract`: non-obvious routing, return shape, side effect, or fallback.
- `artifact contract`: required fields, file, render, citation, or user-visible
  result.
- `verification`: executable or inspectable evidence of completion.
- `observed gotcha`: a repeated failure supported by traces or user feedback.
- `generic default`: behavior the target model already performs without help.
- `legacy compensation`: verbose steps added for a weaker prior model.
- `harness policy`: global autonomy, tone, or permission guidance that belongs in
  system/project instructions rather than this task skill.

Keep the first six when they improve evaluations. Delete or relocate the last
three unless a target-model failure proves they are still needed.

## Subtractive Audit

1. Freeze the evaluation set and record the three-way baseline.
2. Remove duplicate rules, generic knowledge, and process narration first.
3. Replace exhaustive keyword maps or rigid step lists with outcome and decision
   rules when context should determine the path.
4. Preserve exact requirements for destructive, security-sensitive, regulated,
   schema-bound, or deterministic operations.
5. Consolidate repeated output templates into one canonical contract.
6. Move long rationale, examples, and current-version notes into one-level
   references.
7. Add a rule only for a measured failure after subtraction.
8. Re-run the same evaluations after each bounded edit group.

Do not rewrite merely to mention the new model. A successful refresh often
removes text while leaving domain assets and deterministic scripts unchanged.

## Autonomy, Tools, And Multi-Agent Routing

Define autonomy once by request type or side-effect class. Do not repeat “ask
first” around safe, in-scope reads, edits, and tests. Preserve confirmation for
external writes, destructive actions, purchases, secrets, and real scope
expansion.

Expose only relevant tools and describe non-obvious return fields and failures.
Choose the mechanism by task shape:

- Direct calls for small, sequential, approval-sensitive, citation-bearing, or
  native-artifact work.
- Deterministic or programmatic execution for bounded filtering, joining,
  ranking, aggregation, and repeated validation.
- Subagents for independent judgment, context isolation, specialized tools,
  disjoint implementation, or fresh-context verification.

Keep model names and cost tiers in a dedicated routing skill. Portable domain
skills state capabilities and decision rules, not a permanently current model
catalog.

When the same package targets Claude Code and Codex, apply
`cross-harness-skill-authoring` as well. A model comparison alone does not catch
differences in discovery text, invocation, optional metadata, tool names,
permissions, or resource-path behavior.

## Validation Matrix

Measure what the skill claims to improve:

- Trigger precision on positive and near-miss prompts.
- Task success and preservation of required behavior.
- Artifact completeness, schema validity, citations, or render quality.
- Tool choice, arguments, retry behavior, and side-effect boundaries.
- Test/build/lint/smoke results and progress-claim accuracy.
- Total context, turns, latency, and cost when efficiency is part of the goal.
- Unrequested work, overplanning, repeated validation, or early stopping.

Do not score hidden reasoning or request a chain-of-thought transcript. Score the
decision, evidence, artifact, and observable actions.

## Acceptance Rules

Accept a candidate when it clearly beats the current skill without losing the
no-skill model's strengths. Prefer the smaller candidate on a tie. Reject edits
that only change style, add model praise, or shift work without improving the
user-visible outcome.

Report:

- What the no-skill baseline already did well.
- Which legacy instructions regressed or no longer helped.
- Which domain constraints and gotchas remained necessary.
- Accepted and rejected edits.
- Models, harnesses, prompts, tools, and checks actually tested.
- Untested surfaces and the condition that would justify another pass.
