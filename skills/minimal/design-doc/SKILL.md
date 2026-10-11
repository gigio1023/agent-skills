---
name: design-doc
description: >
  Write or update a design document for a module or system, shaped for
  components whose core behavior comes from a trained model, a judge, or an
  agent loop. Converges a chosen concept into a design with fixed interfaces
  and swappable adapters, a split between test-verified and
  evaluation-verified parts, a threat model when adversarial, open questions,
  an experiment queue of unmeasured bets, and a decision log with evidence and
  reversal conditions. Use for "write a design
  doc", "RFC for this module", "turn this concept into a design", "update the
  design with these results", "close the open questions in the design", or
  "설계 문서 써줘". For a design doc in Notion, this skill supplies the content
  and write-notion publishes it. NOT for Notion page mechanics alone
  (write-notion), opening the design space or comparing concepts
  (design-exploration), attacking one hunch (idea-critique), a task plan
  (work-plan), or a product requirements spec or user stories.
---

# Design Doc

Converge a chosen concept into a design document for a module or system that a colleague who knows the field can review, and keep it true as results arrive. The finished document states what is proposed, which interfaces are fixed and which implementations are swappable adapters behind them, which parts tests verify and which parts evaluation verifies, what evidence each decision rests on and what would reverse it, and which bets still wait for a measurement.

The skill works for any system design and is shaped for modules whose core behavior comes from a trained model, a judge, or an agent loop. There, whether the design can work is settled by measurement more than by specification, so the document carries its unmeasured bets and its reversal conditions openly instead of presenting a finished answer.

## Ownership

This skill owns the document's semantic structure: which sections exist, what each must contain, and how they change together. `copydesk` owns the prose in every section. `write-notion` owns Notion publication: page layout, toggles, mentions, figure uploads, and checking the stored page. For a design doc bound for Notion, this skill supplies the sections and their content and write-notion places them: the Verification split fills write-notion's test-plan section, and the Threat model fills its security concern.

A product requirements spec, user stories, or a ticket breakdown is a different genre. Implementation tasks and schedule belong to a plan written with `work-plan` and linked from the document; the experiment queue here holds only the measurements that decide design questions.

## Before Drafting

Confirm that a concept is chosen. A design document converges; it does not open the space. If the user is still asking what could be built, say so and offer `design-exploration`; if they hold one hunch they want attacked before committing, offer `idea-critique`. A chosen concept with unresolved parts is enough to start, because the unresolved parts become open questions and queued experiments.

Gather before asking. Read what earlier work left: exploration notes or a mechanism map, a critique, an Interview Brief, a bet scoped with `praxis-direction`, measurements with their conditions, and literature notes. Carry each into its place: the exploration's root frames Context and Goals, and its rejected concepts with the user's stated reasons seed Alternatives; a critique's status and open attacks join the decision entry it tests, and its deciding measurement becomes a queue item; a bet's kill condition becomes a reversal condition; and an Interview Brief's confirmed decisions enter the decision log with their evidence kind. For brownfield work, read the code and existing interfaces and cite them at a revision. Ask the user only for judgment the material does not settle, such as which goal wins a conflict or how firm a constraint is.

Size the document to the decision. A full design doc earns its length when the module has dependencies, credible alternatives, or effects on other teams. When implementing would take less time than writing, write a mini design doc: Status, Summary, Design with its Interfaces and seams, Verification split, Open questions, and Decision log.

Write the document at the path the user names, else where the project keeps design documents, else at `docs/design/<slug>.md`, and state the path. For a new Markdown document, start from [the template](assets/design-doc.template.md).

## Structure

Default order. A team template or an existing document's convention wins. The sections marked Always form the mini design doc and stay even when short; omit any other section with nothing true to say.

| Section | Holds | Include |
| --- | --- | --- |
| Status | Status word, owner role, date, links | Always |
| Summary | What, how, key open item, next measurement | Always |
| Context and scope | Background facts, system boundary | When the reader lacks them |
| Goals and Non-goals | Checkable goals, deliberate exclusions | Full doc |
| Design | Mechanism, components, data flow, failure behavior | Always |
| Interfaces and seams | Fixed interfaces, adapters behind each | Always |
| Threat model | Assets, boundaries, adversary, scope | Adversarial setting |
| Verification split | Each component: tested or evaluated, where | Always |
| Alternatives considered | Advantage, reason it loses, retired concepts | Credible alternatives exist |
| Open questions | Undecided items as questions | Always |
| Experiment queue | Unmeasured bets, owner skill, status | Bets exist |
| Decision log | Decisions, evidence, reversal conditions | Always |
| References | Evidence and related records | Optional |

