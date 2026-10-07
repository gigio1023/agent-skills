# Document Shapes

Read this when choosing a genre and section order, or when checking whether a section earns its place. Section names are defaults: a team template or an established page convention wins. Sentence-level writing belongs to `copydesk`, whose document-forms reference also explains how design proposals, decision records, reports, and runbooks reason; this file covers which sections a Notion page carries and where they sit. The public sources behind each choice are in [sources](sources.md).

## Contents

- Choose the genre
- Design doc skeleton
- Section notes
- Open-questions page
- Decision record
- Page lifecycle

## Choose The Genre

| Situation | Shape |
| --- | --- |
| New module, service, or feature before implementation | Design doc (RFC) |
| Questions that block a design or its review | Open-questions page |
| One consequential choice, made or about to be made | Decision record |
| Guide, report, runbook, or explanation of an existing system | `copydesk` document forms, with this skill's Notion layout |

A design doc earns its cost when the change has dependencies, real alternatives, or effects on other teams. When implementing would take less time than writing the document, or when the document would only be an implementation manual with no trade-offs, skip it or write a one-to-three-page mini design doc focused on the decision that matters.

## Design Doc Skeleton

| Section | Purpose | Placement |
| --- | --- | --- |
| Header callout | Status, owner, reviewer role, target, date, links | Visible |
| Summary | What, how, scope by deadline, key undecided item | Visible |
| Context and scope | Background facts and the system boundary | Visible |
| Goals and Non-goals | Checkable goals; optional deliberate exclusions | Visible |
| Design | Mechanism figure, then components and behavior | Figure and overview visible; detail toggled |
| Cross-cutting concerns | Security, privacy, observability, rollout | Toggle |
| Alternatives considered | Options with advantage and rejection reason | Toggle |
| Test plan or pre-launch evaluation | How success is judged before launch | Toggle |
| Milestones | Checkpoints with exit conditions | Toggle |
| Open questions | Undecided items as questions | Visible |
| References | Evidence and related records | Toggle |

Omit a section with nothing true to say, and add one the system needs that the skeleton lacks.

## Section Notes

### Header callout

One callout at the top with one field per line: Status, Owner, Reviewer, Target, an updated date, and links. Status takes WIP, In Review, Approved, or Obsolete. Owner is a user mention. Reviewer is a role or team, such as the repository's CODEOWNERS, not a list of mentions. Target names the deliverable or rollout the design aims at. Links go to the repository and the tracker project or issue. An Obsolete page links to the page that supersedes it.

### Summary

Nested bullets with a short label on each top-level item: what is being built, how it works, the scope promised by the deadline, and the key undecided item. Nested bullets carry the reason, number, or condition behind each item. A reviewer who reads only the callout and the summary should know what is proposed and what is still open.

### Context and scope

Objective background: the current behavior, the constraint or failure that motivates the change, and the boundary of the system being designed. It is not a requirements list and not an argument for the solution. Cite the measurement or record that establishes a fact, by what it is and when it was produced.

### Goals and Non-goals

Goals state what the design must achieve, with a completion condition a reviewer can check, such as a latency or accuracy bound. Non-goals are things that could reasonably be goals and are deliberately excluded, each with its reason. "The service should not crash" is not a non-goal. Non-goals are optional: when no exclusion would surprise a reader, leave them out and name the heading "Goals".

### Design

Open with the mechanism figure that answers "how does it work". Then explain components and their responsibilities, the data flow of a representative request or job, state and storage, interfaces, and failure behavior when a dependency is unavailable. Include only the interface and schema fragments that matter for the trade-offs and link the full definitions; copied definitions go stale. Put storage layouts, interface listings, and measurement tables under toggle headings.

### Cross-cutting concerns

Cover only the concerns this design changes, each with how the design affects it and how that is addressed, so a reviewer from that area can check it quickly:

- **Security:** what is protected, where untrusted input enters, what is in scope and out of scope with reasons, the assumptions the protection depends on, and the remaining risk.
- **Privacy:** the personal data collected, where it is stored, and how long it is kept.
- **Observability:** the signals that show the system works and the alerts that show it does not.
- **Migration and rollback:** how a change to a live interface or stored data is rolled out and reversed.

### Alternatives considered

For each credible option, state its advantage first and then the reason it loses under this design's goals. Include the status quo when it is a real option. Keep abandoned ideas with their reasons instead of deleting them, so reviewers do not reopen them. Measured results of the options are comparison evidence; the chosen option is "proposed" until the owner decides.

### Test plan or pre-launch evaluation

How the team will know the design works before launch: the tests or evaluation, the data or traffic they run on, the signal that decides launch, and how a failure would be detected after launch. Name the release criterion, not just the activities. When quality is measured, as for a learned model, state the metric, any decision threshold with its reason, and the evaluation data's source and size; every number keeps its measuring conditions.

### Milestones

A short table of checkpoints with a target date mention and an exit condition each. Assign responsibility by role. Keep a schedule that changes often in the tracker and link it.

### Open questions

Each item is a question that ends with a question mark, grouped by when it must be answered: before review, during implementation, or out of scope for this design. A nested bullet says what the question blocks and what evidence or which role settles it. When a question is answered, move the answer into the body, update the status words, and remove the question.

### References

One line per item: what it is, when it was produced, and why a reviewer would open it. Do not attach author names to internal evidence such as measurements, meeting records, or drafts; published works keep their standard citation. Every link opens for the page's readers.

## Open-Questions Page

Use a separate page when the list is long, when reviewers need to work through it on its own, or when several design pages share it. Title it as the design's open questions, link back to the design with a page mention, and group the questions by when they must be answered:

- **Before review:** questions whose answer changes the design a reviewer is asked to approve.
- **During implementation:** questions that implementation or measurement will settle.
- **Out of scope for this design:** related questions deliberately left to later work, each with the reason.

Each question carries a nested bullet with what it blocks and what settles it. Do not group by person or assign questions to named people unless the user asks; a deciding role is enough.

## Decision Record

One page per consequential decision, one or two screens long:

- **Title:** a short noun phrase naming the decision.
- **Status:** Proposed, Accepted, or Superseded with a page mention of the replacement.
- **Context:** the forces at play, written neutrally.
- **Options considered:** each with its main advantage and drawback.
- **Decision:** "We chose X because Y" only when the choice was made; otherwise the proposed option.
- **Consequences:** the good and the bad, including the drawback the next maintainer would otherwise rediscover.

Do not rewrite an accepted record to fit a later decision. Mark it superseded and link the new record.

## Page Lifecycle

Update the design doc while the design changes, until it ships. When a review settles an item, change the body, header status, summary, open questions, and any affected figure together. After launch, set the status and link later amendments or decision records from the page rather than letting them pile up unlinked.
