# Manual SkillOpt Protocol for Skill Builder

> Source: SkillOpt: Executive Strategy for Self-Evolving Agent Skills,
> arXiv:2605.23904 / Hugging Face paper page:
> https://huggingface.co/papers/2605.23904
> Read through `hf papers info 2605.23904` and `hf papers read 2605.23904`;
> the full markdown was reviewed locally during that read.

## Table of Contents

- Core Translation (what to borrow from SkillOpt)
- When To Use
- Manual Optimization Contract (target, baseline, validation gate, patch budget)
- Evidence Packet
- Role-Separated Analysis (failure analyst, success analyst, merges, rank/select)
- Patch Operations
- Validation Gate
- Rejected-Edit Buffer
- Manual Slow Lessons
- Manual Session Template
- Report Format

Use this reference when the user asks to improve, optimize, train, or debug an
existing skill from observed behavior. This is a manual maintenance protocol,
not an automatic background learner.

## Core Translation

SkillOpt treats the skill document as the trainable state of a frozen agent.
For manual skill work, borrow the discipline, not the full infrastructure:

- Keep the target model, harness, tool surface, prompts/tests, and evaluator fixed
  while comparing a candidate skill.
- Learn from evidence batches, not a single anecdote.
- Analyze failures and successes separately.
- Convert observations into bounded `append` / `insert_after` / `replace` /
  `delete` edits.
- Merge and rank edits before applying them.
- Accept only candidate edits that pass a validation gate.
- Keep rejected edits as session-local negative feedback, not deployed rules.

Do not schedule periodic training or background self-edits unless the user
explicitly asks for an automation.

## When To Use

Use this protocol when there is concrete evidence:

- Failed prompts or traces where the skill triggered but behaved badly.
- Successful prompts worth preserving as reusable procedure.
- Undertriggering, overtriggering, or conflict with adjacent skills.
- User corrections, code review comments, screenshots, logs, command output, or
  validation results.
- Repeated agent mistakes that suggest a missing gotcha, tool policy, output
  contract, or verification step.

If the user only wants a brand-new skill and has no behavioral evidence yet, use
the normal `SKILL.md` creation workflow first. Keep the skill small, then optimize
after real use.

## Manual Optimization Contract

Before editing, establish:

- `target_skill`: path to the SKILL.md and relevant references/scripts.
- `core_loop`: the input -> procedure/action -> verified output loop this skill
  is supposed to improve.
- `target_harness`: direct chat, Codex, Claude Code, local CLI, browser, tests, or
  another execution environment.
- `baseline`: current behavior on the validation prompts/checks before editing.
- `evidence`: failures, successes, trigger examples, and structure issues.
- `validation_gate`: fixed prompts, executable tests, scorer, checklist, or user
  acceptance criteria.
- `patch_budget`: default 1-4 accepted edits for one manual pass.

If no validation gate exists, create a small one before editing. For subjective
skills, use before/after examples and explicit user preference. If even that is
not possible, make only the smallest evidence-backed edit and report the risk.

## Evidence Packet

Build a compact evidence table before proposing edits:

| ID | Type | Evidence | Pattern | Candidate lesson |
|----|------|----------|---------|------------------|
| F1 | failure | prompt/trace/test | recurring failure mode | missing or wrong rule |
| S1 | success | prompt/trace/test | reusable successful behavior | preserve or reinforce |
| T1 | trigger | prompt/skill list | under/overtrigger | description boundary |
| R1 | structure | file/path/check | packaging issue | split, move, or fix path |

Evidence types:

- `failure`: wrong behavior, incomplete work, skipped verification, bad output
  format, unsafe action, wrong tool policy, or ignored local convention.
- `success`: behavior that worked and should not regress.
- `trigger`: description is too broad, too narrow, or loses to an adjacent skill.
- `structure`: duplicated rules, stale references, missing files, long SKILL.md,
  broken scripts, or packaging mismatch.

Prefer patterns that recur across multiple examples. Single examples can justify
a fix only when they reveal a clear general rule, a safety issue, or a broken path.

## Role-Separated Analysis

For nontrivial optimization, work in the same roles SkillOpt separates. In a
manual session, one agent may perform all roles, but keep the outputs distinct.

### 1. Failure Analyst

Read failed trajectories and the current skill. Identify common failure patterns.

Output:

```json
{
  "failure_summary": [
    {"failure_type": "string", "count": 2, "description": "one line"}
  ],
  "edits": [
    {
      "op": "append|insert_after|replace|delete",
      "target": "exact target when needed",
      "content": "markdown when needed",
      "support_count": 2,
      "source_type": "failure",
      "reasoning": "why this fixes a recurring failure"
    }
  ]
}
```

Rules:

- Address common failure patterns, not task-specific values.
- Patch gaps in the existing skill instead of duplicating content.
- Prefer concrete procedure over broad advice.
- Produce fewer edits than the budget when evidence is weak.