### Status and Summary

The status header carries one status word (WIP, In Review, Approved, or Obsolete with a link to its successor, unless the team has its own vocabulary), the owner by role, the last-updated date, and links to the code, plan, and result records. The Summary says what is being built, how it works in a sentence or two, the key undecided item, and what the next queued measurement would decide. A reviewer who reads only these two sections knows what is proposed and what is still open.

### Goals and Non-goals

Each goal carries a completion condition a reviewer can check. For a learned component, a goal names the metric, the population it is measured on, and the difference that would count, or states that the evaluation design will fix them; do not invent a threshold to make a goal look checkable. Non-goals are things that could reasonably be goals and are excluded on purpose, each with its reason; leave them out when no exclusion would surprise a reader.

### Design

Open with the mechanism figure when the reader needs to see how the module works, then explain components and responsibilities, the path of a representative request or episode, state and storage, and behavior when a dependency or model is unavailable, slow, or returns malformed output. For a learned component, also cover its lifecycle: where training and evaluation data come from, how a new adapter revision is promoted, and how a drop in deployed quality would be noticed. Link full schemas instead of copying them.

### Interfaces and Seams

State which interfaces are fixed and which implementations are swappable adapters behind them.

- A seam with one adapter is hypothetical; with two it is real. Put a seam where something actually varies, and write a component with one implementation as plain code.
- Put every learned or judging component behind a fixed interface so candidates can be swapped and compared. The second adapter usually costs little and earns its place: a rule or majority-class baseline, the incumbent, or a fake for tests.
- Shape the interface from what callers need, not from a candidate's raw output. The interface includes the output's meaning (the label set, whether a score only ranks or is a calibrated probability, an abstain outcome) and its failure behavior, because callers depend on both and evaluation measures them.
- Prompts, decoding settings, model revisions, and thresholds that belong to one candidate are adapter configuration, recorded per adapter revision so every result binds to an identifiable adapter.
- For an agent loop, the interface is the task contract and the end state it leaves; the loop is the adapter, and each tool sits behind its own seam with a production adapter and a controlled one.

Read [interfaces and verification](references/interfaces-and-verification.md) when writing this section or the Verification split, or when it is unclear where a seam goes. It has the vocabulary, the source note, and a worked synthetic example.

### Threat Model

Include it when an adversary chooses inputs or tries to move the system past a boundary: a fraud or spam classifier facing senders who adapt, an agent that reads untrusted web content, a model retrained on user-submitted data. State the assets, the trust boundaries (which inputs an adversary controls and which identity and state stay fixed), the adversary's access and budget and whether it adapts to the deployed system, the objective categories in scope and out of scope with reasons, the assumptions the protection depends on, and the residual risk. For a learned component, say how the evaluation will account for an adversary who adapts after deployment, since a fixed test set measures only the adversary of the past.

Write it in methodology language: boundary, objective category, metric, judge, environment, budget. The document holds no attack procedures and no concrete adversarial inputs. For a new system, the failure-mode pass in `praxis-direction` supplies the list to check against; adversarial evaluation scope and judging are designed with `evaluation-design`.

### Verification Split

Put every component on one side and say where its verification lives.

