# Mermaid Renderer Compatibility And Validation

Where the diagram will be viewed decides which syntax is safe. Host versions checked 2026-09-23, when Mermaid core latest was 12.0.0 (released 2026-09-10); pinned host versions drift, so verify when a feature matters.

## Contents

- Host matrix
- Version-safety rules
- Validation workflow

## Host Matrix

| Host | Mermaid version | Notes |
| --- | --- | --- |
| GitHub | 11.17.2 (version string in the `viewscreen.githubusercontent.com` Mermaid bundle; render an `info` block to recheck) | Sandboxed iframe rendering; no JS/click. Theme auto-syncs to viewer light/dark mode only for unstyled diagrams. |
| GitLab | 11.16.1 on master (`mermaid-v11: npm:mermaid@11.16.1`, with `@mermaid-js/layout-elk` 0.2.2) | Older self-managed releases may run an older engine; 50k char limit. Self-managed with `Cross-Origin-Resource-Policy` headers can silently break rendering. |
| VS Code | Built into core markdown preview (`extensions/mermaid-markdown-features`; main declares `mermaid ^11.16.1`, lockfile 11.17.0) | Stable releases trail main. Light/dark theme settings; `maxTextSize` setting. |
| mermaid-cli (`mmdc`) | 11.17.0; declares `mermaid ^11.14.0`, so an unpinned `npx` renders the newest 11.x (11.17.2), not 12.0 | ELK bundled; renders via headless Chromium — good validation oracle for v11. Checking v12 needs a pinned override (Validation Workflow). |
| Docusaurus | Follows the site lockfile: `@docusaurus/theme-mermaid` 3.10.2 accepts `mermaid >=11.6.0`, so a fresh install resolves 12.0.0 | Config controllable site-wide; ELK needs `@mermaid-js/layout-elk` on an 11.x lockfile and is bundled in 12. |
| mkdocs-material | Newest 11.x, loaded from `unpkg.com/mermaid@11` (since 2024-08) | Material's own `themeCSS` restyles diagrams; v12 defaults do not apply unless the site loads its own Mermaid. |
| Confluence | Plugin-dependent, often old | No native support. Assume no frontmatter, no new types, narrow width; simpler structure beats config. |
| Notion | Code-block language with preview | Basic support; verify anything beyond core types. |

## Version-Safety Rules

- **Unknown host → write to the v10-safe core**: stable diagram types, `<br/>` line breaks, quoted labels, `%%` comments, `classDef`, and no frontmatter-only features. This subset renders everywhere.
- **Frontmatter vs directives**: frontmatter (v10.5+) is preferred and safe on GitHub/GitLab/VS Code today; hosts running older engines need `%%{init: {...}}%%` or nothing.
- **Feature gates worth remembering**: markdown-string labels and `A@{ shape: ... }` extended shapes need v11.3+; edge ids/animation v11.10+; `swimlane-beta` v11.16; collapsible subgraphs (`@{ view: collapsed }`), ER subgraphs, and the `person`/`folder`/`bucket`/`console`/`browser` shapes v11.17; `usecase-beta` and `agentflow-beta` v12.0. GitLab's 11.16.1 lacks the v11.17 features, and only a v12 host renders the v12 types.
- **v12 changes the defaults, not the syntax**: an unconfigured flowchart, state, class, or ER diagram re-lays out with ELK and takes the `redux-color` theme and `neo` look, and the engine needs ES2024 (Safari 17.4+). See `syntax-pitfalls.md` for the per-major defaults and the pin that keeps the v11 look.
- **`layout: elk` degrades silently** to dagre when the host lacks ELK (a v11 host without `@mermaid-js/layout-elk`, or v12's tiny build) — never depend on it for correctness, only for polish.
- **Interactivity (`click`, actor `link`) requires `securityLevel: loose`** on the host; GitHub/GitLab never grant it. Treat links as progressive enhancement.
- When a diagram must ship on a host you cannot test, state which renderer you validated with in the PR/doc so reviewers on other hosts know what to expect.

## Validation Workflow

For markdown files in a repository, run the bundled scripts from the installed skill directory (any working directory; pass absolute paths):

```bash
SKILL_DIR="<absolute path to mermaid-diagrams skill>"
"$SKILL_DIR/scripts/assess_mermaid_density.sh" "<absolute markdown path>"
"$SKILL_DIR/scripts/validate_mermaid_markdown.sh" "<absolute markdown path>"
```

- `validate_mermaid_markdown.sh` renders every ```` ```mermaid ```` block with `@mermaid-js/mermaid-cli` (needs `npx` + `rg`). `MERMAID_VALIDATE_OK` means every block parsed and rendered; any failure prints the parser error and is blocking — fix and rerun.
- The unpinned `npx -y @mermaid-js/mermaid-cli` in that script renders with the newest Mermaid 11.x, because mermaid-cli 11.17.0 (its latest release on 2026-09-23) declares `mermaid ^11.14.0`. To check a v12 destination, install mermaid-cli in a scratch directory whose `package.json` pins the engine through npm `overrides`, run `npm install` there (Node 22.12+), and run the validator with that directory as the working directory; `npx` then uses the local install. Render an `info` block first to confirm the engine version. The script runs `mmdc` without `-t`, which passes `theme: default` at initialization, so this check shows v12's ELK layout and `neo` look but not the `redux-color` palette; judge v12 colors in the host preview.

  ```json
  {
    "private": true,
    "dependencies": { "@mermaid-js/mermaid-cli": "11.17.0" },
    "overrides": { "mermaid": "12.0.0", "@mermaid-js/layout-elk": "1.0.0" }
  }
  ```

- `assess_mermaid_density.sh` reports nodes/edges/long-labels per block with a risk level. A warning is a prompt to look at the render, not an instruction to delete content.
- Then inspect the rendered SVG/PNG or host preview at target width for: clipped or overlapping labels, unreadable edge crossings, `\n` shown literally, low-contrast nodes, and a reading order that fights the intended story.
- If the render toolchain is unavailable, say so: report syntax review and visual verification as separate claims, and never imply a diagram was render-checked when it was not.
- For questions this skill does not answer, consult the official docs source directly (`https://mermaid.js.org` or a sparse clone: `git clone --depth 1 --filter=blob:none --sparse https://github.com/mermaid-js/mermaid.git vendor/mermaid && cd vendor/mermaid && git sparse-checkout set packages/mermaid/src/docs`). Keep such clones out of version control (gitignore `vendor/`).
