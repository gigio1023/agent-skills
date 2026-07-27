# PR Review Comment Format Reference

This file covers structural anti-patterns and comment shape. For voice,
register, and the "sound like a human reviewer" rules (which apply on the
first draft, not after the user complains), read `voice-and-tone.md` in
this same folder.

## Anti-patterns

- Bold severity scaffolds: `**HIGH**:`, `**CRITICAL**:`, `### HIGH`, etc.
- Label prefixes the repo's own review threads do not use. Repo conventions
  like `Nit:` or `Optional:` are fine where adopted; see `voice-and-tone.md`.
- Internal tracking IDs: `C1`, `C2`, `H1`, `NEW-1`
- Structured review headers: `## Code Review`, `**Verdict**:`, `**Review Scope**:`
- AI signature footers: `<sub>Reviewed by Claude Code</sub>`
- Methodology descriptions: review tool names, cross-validation process
- Cross-references between body and inline comments
- Severity summary tables in the review body
- Greetings, compliments, requests, softening phrases

## Tone

Write only the review item itself. Nothing else. Comment on the code, never
the developer.

State what the issue is, why it matters, and how to fix it.
No greetings. No filler compliments. No evidence-free hedging. No apologies.
No filler.

Bad examples:
- "Could you take a look when you get a chance?" (unnecessary request phrasing)
- "Great approach overall. One small concern..." (unnecessary compliment)
- "Maybe this is intended behavior?" (hedging instead of a claim)
- "This part might be affected. Please check." (vague ask instead of the fact)

## Inline Comment Format

```markdown
{what is wrong and why. Name the concrete fix or alternative in prose.}

```suggestion
{code, optional}
```
```

Do not add a title line. Do not use arrows or bold labels. Inline comments
should usually be 1-3 sentences, plus a suggestion block only when the fix is a
small line-level replacement.

## Review Body

Use only for one of these PR-level jobs:

1. Triage which inline findings block merge and which may be deferred.
2. A material cross-cutting or unchanged-code finding that cannot be inline.
3. A direct PR-scope question or refusal.

Otherwise use an empty string. Do not summarize inline comments or the review
methodology.

```markdown
{one short triage, cross-cutting finding, or direct question}
```

No bold section labels, no review summary, no methodology.

## Code Links

```
https://{host}/{owner}/{repo}/blob/{full_sha_40chars}/{file_path}#L{start}-L{end}
```

- Full 40-character SHA required
- 1-indexed line numbers
