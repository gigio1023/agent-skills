---
name: docs-conflict-deprecation-review
description: >
  Use when auditing existing project documentation against the current
  implementation, configuration, scripts, tests, or normative specification to
  find stale commands, broken paths, deprecated guidance, terminology drift,
  and contradictory pages. Trigger for "문서 정합성 점검", "docs review",
  "deprecated 문서 업데이트", and "구현 대비 문서 싱크". NOT for creating a
  new document (use dev-tech-spec-docs) or style-only rewriting (use
  dev-doc-style).
---

# Documentation Conflict and Deprecation Review

Find documentation claims that no longer match their evidence, classify the
mismatch correctly, and fix only when the user authorized edits.

## Modes

- **Audit**: return evidence-backed findings; do not change files.
- **Sync**: patch confirmed documentation drift, then validate the affected
  paths, commands, and links.

Use Audit for requests such as "review", "check", or "report". Use Sync when the
user asks to fix, update, or synchronize. A request to audit one area does not
authorize a repository-wide rewrite.

## Quick Start

1. Read repository instructions and define the document scope from the request.
2. Inventory the in-scope Markdown, MDX, or reStructuredText files with
   `rg --files`.
3. Extract decision-relevant claims: commands, paths, names, versions, defaults,
   environment variables, APIs, architecture, and deprecation or migration
   guidance.
4. Trace each suspect claim to evidence and classify the mismatch.
5. In Sync mode, apply the smallest evidence-supported patch.
6. Run targeted validation and report confirmed fixes, unresolved conflicts, and
   checks not run.

## Evidence and Classification

Use evidence appropriate to the claim:

| Claim | Strong evidence |
| --- | --- |
| Current command or setup | successful command, task runner, package config, CI |
| File or module path | repository tree and imports |
| API, option, or default | implementation, schema, generated API, tests |
| Runtime behavior | focused test, safe execution, logs supplied by the user |
| Intended contract | accepted spec, ADR, user requirement, normative project doc |
| Deprecation or replacement | source annotation, changelog, migration code, upstream official docs |

For current behavior, executable evidence normally outweighs prose. A
specification or ADR may intentionally describe desired behavior, so a
code-versus-doc difference is not automatically documentation drift.

Classify each issue as one of:

- **documentation drift**: implementation changed and the document should follow;
- **implementation drift**: normative documentation describes the intended
  contract and code appears wrong;
- **document conflict**: two maintained pages disagree and no owner is clear;
- **broken reference**: path, link, anchor, command, or name no longer resolves;
- **ambiguous**: evidence cannot establish which side is authoritative.

Patch documentation drift and broken references in Sync mode. Report
implementation drift and ambiguous conflicts unless the user also requested
code changes or supplied the missing decision.

## Search Strategy

Start from claims, not a generic keyword dump:

```bash
rg --files -g '*.md' -g '*.mdx' -g '*.rst'
rg -n 'deprecated|obsolete|legacy|removed|renamed|unfinished|placeholder' <scope>
```

Then search exact commands, identifiers, environment variables, and paths in
the relevant code, configuration, tests, and CI. Use repository-specific terms;
do not treat example framework names as evidence.

When the scope is large, prioritize entry-point and operational documents before
deep reference pages. Parallelize independent areas only when the harness
supports it and the result can be merged into one evidence ledger.

## Patch Rules

- Preserve the document's language, structure, and voice unless structure
  prevents an accurate repair.
- Change the smallest passage that resolves the confirmed mismatch.
- Update repeated copies only after identifying whether one page is the
  maintained owner.
- Replace deprecated guidance with a verified migration path when one exists.
  Otherwise state that the feature is removed or unsupported without inventing
  a substitute.
- Preserve unrelated user edits and never copy one guide wholesale over another
  merely because they usually match.

## Validation

For every edited claim:

- confirm local paths and anchors exist;
- confirm commands against scripts/configuration and run safe focused commands
  when proportionate;
- confirm names, signatures, defaults, and deprecation status at their source;
- search the in-scope documents for stale variants left behind;
- inspect the diff for unrelated churn and run repository documentation checks
  when available.

Record actual command results. Inspection alone is not a successful runtime
test.

## Output

Lead with the result:

- Audit mode: findings ordered by impact, each with document location, conflicting
  claim, evidence, classification, and recommended action.
- Sync mode: changed files and conflicts resolved, followed by validation
  results and open questions.

If no mismatch is found, state the inspected scope and evidence checks so the
result is auditable.

## Gotchas

- Do not assume implementation is correct when a normative specification says
  otherwise.
- A working path does not prove the documented command's flags, prerequisites,
  or output are correct.
- Search hits for "legacy" and "deprecated" may describe supported compatibility,
  not stale guidance.
- Upstream documentation is time-sensitive; verify current official sources
  when a local claim depends on an external version.
- A broad terminology replacement can alter API names, quotations, code blocks,
  or historical migration notes. Patch occurrences in context.
