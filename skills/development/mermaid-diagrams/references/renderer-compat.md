# Mermaid Renderer Compatibility And Validation

Where the diagram will be viewed decides which syntax is safe. Facts
gathered 2026-07; pinned host versions drift, so verify when a feature
matters.

## Contents

- Host matrix
- Version-safety rules
- Validation workflow

## Host Matrix

| Host | Mermaid version | Notes |
| --- | --- | --- |
| GitHub | ~11.15 (user-reported; render an `info` block to check) | Sandboxed iframe rendering; no JS/click. Theme auto-syncs to viewer light/dark mode only for unstyled diagrams. |
| GitLab | 11.4.1 (upgraded for architecture/block/kanban/packet) | Pre-11.13 label regressions patched host-side; 50k char limit. Self-managed with `Cross-Origin-Resource-Policy` headers can silently break rendering. |
| VS Code | Built into core markdown preview (from vscode-markdown-mermaid, ~11.12) | Light/dark theme settings; `maxTextSize` setting. |
| mermaid-cli (`mmdc`) | Tracks latest (11.16 as of this snapshot) | ELK bundled; renders via headless Chromium — good validation oracle. |
| Docusaurus | `@docusaurus/theme-mermaid`; v11 from Docusaurus 3.6 | Config controllable site-wide; ELK needs explicit registration. |
| mkdocs-material | Pinned older major (10.x) | New v11 diagram types and frontmatter features lag — keep to stable syntax. |
| Confluence | Plugin-dependent, often old | No native support. Assume no frontmatter, no new types, narrow width; simpler structure beats config. |
| Notion | Code-block language with preview | Basic support; verify anything beyond core types. |

## Version-Safety Rules

- **Unknown host → write to the v10-safe core**: stable diagram types,
  `<br/>` line breaks, quoted labels, `%%` comments, `classDef`, and no
  frontmatter-only features. This subset renders everywhere.
- **Frontmatter vs directives**: frontmatter (v10.5+) is preferred and safe
  on GitHub/GitLab/VS Code today; hosts running older engines need
  `%%{init: {...}}%%` or nothing.
- **Feature gates worth remembering**: markdown-string labels and
  `A@{ shape: ... }` extended shapes need v11.3+; edge ids/animation
  v11.10+; `swimlane-beta`, collapsible subgraphs (`@{ view: collapsed }`),
  ER subgraphs are v11.16 and effectively preview-only.
- **`layout: elk` degrades silently** to dagre when the host lacks the ELK
  package — never depend on it for correctness, only for polish.
- **Interactivity (`click`, actor `link`) requires `securityLevel: loose`**
  on the host; GitHub/GitLab never grant it. Treat links as progressive
  enhancement.
- When a diagram must ship on a host you cannot test, state which renderer
  you validated with in the PR/doc so reviewers on other hosts know what to
  expect.

## Validation Workflow

For markdown files in a repository, run the bundled scripts from the
installed skill directory (any working directory; pass absolute paths):

```bash
SKILL_DIR="<absolute path to mermaid-diagrams skill>"
"$SKILL_DIR/scripts/assess_mermaid_density.sh" "<absolute markdown path>"
"$SKILL_DIR/scripts/validate_mermaid_markdown.sh" "<absolute markdown path>"
```

- `validate_mermaid_markdown.sh` renders every ```` ```mermaid ```` block
  with `@mermaid-js/mermaid-cli` (needs `npx` + `rg`). `MERMAID_VALIDATE_OK`
  means every block parsed and rendered; any failure prints the parser
  error and is blocking — fix and rerun.
- `assess_mermaid_density.sh` reports nodes/edges/long-labels per block
  with a risk level. A warning is a prompt to look at the render, not an
  instruction to delete content.
- Then inspect the rendered SVG/PNG or host preview at target width for:
  clipped or overlapping labels, unreadable edge crossings, `\n` shown
  literally, low-contrast nodes, and a reading order that fights the
  intended story.
- If the render toolchain is unavailable, say so: report syntax review and
  visual verification as separate claims, and never imply a diagram was
  render-checked when it was not.
- For questions this skill does not answer, consult the official docs
  source directly (`https://mermaid.js.org` or a sparse clone:
  `git clone --depth 1 --filter=blob:none --sparse
  https://github.com/mermaid-js/mermaid.git vendor/mermaid && cd
  vendor/mermaid && git sparse-checkout set packages/mermaid/src/docs`).
  Keep such clones out of version control (gitignore `vendor/`).
