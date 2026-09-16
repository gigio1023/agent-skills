# Source Readings

Use this catalog to select and closely read a public technical exemplar. The value is in the writing operation: how the author states a fact, explains a mechanism, introduces a comparison, qualifies a result, or justifies a choice. A company name or a “technical report” label does not make every sentence worth copying.

The sources below were inspected on 2026-09-15. The package contains original synthesis and small illustrative phrases, not copied reports or image collections. Source claims remain attributed; reading a benchmark is not reproducing it. The dry register and selective use of detail are editorial defaults of this skill, not a claim that every cited source recommends the same voice.

## Contents

- [Google developer documentation: voice without bureaucratic prose](#google-developer-documentation-voice-without-bureaucratic-prose)
- [Google engineering documentation: audience, decisions, and canonical sources](#google-engineering-documentation-audience-decisions-and-canonical-sources)
- [Kubernetes KEP template: make a design operationally reviewable](#kubernetes-kep-template-make-a-design-operationally-reviewable)
- [Rust RFC 2394: observable behavior, then reference semantics](#rust-rfc-2394-observable-behavior-then-reference-semantics)
- [Python PEP 703: distinguish intended capability from measured overhead](#python-pep-703-distinguish-intended-capability-from-measured-overhead)
- [MapReduce: connect system design to controlled experiments](#mapreduce-connect-system-design-to-controlled-experiments)
- [Circuit Tracing: test the explanation, not only the output](#circuit-tracing-test-the-explanation-not-only-the-output)
- [AlphaEvolve: separate the system mechanism from applications](#alphaevolve-separate-the-system-mechanism-from-applications)
- [SRE example: impact, mechanism, and corrective action](#sre-example-impact-mechanism-and-corrective-action)
- [MADR: preserve the decision and its reason](#madr-preserve-the-decision-and-its-reason)
- [Broader foundations and selective transfer](#broader-foundations-and-selective-transfer)
- [Selecting another exemplar](#selecting-another-exemplar)

## Google developer documentation: voice without bureaucratic prose

Source: [Voice and tone](https://developers.google.com/style/tone), particularly the body guidance, avoidance list, and informal/right/formal examples.

Read how the examples preserve the operation while removing either enthusiasm or unnecessary formality. An API is described by what it lets a caller do, not by praise and not by a chain of abstract nouns. The guidance prioritizes useful information for a reader in a hurry and discourages placeholder framing such as “please note.” Use concrete subjects, direct instructions where the genre is procedural, and consistent terms.

The source explicitly favors a conversational, friendly voice rather than a super-dry one. This skill retains directness and semantic completeness while choosing a more restrained register for technical reports. Do not misattribute that preference to Google, copy the page's generated summary as language authority, or turn its English examples into rules against natural Korean syntax.

## Google engineering documentation: audience, decisions, and canonical sources

Source: Tom Manshreck's [Documentation chapter in Software Engineering at Google](https://abseil.io/resources/swe-book/html/ch10.html), “Know Your Audience,” “Documentation Is Like Code,” and “Design Docs.”

Read the difference between a design document for decision makers, a tutorial for a newcomer, and a reference for lookup. The design-doc discussion names implementation strategy, key decisions, and alternatives with strengths and weaknesses. The documentation-ownership discussion explains why competing editable documents become inconsistent.

Transfer the reader-specific depth and the record of why a design was chosen. Keep an existing source of truth and update the document with the system it describes. Do not import Google's review organization or approval dependencies into an unrelated project. The chapter's prose, examples, and book layout are not bundled; its public license is CC BY-NC-ND 4.0, so link to the original rather than republishing a rewritten chapter or its assets.

Supporting source: [Google's Markdown style guide](https://google.github.io/styleguide/docguide/style.html), “Minimum viable documentation,” headings, links, and tables. The useful details are descriptive headings, manageable link text, and tables whose rows share real dimensions. Its Gitiles-specific features and fixed-column wrapping are not this package's format policy; preserve the destination renderer and repository conventions.

## Kubernetes KEP template: make a design operationally reviewable

Source: [KEP template at revision 6ab9bf717d1228928740bdbfe761b6e62b870902](https://github.com/kubernetes/enhancements/blob/6ab9bf717d1228928740bdbfe761b6e62b870902/keps/NNNN-kep-template/README.md), “Proposal,” “Design Details,” “Production Readiness Review Questionnaire,” and “Alternatives.”

Read the separation between the desired outcome and the implementation detail. The production-readiness questions ask for observable behavior under enablement, rollback, version skew, load, dependency failure, and troubleshooting. These questions expose whether a design description has explained its system consequences rather than merely listed components.

Transfer the relevant question and answer, not the entire template. A new stateful protocol may need upgrade and rollback semantics; a short analysis memo does not need release signoff or every scaling question. Required headings remain required when actually contributing a KEP. Non-goals and review procedures belong only where the project's process or a consequential ambiguity requires them. KEP status and implementation status are not interchangeable.

## Rust RFC 2394: observable behavior, then reference semantics

Source: [async/await RFC at revision f17e8623ee2e2854570dcdb936a9f4ab08c0fcd4](https://github.com/rust-lang/rfcs/blob/f17e8623ee2e2854570dcdb936a9f4ab08c0fcd4/text/2394-async_await.md), “Guide-level explanation,” “Reference-level explanation,” “Rationale and alternatives,” and “Unresolved questions.”

The guide-level section explains delayed execution and uses a short program with observable print order. The reference-level section explains the generated state, captured lifetimes, and trait implications. The rationale compares return-type choices through their effect on lifetime elision and usability. Rejected designs and postponed extensions remain separate.

Transfer this movement between reader levels and the specific cost of an alternative. Keep the effect visible before explaining a compiler mechanism. Preserve an exact contract when readers need it; do not compress lifetimes or evaluation order into “works like synchronous code.” This is a historical design proposal with provisional syntax, including `await!`; it is not evidence of today's Rust API or a runnable modern example without rechecking.

## Python PEP 703: distinguish intended capability from measured overhead

Source: [PEP 703](https://peps.python.org/pep-0703/), especially “Backwards Compatibility,” “Performance,” “Reference Implementation,” “Alternatives,” and “Rejected Ideas.” The inspected [source revision](https://github.com/python/peps/blob/f866e77409305866038471574f075cd8d83eee9e/peps/pep-0703.rst) is retained for the historical comparison.

The performance section identifies the build mode, separates single-threaded and multithreaded execution overhead, names hardware and benchmark version, and supplies baseline revision `018be4c`. It then connects the overhead to implementation mechanisms. The compatibility section distinguishes C-API/ABI effects from Python-code effects and conditions them on the affected build configuration. The reference implementations have different evaluation uses rather than being presented as interchangeable.

Transfer the placement of conditions in the specific result and the distinction between an intended capability and its measured cost. Do not turn the historical performance table into a claim about current CPython releases or assume that a proposal's acceptance validates every old benchmark. In prose, a short configuration qualifier often does more work than a general disclaimer.

## MapReduce: connect system design to controlled experiments

Source: Dean and Ghemawat, [MapReduce: Simplified Data Processing on Large Clusters](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/), OSDI 2004; [paper PDF](https://storage.googleapis.com/gweb-research2023-media/pubtools/4449.pdf). Read sections 2–3 for the programming model/implementation separation and sections 5.1–5.5, especially Figure 3, for the experimental argument.

The interface explanation specifies inputs, intermediate grouping, and outputs before describing the distributed implementation. The evaluation names the computations and cluster configuration. The matched panels expose normal execution, disabled backup tasks, and killed workers. The prose links curve features to scheduling, data transfer, output replication, and startup costs.

Transfer the description of what is held constant, the observable difference, and the mechanism that explains it. Keep total elapsed time separate from a peak rate. The paper's historical hardware, production-use counts, and evaluative adjectives are not defaults for new reports. Inspect the original figure before reusing its panel structure; text extraction alone cannot establish its layout.

## Circuit Tracing: test the explanation, not only the output

Source: Ameisen and colleagues, [Circuit Tracing: Revealing Computational Graphs in Language Models](https://transformer-circuits.pub/2025/attribution-graphs/methods.html), introduction, replacement-model description, perturbation validation, and “Limitations,” particularly “Missing Attention Circuits.”

The opening identifies the method's object: a replacement model that approximates components of the original model. The validation discussion tests graph-derived mechanisms through interventions rather than treating output agreement as sufficient. The limitations section links a methodological choice, fixed attention patterns, to computations that the graph cannot explain, then supplies concrete counterexamples.

Transfer the language separating the instrument, the observation, and the inference about the underlying system. Preserve a limitation when it changes what the figure can establish. Do not replace such detail with a generic “results may vary,” or copy rhetorical excitement because it appears in a research paper. Its large interactive graph is useful for investigation; a static report needs a selected explanatory view, not a screenshot of every control.

## AlphaEvolve: separate the system mechanism from applications

Source: Google DeepMind, [AlphaEvolve white paper](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/AlphaEvolve.pdf), system description, Table 1, and Figures 1–2.

Read the representation of candidates as programs, their modification by language models, and the role of automated evaluators. The comparison with prior work and the application-specific results answer different questions. Transfer the named components and feedback relation, then retain each application's own objective, evaluator, and comparison conditions.

Do not inherit the paper's broad promotional language or treat passing an evaluator as an unrestricted correctness guarantee. An evaluator establishes only the properties it actually checks. A single public white paper can contain useful technical description and claims that still need independent support.

## SRE example: impact, mechanism, and corrective action

Source: [Google SRE's Example Postmortem](https://sre.google/sre-book/example-postmortem/), summary/impact, root causes/trigger, resolution/detection, action items, and timeline.

The useful structure separates the user-visible effect, latent conditions, immediate trigger, mitigation, recovery, and corrective work. The timeline distinguishes outage and incident milestones; action items are linked to work rather than left as general intentions. This is a fictional teaching example with humorous elements, not an observed Google outage.

Transfer the causal separation and action specificity. Do not copy its invented incident identifiers, numbers, people, humor, or internal-looking links into a new document. In a real report, evidence must support each material event and causal link, and attribution must fit the recipients.

## MADR: preserve the decision and its reason

Source: [Use Markdown Architectural Decision Records](https://adr.github.io/madr/decisions/0000-use-markdown-architectural-decision-records.html), context/problem, considered options, and decision outcome.

The record asks a concrete format question, names alternative approaches, and records the chosen option with reasons. Transfer the inspectable question-to-choice relationship and preservation of the decision. For engineering decisions, prefer reasons tied to constraints and consequences; broad claims such as a project's liveliness should not replace the technical rationale.

Supporting source: [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html) for documents that explicitly adopt BCP 14 requirement language. Preserve its uppercase convention where used; do not import the RFC's publication boilerplate into unrelated project prose.

## Broader foundations and selective transfer

The expanded [example library](example-library.md) connects project specifications, engineering investigations, and visual explanations to original writing actions. `insight-dashboard` maintains the complementary operational and analysis library; `shadcn-frontend` turns selected information relationships into components and behavior checks. These reading paths extend, rather than replace, the close readings above.

The earlier collection also informs these choices:

- **Reader problem and consequential questions:** [Amazon's product-management discussion](https://aws.amazon.com/executive-insights/content/product-management-at-amazon/) motivates starting from a concrete reader or user need. Adapt the question, not its press-release voice or a compulsory PR/FAQ template.
- **Value, comparison, and local source placement:** [Stripe's annual update](https://stripe.com/annual-updates/2025) provides a visual reference for readable comparison and labeling. Treat it as presentation evidence, not the default voice of an engineering report.
- **Population-specific findings:** [Anthropic's geographic economic analysis](https://www.anthropic.com/research/economic-index-geography) and [GitHub Octoverse](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/) illustrate linking findings to data views. Keep each observed population and measure explicit rather than generalizing to all users or developers.
- **Evaluation conditions:** [OpenAI's reasoning report](https://openai.com/index/learning-to-reason-with-llms/) connects comparisons with compute and sampling choices. Preserve those conditions and the attribution of reported results. AlphaEvolve's system and application distinction is discussed above.
- **Explanatory sequence and exploration:** [Distill on momentum](https://distill.pub/2017/momentum/) and [Segel and Heer](https://idl.uw.edu/papers/narrative), section 4.4, inform concrete-to-general explanation and the relationship between authored findings and reader exploration. Choose interaction when it answers a useful question.
- **Chart composition and text:** [IBM Carbon dashboards](https://carbondesignsystem.com/data-visualization/dashboards), [Datawrapper on text](https://datawrapper.de/blog/text-in-data-visualizations), and [Wilke on making a point](https://clauswilke.com/dataviz/telling-a-story.html) inform reading order, useful detail, and complementary titles, labels, annotations, and prose.
- **Direct language:** [Microsoft's style tips](https://learn.microsoft.com/en-us/style-guide/top-10-tips-style-voice) and [Vercel's writing guidelines](https://github.com/vercel-labs/writing-guidelines) inform concrete wording and efficient editing. Apply the destination's language and register; preserve facts and natural Korean relations.
- **Interface execution:** [Vercel's interface guidelines](https://vercel.com/design/guidelines), [official shadcn skills](https://ui.shadcn.com/docs/skills), and [shadcn MCP](https://ui.shadcn.com/docs/mcp) inform usable state and project-aware composition through `shadcn-frontend`. Component documentation remains authoritative for APIs.
- **Document rendering:** [Typst](https://typst.app/docs/), [Quarto](https://quarto.org/docs/output-formats/pdf-basics.html), and [Pandoc](https://pandoc.org/MANUAL.html#creating-a-pdf) inform the native and conversion routes in [document production](document-production.md). Select the renderer by the recipient workflow and existing source.

Use each source for the property actually inspected. A saved text supports a textual reading; a diagram's layout or an interaction's effect requires the corresponding visual or behavioral inspection. Borrow the explanatory technique in original wording while preserving the actual project's evidence and current API.

## Selecting another exemplar

Prefer a primary method paper, specification, design proposal, decision record, engineering reference, or well-evidenced postmortem over an announcement, annual letter, product brochure, or adoption survey. Match the genre and reader task before the brand. Read the relevant prose and actual figures, then identify what to transfer at sentence, paragraph, evidence, table, caption, and document levels. Reuse the technique in original wording; preserve licenses and attribution when actual content or assets are reused.
