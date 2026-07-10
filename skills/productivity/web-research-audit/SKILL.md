---
name: web-research-audit
description: >
  Use when the user asks to validate, challenge, or re-check web-research
  quality, especially when conclusions may rely on snippets, partial reads,
  stale facts, narrow source diversity, copied upstream claims, or an early
  assumption reused downstream. NOT for ordinary research that does not need a
  separate evidence-quality audit.
---

# Web Research Audit

Determine whether the important claims in a web-researched answer are supported
well enough for their stakes, and state what remains unresolved.

## Modes

- **Pre-answer**: audit the evidence while research is still in progress.
- **Post-answer**: challenge a supplied draft or prior conclusion claim by claim.

Infer the mode from the material supplied. Do not force a post-answer pass when
no draft exists.

## Quick Start

1. Define the audited question, date, and scope.
2. Extract only decision-relevant factual claims and dependent conclusions.
3. Assign each claim a stakes and freshness level.
4. Inspect the sources actually supporting each claim, then search for missing
   primary evidence or plausible contradiction where it could change the answer.
5. Mark claims verified, limited, contradicted, or unresolved.
6. Lead with the verdict and the conclusion changes, not a transcript of search
   rounds.

## Claim Ledger

Track for each important claim:

- exact claim and whether it is fact or inference;
- stable or time-sensitive;
- low, medium, or high stakes;
- supporting source and relevant section;
- contradiction or limiting evidence;
- status and effect on dependent conclusions.

Do not create ledger entries for incidental prose that cannot affect the
answer.

## Risk-Scaled Evidence

| Claim profile | Typical evidence |
| --- | --- |
| Stable, low stakes | one direct authoritative or primary source may be enough |
| Material or time-sensitive | current primary evidence and corroboration when reasonably available |
| High-stakes, disputed, or causal | multiple independent sources, explicit counterevidence search, and uncertainty propagation |

These are defaults, not source-count quotas. Explain why less evidence is
sufficient when a primary artifact directly establishes the fact, and continue
when several pages merely repeat the same upstream claim.

Prefer primary sources for what an organization, standard, dataset, law, API, or
study says. Use independent reporting or analysis for corroboration, context,
and competing interpretation. Community sources can reveal edge cases but
should not be the sole basis for consequential facts.

## Source Comprehension Gate

A citation is usable only after inspecting enough of the source to establish:

- the relevant definition and scope;
- the exact section supporting the claim;
- date, version, geography, or population when material;
- limitations, corrections, and update notes that could reverse interpretation.

Search snippets and aggregator summaries are leads, not evidence. Reading an
entire long page is unnecessary when the claim is directly established in a
self-contained official section, but surrounding context must be checked. Mark
a source partial when truncation, access limits, or missing sections prevent
that check.

## Independence and Contradiction Gate

For each material claim:

1. identify whether apparently different sources copy one press release, paper,
   dataset, or wire story;
2. search for corrections, exceptions, limitations, and credible disagreement
   likely to change the conclusion;
3. compare dates and scopes before treating two claims as contradictory;
4. trace any uncertain premise reused by later conclusions and lower their
   confidence accordingly.

Absence of counterevidence is not proof that a claim is true. Record the search
scope when that distinction matters.

## Quality Decision

Use [scoring-rubric.md](references/scoring-rubric.md) for material claims or a
formal audit. Scores summarize the evidence; they do not replace claim-level
judgment.

Verdicts:

- **pass**: decisive claims are adequately supported for their stakes;
- **conditional pass**: the core answer stands with named limits or lower
  confidence;
- **fail**: a decisive claim lacks support, is contradicted, or depends on an
  unverified premise.

## Stop Rule

Stop when:

- decisive claims meet the required evidence level;
- a targeted contradiction search finds no material change;
- dates, versions, and source independence have been checked;
- further searching is unlikely to change the verdict.

If access or evidence prevents resolution, stop with a specific gap and next
check instead of accumulating weak sources.

## Output

Lead with verdict, confidence, and any conclusion that changed. Then provide a
compact claim ledger with direct links and exact dates for time-sensitive facts.
Separate verified facts from inference.

Use [report-template.md](references/report-template.md) when the user requests a
formal report or the audit has enough claims to benefit from the full tables.
For a small audit, a short verdict plus claim bullets is sufficient.

## Scope and Autonomy

Using this skill does not broaden the user's authorization. Its default
deliverable is read-only research and analysis; it does not include editing
source material, publishing corrections, or contacting source owners. If the
user asks to revise their draft, make only that requested downstream change
after the audit.

## Gotchas

- Two domains are not independent when both repeat the same upstream artifact.
- Publication date and event date are different; track both for news.
- A source can be authoritative about its own policy but not about its
  effectiveness or competitors.
- A citation may be topically relevant yet fail to support the sentence beside
  it.
- Paywalls, snippets, translated mirrors, and truncated pages can hide decisive
  qualifications; label the limitation.
- Do not demand artificial balance when evidence is one-sided, but still test
  the strongest plausible alternative.
