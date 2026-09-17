---
name: write-issue
description: >
  Use when the user asks to write, file, edit, split, or close out an issue or
  ticket in a tracker such as Linear, GitHub Issues, Forgejo, Gitea, or Jira,
  including "이슈 만들어줘", "Linear 티켓 써줘", "이 이슈 sub-issue로 나눠줘",
  "file a bug for this", "open an issue", and "turn this into a ticket". Reads
  the team's existing issues first, writes one task with a clear outcome in a
  short body that states its own findings and keeps only links every reader can
  open, assigns the author by default and leaves the assignee empty when
  ownership is ambiguous, and shows a draft before touching other people's
  issues. NOT for pull requests (use draft-pr), PR review comments (use
  pr-review-comment), or long specs and reports (use technical-report-writing).
---

# Write Issue

Write issues a teammate can scan in a list and act on: one task with a clear outcome, a short body that states what it means, and only the links a reader needs and can open. An issue is a shared record that notifies people and outlives the session that wrote it, so match what the team already does and keep ownership, visibility, and sources deliberate.

The rules for shape (title, body, what to leave out, language) are defaults: the user's instruction and the team's own template or convention win over them. The link check and shared-record safety run on every issue whatever the convention, and the assignee follows its rule unless the user says who.

## Normal Path

