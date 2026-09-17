# Linear

Read this when the tracker is Linear. It covers which container fits the work, where narrative goes, sub-issue behavior that surprises people, templates and triage, and how to express fields through the Linear MCP server or API. The core rules in `SKILL.md`, including the assignee rule and the reader-access rule, still apply and are not repeated here.

Product behavior below was checked against Linear's documentation on 2026-09-17. Recheck the linked page before relying on a detail that matters.

## Contents

- Choose the container
- Where narrative goes
- Sub-issue behavior
- Relations
- Templates and triage
- Express fields through the MCP server or API

## Choose The Container

| Container | Use it when | Notes |
| --- | --- | --- |
| Issue | One task with a clear outcome | Needs only a team, a title, and a status. The description is optional. |
| Parent with sub-issues | The work is "too large to be a single issue but too small to be a project", or it is shared across teammates | The parent stands for the final outcome. |
| Project | The work has a clear outcome or planned completion date and spans several issues, often several people or teams | Linear's own rule of thumb is several people for more than two weeks. An issue belongs to one project at a time. |
| Milestone | A stage inside one project | Milestones exist per project and cannot be shared across projects. |

When a parent keeps growing, Linear's remedy is to turn it into a project, not to nest deeper.

For exploratory work Linear offers two forms: a placeholder issue to break down later, or an issue framed as a deliverable such as "Write project spec". The deliverable form is one of the two the core rule allows for uncertain work; the placeholder form is not, because it names no outcome.

## Where Narrative Goes

The issue description stays a short task statement. Longer material has its own home:

- **Project updates** carry progress: a health indicator plus text on status, challenges, and next steps. The project lead writes them, commonly weekly. Put progress narrative here or in a comment, not in issue bodies.
- **Documents** carry long-form text such as specs, runbooks, and meeting notes. Link the document from the issue.
- **Comments** carry discussion and follow-up on one issue.

## Sub-Issue Behavior

- A new sub-issue inherits the parent's team, priority, and project. Labels are not inherited, so add the labels the team filters by.
- The assignee can be inherited: when the author is assigned to the parent, or when all existing sub-issues share the parent's assignee. Inheritance can therefore assign someone nobody chose. Set or clear the assignee explicitly on every sub-issue according to the core assignee rule, and confirm it when reading the result back.
- A sub-issue created in an active status may join the current cycle. Create it in the team's backlog or not-started status, as the core splitting rule says, move only the one the user names as active, and check the cycle afterwards.
- A sub-issue may live in a different team from its parent.
- Parent auto-close (the parent completes when all sub-issues are done) and sub-issue auto-close (remaining sub-issues complete when the parent is done) are opt-in team workflow settings. Do not assume either. Before closing a parent, look at its open sub-issues, because with sub-issue auto-close enabled they will be closed too. Do not change these settings as part of issue writing.

## Relations

Use blocked by, blocks, related, and duplicate instead of prose. A blocker shows as a flag on the blocked issue, and the relation moves under Related once the blocker is resolved. The documentation does not say that a blocked issue is prevented from changing status, so treat the relation as a signal to readers, not an enforced lock.

## Templates And Triage

- A team can set a default issue template, and templates exist at workspace and team level. Read the template that applies before drafting, keep its headings, and remove placeholders you do not fill.
- Issues created by an integration, or by someone who is not a member of the destination team, land in that team's Triage inbox. The team then accepts, declines, marks as duplicate, or snoozes. When filing into another team, leave the assignee empty and leave priority, cycle, and status for their triage to set.

## Express Fields Through The MCP Server Or API

Parameter names below are from the Linear MCP server's issue save tool as of 2026-09. The tool's namespace differs by harness, and names can change, so confirm against the live tool schema before writing.

| Intent | How |
| --- | --- |
| Assign the author (the default) | `assignee: "me"` |
| Leave the assignee empty on create | Omit `assignee` |
| Keep the current assignee on edit | Omit `assignee`. Passing `null` removes it. |
| Make a sub-issue | `parentId` |
| Relations | `blockedBy`, `blocks`, `relatedTo`, `duplicateOf`. The list forms are append-only, with matching `remove...` parameters. |
| Edit labels without losing others | `addLabels` and `removeLabels`. `labels` replaces the whole set. |
| Edit part of a body | `patch`. `description` replaces the whole body. |
| Use a team template | `template` applies on create only, and a non-empty `description` replaces the template body. To keep the template's structure, fill it in and pass that as the description. |
| No estimate | Omit `estimate` |

Through the GraphQL API there is no `me` shorthand on issue creation: resolve the authenticated user with the `viewer` query and pass its id as `assigneeId`. Confirm field names in the current API schema.

Read neighboring issues, the project, and the template with the server's read tools before writing, and read the saved issue back afterwards to confirm the assignee, labels, cycle, and relations are what was intended.
