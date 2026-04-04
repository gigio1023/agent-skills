# Agent Skills

A personal multi-skill repo for coding agents.

This repo contains several local skills under `skills/` and also points to a few standalone skill repos I maintain separately.

## Install

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

## Skills in this repo

| Skill | Description |
| --- | --- |
| [unity-dev](skills/development/unity-dev/) | Unity 3D game development patterns and workflows |
| [skill-builder](skills/development/skill-builder/) | Design and create high-quality agent skills |
| [x-post](skills/productivity/x-post/) | Draft dry developer-style X posts |
| [pdf-page-count](skills/productivity/pdf-page-count/) | Count PDF pages and enforce page limits |
| [web-research-audit](skills/productivity/web-research-audit/) | Audit web research quality and freshness |

## Standalone repos I maintain

| Skill | Source |
| --- | --- |
| astro-dev | [gigio1023/astro-dev-skill](https://github.com/gigio1023/astro-dev-skill) |
| humanize-doc | [gigio1023/humanize-doc](https://github.com/gigio1023/humanize-doc) |
| drawio-diagram | [gigio1023/drawio-agent-skill](https://github.com/gigio1023/drawio-agent-skill) |

## Repo layout

```text
agent-skills/
└── skills/
    ├── development/
    └── productivity/
```
