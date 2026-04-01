# Agent Skills

A collection of custom agent skills for AI coding assistants (Claude Code, Codex, etc.).

## Repository Structure

```
skills/
  development/       # Software development workflows & frameworks
  productivity/      # Content creation, research & utilities
```

## Custom Skills

### Development

| Skill | Description |
|-------|-------------|
| [unity-dev](skills/development/unity-dev/) | Unity 3D game development -- scene manipulation, C# scripting, architecture patterns (DI, SOA, FSM, GOAP), rendering, NPC AI, UI, audio, testing, CI/CD. Includes multi-agent framework and 20+ advisory sub-skills |
| [skill-builder](skills/development/skill-builder/) | Design and create high-quality agent skills (SKILL.md + directory structure) |

### Productivity

| Skill | Description |
|-------|-------------|
| [humanize](skills/productivity/humanize/) | Detect and fix AI-sounding expressions, invented terminology, and unnatural phrasing in any document (KO/EN) |
| [x-post](skills/productivity/x-post/) | Draft X (Twitter) posts to promote blog posts in dry developer voice |
| [pdf-page-count](skills/productivity/pdf-page-count/) | Count PDF pages and validate page limits (e.g. 1-page resume enforcement) |
| [web-research-audit](skills/productivity/web-research-audit/) | Validate web research quality -- check for partial reads, narrow sources, stale evidence, and error propagation |

## Skills Installed via `npx skills`

The following skills are installed globally via [`npx skills add`](https://skills.sh) and are **not** included in this repo.

### From [gigio1023/astro-dev-skill](https://github.com/gigio1023/astro-dev-skill)

```bash
npx skills add gigio1023/astro-dev-skill@astro-dev
```

| Skill | Description |
|-------|-------------|
| **astro-dev** | Astro 6 development patterns -- .astro/.mdx files, content collections, Tailwind CSS v4, client directives, server features, view transitions, and adapter setup |

### From [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)

```bash
npx skills add kepano/obsidian-skills@obsidian-bases
npx skills add kepano/obsidian-skills@obsidian-cli
npx skills add kepano/obsidian-skills@obsidian-markdown
```

| Skill | Description |
|-------|-------------|
| **obsidian-bases** | Create and edit Obsidian Bases (.base files) with views, filters, formulas, and summaries |
| **obsidian-cli** | Interact with Obsidian vaults via CLI -- read, create, search, manage notes/tasks/properties |
| **obsidian-markdown** | Obsidian Flavored Markdown -- wikilinks, embeds, callouts, properties |

### From [vercel-labs/skills](https://github.com/vercel-labs/skills)

```bash
npx skills add vercel-labs/skills@find-skills
```

| Skill | Description |
|-------|-------------|
| **find-skills** | Discover and install agent skills by querying "how do I do X" or "find a skill for Y" |


### OpenCode Skills (`~/.config/opencode/skills/`)

```bash
# Exact source repos unknown — installed via npx skills
```

| Skill | Description |
|-------|-------------|
| **smart-commit** | Analyze repo changes, follow contribution rules, create reversible commits, and push safely |
| **validate-review-and-fix** | Validate external review feedback against the current repo, apply valid fixes, then use smart-commit to finish |

### Codex System Skills (`~/.agents/skills/.system/`)

Bundled with Codex from [openai/skills](https://github.com/openai/skills):

| Skill | Description |
|-------|-------------|
| **imagegen** | Generate or edit raster images using AI |
| **openai-docs** | Up-to-date OpenAI product/API documentation |
| **plugin-creator** | Scaffold plugin directories for Codex |
| **skill-creator** | Guide for creating or updating Codex skills |
| **skill-installer** | Install skills from the curated list or any GitHub repo |

## Installation

To use these custom skills, copy or symlink into your agent's skills directory:

```bash
cp -r skills/development/unity-dev ~/.agents/skills/
# or
ln -s "$(pwd)/skills/development/unity-dev" ~/.agents/skills/unity-dev
```

## License

Personal use.
