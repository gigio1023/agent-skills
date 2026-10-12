# Document Shapes

Read this when choosing a genre and section order, placing a design doc's sections on a page, or checking whether a section earns its place. Section names are defaults: a team template or an established page convention wins. A design doc's sections and their content belong to `design-doc` when installed, and sentence-level writing belongs to `copydesk`, whose document-forms reference also explains how design proposals, delivery briefs, decision records, reports, and runbooks reason; this file covers where sections sit on a Notion page and gives the fallback design doc skeleton for when `design-doc` is absent. The public sources behind each choice are in [sources](sources.md).

## Contents

- Choose the genre
- Design doc sections on the page
- Section notes
- Delivery brief
- Open-questions page
- Decision record
- Page lifecycle

## Choose The Genre

| Situation | Shape |
| --- | --- |
| New module, service, or feature before implementation | Design doc (RFC), sections from `design-doc` when installed |
| Customer- or deadline-bound product work: outcome, promise, deadline, acceptance | Delivery brief: `copydesk` delivery brief form, with this skill's Notion layout |
| Questions that block a design or its review | Open-questions page |
| One consequential choice, made or about to be made | Decision record |
| Guide, report, runbook, or explanation of an existing system | `copydesk` document forms, with this skill's Notion layout |

A design doc earns its cost when the change has dependencies, real alternatives, or effects on other teams. When implementing would take less time than writing the document, or when the document would only be an implementation manual with no trade-offs, skip it or write a one-to-three-page mini design doc focused on the decision that matters. `design-doc` defines the mini design doc's sections; without it, use the header callout, Summary, Design with Interfaces and seams, Test plan, Open questions, and Decision log.

## Design Doc Sections On The Page

With `design-doc` installed, it decides which sections exist and what each contains, whether the page is drafted for Notion or moved there from a file. Keep its sections and their names, and place them with the table below: its Status fills the header callout, its Verification split (real-run checks, contract tests for essential contracts with their reasons, and evaluation) fills the test plan, its Threat model or Operating boundary fills the security section under Cross-cutting concerns, its Experiment queue sits in a toggle after Open questions, and its other sections map by name. A section that `design-doc` omits stays omitted on the page.

Without `design-doc`, the table is the fallback skeleton. It keeps the essentials of a reviewable design: the fixed interfaces and their seams, a test plan written as a verification split, the open questions, and a decision log, with an operating boundary in place of the threat model when the system is itself the attacker.

| Section | Purpose | Placement |
| --- | --- | --- |
| Header callout | Status, owner, reviewer role, target, date, links | Visible |
| Summary | What, how, scope by deadline, key undecided item | Visible |
| Context and scope | Background facts and the system boundary | Visible |
| Goals and Non-goals | Checkable goals; optional deliberate exclusions | Visible |
| Design | Mechanism figure, then components and behavior | Figure and overview visible; detail toggled |
| Interfaces and seams | Fixed interfaces and the adapters behind each | Toggle |
| Cross-cutting concerns | Threat model, or operating boundary for a system that attacks; privacy, observability, rollout | Toggle |
| Test plan | Verification split: real run, contract test, or evaluation per component; launch criterion | Toggle |
| Alternatives considered | Options with advantage and rejection reason | Toggle |
| Milestones | Checkpoints with exit conditions | Toggle |
| Open questions | Undecided items as questions | Visible |
| Experiment queue | Unmeasured bets, from `design-doc` only | Toggle |
| Decision log | Decisions with evidence and reversal conditions | Toggle |
| References | Evidence and related records | Toggle |

Omit a section with nothing true to say, except Interfaces and seams, Test plan, Open questions, and Decision log, which stay even when short. Add a section the system needs that the skeleton lacks.

## Section Notes

With `design-doc` installed, its rules govern what each section contains; use these notes only for page details such as the header callout fields, date mentions, and references that open for the page's readers. Without it, these notes are the content rules for the fallback skeleton.

### Header callout

One callout at the top with one field per line: Status, Owner, Reviewer, Target, an updated date, and links. Status takes WIP, In Review, Approved, or Obsolete. Owner is a user mention. Reviewer is a role or team, such as the repository's CODEOWNERS, not a list of mentions. Target names the deliverable or rollout the design aims at. Links go to the repository and the tracker project or issue. An Obsolete page links to the page that supersedes it.

### Summary

Nested bullets with a short label on each top-level item: what is being built, how it works, the scope promised by the deadline, and the key undecided item. Nested bullets carry the reason, number, or condition behind each item. A reviewer who reads only the callout and the summary should know what is proposed and what is still open.

### Context and scope

Objective background: the current behavior, the constraint or failure that motivates the change, and the boundary of the system being designed. It is not a requirements list and not an argument for the solution. Cite the measurement or record that establishes a fact, by what it is and when it was produced.

### Goals and Non-goals

Goals state what the design must achieve, with a completion condition a reviewer can check, such as a latency or accuracy bound. Non-goals are things that could reasonably be goals and are deliberately excluded, each with its reason. "The service should not crash" is not a non-goal. Non-goals are optional: when no exclusion would surprise a reader, leave them out and name the heading "Goals".

