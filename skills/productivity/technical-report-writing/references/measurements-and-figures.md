# Measurements and Figures

Use when a document presents data, equations, comparison tables, or technical figures. Check the underlying evidence and calculations before optimizing the display. A restrained style can still make a false comparison appear credible.

## Specify the measured quantity

Identify the unit of observation: request, user, run, machine, task, or dataset example. Keep counts distinct from independent trials. State the relevant population, period, version, hardware, workload, concurrency, warm-up, caching, budget, and success criteria where they affect interpretation. Avoid repeating the full setup beside every number; expose the decisive conditions locally and link a useful methods section.

Define nonstandard metric boundaries. Does latency start before queueing? Does it include retries? Is throughput completed work or attempted work? Does a success rate include timeouts? Is cost per attempt, per successful task, or per token? Do not let familiar metric names hide different calculations.

Compute arithmetic with code or a spreadsheet. Show numerator and denominator when a rate would otherwise be ambiguous. Keep absolute differences, relative changes, ratios, and percentage-point changes distinct. Do not average subgroup percentages with incompatible denominators or silently pool dependent trials. Display precision supported by the measurement rather than every decimal available from a tool.

## Preserve uncertainty and the comparison

Use the same measure, unit, population, and relevant budget across compared systems. If a difference is unavoidable, make it visible and qualify the conclusion. Separate measurement at a historical revision from current product behavior. A source's self-reported benchmark remains an attributed result until independently reproduced.

Keep missing, not measured, failed, timed out, and zero distinct. State how censored or failed observations enter the summary. A lower successful-request latency can coexist with more failures; show both when the decision depends on reliability. Report variability and uncertainty when they affect ranking or a proposed threshold. Label intervals with their type and construction rather than drawing unexplained error bars.

A repeated run, an ablation, a paired comparison, and a causal intervention answer different questions. Describe the actual procedure. If a confidence interval or significance test was not computed, do not invent one; report the observed variation and the limitation it creates. “Not statistically significant” is not proof of equivalence.

## Tables

Make column headings carry repeated context: units, metric names, direction when unclear, and relevant settings. Align numeric values for comparison, keep precision consistent, and order rows for the reader's question. Use restrained emphasis on the meaningful comparison, not a badge in every cell. A status column can be useful; a “verified” decoration usually does not add evidence.

Keep conditions that change a row's interpretation beside that row. Use a short note for a shared exclusion or measurement rule. Keep long explanations out of cells unless the table truly compares prose attributes. A one-row table of unrelated facts is often clearer as a sentence or list. Do not fill missing cells with invented zeroes.

For alternatives, compare the same decision dimensions and explain the chosen trade-off in prose. Avoid a composite score unless its meaning and weights are justified for this decision. Exact lookup may need a table even when a chart looks more impressive.

## Figures and captions

Choose a figure because it clarifies a mechanism, change, distribution, or comparison. Show a decisive result at a legible size before adding detail. Comparable panels need compatible axes and scales, or an explicit reason for differences. Use direct labels when they reduce legend lookup; preserve units, baseline, and the actual meaning of color. Do not rely on color alone.

A caption should identify what was measured or depicted and supply the local interpretation condition missing from the title and axes. Add the finding there only if it is not already clearly stated nearby. Point to a panel or visible feature when explaining a mechanism; do not tour every mark. A methods detail such as fixed attention patterns can be part of the figure's meaning, while a generic warning about the limits of all research is not.

For an ablation or failure experiment, compare the normal and changed condition on aligned panels and explain the expected versus observed effect. MapReduce's Figure 3 uses matched input/shuffle/output panels for normal execution, disabled backup tasks, and killed workers. The useful transfer is the controlled comparison and interpretation, not its historical hardware or palette.

For architecture figures, show real responsibilities, interfaces, state, and flow. Label different kinds of edges. An overview can omit implementation detail but cannot silently remove a component that explains the failure or trust boundary. Use a companion sequence or detailed view when one diagram becomes unreadable.

## Equations, code, and reproduction

Define each symbol's meaning, unit, and domain before or beside its first useful use. Explain what the equation computes and why it is the right quantity; do not use notation to make ordinary arithmetic look scientific. Keep the displayed formula, implementation, and reported value consistent. Refer to equations by number only when that helps navigation.

A code example should demonstrate the behavior under discussion with the smallest meaningful context. Mark pseudocode as such, preserve assumptions affecting order or state, and keep executable examples aligned with the documented version. A historical RFC's provisional syntax is evidence of its design argument, not a modern copy-paste example.

Keep input references, transformation code, configurations, and actual results in the authorized project. Use stable links and versions rather than personal paths in a shared report. Distinguish reproduction instructions from a reproduction already performed. Never manufacture plausible output because a run or download failed.

## Output checks

Verify calculations independently of rendering. Check that the table, chart, text, and filtered view use the same population and definition. Inspect the final document at its delivered size, not just the editable source. For PDF, make essential data visible without hover or controls, preserve searchable text and citations, and inspect dense figures and page boundaries. Use an accessible summary or data representation when the chart is not independently interpretable.
