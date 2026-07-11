# Repository Structure

The README presents the 20 bundled skills in six task-oriented categories.
Their existing source paths stay under `skills/development/` and
`skills/productivity/` because the Skills CLI records each installed skill's
exact path for future updates. The catalog taxonomy can improve without
breaking that compatibility surface.

Installation has one owner: [`npx skills`](https://github.com/vercel-labs/skills).
The CLI discovers the pack, records remote-source metadata, and manages the
destinations for explicitly selected agents. This repository does not carry
per-harness installation adapters.

```mermaid
---
config:
  theme: base
  themeVariables:
    textColor: "#1f2937"
    edgeLabelBackground: "#f8fafc"
---
flowchart LR
  accTitle: agent-skills catalog, source, and installation boundaries
  accDescr: The README groups skills by task. Stable source paths flow through the Skills CLI into selected agents, while standalone repositories are referenced only.

  subgraph repo ["agent-skills repository"]
    IDX["README catalog<br/>6 task categories"]
    SRC["Stable skill sources<br/>development · productivity"]
  end

  CLI["npx skills<br/>add · list · update"]

  subgraph agents ["Selected agents"]
    CX["Codex"]
    CC["Claude Code"]
    OT["Cursor · Gemini CLI · others"]
  end

  EXT["Standalone skill repositories<br/>referenced, not bundled"]

  IDX -->|indexes| SRC
  SRC -->|remote install| CLI
  CLI --> CX & CC & OT
  IDX -.->|links only| EXT

  classDef source fill:#BBCCEE,stroke:#336699,color:#1f2937;
  classDef installer fill:#CCDDAA,stroke:#228833,color:#1f2937;
  classDef outside fill:#DDDDDD,stroke:#555555,color:#1f2937;
  classDef index fill:#ffffff,stroke:#64748b,color:#1f2937;
  class IDX index;
  class SRC source;
  class CLI installer;
  class CX,CC,OT,EXT outside;
  linkStyle default stroke:#64748b,stroke-width:1.6px;
```

Color key: blue is the packaged source, green is the installation and update
path, gray is outside the pack, and white is the reader-facing index. The
README tables are the source of truth for catalog membership.

## Boundaries

- `README.md` owns discovery, task categories, installation, and update
  guidance.
- `skills/<source-category>/<skill-name>/` owns each bundled skill and its
  colocated references, scripts, and assets.
- `npx skills` owns agent selection, installation destinations, lock metadata,
  and on-demand updates.
- Related standalone and external repositories are linked for discovery but
  are not copied into this pack.
