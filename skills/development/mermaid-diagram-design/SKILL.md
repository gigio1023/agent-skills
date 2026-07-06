---
name: mermaid-diagram-design
description: |
  Use when the user asks for Mermaid diagrams, flowcharts, sequence diagrams,
  architecture diagrams, diagram refactors, or diagram readability fixes.
  Guides type selection, reader-first layout direction, anti-pattern avoidance,
  parser-safe syntax, accessibility, color/edge visibility, density checks, and
  render validation. NOT for draw.io native XML authoring; use drawio-diagram.
---

# Mermaid Diagram Design

Use this skill to create Mermaid diagrams that help the reader understand a
system, workflow, or decision quickly. The diagram must reduce ambiguity and make
the main message easy to verify.

All reusable instructions, examples, labels, and outputs in this skill must be
English unless the user explicitly asks for another language. Use neutral sample
domains and never include private company names, internal product names, customer
data, incident details, or unreleased project context.

## Reference Files

| File | When to read | What's in it |
| --- | --- | --- |
| `references/mermaid-patterns.md` | Before choosing a pattern, palette, or renderer preset | Type matrix, frontmatter presets, reusable patterns, palette, validation checklist, aesthetic rules |

## Quick Start

1. Identify the diagram's single message and target reader.
2. Choose the diagram type by purpose: workflow, interaction timeline, layered
   architecture, or state transition.
3. Choose layout direction from the reader path, label length, renderer width,
   and density. Do not default to `LR`, `TD`, or `TB`.
4. Draft 6-12 nodes when possible. Split dense, mixed-message, or scroll-heavy
   diagrams before tuning spacing.
5. Apply parser-safe labels, accessible metadata when useful, and visible edge
   styling.
6. Run density and render validation for markdown files that contain Mermaid
   blocks.

## Hard Rules

- Use `<br/>` for visual line breaks in labels. Do not use literal `\n`; Mermaid
  renders it as text.
- Apply line-break safety to node labels, edge labels, subgraph titles, and all
  Mermaid diagram types.
- Use the Professional Color Palette from `references/mermaid-patterns.md` by
  default.
- When nodes have color, set edge visibility explicitly, such as
  `linkStyle default stroke:#455a64,stroke-width:1.8px;`.

## Workflow

### 1. Split By Message

- Use one primary message per diagram.
- Split complex topics into multiple diagrams instead of forcing one large graph.
- If the document needs several diagrams, give each one a distinct purpose.

### 2. Choose The Diagram Type

- Sequential process, funnel, or branching workflow: `flowchart`
- Request/response timeline: `sequenceDiagram`
- Layered responsibility or architecture boundary: `flowchart + subgraph`,
  `architecture`, or `block`
- State transitions: `stateDiagram`

Select a reusable pattern from `references/mermaid-patterns.md` when one fits.

### 3. Choose Layout Direction

Direction is a reader decision, not a default.

- Use `LR` when the reader must compare parallel lanes, ownership boundaries,
  before/after states, or handoffs across systems.
- Use `TD` or `TB` when the reader must follow a short sequential path, funnel,
  or decision tree.
- Avoid defaulting to `LR` just because the diagram feels architectural. Long
  labels, many branches, and narrow renderers usually make `LR` harder to scan.
- Avoid defaulting to `TD` or `TB` just because the process is sequential. A tall
  scroll tunnel is also hard to read; split by phase or collapse repeated steps.
- Do not rescue the wrong direction with spacing first. Simplify, split, or
  change direction before tuning `nodeSpacing` and `rankSpacing`.

Treat layout risk as high when any condition is true: 12 or more nodes, 16 or
more edges, four or more long labels in `LR`, many cross-subgraph edges, or a
`TD`/`TB` diagram that needs scrolling to connect cause and effect.

### 4. Draft The Structure

- Prefer 6-12 nodes and three levels of depth or fewer.
- Use verb-focused edge labels such as `validate`, `emit`, or `drop`.
- Use `subgraph` only for meaningful boundaries such as ownership, layer, or
  runtime environment.
- Move long explanations into prose. Keep diagram labels short.
- Merge duplicate terminal, drop, or error nodes into shared nodes.
- Split diagrams that mix structure, runtime flow, and detailed mapping.

### 5. Configure And Style

- Prefer Mermaid frontmatter over inline directives for new diagrams.
- Consider `layout: elk` for complex graphs.
- For narrow renderers such as Confluence, prefer simpler structure and split
  diagrams before relying on config-only fixes.
- Pair color with labels or line style; do not rely on color alone.
- Avoid excessive `<b>` and `<i>` tags because they increase box width.
- Include `accTitle` and `accDescr` when the output document benefits from
  accessibility metadata.

### 6. Preflight And Validate

For markdown files that contain Mermaid blocks:

```bash
scripts/assess_mermaid_density.sh <markdown-file>
scripts/validate_mermaid_markdown.sh <markdown-file>
```

Fix and rerun when density reports `contrast_risk=high`,
`edge_style=absent` on colored diagrams, or render validation fails. Also check
common parser breakers: lower-case `end` labels, `o-`/`x-` edge-head surprises,
comments that do not start with `%%`, ignored `subgraph` direction, missing
`sequenceDiagram` participants, and tab characters.

## Output Contract

Always provide:

1. The improved Mermaid code block.
2. Three to six concise improvement notes.
3. The selected pattern name and one sentence explaining why it fits.
4. Preflight results: density diagnosis and render validation status.

When editing a markdown file, also provide the density command, validation
command, and final validation result, such as `MERMAID_VALIDATE_OK ...`.

## Gotchas

- **Direction defaults hide layout bugs.** `LR` can make dense architecture look
  impressive but unreadable; `TD` can turn a simple process into a scroll tunnel.
  Pick direction from the reader path, then verify it against density.
- **Spacing is the last fix.** If a diagram needs extreme spacing values to avoid
  overlap, the structure or direction is wrong.
- **One diagram is not a document outline.** When a graph explains both topology
  and detailed mapping, split it instead of adding more labels and edges.
- **Renderer support differs.** If a host ignores Mermaid frontmatter, trust
  simpler structure and smaller diagrams over renderer-specific configuration.
