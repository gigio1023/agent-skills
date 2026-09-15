# Technical Report Patterns for Data Views

Use a technical paper, experiment report, project specification, or operational document whose reader task matches the dashboard. Borrow how it states a fact and connects evidence to interpretation, not only its layout. For sentence, paragraph, table, and caption detail, use `technical-report-writing` and its Source Readings and Worked Examples references when available.

## Controlled comparison: MapReduce

[MapReduce, section 5 and Figure 3](https://storage.googleapis.com/gweb-research2023-media/pubtools/4449.pdf) presents corresponding input, shuffle, and output panels for normal execution, disabled backup tasks, and killed workers. The prose explains the changes through scheduling and data movement, with the cluster and workloads described before the results.

Transfer aligned conditions and the explanation of a visible difference. Keep total elapsed time distinct from peak throughput. A dashboard's controls can expose additional runs, but its initial view should already show the comparison that supports the report. For PDF, keep the selected panels and their material conditions visible.

## Configuration-specific cost: PEP 703

[PEP 703, Performance](https://peps.python.org/pep-0703/#performance) separates single-threaded and multithreaded execution overhead, names hardware and benchmark version, and gives a baseline revision. The paragraph explains why costs differ and identifies the build configuration to which they apply.

Transfer a compact table whose headings and local note preserve the comparison. Do not turn a historical result into current-product performance, or confuse increased parallel capability with lower single-thread overhead. The same precision applies when a dashboard filter selects a different configuration.

## Mechanism and validation: Circuit Tracing

[Circuit Tracing](https://transformer-circuits.pub/2025/attribution-graphs/methods.html) distinguishes attribution graphs of a replacement model from claims about the underlying model. Its validation and limitations sections connect methodological choices to what the graph can explain and show counterexamples.

Transfer the visible separation of an instrument's output, a hypothesis, and validation evidence. A dry caption can state the relevant fixed condition without a paragraph of generic warnings. Show the selected mechanism clearly before exposing a dense graph explorer. Never imply that a visually convincing graph proves causality by itself.

## Operational view: SRE postmortem structure

[Google SRE's Example Postmortem](https://sre.google/sre-book/example-postmortem/) separates impact, trigger, cause, recovery, and follow-up actions. It is a fictional teaching example, not a real outage dataset.

Transfer the distinct reader questions into an operational view: what is affected, what changed, what action is needed, and whether recovery has occurred. Use the actual project's evidence and authorized attribution. Do not copy the example's invented metrics, names, or humor.

## Chart text and document maintenance

[Datawrapper's text guidance](https://datawrapper.de/blog/text-in-data-visualizations) and [Wilke's discussion of making a point](https://clauswilke.com/dataviz/telling-a-story.html) help select the question and place explanation. [Google's Markdown guide](https://google.github.io/styleguide/docguide/style.html) gives a useful test for whether rows really benefit from a table.

Keep a title, caption, and nearby paragraph complementary. Prefer a question-based title when the result is unresolved. Selective detail should preserve the reason for the interpretation, not reduce a technical argument to a slogan. Announcement pages, annual letters, and product brochures are not the default voice samples for a technical dashboard.
