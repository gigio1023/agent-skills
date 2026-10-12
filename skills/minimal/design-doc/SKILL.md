---
name: design-doc
description: >
  Write or update a design document for a module or system, especially one whose core behavior comes from a trained model, a judge, or an agent loop, with its interfaces and adapters, verification split, threat model or operating boundary, open questions, experiment queue, and decision log. Use for "write a design doc", "RFC for this module", "turn this concept into a design", "update the design with these results", "close the open questions in the design", "설계 문서 써줘", "설계 문서 갱신해줘". For a design doc in Notion this skill supplies the content and write-notion publishes it. NOT for Notion page mechanics (write-notion), opening the design space (design-exploration), attacking one hunch (idea-critique), a task plan (work-plan), or a product requirements spec or user stories.
---

# Design Doc

Converge a chosen concept into a design document for a module or system that a colleague who knows the field can review, and keep it true as results arrive. The finished document states what is proposed, which interfaces are fixed and which implementations are swappable adapters behind them, how each part is verified (a real run on fixed input, a contract test for the few contracts that warrant one, or evaluation), what evidence each decision rests on and what would reverse it, and which bets still wait for a measurement.

The skill works for any system design and is shaped for modules whose core behavior comes from a trained model, a judge, or an agent loop. There, whether the design can work is settled by measurement more than by specification, so the document carries its unmeasured bets and its reversal conditions openly instead of presenting a finished answer.

## Ownership

This skill owns the document's semantic structure wherever the document is published, whether as Markdown in a repository, a Notion page, or another host: which sections exist, what each must contain, and how they change together. `copydesk` owns the prose in every section. `write-notion` owns Notion publication: it maps these sections onto its page layout and handles toggles, mentions, figure uploads, and checking the stored page. For a design doc bound for Notion, this skill supplies the sections and their content and write-notion places them, for example the Verification split in its test-plan section and the Threat model or Operating boundary in its security section. A host's layout changes where sections appear, not which sections exist.

A product requirements spec, user stories, or a ticket breakdown is a different genre, and a delivery deadline does not change that: the document carries the outcome, deliverable form, target date, and scope by that date as context and constraints, not as requirements or stories. Implementation tasks and schedule belong to a plan written with `work-plan` and linked from the document; the experiment queue here holds only the measurements that decide design questions.

## Before Drafting

Confirm that a concept is chosen. A design document converges; it does not open the space. If the user is still asking what could be built, say so and offer `design-exploration`; if they hold one hunch they want attacked before committing, offer `idea-critique`. A chosen concept with unresolved parts is enough to start, because the unresolved parts become open questions and queued experiments.

Gather before asking. Read what earlier work left: exploration notes or a mechanism map, a critique, an Interview Brief, a bet scoped with `praxis-direction`, a delivery brief, measurements with their conditions, and literature notes. Carry each into its place: the exploration's root frames Context and Goals, and its rejected concepts with the user's stated reasons seed Alternatives; a critique's status and open attacks join the decision entry it tests, and its deciding measurement becomes a queue item; a bet's kill condition becomes a reversal condition; and an Interview Brief's confirmed decisions enter the decision log with their evidence kind. For brownfield work, read the code and existing interfaces and cite them at a revision; when the context lives in team records such as a tracker, chat, or wiki, reconstruct it with `internal-source-research` when installed and cite records the reader can open. Ask the user only for judgment the material does not settle, such as which goal wins a conflict or how firm a constraint is.

For product delivery with a deadline, carry the upstream bet or brief into the document: its outcome and deliverable form into Context and Goals, the target date into the header's Target line and into the decision log as a constraint entry with the role that can move it, and the scope promised by that date into Goals, with what will not fit by then stated as a Non-goal or as later work in the plan, each with its reason. The design still states mechanism, interfaces, verification, and open bets; a bet that threatens the date becomes an open question or a queue item, not a silent cut.

Size the document to the decision. A full design doc earns its length when the module has dependencies, credible alternatives, or effects on other teams. When implementing would take less time than writing, write a mini design doc: Status, Summary, Design with its Interfaces and seams, Verification split, Open questions, and Decision log.

Write the document at the path the user names, else where the project keeps design documents, else at `docs/design/<slug>.md`, and state the path. For a new Markdown document, start from [the template](assets/design-doc.template.md).

## Structure

Default order. A team template or an existing document's convention wins. The sections marked Always form the mini design doc and stay even when short; omit any other section with nothing true to say.

