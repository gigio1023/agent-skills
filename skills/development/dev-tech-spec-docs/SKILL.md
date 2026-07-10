---
name: dev-tech-spec-docs
description: >
  Use when creating or materially updating engineering documentation from a
  codebase: README, CONTRIBUTING, setup/how-to guides, API references,
  architecture documents, ADRs, and technical specifications. Trigger for
  "README 작성", "API 문서 작성", "아키텍처 문서", "스펙 작성", and
  "기술 가이드 작성". NOT for style-only rewriting (use dev-doc-style),
  implementation-to-doc conflict audits (use docs-conflict-deprecation-review),
  PR bodies, or Python docstrings.
---

# Engineering Documentation

Produce a document that lets its intended reader complete a task, look up a
fact, or understand a decision using facts verified from the repository.

## Quick Start

1. Read the applicable repository instructions and the target or neighboring
   documents.
2. Identify the document's audience, one primary job, and required facts.
3. Inspect the code, configuration, scripts, tests, and existing terminology
   that establish those facts.
4. Draft only the sections that serve that job. Use the relevant example in
   [TEMPLATES.md](TEMPLATES.md) as a menu, not a mandatory global template.
5. Verify changed links, paths, commands, names, defaults, and examples with
   repository evidence. Report anything that could not be run or confirmed.

When the request is review-only, return findings without editing files. When
the user asks to create or update documentation, edit only the requested
document scope and preserve unrelated content.

## Required Content by Document Job

| Job | Include when applicable |
| --- | --- |
| Start or onboard | prerequisites, supported setup path, commands, success check |
| Perform a task | preconditions, ordered actions, observable verification, evidenced failure recovery |
| Look up an API or option | names, types, required/default behavior, constraints, examples, errors |
| Explain architecture | context, current design, boundaries/data flow, rationale, trade-offs |
| Record a decision | status, context, decision, alternatives considered, consequences |
| Contribute changes | supported environment setup, checks, repository conventions, submission flow |

Do not omit a required fact merely to make the page shorter. If the evidence is
missing or contradictory, mark the gap rather than inventing a value.

## Information Architecture

- Keep an entry page focused on orientation, a verified quick start, and links
  to deeper material.
- Keep task guides procedural, references complete for their declared scope,
  and explanation pages focused on why the system is designed as it is.
- Give volatile facts one maintained owner when practical. Other pages may
  summarize and link without copying the full table or procedure.
- Split a page when it serves unrelated reader jobs, not because it crosses an
  arbitrary line count.

## Writing Contract

- Follow the repository's language, terminology, heading, and formatting
  conventions. If none exist, use direct prose and descriptive headings.
- Put the current outcome or supported command before historical background.
- Prefer copyable examples with realistic placeholders. Never expose real
  credentials or imply that an unrun example was tested.
- State conditions, exceptions, defaults, units, and version constraints when
  they change behavior.
- Use tables, lists, code, and diagrams only when they make comparison,
  sequence, or relationships easier to understand.
- Add troubleshooting only for failures supported by code, tests, issues, or
  user-provided evidence. Do not invent likely-looking errors.
- Include time estimates, owners, escalation paths, or incident procedure only
  when the user requests them or the document's job requires them.

For concrete anti-patterns, consult
[PATTERNS.md](PATTERNS.md). Apply examples contextually; repository conventions
and verified behavior take precedence.

## Verification

Check the facts affected by the change:

- referenced local paths and anchors exist;
- commands match scripts, package configuration, or CI and are run when safe
  and proportionate;
- API names, signatures, defaults, environment variables, and error behavior
  match their source of truth;
- snippets are syntactically valid and do not contain secrets;
- duplicated guidance has a clear maintained owner;
- the final diff contains no unrelated rewrite.

Use [CHECKLIST.md](CHECKLIST.md) as a final compact pass. A failed or skipped
check must be named in the handoff; do not claim validation from inspection
alone.

## Output

Lead with the created or updated document. In the handoff, state:

- files created or changed;
- repository evidence used for non-obvious facts;
- checks run and their results;
- unresolved facts or commands not executed.

## Reference Files

| File | Read when | Purpose |
| --- | --- | --- |
| [TEMPLATES.md](TEMPLATES.md) | A document shape would save time | Optional section patterns by document job |
| [PATTERNS.md](PATTERNS.md) | A draft has clarity or structure problems | Examples of documentation problems and repairs |
| [CHECKLIST.md](CHECKLIST.md) | Before delivery | Compact quality check |

## Gotchas

- Code is evidence of current behavior, but a specification may intentionally
  describe desired behavior. Surface the conflict instead of silently choosing.
- A command copied from another document is not independently verified.
- Placeholder values must be visibly fake; never copy local secrets into docs.
- Do not turn every document into a README-shaped page or force every optional
  template section into the result.
- Avoid broad wording cleanup while documenting one feature. It obscures the
  factual diff and can overwrite the user's voice.
