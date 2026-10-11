# Mechanism Map Format

Use this layout when writing or extending a mechanism map. SKILL.md decides what enters the map, when an axis stops, and how security material is recorded; this file covers the file itself. Replace the bracketed guidance with observed facts, and leave out sections that have no content yet.

## Location and reuse

Keep one Markdown file per problem. Without an established layout, use `maps/<problem-slug>.md` beside the library's `index.md`; a project that keeps investigation write-ups in a research folder can hold the map there instead. The map is not a work, so it gets no row in `index.md`; the works it cites get their usual folders and rows. Link entries to each work's `source.md` with paths relative to the map file.

When extending an earlier map, keep its entries and evidence judgments, add the new axes and entries, and add a dated note where new evidence changes an earlier judgment rather than rewriting it silently. If the earlier map restated the problem differently, keep both statements and say which axes each covers.

## Header

```markdown
# Mechanism map: [problem in the requester's words]

- Restated problem: [the structure without the named field's vocabulary]
- Requested by: [user or calling skill], [date]
- Axes: [axis], [axis] ([named or derived])
- Budget: [stated budget]
- Fields searched: [named field]; [adjacent field], [adjacent field]
```

## Axis sections

One section per axis. Open it with the conventions the axis inherits, then list its entries.

```markdown
## [Axis]

Conventions: [metric, threat model, baseline, dataset, or early arbitrary choice]: [looks justified, or looks unjustified because ...]

### [Mechanism name]

- Problem: [what it addresses on this axis]
- Principle: [one line in your own words]
- Assumptions: [what must hold; what breaks it]
- Evidence: [strength in words]; [who measured, on which data and setting, against which baseline, with which metric]; [replicated independently, authors only, or claimed without measurement]; [convention marks from this axis]
- Cost: [compute, data or labels, latency, integration work, operating burden, what it rules out]
- Field: [named field, or adjacent field with what transfers and which assumption may not hold]
- Sources: [work](relative/path/source.md) section [n], figure [n], table [n]
```

State evidence strength in words tied to its conditions, not as a score. A result reproduced independently in the target setting is stronger than an authors-only result on a proxy setting, and a claim with no measurement is recorded as such. Keep any reported number with its unit, denominator, and setting.

For security and offense material, write the Problem and Principle fields in terms of the boundary, objective category, metric, and judge. Point Sources at the location of any procedure or example input instead of restating it.

## Findings across axes

```markdown
## Across axes

- Trade-offs: [mechanism] gains on [axis] at the cost of [axis]; evidence: [entry links]
- Conflicts: [result] against [result]; differing conditions: [data, metric, baseline, scale]; status: [which the evidence favors, or unresolved]
- Untried combinations: [mechanism] with [mechanism]; compatible because [assumptions]; not found combined in the searched sources on [date]
- Open gaps: [axis or sub-problem] has [no mechanism, or only unmeasured or authors-only claims]
```

## Search log

```markdown
## Search log

| Axis | Query shape | Field | Date | Triaged | New mechanisms |
| --- | --- | --- | --- | --- | --- |

Status: [axis] saturated; [axis] unsaturated, remaining shapes: [list]; [axis] out of scope
```

The log lets a later effort resume an unsaturated axis instead of repeating its search, and shows which query shapes produced the saturation call.

## Finding adjacent fields

Restate the problem as what is being decided, under which constraint, with what feedback, and what an error costs. "Stop unpromising training runs early" becomes "decide sequentially whether to keep paying for an uncertain process, given noisy interim measurements and a cost for stopping the eventual winner". Fields that face that structure include interim analysis in clinical trials, sequential testing in online experiments, and best-arm identification in bandits. Search each in its own vocabulary, then check which of its assumptions hold in the target setting, such as independence between observations or an analysis schedule fixed in advance.
