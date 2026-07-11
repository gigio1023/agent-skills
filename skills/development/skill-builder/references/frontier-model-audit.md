# Frontier-Model Skill Audit

Use this reference when a skill was built around limitations of an older model
generation and must be retuned for GPT-5.6 Sol, Claude Fable 5, or another
frontier model.

## Contents

- Current evidence
- Instruction classification
- Subtractive audit
- Autonomy, tools, and multi-agent routing
- Direct verification
- Finish and report

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

Keep the first six when they are specific to the task contract. Delete or
relocate the last three unless real usage or an observed failure shows they are
still needed.

## Subtractive Audit

1. Read the current skill, its direct references, and any user-provided failure
   or correction before editing.
2. Remove duplicate rules, generic knowledge, and process narration first.
3. Replace exhaustive keyword maps or rigid step lists with outcome and decision
   rules when context should determine the path.
4. Preserve exact requirements for destructive, security-sensitive, regulated,
   schema-bound, or deterministic operations.
5. Consolidate repeated output templates into one canonical contract.
6. Move long rationale, examples, and current-version notes into one-level
   references.
7. Add a rule only for the requested contract or an observed recurring failure.
8. Run direct structural checks and the documented invocation of anything that
   changed.

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
`cross-harness-skills` for discovery text, invocation, optional metadata, tool
names, permissions, and resource-path boundaries. Keep the portable core usable
when either harness-specific adapter is absent.

## Direct Verification

Verify only the artifact surfaces changed by the request:

- Frontmatter and discovery text remain valid and specific.
- Every directly linked reference and documented asset exists.
- Changed scripts and templates pass their exact documented invocation.
- Installation or package listing still discovers the skill when packaging
  changed.
- The skill remains within its authority, portability, and output boundaries on
  a direct read-through.

Do not create prompt suites, model comparisons, scoring rubrics, or benchmark
reports unless the user requested that separate work.

## Finish And Report

Prefer the smallest change that satisfies the requested contract. Reject edits
that only add model praise, repeat global policy, or move text without improving
the skill's usability.

Report:

- What changed and why.
- Which domain constraints and gotchas were preserved.
- Files and direct checks used.
- Any prerequisite or harness surface that remained unavailable.