- **Deterministic:** a rule can decide whether an output is correct (parsing, schema checks, normalization of model output, routing on a verdict, budget enforcement, retries, storage). Tests verify it under the project's own test policy; this skill does not impose test-first development or a coverage target.
- **Judging or learned:** correctness is a judgment over a distribution (a model's labels or scores, a judge's verdicts, a ranking, an agent's task success). Evaluation designed with `evaluation-design` verifies it. A launch or trust verdict on that evaluation or its result belongs to `evaluation-audit`, not to this document.

Split a mixed component at its seam: the wrapper is tested with a fake adapter and the adapter's quality is evaluated. Contract checks at the interface (output schema, error modes, timeouts) run against every adapter, the candidate included. Code whose correctness no rule can state, such as a hand-tuned scoring heuristic, belongs on the evaluation side, and a judge used inside the system is a learned component. Present the split as a short table: component, side, verified by, where the tests or evaluation live, status.

### Alternatives Considered

For each credible option, state its advantage first and then why it loses under this design's goals, including the status quo when it is a real option. Keep retired concepts here with the evidence that retired them, so nobody reopens them without new evidence. A measured comparison of options is evidence; the chosen option stays Proposed in the decision log until the owner accepts it.

### Open Questions

Write each undecided item as a question, grouped by when it must be answered: before review, during implementation, or outside this design. Under each, say what it blocks and what settles it: the owner's judgment (settled with `interview`), a measurement (an experiment queue item), or reading (settled with `literature-research`). Do not put a question that only a measurement can answer to the user.

### Experiment Queue

List the bets the design depends on that nobody has measured yet. Each item names the bet, the decision log entry or open question it would change, the owner skill, and a status: queued, designed, running, measured, or dropped. Hand training, fine-tuning, and weight-adaptation comparisons, serving or inference configuration comparisons, reproductions, and training data to `ml-experiment`; hand what an evaluation measures, its cases and judges, and adversarial evaluation scope to `evaluation-design`. A bet often needs both, and the evaluation comes first when no accepted one exists. The receiving skill designs the measurement and applies its own authorization and spend gates; a queue entry does not authorize a run.

### Decision Log

Record each decision with its status (Proposed, Accepted, or Superseded by a named later entry), its evidence kind (literature, measurement, hunch, or constraint; often more than one), where that evidence lives, and the observable condition that would reverse it. A hunch is a legitimate basis when it is labeled as one, and a rationale the agent proposed is a hunch until evidence arrives; pair a hunch behind a decision that is expensive to reverse with a queue item. For a bet, write a dated prediction before the result exists and append hindsight beside it afterward, without editing the prediction. Supersede an accepted entry with a new one rather than rewriting it. Predictions and hindsight about the design stay in this log, not in `credo-journal`, which records paper-bound research taste.

Read [decision log and experiment queue](references/decision-log-and-queue.md) when writing or updating entries or applying a result. It has the entry formats, what each evidence kind requires, reversal conditions that can be checked, handoff contents for each owner skill, and a worked synthetic example.

## Close Open Decisions

When the user asks to settle the open decisions, or accepts an offer to, run `interview` rooted in this document's Open questions. The frontier is the judgment questions whose prerequisites are settled; inspectable facts are looked up instead of asked, and empirical questions become queue items instead of questions. After the user approves the brief, fold each answer into the body, add a decision log entry with its evidence kind (a requirement the owner states is a constraint; a preference without evidence is a hunch), remove the answered question, and update Status and Summary. Offer the interview once when open questions block review; do not start one unasked.

## Update With Results

When a measurement, a review outcome, or a new source arrives:

1. Read it at its supported strength and with its conditions. An inconclusive difference is not equivalence and does not close a bet. When an Approved decision or a launch rests on an evaluation result, record whether `evaluation-audit` has checked it.
2. Mark the queue item measured and link the result.
3. For each decision the result informs, append hindsight beside the prediction. When the result meets a reversal condition, add an entry that supersedes the old one, make the change it implies in Design, Interfaces and seams, and Verification split, and leave the new entry Proposed until the owner accepts it. When the result is mixed or meets no recorded condition, add an open question instead of choosing.
4. Retire a concept the result rules out: move it to Alternatives with the evidence and keep its decision log entries.
5. Change Status, Summary, Open questions, figure labels, and the queue together, so no section describes a design the log has superseded.

An update request authorizes editing the document. It does not authorize new runs or accepting decisions on the owner's behalf.

## Before Handing Over

Check the document against these before reporting:

- Every learned or judging component sits behind a named interface with its adapters listed, a single adapter has a stated reason, and the component appears on the evaluation side of the split; every deterministic component appears on the test side.
- Every decision has a status, evidence kind, evidence location, and either a reversal condition someone could check or a stated reason it is a commitment.
- Every queue item names the decision it would change and its owner skill.
- Every open question ends with a question mark and says what it blocks and what settles it.
- The threat model exists exactly when the setting is adversarial and holds no procedures or concrete adversarial inputs.
- Status words, terms, and numbers agree across the header, Summary, body, figure labels, and log, and every number keeps its measuring conditions.
- The prose follows `copydesk`; a Notion page has passed write-notion's verification.

Report the path or page link, the sections written or changed, the decisions still Proposed, and the queue items handed to other skills.

## References

| File | Read it when |
| --- | --- |
| [references/interfaces-and-verification.md](references/interfaces-and-verification.md) | Writing Interfaces and seams or Verification split, or placing a seam |
| [references/decision-log-and-queue.md](references/decision-log-and-queue.md) | Writing or updating the decision log or experiment queue, or applying a result |
| [assets/design-doc.template.md](assets/design-doc.template.md) | Starting a new design document as Markdown |
