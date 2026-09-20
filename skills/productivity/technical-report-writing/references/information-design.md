# Information Design

Use when a document needs a new structure, repeated tables conceal the explanation, or a visual contains too much. Make the reader's question determine the unit of presentation. These planning decisions belong in the work, not in a compulsory planning artifact or a preamble to the finished document.

## Reader questions and depth

Establish what a reader should understand or do after each section. Keep the background that makes that possible; omit details gathered only because they were available. Give a first-time reader the necessary context near the claim or example rather than asking them to study a glossary first.

| Purpose | Essential content | Useful structure |
| --- | --- | --- |
| Factual record | Events, observations, impact | Chronology and topic groups |
| Technical explanation | Problem, operation, consequence | Example and mechanism |
| Comparison | Common criteria and differences | Compact table and interpretation |
| Proposal | Change, alternatives, reasons | Recommendation and supporting evidence |
| Procedure | Preconditions, actions, outcomes | Ordered steps |

A restrained factual record may be excellent for an incident brief and insufficient for introducing a technology. Transfer its precise headings, grouping, terminology, and focused figures. Do not transfer the absence of explanatory reasoning to a guide or proposal. Conversely, a request for a factual record does not require speculative causes or recommendations.

Structure must carry meaning. Repeating “One-line summary / Definition / Why it matters” for every concept can create a verbose document made entirely of bullets. Use those elements where they do work, without repeated labels or empty nesting. Several related bullets often need one connective sentence explaining their relationship.

## Table design

Decide the row entity and shared attributes before filling cells. A row may represent a configuration, event, option, component, or lookup term. Headers should name actual attributes, not serve as containers called “Content” or “Notes” for everything left over.

Use these repairs:

- **Different questions across columns:** split into views such as runtime behavior and operating cost, retaining stable row names so readers can connect them.
- **Different kinds of rows:** separate approaches, packaging formats, and measurements instead of assigning them one invented progression or ranking.
- **Paragraphs in cells:** extract the comparison values, then explain the mechanism or trade-off under the table. If there are no common values to compare, use short subsections or a list.
- **Repeated context:** move units and common settings into headers or one local note. Remove columns whose value is constant or irrelevant.
- **Few rows but dense cells:** redesign the information, not just the column widths. A three-column table can still be overloaded.
- **Large factual inventory:** group by the reader's lookup needs and show the relevant subset. Keep a full inventory separately only when someone actually needs it.

A two-column term lookup or event record can be useful when entries are short and parallel. A single-row parameter summary can also fit a required form. Avoid mechanical bans based on shape; evaluate whether the grid aids comparison or lookup.

Cells normally hold a value, identifier, or short phrase. A row-specific condition stays with its value when removal would mislead. Extended explanation belongs beside the table. Do not replace several paragraphs per cell with several dense abbreviations per cell.

The finished table should not need a paragraph explaining that the “Problem” column lists problems and the “Solution” column lists solutions. Improve the labels and organization instead. Define a nonstandard measure when needed, once and at the point of use.

## Figure design

Before drawing, identify the reader's question, the entities or quantities needed, the relationship to show, and the intended reading order. These choices determine what to omit or split.

A process diagram shows operations and state transitions. A component view shows responsibilities and interfaces. A chart shows a quantitative comparison or pattern. A timeline shows change over time. Combining these is justified only when the combination directly answers the same question.

Split a visual when:

- overview and implementation details require different reading scales;
- several legends or reading directions compete;
- benchmark results are appended to a mechanism without helping explain it;
- historical context, distribution details, and internal adoption obscure the main path;
- the figure requires reduced type or long explanatory boxes to fit.

Keep matched panels together when the comparison depends on seeing them together. Splitting must preserve shared units, comparable scales, and the names connecting the views. An arbitrary one-panel rule can be as harmful as an overloaded canvas.

Use a short noun-phrase title. Label the operations on edges and the actual measures on axes. A caption supplies the finding or interpretation condition that the visible labels do not already convey. Do not restate the figure title, every box, and its construction history. Remove redundant warnings and decorative status badges.

## Document reading order

Place each visual beside the question it answers. Introduce only the vocabulary needed for the next explanation. After moving sections, repair figure numbering, cross-references, and captions; asset filenames need not determine visible numbering.

Put the supported finding or purpose early. Let the following blocks establish it. A source catalog, glossary, or archive inventory must not displace that route. Include those only for an actual lookup or audit need, and keep the main explanation self-contained.

At the delivered size, check table wrapping, readable figure labels, surrounding context, and page breaks. Break a long table deliberately, repeat headers where supported, and avoid leaving a section title with only its first row at a page bottom. Do not copy an otherwise useful example's cramped identifiers or awkward page breaks.
