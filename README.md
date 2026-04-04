# Agent Skills

A personal multi-skill repo for coding agents.

This repo contains several local skills under `skills/` and also points to a few standalone skill repos I maintain separately.

## Installation

Preferred:

```bash
npx skills add gigio1023/agent-skills --skill unity-dev
```

Local checkout:

```bash
npx skills add ./agent-skills --skill unity-dev
```

### Codex

Tell Codex:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/gigio1023/agent-skills/refs/heads/main/.codex/INSTALL.md
```

Detailed docs: `docs/README.codex.md`

### Claude Code

Tell Claude Code:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/gigio1023/agent-skills/refs/heads/main/.claude/INSTALL.md
```

Detailed docs: `docs/README.claude.md`

### Gemini CLI

Tell Gemini CLI:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/gigio1023/agent-skills/refs/heads/main/.gemini/INSTALL.md
```

Detailed docs: `docs/README.gemini.md`

### Cursor

Tell Cursor:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/gigio1023/agent-skills/refs/heads/main/.cursor/INSTALL.md
```

Detailed docs: `docs/README.cursor.md`

## Included local skills

These skills live directly in this repo under `skills/`.

| Skill | Description |
| --- | --- |
| [unity-dev](skills/development/unity-dev/) | Unity 3D game development patterns, architecture, performance, NPC AI, tooling, and workflows |
| [skill-builder](skills/development/skill-builder/) | Design and create high-quality agent skills (`SKILL.md`, references, and structure) |
| [x-post](skills/productivity/x-post/) | Draft dry developer-style X posts for blog promotion |
| [pdf-page-count](skills/productivity/pdf-page-count/) | Count PDF pages and enforce page-limit checks |
| [web-research-audit](skills/productivity/web-research-audit/) | Audit web research quality, source coverage, and evidence freshness |

## Standalone repos I maintain

These are separate repos in the same workspace, but not packaged inside this repo.

| Skill | Source | Description |
| --- | --- | --- |
| [astro-dev](https://github.com/gigio1023/astro-dev-skill) | `gigio1023/astro-dev-skill` | Astro 6 guardrails for coding agents |
| [humanize-doc](https://github.com/gigio1023/humanize-doc) | `gigio1023/humanize-doc` | Rewrite AI-sounding drafts into readable human documents |
| [drawio-diagram](https://github.com/gigio1023/drawio-agent-skill) | `gigio1023/drawio-agent-skill` | Create editable draw.io diagrams instead of one-off XML |

## Other external skills I use

| Skill | Source | Description |
| --- | --- | --- |
| obsidian-bases | [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | Edit Obsidian Bases (`.base`) files |
| obsidian-cli | [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | Work with an Obsidian vault from the CLI |
| obsidian-markdown | [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | Obsidian-flavored Markdown editing |
| find-skills | [vercel-labs/skills](https://github.com/vercel-labs/skills) | Search and install more skills |

## Repo layout

```text
agent-skills/
└── skills/
    ├── development/
    └── productivity/
```
