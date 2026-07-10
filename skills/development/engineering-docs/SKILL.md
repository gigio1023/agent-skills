---
name: engineering-docs
description: >
  Use when creating, materially updating, restructuring, or reviewing Markdown
  or MDX engineering documentation in a development repository, including
  README, CONTRIBUTING, setup and how-to guides, API references, architecture
  documents, ADRs, and technical specifications. Covers repository-grounded
  content plus sentence-to-cross-page readability. Trigger for "README 작성",
  "문서 정리해줘", "API 문서", "아키텍처 문서", "스펙 작성", and dense or
  repetitive docs. NOT for PR copy, Python docstrings, tone-only humanization,
  or implementation changes that are not required to document the requested
  scope.
---

# Engineering Documentation

Create or reshape engineering documentation so its intended reader can perform
a task, look up a fact, or understand a decision. Ground technical claims in
the repository, preserve meaning and local voice, and keep the diff within the
requested documentation scope.

## Modes

- **Create or update**: inspect the implementation and edit the requested docs.
- **Structure or style**: improve an existing page without inventing new facts.
- **Review**: return evidence-backed findings without changing files.

Words such as “review”, “assess”, or “check” select review mode unless the user
also asks to fix or rewrite. A documentation request does not authorize
implementation changes.

## Quick Start

1. Read repository instructions, the target document, and nearby pages that
   establish language, terminology, renderer, and navigation conventions.
2. State the intended audience and the page's one primary reader job.
3. Identify the requested mode and evidence needs:
   - for factual creation or updates, inspect code, configuration, scripts,
     tests, schemas, and accepted specifications;
   - for structure-only work, preserve technical claims and flag conflicts
     instead of deciding which claim is true.
4. Draft or revise only the sections that serve the reader job. Use
   [TEMPLATES.md](TEMPLATES.md) as a menu, not a mandatory page shape.
5. Re-read the complete changed page, inspect the diff, and verify affected
   links, anchors, paths, commands, names, defaults, examples, and renderer
   syntax.

## Document Jobs

| Reader job | Include when applicable |
| --- | --- |
| Start or onboard | prerequisites, supported setup path, commands, success signal |
| Perform a task | preconditions, ordered actions, observable verification, evidenced recovery |
| Look up an API or option | names, types, required/default behavior, constraints, examples, errors |
| Understand architecture | context, current design, boundaries or data flow, rationale, trade-offs |
| Record a decision | status, context, decision, alternatives, consequences |
| Contribute changes | supported setup, checks, conventions, submission flow |

Do not omit a necessary fact merely to shorten the page. If decisive evidence
is missing or contradictory, name the gap and its consequence.

## Five Zoom Levels

Apply the smallest level that fixes the reader's problem:

| Level | Desired result | Change when |
| --- | --- | --- |
| Sentence | One visible main assertion with necessary conditions | qualifiers or sources obscure the claim |
| Bullet | Parallel, scannable items | one item contains unrelated facts or false nesting |
| Section | Heading and opening establish the section's job | history or meta prose delays the action or decision |
| Page | One primary reader job | unrelated procedures, reference, and rationale compete |
| Cross-page | Volatile facts have a maintained owner | duplicated copies drift or multiply update points |

These are decision rules, not lint absolutes. Long prose can be precise, and a
short rewrite can be wrong if it removes a condition. Use
[style-zoom-rules.md](references/style-zoom-rules.md) when the right repair is
unclear.

## Content and Editing Contract

- Preserve requirements, conditions, exceptions, uncertainty, citations,
  safety warnings, and intentional terminology.
- Put the current command, supported behavior, or decision before history when
  background does not change interpretation.
- Use prose for reasoning, lists for parallel items, tables for repeated fields,
  code for copyable input, and diagrams only for relationships that prose cannot
  explain as clearly.
- Keep entry pages focused on orientation, a verified start path, and useful
  navigation. Keep task guides procedural, references complete for their stated
  scope, and explanations focused on why.
- Give volatile facts one maintained owner when practical. Retain concise local
  context when a standalone procedure, safety notice, or offline guide needs it.
- Use realistic, visibly fake placeholders. Do not expose credentials or imply
  that an unrun command or example was tested.
- Add troubleshooting only for failures supported by code, tests, issues, or
  user-provided evidence.
- Match the target renderer before adding callouts, tabs, collapsible blocks, or
  MDX components. Search inbound references before renaming headings or anchors.

Use [PATTERNS.md](PATTERNS.md) for technical documentation examples and
[style-anti-patterns.md](references/style-anti-patterns.md) for dense or
repetitive prose. Repository evidence and conventions take precedence over both.

## Scope and Authority

- Review mode reports locations, impact, evidence, and a concrete repair.
- Edit mode changes only requested pages and closely coupled navigation or
  anchors.
- Do not split files, create a new site-wide convention, or rewrite neighboring
  pages unless the request includes that scope.
- When code and a normative specification disagree, surface the conflict. Code
  may show current behavior while the specification intentionally describes the
  desired contract.
- Preserve unrelated user edits and author voice. Avoid broad wording cleanup
  while documenting one feature.

## Verification

Apply [CHECKLIST.md](CHECKLIST.md) before delivery. At minimum:

- verify changed paths, links, anchors, commands, API names, defaults, units,
  environment variables, and examples against their source of truth;
- run safe, proportionate commands and the repository's Markdown formatter,
  link checker, or docs build when available;
- search inbound references before deleting or renaming sections;
- inspect the diff for unrelated wording churn and re-read the page as its
  intended reader;
- distinguish checks run from inspection-only or unavailable checks.

A passing formatter does not prove factual accuracy, and visual inspection does
not prove that links or commands work.

## Output

Lead with the created document, revised page, or highest-impact findings. For
edits, report changed files, important structural decisions, repository evidence
for non-obvious facts, checks run, and any unresolved conflict that limits
confidence.

## Reference Files

| File | Read when | Purpose |
| --- | --- | --- |
| [TEMPLATES.md](TEMPLATES.md) | A document shape would save time | Optional sections by reader job |
| [PATTERNS.md](PATTERNS.md) | Technical content or examples are unclear | Documentation problems and repairs |
| [CHECKLIST.md](CHECKLIST.md) | Before delivery | Evidence, meaning, structure, navigation, and diff gate |
| [style-zoom-rules.md](references/style-zoom-rules.md) | Choosing a structural repair | Sentence-to-cross-page examples |
| [style-anti-patterns.md](references/style-anti-patterns.md) | Diagnosing dense or repetitive prose | High-signal readability failures |

## Gotchas

- Style judgment cannot establish which technical claim is true.
- Removing “optional”, “may”, “when”, units, or version limits can create a
  false guarantee.
- A polished command copied from another page is not independently verified.
- Moving detail behind a link can break standalone runbooks, searchability, and
  offline use.
- Line-count budgets are diagnostic only; generated references and code-heavy
  pages are legitimate exceptions.
- Do not force every document into a README template or every argument into a
  bullet list.
