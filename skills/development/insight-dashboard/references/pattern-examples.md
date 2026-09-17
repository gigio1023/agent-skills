# Pattern Examples for Data Views

Choose a reader situation, then inspect the relevant public work. The finished specifications below are independently **synthetic examples**; public sources motivate the structure, not the example numbers. Public demos establish neither a production result nor the correctness of their causal commentary.

## Contents

- [Choose a configuration](#choose-a-configuration)
- [Find an operational exception](#find-an-operational-exception)
- [Review a week](#review-a-week)
- [Explain a metric](#explain-a-metric)
- [Investigate through linked views](#investigate-through-linked-views)
- [Answer one recurring question](#answer-one-recurring-question)
- [Public reading library](#public-reading-library)
- [Technical and editorial foundations](#technical-and-editorial-foundations)

## Choose a configuration

**Reader task:** assess latency and completion together.

**Finished view, synthetic:** a table compares Baseline and Candidate on the same 100-request replay. Baseline completes 92 with a successful-request median of 240 ms; Candidate completes 96 with a median of 180 ms. The heading states the observed lower median, the columns retain both denominators, and a local note says timeouts are excluded from latency. A repeat-run view is useful when release selection needs variation estimates.

**Build:** derive the completion counts, median comparison, and heading from the selected run and configuration. Use enough room for exact values and the important contrary result when present.

**Check:** change the run or subgroup so that the original ranking no longer holds. The headline and comparison must change with it. Keep a single replay distinct from evidence of general superiority.

**Read:** LLVM Compile-Time Tracker and rustc performance data below for configuration, comparison reference, and detail beneath an aggregate; PEP 703 for measurement conditions.

## Find an operational exception

**Reader task:** decide which service needs investigation.

**Finished view, synthetic:** a current-state summary leads to service rows with availability, remaining error budget, latest observation, and investigation status. The selected service opens a time-aligned trend and relevant events. Missing telemetry has its own state rather than a healthy-service badge.

**Build:** choose the priority rule from the actual operational need. Keep comparable rows, text-supported status colors, visible freshness, and a direct route to the affected entity.

**Check:** exercise one affected service, one stale source, and a failed refresh. Confirm that severity, investigation status, and data freshness remain distinct.

**Read:** Grafana SLO, Netdata, Cloudflare Status, and GitHub Status below. Their information structures are useful independently of their panel count or visual styling.

## Review a week

**Reader task:** connect previous work to current evidence and the next useful action.

**Finished view, synthetic:** the previous action states that a retry policy was changed before the replay. The comparison shows the completion and latency results above. Commentary identifies the remaining timeouts as the next investigation, without claiming the policy caused the improvement. The next action is to inspect those requests.

**Build:** associate commentary with the same period, population, and data version as the measures it explains. Let the reader browse previous periods and follow relevant sources.

**Check:** navigate to another period and inspect whether commentary still belongs there. A missing comment is preferable to carrying forward the prior period's explanation.

**Read:** Evidence Weekly Business Review for the action/measure/action relationship; Wikimedia Movement Metrics for a static periodic report with interpretation and data-definition context. Evidence's demo chronology and external causal comments are not evidence for a real business result.

## Explain a metric

**Reader task:** understand what a number measures and whether it applies.

**Finished view, synthetic:** a completion-rate page shows the selected period, completed and attempted counts, the rate, and a trend. A local definition states timeout handling. A breakdown exposes a small subgroup whose rate differs from the overall result; the subgroup's count remains visible.

**Build:** keep the definition, comparison, and calculation consistent. Put longer methodology or an authorized query behind a clear link. State forecast or imputed values as such.

**Check:** test an empty population and a subgroup with a different denominator. Compare displayed values with an independent calculation.

**Read:** Mozilla GLAM, Firefox Public Data Report, RIPEstat, and Taipower below for counts, definitions, input transformations, and capacity references.

## Investigate through linked views

**Reader task:** narrow a change from an aggregate to its contributing population.

**Finished view, synthetic:** a resource-cost view begins with a period comparison, then groups costs by service. Selecting a service updates its usage, unit-cost view, detail table, and title together. A shared link restores the filters; the exported report includes their visible labels and observation period. If the reader must reproduce the export, its source detail identifies the retained dataset version or snapshot.

**Build:** offer groupings and resolution choices that answer different questions. Keep one selection-to-result path and handle delayed requests so old responses do not overwrite the newest selection.

**Check:** change range and grouping, reload the URL, navigate back, and inspect the export. A live shared URL is not an immutable snapshot.

**Read:** Open Electricity, Plausible, Evidence KPI Portal, and Wikimedia Topviews below. Validate the actual implementation, not merely the existence of analogous controls elsewhere.

## Answer one recurring question

**Reader task:** find the current deployment version or next relevant milestone.

**Finished view, synthetic:** a page names the environment, current release identifier, observation time, and next scheduled milestone, with a link to the release record. It can be complete without a chart.

**Build:** prioritize the answer and the next useful link. Add history only when the reader needs it.

**Check:** compare the displayed identifier with its source and inspect the missing/stale-source case.

**Read:** What Firefox trains are we in? below. Borrow the narrow question-and-answer relationship rather than the source's release numbers.

## Public reading library

Each entry is a reading pointer and original adaptation. Text or a dashboard model can support its information structure; inspect figures and exercise controls separately before claiming their semantic behavior. This library does not certify every control on the linked sites.

- **[Grafana Play — SLO Overview](https://play.grafana.org/d/slo-dashboard-overview/slo-overview?orgId=1)** — Inspect SLO overview. Prioritize affected services, then give each service comparable achievement and remaining-budget fields. Choose the time window for the operational task.

- **[Grafana Play — Kubernetes / Compute Resources / Pod](https://play.grafana.org/d/6581e46e4e5c7ba40a07646395ef7b23/kubernetes-compute-resources-pod?orgId=1)** — Inspect pod usage and quota. Pair resource consumption with its limit and throttling signal, using hierarchical filters that reflect the resource relationship.

- **[Netdata Demo Space — All Nodes](https://app.netdata.cloud/spaces/netdata-demo/rooms/all-nodes)** — Inspect latest observation and node breakdown. Show freshness and relevant aggregation with the measure, and expose the node that an overall average can conceal. Toggle semantics need their own test.

- **[Evidence — Internal KPI Portal](https://evidence-demo.netlify.app/)** — Inspect date-based KPI pages. Generate a concise comparison sentence from the same data as the values, and preserve the selected date in navigation.

- **[Evidence — Weekly Business Review](https://business-review-demo.netlify.app/weekly-reports/2021/52)** — Inspect previous actions, measures, and next actions. Connect periodic review to action. Use the demo for organization, while replacing its inconsistent chronology and causal comments with actual evidence.

- **[Evidence — Northstar Report](https://northstar-report.netlify.app/)** — Inspect output/input metrics and definitions. Explain why a measure belongs and group related drivers. Compute percentage-point changes explicitly rather than copying the demo labels.

- **[LLVM Compile-Time Tracker](https://llvm-compile-time-tracker.com/)** — Inspect configuration, values, and deltas. Pair a relevant summary with individual benchmarks and retain the selected measurement configuration. Choose aggregation to fit the new metric.

- **[Cloudflare System Status](https://www.cloudflarestatus.com/)** — Inspect incident summary and timeline. Separate severity from investigation state, and show impact and event times in terms useful to affected readers.

- **[NESO Carbon Intensity Dashboard](https://carbonintensity.org.uk/)** — Inspect actual/forecast and regional values. Make observed and forecast quantities distinguishable, with units, aggregation, and accessible source data near the display.

- **[Mozilla GLAM — Glean Aggregated Metrics Explorer](https://glam.telemetry.mozilla.org/)** — Inspect probe detail and coverage. Pair a rate or distribution with its population, definition, and a useful route to inspect the underlying query or data.

- **[Firefox Public Data Report — User Activity](https://data.firefox.com/dashboard/user-activity)** — Inspect metric definition and region selection. Put the measurement boundary beside the chart and keep selected-region values and labels aligned.

- **[Taipower Daily Power Information](https://www.taipower.com.tw/d006/loadGraph/loadGraph/load_briefing3.html)** — Inspect load, utilization, and capacity. Combine a current quantity with its capacity reference and a readable state; expose the calculation and observation time.

- **[GitHub Status](https://www.githubstatus.com/)** — Inspect component status and uptime. Organize status by user-facing task, then link current state to useful historical evidence.

- **[rustc performance data](https://perf.rust-lang.org/)** — Inspect comparison baseline and interpolation note. Make the chosen comparison and missing-data treatment visible. Keep estimated or carried-forward values distinct from measurements.

- **[Open Electricity (OpenNEM) NEM Tracker](https://explore.openelectricity.org.au/energy/nem/)** — Inspect time range, resolution, and generation groups. Coordinate period and resolution while keeping resulting units visible; offer groupings that answer distinct analytical questions.

- **[Plausible Analytics Public Demo](https://plausible.io/plausible.io)** — Inspect period selector and comparison values. Update values and comparison context together, and preserve appropriate selection state in a shareable URL.

- **[Matomo Online Demo](https://demo.matomo.cloud/)** — Inspect overview widgets and live visits. Use modular regions when the tasks are genuinely independent; connect summary measures to relevant events rather than adding unrelated widgets.

- **[Wikimedia Movement Metrics Monthly Report](https://upload.wikimedia.org/wikipedia/commons/a/ab/February_2025_Wikimedia_movement_metrics.pdf)** — Inspect metric interpretation and missing-data notes. Keep a periodic static report interpretable with useful source links, definition changes, and specific missing-data explanations.

- **[Wikimedia Topviews Analysis](https://pageviews.wmcloud.org/topviews?project=en.wikipedia.org)** — Inspect ranked table and excluded items. Pair consumption with contribution when the question needs both, and make consequential filtering visible beside the result.

- **[Hacker News Insight (TiDB+Evidence)](https://hackernews-insight.vercel.app/)** — Inspect schema, composition, and trends. For a data-exploration audience, establish the data shape and quality before detailed analysis; make calculations retrievable.

- **[RIPEstat Routing Status](https://stat.ripe.net/8.8.8.8)** — Inspect routing visibility and input conversion. State the observation time, analyzed entity, and denominator; explain an input transformation when it changes what was analyzed.

- **[What Firefox trains are we in?](https://whattrainisitnow.com/)** — Inspect current channels and next milestone. Answer a narrow recurring question with the current relationship and next relevant event instead of inventing a larger dashboard.

- **[OpenAQ Explorer](https://explore.openaq.org/)** — Inspect sensor type and freshness filters. Expose meaningful source-quality and freshness differences when comparing measurements, with an accessible alternative to the map.

## Technical and editorial foundations

- [MapReduce, section 5 and Figure 3](https://storage.googleapis.com/gweb-research2023-media/pubtools/4449.pdf): compare normal execution and changed conditions with aligned evidence, then explain the visible difference through system behavior.
- [PEP 703, Performance](https://peps.python.org/pep-0703/#performance): put build configuration and baseline with a historical measurement rather than implying current-product performance.
- [Circuit Tracing](https://transformer-circuits.pub/2025/attribution-graphs/methods.html): distinguish an instrument's output, an inferred mechanism, and its validation. A convincing graph is not sufficient causal evidence.
- [Google SRE's fictional postmortem example](https://sre.google/sre-book/example-postmortem/): separate impact, trigger, recovery, and corrective action; use actual evidence in a real operational view.
- [Datawrapper on chart text](https://datawrapper.de/blog/text-in-data-visualizations), [Wilke on making a point](https://clauswilke.com/dataviz/telling-a-story.html), and [IBM Carbon dashboards](https://carbondesignsystem.com/data-visualization/dashboards): choose a useful comparison and make text, visual hierarchy, and detail work together.

For document-level information selection and prose, use `technical-report-writing` when available. For shadcn component behavior, use the [official shadcn skill](https://ui.shadcn.com/docs/skills) when available or consult the official component documentation. Match techniques to the current reader task instead of importing a brand skin or fixed template.
