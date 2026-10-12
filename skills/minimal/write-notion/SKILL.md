---
name: write-notion
description: >
  Use when the user asks to create, draft, restructure, or revise a team document as a Notion page through the Notion MCP tools: a design doc or RFC, a delivery brief, an open-questions page, a decision record, or any team page whose layout, tables, mentions, or figures need work: "write the design doc in Notion", "put this RFC on our Notion", "Notion에 설계 문서 써줘", "노션 페이지 고쳐줘", "fix the tables on this Notion page". design-doc supplies a design doc's sections, copydesk owns the prose, and technical-figure, when installed, draws the figures. NOT for quick chat answers, Notion database administration, saving chat or meeting content as notes, meeting pre-reads, research synthesis across pages, turning a spec into tasks, or documents published outside Notion (copydesk, design-doc).
---

# Write Notion

Publish a team document in Notion that a colleague can review from the page alone. The design or decision is at the top of the page, details are one click away, people are referenced without leaking names or flooding notifications, and the stored page matches what was intended.

This is a publication workflow skill, in the way `write-issue` is for trackers. It owns the genre choice, the Notion page layout and its toggles, people references, tables, figures, the Notion Markdown editing mechanics, publication, and post-publish verification. A design doc's sections and their content rules belong to `design-doc` when installed, whatever the destination. It is not a style skill: `copydesk` owns sentence-level writing (meaning preservation, claim strength, voice, and the author's writing profile) and applies to every paragraph, bullet, caption, and table cell. This skill decides which figures the page needs and uploads them. Tracker issues and pull requests stay with `write-issue` and `draft-pr`; the page links to them.

Prerequisites: `copydesk` from this pack supplies the base writing rules through its writing profile, and each section below that builds on the profile states the essential base rule before its Notion-specific part, so the skill still works when `copydesk` is absent. `design-doc` from this pack supplies a design doc's sections; without it, the fallback order in [Shape Before Writing](#shape-before-writing) keeps the essential sections. Figures come from `technical-figure` (gigio-figures repository) when installed, or the project's figure tool; otherwise the page gets no figure or a simple text diagram.

Not for: an answer that belongs in chat, database schema, view, or property administration, saving chat or meeting content as notes, meeting pre-reads and agendas, research synthesis across existing pages, turning a spec into tasks, or a document delivered as a file or on another platform.

The user's instruction and a team template or existing page convention win over the layout defaults below. The people and mention rules and [verification](#verification) checks 1 to 7 and 10 apply whatever the convention. Checks 8 and 9 carry the writing profile, so they apply only when that profile governs and the page has no differing convention.

## Normal Path