| Section | Holds | Include |
| --- | --- | --- |
| Status | Status word, owner role, date, links, optional target | Always |
| Summary | What, how, key open item, next measurement | Always |
| Context and scope | Background facts, system boundary | When the reader lacks them |
| Goals and Non-goals | Checkable goals, deliberate exclusions | Full doc |
| Design | Mechanism, components, data flow, failure behavior | Always |
| Interfaces and seams | Fixed interfaces, adapters behind each | Always |
| Threat model | Assets, boundaries, adversary, scope | Adversarial setting |
| Operating boundary | Targets, budgets, containment, never-do list | System that attacks |
| Verification split | Each component: real-run check, contract test, or evaluation; where | Always |
| Alternatives considered | Advantage, reason it loses, retired concepts | Credible alternatives exist |
| Open questions | Undecided items as questions | Always |
| Experiment queue | Unmeasured bets, owner skill, status | Bets exist |
| Decision log | Decisions, evidence, reversal conditions | Always |
| References | Evidence and related records | Optional |

### Status and Summary

The status header carries one status word (WIP, In Review, Approved, or Obsolete with a link to its successor, unless the team has its own vocabulary), the owner by role, the last-updated date, and links to the code, plan, and result records. When delivery is bound to a date, a Target line names the deliverable form and the date. The Summary says what is being built, how it works in a sentence or two, the key undecided item, and what the next queued measurement would decide. A reviewer who reads only these two sections knows what is proposed and what is still open.

### Goals and Non-goals

Each goal carries a completion condition a reviewer can check. For a learned component, a goal names the metric, the population it is measured on, and the difference that would count, or states that the evaluation design will fix them; do not invent a threshold to make a goal look checkable. Non-goals are things that could reasonably be goals and are excluded on purpose, each with its reason; leave them out when no exclusion would surprise a reader.

### Design

Open with the mechanism figure when the reader needs to see how the module works, then explain components and responsibilities, the path of a representative request or episode, state and storage, and behavior when a dependency or model is unavailable, slow, or returns malformed output. For a learned component, also cover its lifecycle: where training and evaluation data come from, how a new adapter revision is promoted, and how a drop in deployed quality would be noticed. For an agent loop, also cover which code enforces its permissions and budgets and what a restart does to an episode and its external side effects, as described under Interfaces and seams. Link full schemas instead of copying them.

### Interfaces and Seams

State which interfaces are fixed and which implementations are swappable adapters behind them.

- A seam with one adapter is hypothetical; with two it is real. Put a seam where something actually varies, and write a component with one implementation as plain code.
- Put every learned or judging component behind a fixed interface so candidates can be swapped and compared. The second adapter usually costs little and earns its place: a rule or majority-class baseline, the incumbent, or a fake for real-run checks and contract tests.
- Shape the interface from what callers need, not from a candidate's raw output. The interface includes the output's meaning (the label set, whether a score only ranks or is a calibrated probability, an abstain outcome) and its failure behavior, because callers depend on both and evaluation measures them.
- Prompts, decoding settings, model revisions, and thresholds that belong to one candidate are adapter configuration, recorded per adapter revision so every result binds to an identifiable adapter.
- For an agent loop, the interface is the task contract and the end state it leaves; the loop is the adapter, and each tool sits behind its own seam with a production adapter and a controlled one. Name the deterministic code that enforces each permission and budget, such as an allowlist in a tool adapter or a meter in the loop shell; prompt text can state a limit but does not enforce it. When episodes persist or touch external state, state the restart and side-effect semantics: what is checkpointed, whether a restarted episode resumes or starts over, which tool calls are idempotent, and how a duplicated or unconfirmed external write is detected and handled.

Read [interfaces and verification](references/interfaces-and-verification.md) when writing this section or the Verification split, when it is unclear where a seam goes or whether a contract is essential, or when an agent loop needs its enforcement and restart semantics stated. It has the vocabulary, the three verification means, the source note, and a worked synthetic example.

### Threat Model

Include it when an adversary chooses inputs or tries to move the system past a boundary: a fraud or spam classifier facing senders who adapt, an agent that reads untrusted web content, a model retrained on user-submitted data. State the assets, the trust boundaries (which inputs an adversary controls and which identity and state stay fixed), the adversary's access and budget and whether it adapts to the deployed system, the objective categories in scope and out of scope with reasons, the assumptions the protection depends on, and the residual risk. For a learned component, say how the evaluation will account for an adversary who adapts after deployment, since a fixed test set measures only the adversary of the past.

Write it in methodology language: boundary, objective category, metric, judge, environment, budget. The document holds no attack procedures and no concrete adversarial inputs. For a new system, the failure-mode pass in `praxis-direction` supplies the list to check against; adversarial evaluation scope and judging are designed with `evaluation-design`.

### Operating Boundary

When the system is itself the attacker, such as a red-teaming agent, an automated security-testing harness, or a fuzzing service, the threat model's place is taken by the operating boundary: the limits the system acts within. State:

