---
name: dev-doc-style
description: >
  Use when writing, restructuring, or reviewing Markdown/MDX in a development
  repository, especially README, AGENTS.md, and docs pages that feel dense,
  repetitive, or hard to scan. Applies sentence, bullet, section, page, and
  cross-page structure while preserving technical meaning and repository style.
  Trigger for "문서 정리해줘", "README 다듬어줘", "이 문서 장황해", and
  "dev-doc-style 적용". NOT for discovering new technical content (use
  dev-tech-spec-docs), implementation-to-doc audits, PR bodies, or tone-only
  humanization.
---

# Development Documentation Style

Make the document easier to use without deleting required facts, flattening the
author's voice, or imposing one house style on every repository.

## Quick Start

1. Read repository writing rules, the target document, and nearby pages that
   establish local conventions.
2. Determine whether the user wants findings only or an edit. A review request
   does not authorize file changes.
3. State the page's primary reader job in one sentence and identify the few
   structures that obstruct it.
4. Apply the smallest useful changes across the five zoom levels below.
5. Re-read the full page and inspect the diff. Verify links and anchors affected
   by moves, renames, or deduplication.

## Five Zoom Levels

| Zoom | Desired result | Change when |
| --- | --- | --- |
| Sentence | One clear main assertion with necessary conditions intact | qualifiers, sources, or parentheticals obscure the assertion |
| Bullet | Items have parallel shape and are easy to scan | one item contains several distinct subfacts or nesting hides hierarchy |
| Section | The heading and opening establish the section's job | background delays the instruction, decision, example, or evidence |
| Page | The page serves one primary reader job | unrelated procedures, references, and explanations compete for attention |
| Cross-page | Repeated volatile facts have a clear maintained owner | copies have drifted or create multiple update points |

These are decision rules, not lint absolutes. A long sentence can be precise; a
short sentence can omit the condition that makes it true.

## Editing Rules

### Preserve meaning first

- Keep constraints, exceptions, scope, uncertainty, citations, and safety
  warnings that affect correctness.
- Do not convert narrative into bullets unless scanning improves.
- Do not remove a references section when the repository or citation style
  requires one.
- Keep necessary repetition in entry pages, safety notices, and standalone
  procedures. Deduplicate only when readers can still complete the page's job.

### Match the document type

- Task guide: put prerequisites and the next action early; keep commands near
  their verification.
- Reference: optimize for complete lookup and consistent fields.
- Explanation or architecture page: preserve causal reasoning and trade-offs;
  prose may be the right surface.
- README or index: orient the reader, provide a verified entry path, and link to
  deeper material without becoming a copy of every page.

### Choose surfaces deliberately

- Use prose for reasoning, lists for parallel items, tables for repeated fields,
  and diagrams for relationships that are hard to explain linearly.
- Use notes, warnings, tabs, or collapsible sections only when the target
  renderer supports them and hiding the content does not reduce safety.
- Use descriptive link text. A path or raw URL alone is acceptable only where
  the document convention treats it as data, such as a manifest or link list.
- Preserve established technical terms and the document's language. Prefer
  active, current wording, but retain modality when it expresses a real option
  or requirement level.

Detailed examples live in
[zoom-rules.md](references/zoom-rules.md) and
[anti-patterns.md](references/anti-patterns.md). Read only the relevant example
set; the rules in this file and repository conventions take precedence.

## Scope and Autonomy

- In review mode, report concrete locations, impact, and a suggested repair.
- In edit mode, change only the requested pages and closely coupled links.
- Do not split files, rename headings with inbound anchors, or establish a new
  site-wide convention unless the request includes that scope.
- If fixing structure reveals a factual conflict, preserve it and flag it for a
  documentation audit instead of choosing a technical truth by style judgment.

## Validation

Use [checklist.md](references/checklist.md) for the final pass. At minimum:

- compare the final text with the original intent and required facts;
- verify changed local links, headings, and anchors;
- search for inbound references before removing or renaming a section;
- inspect the diff for unrelated wording churn;
- run the repository's documentation formatter, linter, or build when available
  and proportionate.

Report commands actually run. If a renderer or link check was not available,
say so instead of implying the page was rendered.

## Output

Lead with the revised text or highest-impact findings. For edits, report changed
files, structural decisions that affect navigation, validation results, and any
factual issue intentionally left unresolved.

## Reference Files

| File | Read when | Purpose |
| --- | --- | --- |
| [zoom-rules.md](references/zoom-rules.md) | A zoom-level repair is unclear | Focused before/after patterns |
| [anti-patterns.md](references/anti-patterns.md) | Diagnosing dense or repetitive prose | High-signal failure patterns |
| [checklist.md](references/checklist.md) | Before delivery | Meaning, navigation, and diff checks |

## Gotchas

- Style review cannot establish whether a technical claim is true.
- Removing "optional", "may", or "when" can turn valid conditional behavior into
  a false guarantee.
- Moving content to another page can break self-contained runbooks, copied
  snippets, search discoverability, and offline use.
- Markdown components differ across GitHub, MkDocs, Docusaurus, Mintlify, and
  other renderers; inspect the target convention before introducing syntax.
- Line-count budgets are diagnostic signals only. Code-heavy references and
  generated API pages are legitimate exceptions.
