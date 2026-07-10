---
name: terminology-review
description: >
  Use when the user asks to review or replace unnatural, inflated, translated,
  or domain-inaccurate terminology in technical and workplace writing,
  including docs, comments, PR bodies, tickets, wiki pages, and messages.
  Trigger for "AI slop 없는지", "이상한 용어 안 썼는지", "term check",
  "naturalize terminology", and "industry-standard 표현으로 바꿔줘". NOT for
  grammar-only correction, general tone humanization, or renaming code symbols
  without explicit scope.
---

# Terminology Review

Find terms that are wrong or unnatural in their actual domain and replace them
with language the intended readers use. A watch-list hit is a review lead, not
proof that text was AI-generated or that the term is wrong.

## Quick Start

1. Identify the text scope, audience, language, and technical domain from the
   request and surrounding files.
2. Read applicable glossaries, style guides, neighboring human-authored text,
   and exact type or protocol names.
3. Scan for suspicious terms with
   [known-slop-terms.md](references/known-slop-terms.md), then read every hit in
   its sentence and domain context.
4. Keep established terms, directly replace obvious generic filler when edits
   are authorized, and investigate only consequential or genuinely uncertain
   terminology.
5. Re-read each changed sentence for meaning and grammar, then search the edited
   scope for missed variants.

## Decision Test

For each candidate, ask:

1. Is it an exact product, protocol, legal, academic, or code-defined term?
2. Does it express a distinction that a simpler replacement would lose?
3. Is it normal for this audience and genre?
4. Is it consistent with the project's deliberate vocabulary?
5. Would removing or replacing it make the sentence more specific?

Classify the result:

- **keep**: established or meaningfully precise in context;
- **replace**: inflated, mistranslated, vague, or borrowed from the wrong domain;
- **rewrite**: the problem is the whole construction, not one word;
- **uncertain**: available evidence does not justify a confident change.

Do not turn this into a blacklist pass. For example, `contract`, `surface`,
`artifact`, `canonical`, and `envelope` are correct in some technical
contexts and misleading in others.

## Evidence Proportional to the Decision

Use evidence when a term is domain-specific, disputed, unfamiliar, externally
defined, current, or consequential. Follow
[verification-procedure.md](references/verification-procedure.md) then.

Prefer:

1. the governing specification, standard, official API, or project glossary;
2. the target project's established vocabulary, while checking whether it is
   itself inconsistent;
3. representative practitioner or academic usage when official sources do not
   settle natural phrasing.

A generic cliché such as "it is worth noting" usually does not require five web
searches. A proposed replacement for a protocol field, regulated term, or
specialist concept may require primary evidence and independent corroboration.
When browsing, cite the sources that actually support the terminology decision.

## Replacement Rules

Use [replacement-patterns.md](references/replacement-patterns.md) as a candidate
menu, not an automatic mapping.

- Preserve technical meaning, requirement level, uncertainty, and the author's
  intended register.
- Prefer the term already used by the governing API or community when it fits
  the same concept.
- Rewrite the full sentence when a one-word substitution creates awkward Korean
  or English.
- Do not alter identifiers, schema fields, commands, quoted source text,
  trademarks, or external API names unless the user explicitly requested such
  changes.
- Preserve intentionally formal language in legal, policy, academic, or
  standards writing.

## Scope and Autonomy

- A review request produces findings and suggested replacements without editing.
- An explicit "fix", "replace", or "rewrite" request authorizes changes within
  the supplied files or text; do not ask for a second confirmation.
- Do not expand a paragraph review into a repository-wide terminology migration.
- Infer the domain from the text and repository when evidence is clear. Ask only
  when unresolved domain ambiguity would materially change the replacement.

## Output

Lead with the corrected text or the highest-impact findings. For a review with
several candidates, use a compact table:

| Location | Term | Verdict | Replacement | Evidence or reason |
| --- | --- | --- | --- | --- |

Omit unchanged watch-list hits unless explaining a likely false positive matters.
Separate evidence-backed terminology facts from stylistic preference.

For file edits, report changed files, notable terms kept or replaced, evidence
looked up, and validation performed.

## Validation

- Search the edited scope for the exact suspect terms and morphological
  variants that were meant to change.
- Re-read full sentences and neighboring paragraphs; confirm agreement,
  particles, articles, tense, and requirement level.
- Confirm links, code spans, quotations, and identifiers were not accidentally
  altered.
- Inspect the diff for unrelated tone or content changes.

A clean grep is not enough if the replacement changed meaning.

## Reference Files

| File | Read when | Purpose |
| --- | --- | --- |
| [known-slop-terms.md](references/known-slop-terms.md) | Scanning a substantial text | Context-sensitive watch list |
| [replacement-patterns.md](references/replacement-patterns.md) | Drafting alternatives | Candidate replacements and domain exceptions |
| [verification-procedure.md](references/verification-procedure.md) | A decision needs external evidence | Risk-scaled source and search procedure |

## Gotchas

- A term cannot prove AI authorship. Report the wording problem, not an
  unsupported attribution.
- Local repetition may reflect a team convention, copied boilerplate, or
  repeated generated text; it is preference evidence, not automatic truth.
- Simplifying every abstract noun or English loanword can erase necessary
  technical distinctions.
- Current vendor terminology and standards can change; browse when freshness
  matters.
- A less common term may be correct for a specialist audience. Frequency alone
  is not a verdict.