- **Authorized targets and scope:** the systems, environments, and accounts it may act on, the authorization record each rests on, and what is out of scope.
- **Budgets:** requests, tokens, wall time, spend, and rate per target, and what happens when one runs out.
- **Containment:** where it runs, the network reach and credentials it holds, how its traffic and state stay apart from production and from third parties, and how a run is stopped.
- **Never-do list:** action categories forbidden whatever the objective, such as acting on an unlisted target, making irreversible changes to target state, keeping data beyond what evidence requires, or raising its own permissions or budget.
- **Evidence handling:** what each run records, where it is stored, who can read it, how long it is kept, and how sensitive data captured from a target is redacted.
- **Change authority:** the role that approves widening targets, budgets, or the never-do list; each change is a decision log entry.

Each limit is enforced by deterministic code outside the model, named in Design and listed as an essential contract in the Verification split. Target responses are untrusted input to the attacking system; when that matters, keep threat-model items for them beside the boundary. The methodology-language rule applies here too: the boundary names objective categories, environments, and limits, never attack procedures or concrete inputs.

### Verification Split

Put every component on one side, name what verifies it, and say where that lives.

- **Deterministic:** a rule can decide whether an output is correct (parsing, schema checks, normalization of model output, routing on a verdict, budget and permission enforcement, retries, storage). A real-run check verifies it by default: the real entry point runs on fixed input and leaves an artifact someone else can rerun, namely the input, the command, and the recorded output.
- **Judging or learned:** correctness is a judgment over a distribution (a model's labels or scores, a judge's verdicts, a ranking, an agent's task success). Evaluation designed with `evaluation-design` verifies it. A launch or trust verdict on that evaluation or its result belongs to `evaluation-audit`, not to this document.

A contract test is reserved for an essential contract: one whose break would pass a real run unnoticed and would be costly, unsafe, or felt outside the module. Typical cases are the interface every adapter at a seam must honor, budget and permission enforcement, and a persisted or transmitted format another party reads. Mark each essential contract and say why it is essential. Its test is written from the interface contract by an author who has not seen the implementation, following `coding-standards` when installed. Most deterministic parts have no contract test, and this skill imposes no test-first development or coverage target. When the project's documented test policy, a reviewer, or CI asks for more, record the requirement and its source beside the split; tests beyond what CI requires are the owner's call, kept as an open question until settled.

Split a mixed component at its seam: the wrapper gets a real-run check with a fake or rule adapter and the adapter's quality is evaluated; when the interface contract is essential, its contract test runs against every adapter, the candidate included. Code whose correctness no rule can state, such as a hand-tuned scoring heuristic, belongs on the evaluation side, and a judge used inside the system is a learned component. Present the split as a short table (component, side, verified by, where, status) followed by the essential contracts with their reasons.

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

- Every learned or judging component sits behind a named interface with its adapters listed, a single adapter has a stated reason, and the component appears on the evaluation side of the split; every deterministic component names its real-run check, and every contract test belongs to an essential contract whose reason is stated.
- For an agent loop, the code that enforces each permission and budget is named, and restart and side-effect semantics are stated when episodes persist or touch external state.
- Every decision has a status, evidence kind, evidence location, and either a reversal condition someone could check or a stated reason it is a commitment.
- Every queue item names the decision it would change and its owner skill.
- Every open question ends with a question mark and says what it blocks and what settles it.
- The threat model exists exactly when the setting is adversarial and the operating boundary exactly when the system itself attacks; every boundary limit names the code that enforces it, and neither section holds procedures or concrete adversarial inputs.
- When delivery is bound to a date, the Target line, Goals, Non-goals, and the date's constraint entry agree.
- Status words, terms, and numbers agree across the header, Summary, body, figure labels, and log, and every number keeps its measuring conditions.
- The prose follows `copydesk`; a Notion page has passed write-notion's verification.

Name the implementer path. Implementation follows `coding-standards`, when installed, which reads Interfaces and seams for where ports go and which adapter the composition root wires, the Verification split for what gets a real-run check, a contract test, or evaluation, Design for failure behavior and any agent-loop enforcement and restart semantics, the Operating boundary when present, and the Decision log for which decisions are still Proposed. Without that skill, the implementer reads the same sections. Implementation tasks and their order go in a plan written with `work-plan`.

Report the path or page link, the sections written or changed, the decisions still Proposed, the queue items handed to other skills, and the implementer path with the sections it reads.

## References

| File | Read it when |
| --- | --- |
| [references/interfaces-and-verification.md](references/interfaces-and-verification.md) | Writing Interfaces and seams or Verification split, placing a seam, judging whether a contract is essential, or stating agent-loop enforcement and restart semantics |
| [references/decision-log-and-queue.md](references/decision-log-and-queue.md) | Writing or updating the decision log or experiment queue, or applying a result |
| [assets/design-doc.template.md](assets/design-doc.template.md) | Starting a new design document as Markdown |
