# Terminology Verification Procedure

Use this procedure only when context and local conventions do not settle a
consequential terminology decision.

## 1. Define the Question

Record:

- the candidate term and exact sentence;
- the meaning intended in that sentence;
- domain, audience, language, and genre;
- proposed alternatives;
- whether the decision is stable or time-sensitive.

Searching a word without its intended meaning produces false positives.

## 2. Check Governing Sources

Start with the source that defines the concept:

- protocol, RFC, standard, regulator, official API, or product documentation;
- project glossary, schema, type definition, ADR, or established style guide;
- textbook or peer-reviewed/primary academic source for disciplinary terms.

Use exact phrases and domain filters. Confirm that the source uses the term for
the same concept, not merely somewhere on the page.

One authoritative source can settle an exact defined name. It does not always
settle which wording sounds natural in surrounding prose.

## 3. Check Real Usage When Needed

Use representative practitioner, editorial, or academic examples when:

- official sources disagree or use different terms;
- the question is natural phrasing rather than a defined name;
- regional Korean/English usage matters;
- a proposed replacement may be jargon from another field.

Prefer sources with identifiable authorship and domain expertise. Community
usage can establish naturalness but should not override a governing
specification.

Search the target repository for deliberate vocabulary as well. Treat it as
local preference evidence, not an automatic correctness score.

## 4. Scale Corroboration

- **Low-stakes, obvious filler**: context and a direct rewrite are enough.
- **Domain-specific but stable**: one governing source, plus local usage if
  relevant.
- **Disputed or high-impact**: a governing source and at least one independent
  source or contrasting usage.
- **Time-sensitive**: current official material with visible dates or versions;
  resolve older terminology explicitly.

Do not require textbooks, papers, forums, and five source families for every
word. Continue only while another source could change the decision.

## 5. Decide

Classify as:

- **keep**: the same term and meaning are established;
- **replace**: evidence favors a clearer or governing term;
- **rewrite**: sentence construction, not vocabulary alone, is the problem;
- **uncertain**: evidence is incomplete or genuinely divided.

For uncertain cases, give the safest option and what evidence would resolve the
choice. Do not manufacture a numerical score from incomparable source types.

## 6. Record Evidence

For researched candidates, capture only what the decision needs:

| Term and meaning | Domain | Key source | Contrasting evidence | Verdict |
| --- | --- | --- | --- | --- |

Link the exact page or section. Distinguish source wording from your inference
and avoid long quotations.

## Korean Terminology

For Korean technical terms, compare:

- Korean standards or official localized documentation;
- the governing English term;
- established Korean technical publications and practitioner usage;
- the project's existing Korean vocabulary.

A loanword, translated term, or formal Sino-Korean noun is not wrong merely
because a simpler paraphrase exists. Choose for precision and audience.

## Stop Rule

Stop when the intended meaning is clear, the governing term has been checked,
and additional searching is unlikely to change the replacement. Report the
remaining uncertainty instead of padding the evidence count.
