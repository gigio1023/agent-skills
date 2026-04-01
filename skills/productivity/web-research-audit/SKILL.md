---
name: web-research-audit
description: Use when the user asks to validate or re-check web research quality, especially for multi-round searches where conclusions may be based on partial page reads, narrow source diversity, stale evidence, or error propagation from early mistakes.
---

# Web Research Audit

Audit web-search-based findings before finalizing an answer. Focus on evidence quality rather than writing quality.

## What This Skill Prevents

- judging from snippets or partial page reads
- over-reliance on a single site or source family
- missing contradictory evidence
- carrying forward an early wrong assumption
- mixing outdated and current facts without explicit dates

## Execution Mode

- `pre-answer`: run during investigation before synthesis
- `post-answer`: run after a draft answer and challenge each claim

If no mode is provided, default to `post-answer`.

## Step 1: Build a Claim Ledger

List each factual claim with initial status `unknown`. For each claim, track:

- claim text
- recency need (`stable` or `time-sensitive`)
- stakes (`low`, `medium`, `high`)
- current supporting URLs (if available)

## Step 2: Plan Multi-Round Search

Define at least three source families before searching:

1. primary/official sources (docs, regulator, company release, paper)
2. independent reporting or analysis
3. community/aggregator sources (supporting context only, not sole evidence)

For time-sensitive claims, include at least one source updated recently unless the claim is clearly stable.

Run at least three rounds:

- Round A `confirm`: gather strongest supporting evidence
- Round B `disconfirm`: search for contradiction, correction, or exceptions
- Round C `widen`: add source-family/domain diversity when coverage is narrow

## Step 3: Enforce Full-Page Comprehension Per Source

For every source used as evidence:

1. read opening sections to capture scope and definitions
2. inspect lower sections for references, update notes, and limitations
3. capture section-level provenance for every cited point
4. label source status as `full-read` or `partial-read`

Never treat `partial-read` sources as final evidence; use them only as leads for more reading.

If tooling truncates content, reopen the page by offsets until key sections are covered.

## Step 4: Run Source Diversity Gate

A claim fails the diversity gate if any of these are true:

- only one domain supports the claim
- all supporting evidence comes from one source family
- multiple pages repeat one upstream source without independent confirmation

Minimum pass criteria for important claims:

- `2+` independent domains
- `2+` source families
- `1+` primary/official artifact when reasonably available

## Step 5: Run Contradiction and Propagation Gate

For each claim:

1. search explicitly for counterevidence (`counterexample`, `criticism`, `limitations`, `correction`, `updated`)
2. compare contradictions and record why one interpretation is stronger
3. check whether earlier uncertain claims were reused downstream
4. propagate uncertainty tags to dependent conclusions

## Step 6: Score Research Quality

Use `references/scoring-rubric.md`.

Do not finalize with confident language unless:

- evidence depth `>= 2`
- coverage and triangulation `>= 2`
- recency and consistency `>= 2` for time-sensitive claims
- uncertainty handling `>= 2`

If any threshold fails, continue search rounds or clearly return unresolved risk.

## Step 7: Produce Audit Report

Use `references/report-template.md` and return:

- verdict: `pass` | `conditional-pass` | `fail`
- claim-by-claim support and contradiction links
- unresolved gaps and next searches
- confidence statement tied to concrete dates

## Output Rules

- include exact dates for time-sensitive facts
- separate verified fact from inference
- avoid long quotes; cite links and paraphrase
- never hide uncertainty