### 2. Success Analyst

Read successful trajectories and the current skill. Identify behavior worth
preserving or making explicit.

Rules:

- Only propose edits for patterns not already covered.
- Prefer reinforcing an existing section over adding a new top-level section.
- Use success edits to prevent regressions, not to praise the skill.
- Keep success edits lower priority than repeated failure fixes unless they guard
  against a likely regression.

### 3. Failure Merge

Merge failure-driven edits:

- Deduplicate similar edits.
- Resolve contradictions.
- Drop one-off or overfit rules.
- Preserve edits supported by multiple failures.
- Ensure no two edits target the same text region.

### 4. Success Merge

Merge success-driven edits:

- Deduplicate.
- Keep only generalizable success patterns.
- Drop anything already covered by the skill.
- Preserve support counts.

### 5. Final Merge

Combine failure and success edits:

- Failure fixes have priority.
- If failure and success edits cover the same point, keep the failure version.
- Keep success edits only when they preserve behavior not covered by failure fixes.
- Remove conflicting or redundant edits before ranking.

### 6. Rank And Select

Rank the merged edit pool and select at most `patch_budget` edits.

Ranking criteria, in order:

1. `systematic_impact`: fixes recurring or high-severity behavior.
2. `complementarity`: fills a real gap instead of duplicating existing guidance.
3. `generality`: applies across tasks and avoids hardcoded examples.
4. `actionability`: tells the agent exactly what to do or verify.

Carry `support_count` and `source_type` into the final decision. A supported,
general, concrete edit should beat a clever but isolated rule.

## Patch Operations

Use only these operations:

| Op | Required fields | Use when |
|----|-----------------|----------|
| `append` | `content` | Adding a short gotcha, validation step, or small section |
| `insert_after` | `target`, `content` | Adding detail under an existing heading or line |
| `replace` | `target`, `content` | Sharpening wording that caused bad behavior |
| `delete` | `target` | Removing stale, duplicated, contradictory, or over-specific text |

Patch constraints:

- `target` must be exact text from the current file.
- Do not edit unrelated files in the same pass.
- Do not rewrite the whole skill unless the current file is structurally broken
  and the user accepts that scope.
- Keep SKILL.md compact. Move long details into `references/`.
- If the skill uses a protected slow-update block, step-level edits must not
  target that block.

## Validation Gate

Evaluate the candidate against the same gate used for baseline.

Good gates:

- 2-5 realistic positive prompts that should trigger the skill.
- 1-2 negative-control prompts where another skill should trigger or no skill is
  needed.
- Executable checks for scripts, generated files, templates, paths, or examples.
- Re-reading SKILL.md with referenced files to verify packaging consistency.
- A user-scored before/after comparison for subjective skills.

Acceptance rule:

- Accept only if the candidate clearly improves target behavior or removes a
  verified blocker without regression.
- Treat ties conservatively. If behavior is unchanged, reject the behavioral edit.
- Non-behavioral fixes such as broken paths, invalid frontmatter, missing files,
  or executable-bit repairs can be accepted when directly verified.
- Keep the target model, harness, evaluator, and prompts fixed during comparison.

## Rejected-Edit Buffer

Rejected edits are useful during the session, but should not accumulate in
deployed skill instructions.

Record them like this:

```markdown
Rejected edit:
- Proposed change:
- Evidence it tried to address:
- Validation result:
- Why rejected:
- What to avoid next:
```

Use the buffer to avoid repeating failed ideas in the same manual pass. Keep it
outside SKILL.md unless the skill explicitly has a maintenance log.

## Manual Slow Lessons

After several accepted passes or repeated user corrections, consolidate durable
lessons:

- Add one high-signal Gotcha for a repeated failure mode.
- Tighten the frontmatter description if triggering was the actual issue.
- Move long rationale, examples, or tool details into `references/`.
- Bundle a deterministic script only when the agent keeps recreating the same
  code and no judgment is needed after the script runs.
- Remove stale rules that validation or user feedback has disproved.

Do not copy optimizer notes into deployed instructions. The user-facing skill
should remain compact, procedural, and auditable.

## Manual Session Template

Use this sequence when the user says "optimize this skill" or provides failures:

1. Read the target SKILL.md and directly referenced files.
2. State the core loop and current trigger contract.
3. Record the baseline validation prompts/checks.
4. Build the evidence packet.
5. Run failure analysis and success analysis separately.
6. Merge failure edits, merge success edits, then perform a final merge.
7. Rank edits and select at most 1-4 atomic operations.
8. Apply the patch.
9. Run the same validation gate.
10. Report accepted edits, rejected ideas, validation result, and residual risk.

## Report Format

When done, report:

- `Accepted`: edits that landed and why.
- `Rejected`: plausible edits not applied and why.
- `Validation`: prompts/checks run and result.
- `Residual risk`: what the current evidence still cannot prove.
