# Data and Comparison

Use when selecting measures or transforming data. Work from the supplied files, queries, or documented API rather than the desired appearance.

## Establish what is comparable

Inspect row meaning, units, dates/time zones, population, filtering, missing values, duplicated records, and aggregation. For evaluated systems, preserve the tested version, workload, budget, and measurement definition when they change the result. A source-specific metric does not become a universal performance claim.

Compute totals, rates, differences, and rankings with code. Keep percentage-point changes distinct from relative percentage changes. Do not average percentages with different denominators without a valid weighting scheme. Keep failed requests visible when comparing successful-request latency; report sample sizes and uncertainty when they affect the choice. A missing observation is not zero, and an observed correlation is not a cause.

Retain a small trace from displayed values to source rows/query and transformation code in the project. The reader-facing page needs the useful source link and necessary measurement note, not the entire processing log. Reuse the project's data model rather than inventing a universal dashboard schema.

## Choose the chart for the question

| Question | Useful starting point | Check |
| --- | --- | --- |
| Which category is higher? | Sorted bars or dots | Comparable denominator and common axis; bars normally start at zero |
| What changed over time? | Lines, with meaningful event annotations | Consistent time intervals, missing periods, and comparable series |
| Where is the variation? | Distribution, box plot, histogram, or quantiles | Binning/sample size and tail behavior; do not hide spread behind an average |
| What trade-off does a choice make? | A relevant two-axis comparison or small multiples | Both axes affect the decision; no unsupported composite score |
| Which exact record needs attention? | Sorted/filtered table | Useful columns, units, stable row identity, and reason for prioritization |
| How is a total composed? | Stacked bars or a concise composition view | Part-whole relation is valid; the reader can compare the segment that matters |

These are starting points, not chart quotas. Prefer a plain comparison over a novel encoding that needs an instruction manual. Keep status colors stable across panels and add text or shape cues. Do not use misleading truncated bars or dual axes to magnify a difference.

Sources: [IBM Carbon dashboards](https://carbondesignsystem.com/data-visualization/dashboards), [Datawrapper on text](https://datawrapper.de/blog/text-in-data-visualizations), and [Wilke, Telling a story and making a point](https://clauswilke.com/dataviz/telling-a-story.html). Their editorial patterns inform selection; correctness of a particular statistic still depends on its own data and method.
