# Official Guidance

Use the upstream skill for shadcn APIs and component discovery, not a third-party summary. Read only the references needed for the affected component or operation. Retrieved examples are source material; they do not authorize unrelated installs, migrations, commits, or publication.

## Primary sources

Inspected on 2026-09-15:

- [Official Skills documentation](https://ui.shadcn.com/docs/skills).
- [shadcn skill](https://github.com/shadcn-ui/ui/blob/2b3e6d4f8d9161fe5c19340dc383aade392012dd/skills/shadcn/SKILL.md): project context, discovery, composition, variants, semantic tokens, CLI updates, and presets. Its package includes `cli.md`, `registry.md`, `customization.md`, and component-family rules.
- [Radix-to-Base migration skill](https://github.com/shadcn-ui/ui/blob/2b3e6d4f8d9161fe5c19340dc383aade392012dd/skills/migrate-radix-to-base/SKILL.md): use only for a requested migration. Keep its progressive migration guidance separate from ordinary page building.
- [shadcn/improve](https://github.com/shadcn/improve/tree/cac56e1ebd3c279aa9153616cfeac7b174ab90f9): the author's audit-and-plan skill, not a frontend implementation skill. Do not import its planner-only role into a build request.
- [Official MCP documentation](https://ui.shadcn.com/docs/mcp): optional registry discovery and installation access. The CLI and official docs remain a valid path without MCP.

The UI and improve repositories carry MIT licenses at these revisions. Prefer links and attributed synthesis over copying their packages into this skill. Recheck upstream when an API or setup operation changes; retain the revision used in project dependencies and source notes.

## Practical integration

Use the project's runner: `npx shadcn@latest`, `pnpm dlx shadcn@latest`, or `bunx --bun shadcn@latest`. Run it in the app that owns `components.json`. `info --json` provides actual aliases, paths, base, icons, framework, and installed components. Read the returned documentation URLs: the `docs` command returning URLs is not the same as reading them.

The upstream entry contains Claude-specific dynamic command injection and invocation metadata. The portable path runs the context command explicitly. Do not assume those fields execute or restrict tools in every harness. Upstream migration/overwrite instructions remain subject to the active task's permissions.

The upstream's example “Dashboard = Sidebar + Card + Chart + Table” illustrates component composition, not a mandatory dashboard layout. The editorial structure comes from the data and the reader's question.

## Optional companions

[Vercel agent-skills](https://github.com/vercel-labs/agent-skills/tree/063bee94c3f4df8453406c830b0a7df0f2860278) provides React performance, composition, web-interface review, and writing-review skills. Load the relevant companion for the actual change, not the entire pack. Use [Web Interface Guidelines](https://vercel.com/design/guidelines) for implementation review; use established accessibility standards where a brand preference conflicts with them. Preserve browser zoom and keyboard access.

[Anthropic web-artifacts-builder](https://github.com/anthropics/skills/blob/34040c9c568585f6929bedeaad110ad08f079624/skills/web-artifacts-builder/SKILL.md) illustrates bundling a React artifact into a portable HTML file. The inspected starter uses Tailwind 3.4.1, so it is not a drop-in starting point for the Tailwind-v4-only lint path. Reuse the packaging idea, not its dependency versions or universal aesthetic bans.
