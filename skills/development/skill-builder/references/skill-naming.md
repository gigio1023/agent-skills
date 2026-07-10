# Naming Agent Skills

Use this reference when creating or renaming a skill. A good name is a compact,
stable handle; the frontmatter description remains the primary discovery and
routing surface.

## Evidence Snapshot

Reviewed on 2026-07-10:

- the first 120 visible entries in the skills.sh all-time leaderboard;
- 44 top-level OpenAI catalog skills;
- 17 top-level Anthropic catalog skills;
- 9 Vercel agent skills; and
- 27 top-level Microsoft Azure skills.

In the leaderboard sample, 19 of 120 names contained an `-ing` token, 21 were a
single token, and 10 used four or more hyphen-separated tokens. Gerunds are a
valid pattern, but the ecosystem does not treat them as the default.
Anthropic's authoring guide likewise says to consider gerunds while explicitly
accepting noun phrases and action-oriented alternatives.

Representative names from the reviewed sample:

| Domain or capability | Action or command | Activity or method | Scoped or conventional |
| --- | --- | --- | --- |
| `pdf` | `find-skills` | `brainstorming` | `vercel-react-best-practices` |
| `pptx` | `grill-me` | `systematic-debugging` | `web-design-guidelines` |
| `xlsx` | `improve-codebase-architecture` | `writing-plans` | `microsoft-foundry` |
| `docx` | `setup-matt-pocock-skills` | `using-superpowers` | `remotion-best-practices` |
| `frontend-design` | `write-a-skill` | `requesting-code-review` | `azure-hosted-copilot-sdk` |
| `agent-browser` | `zoom-out` | `test-driven-development` | `lark-workflow-standup-report` |
| `azure-compute` | `redesign-existing-projects` | `executing-plans` | `supabase-postgres-best-practices` |
| `lark-doc` | `deploy-to-vercel` | `grilling` | `ui-ux-pro-max` |
| `handoff` | `extract-design-system` | `subagent-driven-development` | `caveman-commit` |
| `prototype` | `request-refactor-plan` | `verification-before-completion` | `security-threat-model` |
| `skill-creator` | `analyze-project` | `domain-modeling` | `security-ownership-map` |
| `webapp-testing` | `setup-pre-commit` | `receiving-code-review` | `figma-implement-design` |
| `openai-docs` | `scaffold-exercises` | `writing-great-skills` | `notion-spec-to-implementation` |
| `screenshot` | `migrate-to-shoehorn` | `writing-skills` | `react-native-skills` |
| `playwright` | `define-goal` | `diagnosing-bugs` | `react-view-transitions` |
| `sentry` | `transcribe` | `dispatching-parallel-agents` | `internal-comms` |

Sources:

- https://www.skills.sh/
- https://github.com/openai/skills/tree/main/skills
- https://github.com/anthropics/skills/tree/main/skills
- https://github.com/vercel-labs/agent-skills/tree/main/skills
- https://github.com/microsoft/azure-skills/tree/main/skills
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

## Choose The Shape

Start from the user's language and choose the shortest shape that stays clear:

1. **Domain or capability label** for a broad, recognizable surface:
   `pdf`, `frontend-design`, `openai-docs`.
2. **Action-object or command** for a bounded operation:
   `find-skills`, `deploy-to-vercel`, `define-goal`.
3. **Activity or method** when the process itself is the reusable capability:
   `systematic-debugging`, `writing-plans`, `requesting-code-review`.
4. **Outcome, policy, or guardrail** when the result or invariant is the useful
   handle: `verification-before-completion`, `security-threat-model`.

Add a scope prefix only when it disambiguates a crowded catalog. Keep branch
names, paths, implementation tools, and temporary lifecycle states in the
description unless users genuinely distinguish the skill by that term.

## Candidate Pass

Generate three candidates in different shapes, say each aloud as a command or
menu item, then score 0-2 on:

- immediate meaning;
- natural phrasing;
- distinction from sibling skills;
- search terms users are likely to type; and
- durability if implementation details change.

Prefer two or three meaningful tokens. One token is fine for an established
format, product, or concept. Four or more tokens need a concrete reason. Do not
add `agent` or `skill` merely to announce the package type.

## Rename Gate

Before accepting a name:

- compare it with every sibling name and description;
- confirm the directory and frontmatter name match;
- update package indexes, examples, cross-skill references, and install docs;
- test positive and near-miss trigger prompts after the rename; and
- keep source constraints and exclusions explicit in the description.

Reject a candidate that is grammatical but awkward, encodes incidental
implementation detail, or needs its description to explain what the words mean.
