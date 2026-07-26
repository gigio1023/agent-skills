---
name: mermaid-diagrams
description: |
  Use when the user asks for Mermaid diagrams, flowcharts, sequence diagrams,
  architecture diagrams, diagram refactors, or diagram readability fixes.
  Guides type selection, reader-first layout, parser-safe syntax, palettes and
  dark-mode-safe styling, renderer compatibility, density control, and render
  validation. NOT for draw.io native XML authoring; use drawio-diagram.
---

# Mermaid Diagrams

Produce a Mermaid diagram that a human reads correctly on the first pass and
that actually renders on the destination host. Readability outranks
completeness: a diagram that needs study has failed even if every fact is in
it.

Baseline: Mermaid v11.16 syntax, written down to the version-safe subset when
the destination host is older or unknown. Keep reusable examples in English
with neutral sample domains; for user artifacts, follow the requested or
source language and never introduce names, incident details, or unreleased
context the user did not provide.

## Reference Files

| File | Read when |
| --- | --- |
| `references/syntax-pitfalls.md` | Before writing any non-trivial diagram, or when a diagram fails to parse — line-break trap, parser breakers, escaping, frontmatter config |
| `references/diagram-catalog.md` | Choosing a type, choosing detail level, or wanting a starting pattern — includes v11 types and compact-vs-detailed forms |
| `references/color-and-style.md` | When color/emphasis would add meaning — ready palettes, themeVariables, dark-mode survival, hierarchy without color |
| `references/renderer-compat.md` | When the destination host matters or before shipping — host matrix, version gates, validation workflow |

## Non-Negotiable Syntax Rules

The five failures that dominate real-world broken diagrams:

1. **Line breaks are `<br/>`, never `\n`.** Literal `\n` renders as visible
   `\n` text in sequence messages, notes, and state labels (render-verified),
   and on older hosts everywhere else.
2. **Quote any label with punctuation**: `A["validate (strict)"]`. Unquoted
   `()[]{}|;#&` breaks the parser.
3. **Never use lowercase `end`** as a node/label word in flowcharts and
   sequence diagrams; write `End` or quote it.
4. **Flowchart arrows are `-->`**, not `->`.
5. **Balance every block**: `subgraph`/`end`, `alt`/`end`, `activate +`/`-`.

## Workflow

1. **One message.** State what the reader must be able to verify in one
   sentence. Split topics that need two sentences into two diagrams.
2. **Type by reader task** (`diagram-catalog.md`): process → `flowchart`,
   call order → `sequenceDiagram`, boundaries → subgraphs or
   `architecture-beta`, lifecycle → `stateDiagram-v2`, data model →
   `erDiagram`.
3. **Direction from the reading path, not habit.** `LR` for comparisons,
   lanes, and handoffs; `TD`/`TB` for short sequential paths and decision
   trees. Long labels, many branches, or a narrow host argue against `LR`;
   a scroll-tunnel argues against `TD`. Restructure or split before touching
   `nodeSpacing`/`rankSpacing`, and treat 12+ nodes, 16+ edges, or many
   cross-subgraph edges as a signal to simplify.
4. **Draft at the right detail level** (`diagram-catalog.md`): compact form
   for overviews (chained edges, `&` fan-out, shared terminal nodes, labeled
   edges instead of trivial diamonds); detailed form for design docs
   (subgraphs for real boundaries, markdown-string labels, `autonumber`,
   `alt`/`par` blocks). Labels stay short — sentences belong in prose.
5. **Style only with purpose** (`color-and-style.md`): unstyled is the most
   portable and often best. When color encodes meaning, use the bundled
   palettes (fill + stroke + text always set together so dark mode cannot
   break contrast), pair color with labels or line style, keep to ≤4 colors,
   and set edge visibility (`linkStyle default stroke:#64748b`) when fills
   would wash edges out. When edges carry text, set `edgeLabelBackground`
   and `textColor` together so the label remains readable over lines and on
   both host themes. Add `accTitle`/`accDescr` when the destination benefits
   from accessibility metadata.
6. **Validate** (`renderer-compat.md`): for repository markdown, run the
   bundled density and render scripts (absolute paths, from any cwd):

   ```bash
   SKILL_DIR="<absolute path to this skill>"
   "$SKILL_DIR/scripts/assess_mermaid_density.sh" "<absolute markdown path>"
   "$SKILL_DIR/scripts/validate_mermaid_markdown.sh" "<absolute markdown path>"
   ```

   Render failure blocks; fix and rerun. Density warnings start a visual
   look, not automatic deletion. Then inspect the rendered output (or host
   preview) for clipping, literal `\n`, unreadable crossings, and reading
   order.

## Authority

Return what was asked: a code block for "give me a diagram", a file edit for
"add/fix the diagram in this doc". Do not restructure surrounding documents,
re-theme existing diagrams, or convert diagram types beyond the request; if a
different type would serve the reader clearly better, deliver the requested
artifact and note the alternative in one sentence.

## Output Contract

Artifact first. Add design notes only for non-obvious choices the user should
review (direction choice, what was omitted in a compact form, host caveats).
Report validation results only for checks actually run, naming the renderer
used; never imply visual inspection happened when only parsing was checked.

## Gotchas

- **Direction defaults hide layout bugs.** Dense `LR` architecture renders
  impressive and unreadable; sequential `TD` becomes a scroll tunnel. Pick
  from the reader path, then check the render.
- **A compact diagram that silently dropped a required fact is wrong**, not
  elegant — say what was compressed out, or split instead.
- **Host version is part of correctness.** Markdown strings, `@{ shape: }`,
  ELK, and beta diagram types fail or degrade on pinned hosts (GitLab 11.4,
  mkdocs-material 10.x, Confluence plugins). Unknown host → version-safe
  subset.
- **`linkStyle` indexes shift** when edges are added or reordered — re-check
  indexed styles after any edge edit.
- **Edge labels need their own contrast pair.** Styling nodes and lines does
  not protect text on an edge; set both `edgeLabelBackground` and `textColor`
  in `themeVariables`, then inspect the light and dark render.
- **Density thresholds are heuristics.** They trigger a look at the render;
  required nodes and relationships stay.
