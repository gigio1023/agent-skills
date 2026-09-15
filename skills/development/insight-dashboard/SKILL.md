---
name: insight-dashboard
description: >
  Use when creating or redesigning a data dashboard, interactive analysis report,
  or static dashboard for print. Makes the key comparison and supported insight
  visible before exploration. NOT for generic forms or landing pages
  (shadcn-frontend), or ordinary technical prose documents (technical-report-writing).
---

# Insight Dashboard

Deliver a data view that answers the reader's question, using real results and an intelligible initial view. Select the useful comparison before choosing components. A collection of metrics is not an analysis, and the reader should not need to discover the author's point by manipulating filters.

## Connect the content and production skills

For a technical analysis, use `technical-report-writing` when available for dry factual prose, measurement conditions, mechanisms, and sentence-to-caption examples. For an internal deliverable, use `share-internal-doc` when available for reader context, recipient suitability, and source access. Apply these specialties within this task without restarting intake. Without optional companions, retain a clear question, supported interpretation, material comparison conditions, and usable sources, without promotional copy, process narration, or irrelevant definitions.

When implementing in shadcn/ui, use `shadcn-frontend` for project discovery, composition, lint, and rendered behavior. For a PDF or static document, use the document-production guidance in `technical-report-writing` instead. Shadcn is a web implementation choice, not a required intermediate format for every dashboard.

## Choose the useful shape

- **A report that communicates a finding:** put the supported finding and decisive comparison first, then contributing factors, alternatives, or the observations that explain it. Add exploration only when it serves another reader question.
- **An exploration tool:** start with an informative comparison and visible selections. Search, filters, drill-down, and linked charts should let readers answer the stated class of questions.
- **Operational monitoring:** prioritize exceptions, current state, freshness, and the action needed. Do not manufacture an executive narrative over a screen whose purpose is to detect problems.

Read [data and comparison](references/data-and-comparison.md) when choosing measures, transformations, and charts. Read [interaction and static delivery](references/interaction-and-static.md) when filters, sharing, or printing change the visible population. These are design choices, not compulsory headings.

## Make the point visible

Give the decisive comparison more space and visual emphasis than supporting data. Use a finding-bearing chart title where the data supports one; let axis labels and a short local note supply units and conditions. Do not repeat the same statement in a title, caption, metric card, and paragraph. Use neutral question-based headings when the result is genuinely unresolved.

Choose chart forms by the comparison: aligned bars or dots for categories, lines for change over time, distributions for spread, and scatterplots for a meaningful relationship. A table is often best for exact lookup. Use a common scale for comparable panels and direct labels where they reduce lookup effort. Avoid converting every datum into a card or compressing a wide data dump until it fits.

Keep limitations that change interpretation beside the affected result. Delete generic disclaimers, routine definitions, UI tours, and claims about the report's rigor. A useful methods section explains an actual calculation or sampling choice; it does not warehouse every deleted sentence. The [pattern examples](references/pattern-examples.md) illustrate how technical reports state and explain evidence, rather than supplying fixed brand skins.

## Build and verify

Compute displayed quantities from the supplied data; keep missing values distinct from zero. Do not invent metrics to fill a layout. If the main comparison cannot be supported, expose the specific missing input and continue only with supported views. Development fixtures must be visibly synthetic and stay out of an unlabeled shared report.

Verify the calculation, displayed population, and interpretation together. Exercise changed filters and empty states; confirm derived statements update or remain attached to a clearly separate fixed analysis. Inspect the result at its delivered size. For PDF, replace interactions with the selected comparisons and retain necessary labels, sources, and conditions on the page.

Deliver the requested working dashboard or document and its editable source. Use the original request's publication and installation permissions. Keep build/check details in the short delivery note, not in the reader-facing dashboard.
