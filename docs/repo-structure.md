# Repository Structure

How this skill pack is organized and how skills reach a coding agent: local
skills in two categories are indexed by the README, exposed through
per-harness install adapters, and installed into coding agents. External
skill repos are referenced from the index but not packaged here.

```mermaid
---
config:
  theme: base
  themeVariables:
    textColor: "#1f2937"
    edgeLabelBackground: "#f8fafc"
---
flowchart LR
  accTitle: agent-skills repository structure
  accDescr: Local skills in two categories are indexed by the README, exposed through per-harness install adapters, and installed into coding agents. External skill repos are referenced but not packaged.

  subgraph repo ["agent-skills repository"]
    IDX["README.md<br/>skill index"]
    subgraph pack ["skills/ local pack"]
      DEV["development · 17 skills<br/>draft-pr, skill-builder,<br/>gpt56-sol-prompting-guide, ..."]
      PROD["productivity · 8 skills<br/>handoff-prompt-writer,<br/>write-pr, ..."]
    end
    ADP["Install adapters<br/>.claude · .codex · .cursor · .gemini"]
  end

  EXT["External skill repos<br/>unity-game-dev, astro-dev"]

  subgraph agents ["Coding agents"]
    CC["Claude Code"]
    CX["Codex"]
    OT["Cursor · Gemini CLI"]
  end

  IDX --> DEV & PROD
  IDX -.->|references only| EXT
  DEV & PROD --> ADP
  ADP -->|install| CC & CX & OT

  classDef packNode fill:#BBCCEE,stroke:#336699,color:#1f2937;
  classDef adapter fill:#CCDDAA,stroke:#228833,color:#1f2937;
  classDef outside fill:#DDDDDD,stroke:#555555,color:#1f2937;
  classDef boundary fill:#f8fafc,stroke:#94a3b8,color:#1f2937;
  classDef index fill:#ffffff,stroke:#64748b,color:#1f2937;
  class DEV,PROD packNode;
  class ADP adapter;
  class CC,CX,OT,EXT outside;
  class repo,pack,agents boundary;
  class IDX index;
  linkStyle default stroke:#64748b,stroke-width:1.6px;
```

Color key: blue = skills packaged in this repo, green = install adapters,
gray = things outside the pack (agents that consume it, external repos that
are only referenced). Edge labels use a fixed light background and dark text
so their text remains legible over lines in both light and dark viewers. Skill
counts are as of 2026-07; the README tables are the source of truth.