### Design

Open with the mechanism figure that answers "how does it work". Then explain components and their responsibilities, the data flow of a representative request or job, state and storage, and failure behavior when a dependency is unavailable. Include only the schema fragments that matter for the trade-offs and link the full definitions; copied definitions go stale. Put storage layouts and measurement tables under toggle headings.

### Interfaces and seams

State which interfaces are fixed and which implementations are swappable adapters behind them. Put a seam where something actually varies; a component with one implementation is plain code. A learned or judging component sits behind a fixed interface, usually with a baseline, the incumbent, or a fake for tests as its second adapter. The interface includes the output's meaning and its failure behavior, because callers depend on both. Include only the signature fragments that matter for the trade-offs and link the full definitions.

### Cross-cutting concerns

Cover only the concerns this design changes, each with how the design affects it and how that is addressed, so a reviewer from that area can check it quickly:

- **Security:** what is protected, where untrusted input enters, what is in scope and out of scope with reasons, the assumptions the protection depends on, and the remaining risk.
- **Operating boundary:** for a system that is itself the attacker, such as a red-teaming agent, an automated security-testing harness, or a fuzzing service, this takes the threat model's place. State the authorized targets and the authorization each rests on, budgets per target and what happens when one runs out, containment and how a run is stopped, a never-do list, how run evidence is stored and redacted, and the role that approves widening any limit. Name the code outside the model that enforces each limit. Write it in methodology language: objective categories, environments, and limits, never attack procedures or concrete inputs.
- **Privacy:** the personal data collected, where it is stored, and how long it is kept.
- **Observability:** the signals that show the system works and the alerts that show it does not.
- **Migration and rollback:** how a change to a live interface or stored data is rolled out and reversed.

### Alternatives considered

For each credible option, state its advantage first and then the reason it loses under this design's goals. Include the status quo when it is a real option. Keep abandoned ideas with their reasons instead of deleting them, so reviewers do not reopen them. Measured results of the options are comparison evidence; the chosen option is "proposed" until the owner decides.

### Test plan

Write the test plan as a verification split. Put each component on one side, name what verifies it, and say where that lives. A deterministic part, where a rule decides whether an output is correct, is verified by a real run of its entry point on fixed input that leaves the input, the command, and the output for someone else to rerun. A contract test is kept for an essential contract, one whose break a real run would miss and that would be costly or felt outside the module, such as the interface every adapter at a seam must honor; mark each essential contract with its reason, and record any further tests the project's documented policy or CI requires, with that source. A judging or learned part, where correctness is a judgment over a distribution, is verified by evaluation, and a property that only shows under real traffic, such as latency at peak, is measured. A short table holds the component, its side, what verifies it, where that lives, and its status. Then name the launch criterion, not just the activities, and how a failure would be detected after launch. When quality is measured, as for a learned model, state the metric, any decision threshold with its reason, and the evaluation data's source and size; every number keeps its measuring conditions.

### Milestones

A short table of checkpoints with a target date mention and an exit condition each. Assign responsibility by role. Keep a schedule that changes often in the tracker and link it.

### Open questions

Each item is a question that ends with a question mark, grouped by when it must be answered: before review, during implementation, or out of scope for this design. A nested bullet says what the question blocks and what evidence or which role settles it. When a question is answered, move the answer into the body, update the status words, and remove the question.

### Decision log

One entry per decision: its status (Proposed, Accepted, or Superseded by a later entry), the kind of evidence it rests on (literature, measurement, constraint, or a hunch labeled as one), where that evidence lives, and the observable condition that would reverse it. An option the owner has not accepted stays Proposed here and in the header status. Supersede an accepted entry with a new one instead of rewriting it.

### References

One line per item: what it is, when it was produced, and why a reviewer would open it. Do not attach author names to internal evidence such as measurements, meeting records, or drafts; published works keep their standard citation. Every link opens for the page's readers.

## Delivery Brief

A delivery brief tells the people who deliver, accept, and decide what is promised by a deadline and how acceptance will be judged. Its sections and their content come from `copydesk`'s delivery brief form. Without `copydesk`, use the outcome and whose decision it serves, the relevant workflow, the promised behavior and explicit exclusions, priorities and the deadline, the acceptance evidence and who accepts, open decisions, and links to the design doc and the plan. It is not a product requirements spec or a set of user stories, and it never replaces the design doc.

On a Notion page:

- **Header callout:** Status, Owner as a user mention, the accepting role, the deadline as a date mention, and links to the design doc and the plan, as page mentions when they live in Notion.
- **Visible:** the outcome and the decision it serves, a short statement of the workflow, the promised behavior with its exclusions, priorities, acceptance, and open decisions. A reader who opens no toggle knows what is promised, by when, and how it will be accepted.
- **Under toggles:** workflow detail, supporting measurements, and references.
- **Length:** one or two screens. Design detail stays in the design doc and tasks stay in the plan or tracker; the brief links to them instead of restating them.

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

Update the design doc while the design changes, until it ships. When a review settles an item, change the body, header status, summary, open questions, decision log, and any affected figure together. After launch, set the status and link later amendments or decision records from the page rather than letting them pile up unlinked.
