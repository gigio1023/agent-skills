# Agent Skills

A personal collection of agent skills that I use across Claude Code, Codex, Cursor, and other skills-compatible coding agents.

This repo is different from the standalone skill repos in this workspace:

- it contains **multiple local skills** under `skills/`
- it also serves as an index for a few **separate standalone skill repos**
- it is useful when you want one place to browse, install, or symlink several skills at once

## Installation

Installation differs a little depending on how you want to use the repo.

- Use **`npx skills add`** when you want a normal skills-compatible install flow.
- Use **a local path** when you are developing the skills in this repo.
- Use **symlinks** only if you intentionally want the agent to read directly from your working copy.

### Install from a local checkout

If you already cloned this repo locally, install a skill from the current folder:

```bash
npx skills add ./agent-skills --skill unity-dev
npx skills add ./agent-skills --skill skill-builder
```

Install several at once:

```bash
npx skills add ./agent-skills \
  --skill unity-dev \
  --skill skill-builder \
  --skill web-research-audit
```

### Install from GitHub

```bash
npx skills add gigio1023/agent-skills --skill unity-dev
npx skills add gigio1023/agent-skills --skill skill-builder
npx skills add gigio1023/agent-skills --skill web-research-audit -g
```

### Manual symlink setup

Use this only when you want your agent to track the live files in this repo.

<details>
<summary>Claude Code</summary>

```bash
ln -s "$(pwd)/skills/development/unity-dev" ~/.claude/skills/unity-dev
ln -s "$(pwd)/skills/development/skill-builder" ~/.claude/skills/skill-builder
```
</details>

<details>
<summary>Codex CLI</summary>

```bash
ln -s "$(pwd)/skills/development/unity-dev" ~/.codex/skills/unity-dev
ln -s "$(pwd)/skills/development/skill-builder" ~/.codex/skills/skill-builder
```
</details>

<details>
<summary>Other agents</summary>

```bash
ln -s "$(pwd)/skills/productivity/x-post" ~/.agents/skills/x-post
ln -s "$(pwd)/skills/productivity/pdf-page-count" ~/.agents/skills/pdf-page-count
```
</details>

### Verify installation

Start a fresh session in your agent and ask for something that should clearly trigger one of these skills.

Examples:

- `review this Unity project architecture`
- `make a skill for this workflow`
- `count pages in this PDF`
- `audit this web research`

If the install worked, the agent should discover the matching skill without you having to explain the whole workflow again.

## Included local skills

These skills live directly in this repo under `skills/`.

| Skill | Category | Description |
| --- | --- | --- |
| [unity-dev](skills/development/unity-dev/) | Development | Unity 3D game development patterns, architecture, performance, NPC AI, tooling, and workflows |
| [skill-builder](skills/development/skill-builder/) | Development | Design and create high-quality agent skills (`SKILL.md`, references, and structure) |
| [x-post](skills/productivity/x-post/) | Productivity | Draft dry developer-style X posts for blog promotion |
| [pdf-page-count](skills/productivity/pdf-page-count/) | Productivity | Count PDF pages and enforce page-limit checks |
| [web-research-audit](skills/productivity/web-research-audit/) | Productivity | Audit web research quality, source coverage, and evidence freshness |

## Standalone skill repos I maintain

These are separate repos in the same workspace, but not packaged inside this repo.

| Skill | Source | Description |
| --- | --- | --- |
| [astro-dev](https://github.com/gigio1023/astro-dev-skill) | `gigio1023/astro-dev-skill` | Astro 6 guardrails for coding agents |
| [humanize-doc](https://github.com/gigio1023/humanize-doc) | `gigio1023/humanize-doc` | Rewrite AI-sounding drafts into readable human documents |
| [drawio-diagram](https://github.com/gigio1023/drawio-agent-skill) | `gigio1023/drawio-agent-skill` | Create editable draw.io diagrams instead of one-off XML |

Install them with `npx skills add owner/repo@skill-name`, for example:

```bash
npx skills add gigio1023/astro-dev-skill@astro-dev
npx skills add gigio1023/humanize-doc@humanize-doc
npx skills add gigio1023/drawio-agent-skill@drawio-diagram
```

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
├── README.md
└── skills/
    ├── development/
    │   ├── skill-builder/
    │   └── unity-dev/
    └── productivity/
        ├── pdf-page-count/
        ├── web-research-audit/
        └── x-post/
```

## License

Personal use.
