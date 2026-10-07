---
name: write-notion
description: >
  Use when the user asks to create, draft, restructure, or revise a team
  document as a Notion page through the Notion MCP tools: a design doc or RFC
  for a new module or feature, an open-questions page, a short decision record,
  or any team page whose layout, tables, mentions, or figures need work.
  Phrases include "write the design doc in Notion", "put this RFC on our
  Notion", "Notion에 설계 문서 써줘", "노션 페이지 고쳐줘", and "fix the tables on
  this Notion page". A publication workflow skill: chooses the document shape,
  page layout, people mentions, tables, and figures, edits Notion Markdown
  safely, and verifies the stored page. copydesk owns sentence-level writing;
  technical-figure draws the figures. NOT for quick chat answers, Notion
  database administration, saving chat or meeting content as notes, meeting
  pre-reads, research synthesis across existing pages, turning a spec into
  tasks, or documents published outside Notion (use copydesk).
---

# Write Notion

Publish a team document in Notion that a colleague can review from the page alone. The design or decision is on the first screen, details are one click away, people are referenced without leaking names or flooding notifications, and the stored page matches what was intended.

This is a publication workflow skill, in the way `write-issue` is for trackers. It owns the document shape, the Notion page layout, people references, tables, figures, the Notion Markdown editing mechanics, and post-publish verification. It is not a style skill: `copydesk` owns sentence-level writing (meaning preservation, claim strength, voice, and the author's writing profile) and applies to every paragraph, bullet, caption, and table cell. `technical-figure`, or the project's own figure tool, draws the figures; this skill decides which figures the page needs and uploads them. Tracker issues and pull requests stay with `write-issue` and `draft-pr`; the page links to them.

Not for: an answer that belongs in chat, database schema, view, or property administration, saving chat or meeting content as notes, meeting pre-reads and agendas, research synthesis across existing pages, turning a spec into tasks, or a document delivered as a file or on another platform.

The user's instruction and a team template or existing page convention win over the layout defaults below. The people rules and the verification pass apply whatever the convention.

## Normal Path

1. Read before writing. Fetch the target page or the destination parent, a few sibling pages, and any template the team uses, and match their language and conventions. Check who can read the destination (a teamspace, the whole workspace, or a page published to the web); keep secrets, credentials, personal data, and customer-confidential text out, and apply `copydesk`'s sharing-and-delivery reference for a wider audience. Read the source material the page will rest on: code, measurements, meeting records, tracker items. Read the Notion enhanced Markdown specification once per session when the client exposes it. [Notion Markdown mechanics](references/notion-markdown.md) covers the tools, exact syntax, and failure modes.
2. Choose the shape before drafting: the genre, the section order, and what stays visible versus what goes under toggles. [Document shapes](references/document-shapes.md) gives the design doc skeleton, the open-questions page, and the decision record.
3. Draft the content with `copydesk`. Resolve the few people mentions the page needs, and render and upload its figures.
4. Decide whether to show the draft first. Show the complete draft and wait when the user asked for a draft, the page belongs to someone else and editing it was not authorized, the destination is a guess, the edit would delete child pages or databases, or a mention could notify someone other than the owner the user named. Otherwise the request is the grant; add no second confirmation. With no destination named for a new page, create a private draft page and say that it is private.
5. Write with `notion-create-pages` for a new page or `notion-update-page` for an existing one, using the smallest edit that does the job.
6. Verify the stored page with the checks in [Verification](#verification) and fix what fails.
7. Report as described in [Report](#report).

Without a working Notion connection, deliver the page as Notion Markdown and say that nothing was published. Do not install or authenticate a connector implicitly.

## Shape Before Writing

Decide the genre first, because it decides the sections. A new module, service, or feature uses a design doc (also called an RFC). One consequential choice uses a short decision record. A question list, when the user asks for one or it outgrows the design doc's Open questions section, is its own short page grouped by when each question must be answered: before review, during implementation, or out of scope. Group by person only when asked. A guide, report, or runbook takes its structure from `copydesk`'s document forms; this skill still handles its Notion layout.

The default design doc order is:

1. Header callout: Status (WIP, In Review, Approved, Obsolete), Owner as a user mention, Reviewer as a role, Target, a date mention, and repository and tracker links.
2. Summary, then Context and scope, then Goals and Non-goals. Non-goals are optional; when they are omitted, the heading is "Goals".
3. Design, with the mechanism figure first and details after it.
4. Cross-cutting concerns the design changes, such as security, privacy, observability, or migration and rollback.
5. Alternatives considered, each with its rejection reason.
6. Test plan or pre-launch evaluation, then Milestones.
7. Open questions, then References.

Drop a section that has nothing true to say instead of filling it with a placeholder. Section purposes, size guidance, and the shapes of the other genres are in [document shapes](references/document-shapes.md).

## Page Layout

- **Summary** is nested bullets: what is being built, how it works, the scope promised by the deadline, and the key undecided item. A top-level bullet carries a short label and the claim; nested bullets carry its reason or condition.
- **Visible:** summary, context, goals, figures, and open questions. A reader who never opens a toggle still learns what is proposed, why, and what is undecided.
- **Under toggle headings:** measurement tables, storage, interfaces, cross-cutting concerns, alternatives, test plan, schedule, and references. Toggles are the default for detail on a design doc page, but the decision summary and the open questions are never toggled.
- **Undecided items:** the writing profile's rule applies; on a Notion page: the Open questions section is a visible heading near the end, each question says what it blocks, and a passage that depends on an open item points to that question once.

## Status Words

The writing profile's rule applies; on a Notion page: status appears in the header callout's Status field, headings, body, table cells, and figure labels, and all of them must agree. Put "comparison evidence" in the heading of an option measurement table. Set Approved only when the reviewer role approved. When the owner decides, say where the decision was made, such as the design review on a date mention, and update every place the status appears, including re-rendering an affected figure, in the same edit.

## People

The writing profile's rule applies; on a Notion page:

- Identify a person who must be named, such as the owner or the directly responsible person, with a user mention found through `notion-get-users`, never `@Name` or a plain-text name.
- Mentions can notify, and names travel with exports and search. Mention as few people as possible, usually only the owner. Never list many mentions; a review audience is a role or a team, such as the repository's CODEOWNERS.
- Refer to someone outside the workspace by role or organization; they cannot be mentioned.
- Name an evidence link by what it is and when it was produced, such as "internal measurement on 2026-09-30". Do not attach author names to internal evidence such as measurements, meeting records, or drafts; published works keep their standard citation.
- On another author's page, keep their existing mentions unless asked to change them, and apply these rules to the passages you write or edit.

## Terms

The writing profile's rule applies; on a Notion page: one term per concept across text, tables, and figure labels. When a term changes, re-render and re-upload the affected figures in the same edit, because an uploaded image does not change with the text.

## Tables

The writing profile's rule applies; on a Notion page:

- Always set `<table header-row="true">`. Table attributes default to false, so without it the first row is ordinary data.
- Put what a cell cannot hold in bullets directly under the table; a cell never holds a sentence.
- Set column widths with `<colgroup>` and `<col width="N">`, sized to content: about 70 for a short status or yes/no column, 150 to 220 for names, and 240 to 300 for short descriptions. Keep the total to about 700 on a default-width page, less inside toggles and callouts, and wider on a full-width page. These are working values; confirm them on the rendered page. When the total overflows, move a column's content into the bullets under the table.
- Leave `fit-page-width` unset; the column widths size the table.
- Use a table to compare several items on shared attributes. One item, or content that needs sentences, belongs in bullets.

## Figures

- Make one figure per question the reader has, such as how the mechanism works or when requests arrive. The mechanism figure opens the Design section.
- Draw with `technical-figure` or the project's figure tool, and deliver a light-theme PNG.
- Upload with `notion-create-file-upload`, send one multipart POST of the file to the returned upload URL with the returned headers, and embed it with the `markdown_source` or `suggested_markdown` the upload returns, adding the caption. Write `![caption](file-upload://<upload-id>)` by hand only when neither is returned. The exact steps are in [Notion Markdown mechanics](references/notion-markdown.md#upload-a-figure).
- The upload needs a shell with network access, such as `curl`. Without one, give the PNG to the user and report that the figure is not attached; do not leave a path in the page.
- Write the caption as the claim first, then the reading key.
- When a label, term, or number in a figure changes, re-render, re-upload, and replace the old image. A file path or local link is not a figure.

## Editing Mechanics

The fragile points, with exact syntax in [Notion Markdown mechanics](references/notion-markdown.md):

- Fetch before editing. Prefer `update_content` for small text edits, with the smallest unique `old_str`.
- `update_content` cannot target image blocks, and its exact match can fail on long non-ASCII strings or strings that contain mention tags. When it fails, first retry with a shorter unique fragment that avoids the mention. If that also fails, fetch again and use `replace_content` with the whole body.
- Before a whole-body replace on a page with open discussions (check with `notion-fetch` and `include_discussions: true`), tell the user that comment anchors may not survive and ask.
- In `replace_content`, keep every fetched tag that carries a `url` or `src` exactly as fetched: page, database, folder, synced block, custom block, and files, including `notion-file-block://` image sources. Removing a child page tag `<page url="...">Title</page>` deletes or moves the child page. Set every column ratio when the page has columns, and leave a meeting-notes transcript untouched. Never pass `allow_deleting_content: true` without the user's confirmation, and never replace a body from a truncated fetch.
- A toggle heading is `## Title {toggle="true"}` with tab-indented children; tables and images inside a toggle are indented too.
- Escape `~` in ranges (`10/07\~10/09`), `<` and `>` in comparisons (`p99 \< 2 ms`), and `$` in prices (`\$40`). Mentions are `<mention-user url="user://<user-id>"/>`, `<mention-date start="YYYY-MM-DD"/>`, and `<mention-page url="..."/>`.
- Change the page title and database properties with `update_properties`, separately from content.

## Verification

After every structural edit, wait for any asynchronous write to finish, fetch the page, and check:

1. No plain-text person names remain outside mentions. Compare against the names in the source material and in the `notion-get-users` results you used.
2. Each toggle heading contains its children; content meant to be hidden is indented under it.
3. Every table carries `header-row="true"`, `colgroup` widths that total about 700 or less on a default-width page (a working value to confirm on the rendered page), and short cells.
4. Images and child pages are still present; compare their count with the fetch before the edit.
5. Numbers match their sources, including unit, population, and measurement conditions.
6. Decision status matches the owner's decisions everywhere it appears.
7. Terms in text, tables, and figure labels match; check the rendered labels of the images you uploaded.
8. Prose and punctuation follow the writing profile that `copydesk` applies.
9. Links open for the page's readers: no paths on the author's machine and no private scratch files.

Fix failures and fetch again. A simple text edit that changed no structure needs no extra fetch.

## Report

Report in the user's language. Lead with the page link and the action completed. State what changed (sections, tables, figures), what was verified, and anything that failed or could not be checked, such as rendered table width. Name who a new mention can notify, by role. Keep the report proportional; do not repeat the page.

## References

| File | Read it when |
| --- | --- |
| [references/notion-markdown.md](references/notion-markdown.md) | Before any create or edit: tools, exact syntax, uploads, mentions, failure modes |
| [references/document-shapes.md](references/document-shapes.md) | Choosing a genre, section order, or what a section must contain |
| [references/examples.md](references/examples.md) | Building a design doc page, an open-questions page, or correcting an existing page |
| [references/sources.md](references/sources.md) | A rule is questioned or being changed: public sources and local choices |
