# Terminology Verification Procedure

Use this procedure only when context and local conventions do not settle a
consequential terminology decision.

## Contents

- Define the question
- Check governing sources and defining mechanisms
- Check real usage
- Handle search pollution
- Scale corroboration and decide
- Record evidence
- Korean terminology
- Stop rule

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

For a term borrowed across domains, extract the relation or mechanism that the
source defines. Do not stop at “an official page contains this word.” Examples:

- Pact's [consumer-provider model](https://docs.pact.io/getting_started/how_pact_works)
  gives `contract` interacting parties, expected requests/responses, and a
  verification consequence.
- Sonar's [quality gate](https://docs.sonarsource.com/sonarqube-server/quality-standards-administration/managing-quality-gates/introduction-to-quality-gates)
  evaluates explicit metric conditions; the result can control whether code is
  promoted.
- Unity defines a game [vertical slice](https://learn.unity.com/course/practical-game-accessibility/unit/welcome-to-the-course/tutorial/explore-out-of-circulation)
  as a small playable portion demonstrating the major systems, features, and
  art of the larger game.
- RFC 7519 defines JWT [claims](https://www.rfc-editor.org/rfc/rfc7519.html#section-4)
  as named values in a JWT Claims Set. Purdue Writing Lab separately uses
  `claim` for an [arguable thesis backed by reasons and evidence](https://owl.purdue.edu/owl/resources/teaching_resources/documents/new-organizing-your-argument_-09042025.pdf).
- GitHub Actions defines a workflow
  [artifact](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts)
  as a file or collection of files produced during a workflow run and retained
  or passed between jobs.
- OpenAPI 3.2 explicitly uses
  [API surface](https://spec.openapis.org/oas/v3.2.0.html#openapi-description-structure).
  Kubernetes API Governance describes flags, configuration files, runtime
  interactions, and persistence as API
  [surfaces](https://kubernetes.io/blog/2026/02/12/sig-architecture-api-spotlight/),
  while Microsoft uses
  [public API surface area](https://learn.microsoft.com/en-us/openapi/kiota/support)
  when discussing compatibility and breaking changes. Together these show that
  `surface` can name a concrete set of observable or controllable touchpoints,
  not only a formal method list.
- OpenTelemetry instead defines
  [instrumentation scope](https://opentelemetry.io/docs/specs/otel/common/instrumentation-scope/)
  as the logical software unit associated with emitted telemetry. When that is
  the intended concept, an invented `instrumentation surface` is less precise
  even if `surface` is legitimate elsewhere.
- NIST's engineering statistics handbook defines a
  [response surface model](https://www.itl.nist.gov/div898/handbook/glossary.htm)
  as a polynomial model over several factors. This established mathematical
  sense is unrelated to interface exposure and must be kept in its domain.

These anchors illustrate the method; they are not an allowlist. Check the
governing source for the actual domain under review.

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

## Handle Search Pollution

Current web results may repeat generated prose, SEO pages, copied glossaries,
or text that borrowed the same term loosely. Raw hit counts and a long result
list are therefore weak evidence of industry convention.

1. Use model knowledge only to generate candidate senses, domains, and exact
   collocations to investigate.
2. Search the full phrase with the intended mechanism, then restrict to the
   relevant standards body, official project, professional organization,
   university, or primary publication.
3. Open the source and verify that the same actors, relation, mechanism, and
   consequence are present. A navigation hit or unrelated occurrence does not
   count.
4. When natural prose rather than a defined term is at issue, sample independent
   practitioner or academic writing with identifiable authorship. Discount
   mirrors, aggregators, vendor content farms, and unattributed summaries.
5. Treat absence cautiously. Failure to find an official use supports a plain
   replacement only when the specialized meaning is also missing from context;
   it does not prove that no community uses the term.

Model familiarity and search frequency may prioritize investigation, but
neither should be reported as proof.

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
