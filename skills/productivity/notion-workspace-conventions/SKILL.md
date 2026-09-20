---
name: notion-workspace-conventions
description: >
  Use whenever a task reads, writes, moves, or reorganizes content in this
  user's Notion workspace through the Notion MCP: saving notes or research,
  creating or updating pages and database rows, deciding where a document
  belongs, or preparing a Notion-delivered document. Triggers on "Notion에
  저장", "Notion 정리", "노션 문서", and "save/update/organize in Notion".
  Defines this workspace's destinations, naming, language mix, and edit
  policies on top of the official notion-* skills. NOT for restating Notion
  MCP tool syntax; the tool descriptions and notion://docs resources own that.
---

# Notion Workspace Conventions

This skill defines how this user's Notion workspace is organized and edited: where durable content goes, how pages are titled, which language is used, and which changes need confirmation first. It sits on top of two layers that already exist and does not duplicate them.

## Layering

| Layer | Owner |
| --- | --- |
| Tool capability and call syntax | Notion MCP tool descriptions, plus the `notion://docs/*` resources fetched on demand |
| Generic task playbooks: knowledge capture, meeting prep, research reports, spec breakdown | Official `notion-knowledge-capture`, `notion-meeting-intelligence`, `notion-research-documentation`, `notion-spec-to-implementation` skills |
| This workspace's destinations, naming, language, and policies | This skill |

When a playbook suggests a destination, title, or edit that this skill governs differently, this skill wins. When the workspace map and a live page disagree, the page wins; report the drift and update the map in the source repository.

## Before Creating A Page

1. Search the workspace for an existing page on the topic; updating a found page beats creating a near-duplicate.
2. Resolve the destination from [references/workspace-map.md](references/workspace-map.md).
3. If the destination is unmapped, search, propose one matching parent, and let the user confirm. Do not guess, and do not create a top-level page on your own initiative.
4. Title the page per the naming rules below before writing content.

## Naming And Language

- Write new pages in English by default: English titles and English body prose.
- Use Korean-based titles — Korean topic with English technical terms inline — only when the user explicitly asks for Korean; the scope-after-colon pattern then applies (예: "클라이언트 × 프록시 상세 비교: 기능·경로·보존 범위").
- Whatever the language, product names, system names, code identifiers, and API terms stay in English exactly as written.
- Dated documents such as meeting records and direction notes carry the date in the title, matching their neighbor pages (관측 패턴: "8/31 리더십 회의 …", "… 제품 방향성 260807").
- One page serves one purpose. Split when a section starts serving a different reader.

## Quality Bar For New Or Rewritten Pages

- Lead with the conclusion or summary; detail follows, it does not open the page.
- Short paragraphs, meaningful `##` sections, lists for real enumerations; no decorative formatting for its own sake.
- Make claims checkable: cite source pages as native page mentions rather than bare URLs, and state uncertainty explicitly instead of padding it.
- Link a new page back from its hub once so it stays discoverable; do not scatter duplicate links.

## Editing Existing Pages

- Make the smallest complete edit: match the page's heading levels, language mix, and list style, and leave paragraphs you were not asked to touch alone.
- Never move, rename, or re-parent an existing page, never change database schemas (properties, options, views), and never change page sharing; propose the change and wait for confirmation.
- Scratchpad is private scratch space: never link to it from other pages and never route durable content there.

## Gotchas

- Page titles in this workspace are mostly Korean; search Korean terms first, then English.
- When the target is a database, fetch it first and use its data source ID and exact property names; the schema owns the row's shape.
- If the Notion MCP is not connected, stop and report that; this skill does not replace the connection.
- Conventions are maintained in the agent-skills repository; edits to an installed copy are overwritten by `skills update`.