1. Read before writing. Fetch the target page or the destination parent, a few sibling pages, and any template the team uses, and match their language and conventions. Check who can read the destination (a teamspace, the whole workspace, or a page published to the web); keep secrets, credentials, personal data, and customer-confidential text out, and apply `copydesk`'s sharing-and-delivery reference for a wider audience. Read the source material the page will rest on: code, measurements, meeting records, tracker items. Read the Notion enhanced Markdown specification once per session when the client exposes it. [Notion Markdown mechanics](references/notion-markdown.md) covers the tools, exact syntax, and failure modes.
2. Choose the shape before drafting: the genre, the section order, and what stays visible versus what goes under toggles. [Document shapes](references/document-shapes.md) gives the placement of `design-doc` sections, the fallback design doc skeleton, the delivery brief layout, the open-questions page, and the decision record.
3. Draft the content. A design doc takes its sections and their content from `design-doc` when installed; the prose comes from `copydesk` when installed, otherwise from the base rules stated in the sections below. Resolve the few people mentions the page needs, and render and upload its figures.
4. Decide whether to show the draft first. Show the complete draft and wait when the user asked for a draft, the page belongs to someone else and editing it was not authorized, the destination is a guess, the edit would delete child pages or databases, or a mention could notify someone other than the owner the user named. Otherwise the request is the grant; add no second confirmation. With no destination named for a new page, create a private draft page and say that it is private.
5. Write with `notion-create-pages` for a new page or `notion-update-page` for an existing one, using the smallest edit that does the job.
6. Verify the stored page with the checks in [Verification](#verification) and fix what fails.
7. Report as described in [Report](#report).

Without a working Notion connection, deliver the page as Notion Markdown and say that nothing was published. Do not install or authenticate a connector implicitly.

## Shape Before Writing

Decide the genre first, because it decides the sections. A new module, service, or feature uses a design doc (also called an RFC). Customer- or deadline-bound product work that needs its outcome, promise, deadline, and acceptance on one page uses a delivery brief, which takes its sections from `copydesk`'s delivery brief form and its layout from this skill; it links to the design doc and the plan and never replaces the design doc. One consequential choice uses a short decision record. A question list, when the user asks for one or it outgrows the design doc's Open questions section, is its own short page grouped by when each question must be answered: before review, during implementation, or out of scope. Group by person only when asked. A guide, report, or runbook takes its structure from `copydesk`'s document forms; this skill still handles its Notion layout.

A design doc's sections and their content rules come from `design-doc` when installed, whether the page is drafted for Notion or moved there from elsewhere: interfaces and seams, the threat model or operating boundary, the verification split, open questions, the experiment queue, and the decision log. This skill decides where each of those sections sits on the page, which stay visible and which go under toggles, and who is mentioned, then publishes the page and reads it back. Do not replace `design-doc`'s sections with the order below.

When `design-doc` is not installed, use this fallback order. It keeps the essentials a reviewer needs: the fixed interfaces and their seams, how each part is verified, the open questions, and a decision log.

1. Header callout: Status (WIP, In Review, Approved, Obsolete), Owner as a user mention, Reviewer as a role, Target, a date mention, and repository and tracker links.
2. Summary, then Context and scope, then Goals and Non-goals. Non-goals are optional; when they are omitted, the heading is "Goals".
3. Design, with the mechanism figure first and details after it, then Interfaces and seams: the fixed interfaces and the swappable adapters behind each.
4. Cross-cutting concerns the design changes, such as security, privacy, observability, or migration and rollback. For a system that is itself the attacker, such as a red-teaming agent or a fuzzing service, the security concern is an operating boundary: authorized targets, budgets, containment, and a never-do list.
5. Test plan, written as a verification split: each component, whether a real run on fixed input, a contract test for an essential contract with its reason, or evaluation verifies it, where that lives, and the launch criterion.
6. Alternatives considered, each with its rejection reason, then Milestones.
7. Open questions, then Decision log, then References.

Drop a section that has nothing true to say instead of filling it with a placeholder, except Interfaces and seams, Test plan, Open questions, and Decision log, which stay even when short. Section purposes, size guidance, the placement of `design-doc` sections, and the shapes of the other genres are in [document shapes](references/document-shapes.md).

## Page Layout

- **Summary** is nested bullets: what is being built, how it works, the scope promised by the deadline, and the key undecided item. A top-level bullet carries a short label and the claim; nested bullets carry its reason or condition.
- **Visible:** summary, context, goals, figures, and open questions. A reader who never opens a toggle still learns what is proposed, why, and what is undecided.
- **Under toggle headings:** measurement tables, storage, interfaces and seams, cross-cutting concerns including a threat model or operating boundary, the test plan or verification split, alternatives, schedule, the experiment queue, the decision log, and references. Toggles are the default for detail on a design doc page, but the decision summary and the open questions are never toggled.
- **Undecided items:** gather undecided decisions as questions in one open-questions section instead of scattering disclaimers through the body. On a Notion page, the Open questions section is a visible heading near the end, each question says what it blocks, and a passage that depends on an open item points to that question once.

## Voice

- **Korean pages** default to short 합니다체 bullets in the voice the author uses with teammates, not noun-ending fragments. Write dates in prose as M/D within the year, such as 11/3, and use a date mention for a date that readers act on. A team page's existing convention wins.
- **Parentheses and identifiers:** when the writing profile governs and the page has no differing convention, avoid parenthetical asides in prose, headings, table cells, and figure labels, while code, identifiers, citations, and official names keep their own parentheses, and link every tracker identifier wherever it appears. On a Notion page, the parentheses rule covers the labels inside uploaded figures too, so a label change means re-rendering and re-uploading the figure in the same edit, and the linking rule covers the header callout and toggle headings.

## Status Words

A candidate stays a candidate and a proposal stays a proposal, and measured results of options are comparison evidence until the owner selects one. On a Notion page, status appears in the header callout's Status field, headings, body, table cells, and figure labels, and all of them must agree. Put "comparison evidence" in the heading of an option measurement table. Set Approved only when the reviewer role approved. When the owner decides, say where the decision was made, such as the design review on a date mention, and update every place the status appears, including re-rendering an affected figure, in the same edit.

## People

Refer to roles, teams, or sources instead of naming people. On a Notion page:

- Identify a person who must be named, such as the owner or the directly responsible person, with a user mention found through `notion-get-users`, never `@Name` or a plain-text name.
- Mentions can notify, and names travel with exports and search. Mention as few people as possible, usually only the owner. Never list many mentions; a review audience is a role or a team, such as the repository's CODEOWNERS.
- Refer to someone outside the workspace by role or organization; they cannot be mentioned.
- Name an evidence link by what it is and when it was produced, such as "internal measurement on 2026-09-30". Do not attach author names to internal evidence such as measurements, meeting records, or drafts; published works keep their standard citation.
- On another author's page, keep their existing mentions unless asked to change them, and apply these rules to the passages you write or edit.

## Terms

Prefer established field terms over coined local translations, and use one term per concept. On a Notion page, that term holds across text, tables, and figure labels. When a term changes, re-render and re-upload the affected figures in the same edit, because an uploaded image does not change with the text.

## Tables

Keep table cells to a value, identifier, or short phrase, size columns to their content, and put reasoning beside the table. On a Notion page:

- Always set `<table header-row="true">`. Table attributes default to false, so without it the first row is ordinary data.
- Put what a cell cannot hold in bullets directly under the table; a cell never holds a sentence.
- Set column widths with `<colgroup>` and `<col width="N">`, sized to content: about 70 for a short status or yes/no column, 150 to 220 for names, and 240 to 300 for short descriptions. Keep the total to about 700 on a default-width page, less inside toggles and callouts, and wider on a full-width page. These are working values; confirm them on the rendered page. When the total overflows, move a column's content into the bullets under the table.
- Leave `fit-page-width` unset; the column widths size the table.
- Use a table to compare several items on shared attributes. One item, or content that needs sentences, belongs in bullets.

## Figures

- Make one figure per question the reader has, such as how the mechanism works or when requests arrive. The mechanism figure opens the Design section.
- Draw with `technical-figure` when installed or the project's figure tool, and deliver a light-theme PNG. Without either, leave the figure out or use a simple text diagram.
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
- Escape `~` in ranges (`11/02\~11/04`), `<` and `>` in comparisons (`p99 \< 2 ms`), and `$` in prices (`\$40`). Mentions are `<mention-user url="user://<user-id>"/>`, `<mention-date start="YYYY-MM-DD"/>`, and `<mention-page url="..."/>`.
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
8. When the writing profile governs and the page has no differing convention, prose and punctuation follow the profile that `copydesk` applies.
9. Under the same condition, no parenthetical asides remain outside code, identifiers, citations, and official names, including the labels of uploaded figures, and every tracker identifier is a link where it appears.
10. Links open for the page's readers: no paths on the author's machine and no private scratch files.

Fix failures and fetch again. A simple text edit that changed no structure needs no extra fetch.

## Report

Report in the user's language. Lead with the page link and the action completed. State what changed (sections, tables, figures), what was verified, and anything that failed or could not be checked, such as rendered table width. Name who a new mention can notify, by role. Keep the report proportional; do not repeat the page.

## References

| File | Read it when |
| --- | --- |
| [references/notion-markdown.md](references/notion-markdown.md) | Before any create or edit: tools, exact syntax, uploads, mentions, failure modes |
| [references/document-shapes.md](references/document-shapes.md) | Choosing a genre, placing `design-doc` sections, using the fallback section order, or laying out a delivery brief |
| [references/examples.md](references/examples.md) | Building a design doc page, an open-questions page, or correcting an existing page |
| [references/sources.md](references/sources.md) | A rule is questioned or being changed: public sources and local choices |