1. Read before writing. Fetch the issue being edited, the conventions of its project or milestone including any issue template, and two or three neighboring issues. Stop once you can say what language, length, and structure the team uses, then match that instead of imposing a shape.
2. Draft the title, body, and fields with the rules below.
3. Run the check in [State The Claim, Justify Every Link](#state-the-claim-justify-every-link) on every link, path, and attachment in the draft.
4. Decide whether to show it first. Show the complete draft with its intended field values and wait when the user asked for a draft or it is unclear whether they want a draft or a posted issue, when the change touches an issue someone else created or owns, when you had to guess the destination team or repository, when the destination is more visible than the user may expect, or when the check dropped a link or file the user asked to include. Otherwise the request to create or edit is the grant: follow the harness's approval rules and add no second confirmation.
5. Write through the tracker's tool. On create, set only the fields the request or the team's convention calls for and leave the rest at the tracker's defaults. On edit, change only the requested fields. Read the result back and report.

Without a working tracker tool or authentication, deliver the draft and its field values as text, and say that the issue was not created and that the team's conventions could not be read. Do not install or authenticate a tool implicitly.

## What An Issue Holds

An issue is one task with a clear outcome: a change, a document, a decision, an action. When the request is not a task, such as an open discussion or a running log, say so and offer the home that fits.

- **Title:** the target and the action ("Retry payment webhooks on 5xx responses"), the deliverable ("Reranker comparison table for long queries"), or, for a bug reported to someone else, the symptom ("CSV export drops the last row at exactly 1000 rows"), since the fix is theirs to choose. It is read in a list beside other titles.
- **Body:** at most one sentence of purpose when the title does not carry it, then an overview table or figure only when [Tables, Figures, And Collapsed Detail](#tables-figures-and-collapsed-detail) calls for one, then three to five concrete tasks or facts, then only the links that pass the check below. Fewer is fine, and the description may be empty when the title is enough. When the user has not supplied a particular, do not invent it: write the issue without it and name the gap in the report.
- **Fields:** relations, labels, milestone, and parent carry structure. Do not restate them in prose.

Leave these out unless the user asks or the team's template requires them, because each has a better home: acceptance criteria or definition-of-done sections (checks belong where the work is reviewed, such as a pull request checklist or a plan on a shared branch, so link that), as-is and to-be framing, background already stated in the parent or project, defensive disclaimers, and status narration. Saying what has not been checked yet is a fact the reader can act on, not a disclaimer.

By kind:

- **Bug or request:** quote the reporter's words and link the conversation rather than paraphrasing, attributing by role unless readers need the name to act. Cut anything confidential from the quote and mark the cut. Add what the reader needs to reproduce it: where, observed, expected.
- **Wrong output in data or an evaluation:** show one real input with its observed and expected output in a small table, and link the dataset revision.
- **Uncertain or research work:** name the issue as the question, or as the deliverable that answers it (a comparison table, a decision memo, a case set). No estimates and no invented sub-tasks. The full results and the reasoning stay in the experiment log, document, dashboard, or pull request. The issue states the headline finding in two or three lines, at the latest when it is closed, and links that record when readers can open it. Progress narrative goes to a project or status update or a comment, not the body.

## Tables, Figures, And Collapsed Detail

Concise comes first. Most issues need none of these, because a title and a few lines already scan. Add a table or a figure only when the reader takes in the content faster with it than with the sentences it replaces. None of them may hide the point: the finding, the tasks, and the decision stay in visible text.

- **Overview table, right after the purpose sentence.** Use it when the content is the same few fields repeated over several items, such as sub-issues with their state, candidates with their metrics, or components with their impact, so the reader sees the whole set before the details. Give every column a header and let the first column name each row. Keep a cell to a few words, a number, or a link. A cell that needs a sentence means the material is not tabular, so write it as a bullet instead. A table for a single item, or one that repeats the bullets under it, is decoration.
- **Figure, when structure is the point.** A flow, an architecture, a dependency between parts, or a before and after that would take a paragraph reads faster as a small diagram. Make it with the `technical-diagram` skill when that skill is available, giving it the reader's question and the issue text as the surrounding context. Otherwise use a diagram format the tracker renders natively, or leave the figure out. Skip it when a sentence or the table already carries the structure, or when making it would cost more than it saves the reader. Put the rendered image into the issue through the tracker's upload or attach function, in a format the tracker displays inline, and say in one visible line what it shows. A path to the file is not a figure. When the available tool cannot upload, give the file to the user and report that it is not attached.
- **Collapsed section, as a last resort.** A shorter issue beats a folded one. First cut the detail, or put it where it belongs, such as a comment, the pull request, or a shared document, and state its conclusion in the body. Collapse only when a long block has to sit in the issue itself and most readers will skip it, for example a log that whoever takes the fix must read and that has no shared home. Then the summary line says what the block holds and what it concludes, and the body reads complete with it closed. Never collapse the finding, the task list, the decision, or anything a reader must see to act. Use the tracker's own collapsible form.

## State The Claim, Justify Every Link

An issue is a shared internal document. Its readers have the tracker, not the author's machine, server, or session.

- **The text stands on its own.** A teammate who was not in the session can tell from the issue alone what the matter is, what was found or decided, and what is to be done. Give the one piece of background they lack, and do not assume they saw the chat, the run, or an earlier draft.
- **No defensive writing.** Do not pad the issue with hedges, caveats that protect the author, reminders of how carefully the work was done, or lists of everything that was not checked. State what is known. Name an unknown once, next to the claim it limits, when the reader would act differently for knowing it.
- **The author owns the claim.** State the finding, number, decision, or task in the issue's own text. A link lets the reader verify it or go deeper; it never stands in for the statement. "See <path>" or "details in <link>" without saying what is there pushes the work of finding out onto the reader and lets the author avoid committing to a statement.
- **Every link and attachment earns its place.** Keep one only when the reader needs it to act on the issue or to check a specific claim made in it, and say what it is and why one would open it. Drop links and files that are merely related, that duplicate another link, or that were added to look thorough.
- **Every link opens for the issue's readers.** Usable: a repository URL or a repository-qualified path on a shared branch, a shared document, a tracker item, a chat permalink, a dataset or dashboard URL. Not usable: a path on the author's machine, a path on a server or GPU node given as if it were a link, localhost or a private IP address without stated access conditions, an unpushed branch or local-only commit, a scratch or session file, a plan or notes file that was never shared, a private document the readers cannot access, an expired signed URL, a dead link.
- **When the material lives only on the author's machine or on a server the readers cannot reach,** put the facts the reader needs into the issue and state plainly that no shared copy exists yet. Move it somewhere shared first only when the user asked for that. A server the readers can reach is a usable location only when the issue names the host and the access condition; a bare path never is. When access is restricted, such as VPN only or a private channel, or the link will stop working, such as a live process, state that next to the link.
- **Name the repository** when citing a repository-relative path, for example `payments-api: docs/webhook-retries.md` on `main`, and prefer a commit-pinned URL where the forge offers one. Readers do not know which checkout the author had open.
- **Remove incidental authoring context:** session history, which agent or tool did what, local tool state. Keep particulars the reader needs to interpret or reproduce a result, such as a model version, dataset revision, or commit.

Check before posting. For each link, path, or attachment in the draft:

1. Name the claim or action it supports. That claim or action has to come from the work itself, not be written to justify the link. If there is none, delete the link.
2. Confirm it resolves for the readers: a repository file exists on a shared branch of a named repository (an untracked, ignored, or unpushed file is local-only, however tidy its path looks), a pull request or issue reference exists, a document sits in a shared space. When you cannot verify access, say so to the user, in the draft you show or in the report, instead of posting the link silently.
3. Confirm the sentence around it still makes sense with the link removed.

Links the user hands you are candidates, not an instruction to include each one. Run the same check. When it drops a link or file the user asked to include, show the draft with the reason before posting. Restore what the user then asks for, with any access limit stated beside it so the issue stays honest about what readers can open.

When editing an existing issue, run the same check on the body you are changing: remove references that are unreachable or useless, and tell the user what was removed. In someone else's issue, those removals are part of the draft you show first.

These are the reader-access principles of `share-internal-doc` from Gigio Pack. Use that skill when available for sensitive material, criticism of named people, or an audience wider than the team.

## Splitting And Relations

Use a parent with sub-issues for work too large for one issue and too small for a project. Split only after the separate lumps have shown up in the work, because imagined tasks make poor sub-issues. The parent stands for the final outcome: leave its title, body, and fields as they are, and do not add a sub-issue that merely restates it, meaning one that names the parent's outcome again without a separate piece of work of its own. Express blocked-by, related, and duplicate as relations, not prose.

Keep each person's in-progress issues few, reading the count from the tracker when the user does not give it. Create sub-issues as not started where the tracker has a status, and ask which one is being worked on now instead of marking several in progress. When a request would push the in-progress count up, say so before changing any status and let the user decide.

## Assignee

The author is the person you are acting for. Assign the author by default, using the tracker's self-assign form (`me`, `@me`) where it exists.

Leave the assignee empty when ownership is ambiguous: the work belongs to another team or person, the issue is a request or report for someone else to triage, several people are plausible owners, or the user has not said who will do it and nothing shows it is their own work. Assign another named person only when the user asked for exactly that, and follow an explicit instruction to leave it empty. When editing, keep the current assignee. Report what was assigned and why in one line.

## Shared-Record Safety

Creating or editing an issue notifies people and may sync to chat, email, and search, where a later edit does not recall it. Keep secrets, credentials, personal data, and customer-confidential text out, and link the access-controlled source instead. Check the sharing boundary before writing: a public repository and a private workspace are different audiences.

When editing, preserve status, assignee, labels, attachments, and relations unless asked to change them. Send only the fields being changed, prefer a partial body edit over replacing the whole body, and watch for fields that replace a whole set. Do not close, reassign, re-prioritize, or re-label other people's issues as a side effect.

## Language And Style

Write in the language the team's tracker already uses, titles included. Spell terms out: an abbreviation or label coined during the session means nothing to a reader outside it. Keep the field's established English technical terms in English inside non-English text, following the team's own spelling for settled loanwords. Write dates in full, with the year.

For Korean trackers, default to a noun-phrase outline (개괄식) for bodies, closing notes, and status updates: bullet items that end in a noun or read `label: value`, not past-tense narrative sentences such as "~했다". This preference covers tracker records only, and an established team convention wins.

## Tracker Specifics

Read the matching file when the tracker is:

| Tracker | File | What it resolves |
| --- | --- | --- |
| Linear | [references/linear.md](references/linear.md) | Issue versus sub-issue, project, and milestone; where narrative goes; sub-issue inheritance and auto-close; templates and triage; tables, diagrams, collapsible sections, and file upload; field names |
| GitHub Issues | [references/github-issues.md](references/github-issues.md) | Visibility, templates, task lists versus sub-issues, relations, collapsed sections, diagrams, image attachment, `gh` flags |
| Forgejo, Gitea, Jira, others | None | Apply the rules above, and discover fields, templates, and the self-assign form from the tracker's own tool help |

[references/examples.md](references/examples.md) has worked drafts for each kind, including a Korean outline, a draft with an overview table and a figure where a long log was cut instead of collapsed, and a draft whose sources were local paths, a server path, and a pile of loosely related links; read it when the right shape is unclear. [references/sources.md](references/sources.md) records the public sources behind the non-obvious rules and how strong they are; read it when a rule is questioned or being changed.

## Report

Report in the language the user is using. Lead with the issue URL or identifier and what was done: created, edited, split, closed, or drafted only. Then give the one-line assignee decision, the fields set or changed and, on an edit, the fields deliberately left alone, every link or reference removed and why, material that has no shared copy yet, any kept link whose access you could not verify, particulars the user still has to supply, and anything the user must decide, such as a rising in-progress count.
