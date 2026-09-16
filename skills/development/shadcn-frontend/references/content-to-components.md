# Content to Components

Use when the page contains technical prose, data comparisons, operational status, or a visual explanation. Choose the content relationship first, implement it with the installed primitives, and verify the resulting behavior. Public works illustrate information design; they are not shadcn implementations or component API specifications.

## Report with a decisive comparison

**Intent:** let the reader understand the finding and inspect its evidence.

**Compose:** use a clear document heading, short finding paragraph, and a dominant comparison table or figure. Put method detail beside the affected result or in a named disclosure. Give longer documents an anchored contents list. Preserve the prose's reading order in the DOM and let a wide figure extend beyond the text measure when useful.

**Example:** a synthetic configuration report shows completion counts and successful-request latency in one table. Its note states how timeouts enter the comparison. A methods disclosure contains replay setup; it does not hide the denominator needed to understand the first view.

**Verify:** read the initial viewport without operating controls, navigate headings and anchors with a keyboard, and check that long headings and values remain legible at a narrow width. Print the selected comparison and material conditions rather than collapsed methods controls.

**Study:** [Distill Feature Visualization](https://distill.pub/2017/feature-visualization/), figure-adjacent explanation; [LLVM Compile-Time Tracker](https://llvm-compile-time-tracker.com/), configuration, values, and changes; [Datawrapper on chart text](https://datawrapper.de/blog/text-in-data-visualizations), complementary text roles.

## Filtered analysis with consistent meaning

**Intent:** change the selected population without disconnecting values from their explanation.

**Compose:** keep selection state in the project's router or established state owner. Validate URL parameters against allowed values. Derive the request and all selection-dependent representations from that state. Bind rows, totals, percentages, title, chart, and export to the same result; keep fixed editorial context visibly separate. Clear or deliberately reconcile dependent selections when their parent changes.

**Example:** selecting a service updates the period label, attempted/completed counts, latency series, and finding together. With no matching rows, the page says that the selection has no observations and offers a relevant reset; its headline does not retain the previous service's improvement.

**Verify:** select a population that reverses the original ranking. Reload the URL, use browser back, reset, and change filters rapidly under delayed responses. Confirm that the newest selection owns the displayed result. A URL shares a query; add a data version or snapshot mechanism only when an immutable result is required. Keep confidential filter values out of URLs when their exposure is inappropriate.

**Study:** [Plausible demo](https://plausible.io/plausible.io), selected period in URL and changing values; [Evidence KPI portal](https://evidence-demo.netlify.app/), date-based navigation; [Vercel interface guidelines](https://vercel.com/design/guidelines), URL state and usable controls.

## Operational exceptions and drill-down

**Intent:** identify what needs attention, then inspect its evidence.

**Compose:** use a current-state summary followed by a prioritized table with stable row IDs. Align comparable numbers and put units in column headings. Use status text with semantic color, keeping severity distinct from investigation state. Link a row's entity name to detail; use a dialog only when the detail is a bounded task that benefits from preserving the current context.

**Example:** a synthetic service row shows the service name, observed availability, remaining error budget, latest observation time, and investigation state. Opening detail preserves the selected time window. Stale telemetry is labeled stale rather than converted to a healthy or failed service verdict.

**Verify:** sort raw numeric values rather than formatted strings, inspect a long service name and dense rows, follow detail and return to the prior selection, and test stale and failed-refresh states. Keep keyboard focus and screen-reader names meaningful.

**Study:** [Grafana SLO overview](https://play.grafana.org/d/slo-dashboard-overview/slo-overview?orgId=1), comparable service rows; [GitHub Status](https://www.githubstatus.com/), user-facing component boundaries; [Cloudflare Status](https://www.cloudflarestatus.com/), incident state and severity.

## Definition beside a data view

**Intent:** make a value interpretable without overwhelming the reading path.

**Compose:** put the unit, active period, and important population condition next to the value. Use an expandable definition for longer calculation details. A tooltip can supplement a visible label, not replace essential meaning. Provide a table or textual representation for an interactive chart where needed.

**Example:** a synthetic completion-rate view shows completed and attempted counts with the rate. A definition explains timeout handling. A query/source link opens only material the intended recipients are permitted to access.

**Verify:** compare values across card, chart, and table; test a zero denominator; inspect keyboard access to the definition; confirm that print carries the selected denominator and definition needed for interpretation.

**Study:** [Mozilla GLAM](https://glam.telemetry.mozilla.org/), sample/client counts and metric details; [RIPEstat](https://stat.ripe.net/8.8.8.8), visibility with its observation denominator and input transformation; [Firefox Public Data Report](https://data.firefox.com/dashboard/user-activity), definitions beside charts.

## Explain one changing parameter

**Intent:** show how one input changes system behavior.

**Compose:** give the control a name, unit or domain, visible value, and initial state. Place a short observation prompt before the demonstration and the explanation after it. Drive related representations from one model. Prefer a native or installed accessible input; add reset when readers need to return to the comparison baseline.

**Example:** an independently synthetic retry demonstration changes the acknowledgement delay while showing lease ownership and stored output. The explanatory text names the transition to watch. A static export shows labeled before/after states and the same rule.

**Verify:** change the parameter with keyboard and pointer input and check the expected semantic state, not merely a changed pixel hash. Exercise boundary values and reset. Respect reduced-motion preferences and provide a readable fallback if a canvas or WebGL view cannot render.

**Study:** [Red Blob Games hexagonal grids](https://www.redblobgames.com/grids/hexagons/), linked coordinate views; [GPS](https://ciechanow.ski/gps/), parameter guidance and progressive explanation. A working widget on one source page does not verify another page's implementation.

## Choose the output deliberately

**Intent:** deliver the format the recipient can actually use.

**Compose:** keep the source facts and calculations shared, while selecting a layout for the medium. For a hosted app, preserve access controls and meaningful navigation. For offline HTML, package necessary scripts, fonts, images, and data according to their licenses and the sharing scope. For print, expose selected content and replace controls with labels or comparison panels. For a new print-first report, use native document tooling directly.

**Verify:** open the built file in its intended environment, disable networking for offline promises, and inspect the actual PDF for hidden tabs, clipped tables, missing glyphs, and unreadable labels. Verify asset and data access as the intended recipient where authorized.

**Study:** [Wikimedia's monthly metrics PDF](https://upload.wikimedia.org/wikipedia/commons/a/ab/February_2025_Wikimedia_movement_metrics.pdf), a static periodic report; [Red Blob Games hexagonal grids](https://www.redblobgames.com/grids/hexagons/), print and interactive forms. Select the useful information rather than reproducing a source's technology stack.
