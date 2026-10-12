# Decision Log and Experiment Queue

Read this when writing or updating decision log entries or experiment queue items, or when a result arrives and the design must change. SKILL.md holds the rules; this file holds the formats, what each evidence kind requires, the handoff contents, and a worked synthetic example.

## Contents

- Decision log entry
- Evidence kinds
- Reversal conditions
- Predictions and hindsight
- Experiment queue item
- Handoff to the owner skill
- Applying a result
- Worked example

## Decision Log Entry

Number entries in order and never reuse a number. Give each a short noun-phrase title naming the decision. A long log can move to a sibling file linked from the section.

```markdown
### D4. Language-model candidate behind the existing Verdict interface

- Status: Proposed, 2026-03-02
- Evidence: hunch, from reading the incumbent's misses in a February sample; literature, a paraphrase-robustness study (citation), shown on a different message domain
- Reverse if: in E1, the candidate's spam recall at the incumbent's false-positive rate is within 1 point of the incumbent's on the held-out month
- Prediction, 2026-03-02: recall rises 3 to 6 points on paraphrased spam and changes little elsewhere
- Critique, 2026-02-27: unmeasured; deciding measurement is E1; open attack: paraphrased spam may be too rare in deployment for any gain to matter
- Hindsight: appended when E1 is measured
- Supersedes: none
```

- **Status:** Proposed until the owner accepts it; Accepted with the date; Superseded by a named later entry. A reversal is a new entry that supersedes the old one.
- **Evidence:** each kind the decision rests on, with its location.
- **Reverse if:** the observation that would change the decision and the direction it would move.
- **Prediction and Hindsight:** for a decision that is a bet on an unmeasured result.
- **Critique:** a dated line per critique from `idea-critique`, with its status (supported, contradicted, inconclusive, or unmeasured), its deciding measurement as a queue ID, and the attacks still open. A later critique adds a line; earlier lines stay. An open attack that names a checkable observation can become the reversal condition.
- **Supersedes:** the earlier entry this one replaces, if any.

## Evidence Kinds

| Kind | Counts as | Location records |
| --- | --- | --- |
| Literature | Published work, prior-art check, mechanism map entry | Citation, conditions shown under |
| Measurement | A result from this project's runs | Result record, revision, data, metric, n |
| Hunch | Intuition without evidence yet | Whose, by role, and what it rests on |
| Constraint | Budget, hardware, latency, policy, deadline, an interface another team owns | Source, role that can change it |

- Name every kind a decision rests on. A decision resting on a hunch and a constraint says both.
- A loosely related paper does not turn a hunch into literature. Record the hunch and link the paper as context, with the condition under which it was shown.
- A measurement keeps its conditions. A result from a different model revision, data population, or serving mode is evidence about that configuration; say so when it differs from the design's. When a launch rests on an evaluation result, record whether `evaluation-audit` has checked it.
- A rationale the agent proposed is a hunch until evidence arrives. The owner's acceptance changes the status, not the evidence kind.
- A constraint is recorded as the owner or source states it. If its firmness is unclear, that is an open question for the owner.
- A delivery date is a constraint entry of its own, such as "D2. Batch scoring endpoint delivered by 2026-11-30", with the source that set it and the role that can move it. Its reversal condition is the date or the scope promised by it changing, and decisions that trade quality or scope for the date cite it.

## Reversal Conditions

A reversal condition names an observation someone could make and what the design would do. "If the candidate's recall at the incumbent's false-positive rate is within 1 point of the incumbent's, keep the incumbent" can be checked. "If it doesn't work" cannot. Use the smallest decision-relevant difference from the evaluation design when one exists; otherwise mark the threshold as proposed and let the evaluation design confirm or replace it. A condition stated as a margin is met only when the interval, not just the point estimate, falls on its side.

For a constraint, the reversal condition is the constraint changing: "if the latency budget rises above 300 ms". For a hunch, it is the measurement queued to test it. When no observation would reverse a decision, say so: it is a commitment, and the entry explains why the commitment is worth making without evidence.

## Predictions And Hindsight

For a bet, write the prediction before its result exists, dated, in a sentence or two: the direction and rough size of the effect and where it should appear. When the result arrives, append hindsight beside it: what happened, how far the prediction was off, and which assumption the miss points to. Never edit the prediction. Over time, the pairs show which kinds of hunches hold for this system.

## Experiment Queue Item

A table keeps the queue scannable; reasoning that does not fit a short cell goes under the table.

| ID | Bet | Changes | Owner skill | Status | Result |
| --- | --- | --- | --- | --- | --- |
| E1 | Candidate beats incumbent on paraphrased spam | D4 | evaluation-design | Designed | None yet |

Statuses:

- **queued:** recorded, not yet handed off.
- **designed:** the owner skill returned a design or measurement contract.
- **running:** an authorized run is in progress.
- **measured:** the result is linked and applied to the log.
- **dropped:** no longer needed, with the reason, such as the decision it served being settled another way.

Order the queue by the decisions the items would change and their cost. An item that unblocks review or could retire the leading concept goes first, and among those the cheapest check that could discriminate between the alternatives goes first.

## Handoff To The Owner Skill

Hand an item over with enough for the receiving skill to start without this conversation:

- the question, and the decision log entry or open question it would change;
- the alternatives the measurement must separate, and the prediction;
- the smallest difference that would change the decision, when known;
- the interface and adapters involved, with their revisions;
- the constraints: data available, budget tier, latency or hardware limits, deadline.

Route by what the item needs:

- `ml-experiment`: training, fine-tuning, and weight-adaptation comparisons, serving or inference configuration comparisons, reproductions, and training data.
- `evaluation-design`: what an evaluation measures, its cases and labels, its checks and judges, and adversarial evaluation scope.
- `load-testing`: latency, throughput, and capacity under load.
- Both, evaluation first, when candidates must be compared and no accepted evaluation exists for the behavior.

A question that reading can settle is not an experiment; it stays an open question settled with `literature-research`. The receiving skill applies its own authorization and spend gates, and a queue entry authorizes no run.

## Applying A Result

| Result against the reversal condition | Change to the document |
| --- | --- |
| Meets it | New Proposed entry superseding the old; Design, Interfaces and seams, Verification split, and Alternatives changed to match |
| Supports the decision | Evidence and hindsight added; status unchanged |
| Inconclusive | Item stays open or is reframed with the reason; design unchanged |
| Outside every recorded condition | Open question added; design unchanged until the owner decides |

In every case, append hindsight beside the prediction, mark the queue item, and update Status, Summary, Open questions, and affected figure labels together.

## Worked Example

Synthetic, continuing the message spam classifier from [interfaces and verification](interfaces-and-verification.md). Dates and numbers are invented.

Decision log before measurement:

- **D1. Abstain outcome routed to human review.** Accepted, 2026-02-10. Evidence: constraint, review capacity of 2,000 messages a day in the operations plan. Reverse if: abstentions exceed review capacity on five consecutive days.
- **D2. Rule set kept as fallback adapter.** Accepted, 2026-02-10. Evidence: constraint, the service must classify when the model host is down; measurement, rule-set recall on the February sample (link). Reverse if: the model host's measured availability makes fallback traffic negligible for a quarter.
- **D3. Rank-only score with the threshold in the router.** Accepted, 2026-02-12. Evidence: hunch, candidate scores will not share a calibration. Reverse if: a downstream consumer needs a probability.
- **D4. Language-model candidate behind the existing Verdict interface.** Proposed, as in the entry format above.

| ID | Bet | Changes | Owner skill | Status | Result |
| --- | --- | --- | --- | --- | --- |
| E1 | Candidate beats incumbent on paraphrased spam | D4 | evaluation-design | Designed | None yet |
| E2 | Candidate meets 150 ms at p95 on target hardware | D4, Goal 2 | load-testing | Queued | None yet |

E1's result arrives. On the held-out month (4,800 spam messages, candidate revision r3, incumbent revision r12), recall at the incumbent's false-positive rate is 0.4 points higher overall, with a 95% interval of -0.2 to 0.9, and 2.1 points higher on the paraphrased slice (610 messages, interval 0.4 to 3.8).

Changes:

- E1 is marked measured with a link to the result record.
- D4 gets hindsight: "Predicted 3 to 6 points on paraphrased spam; measured 2.1. The critique's open attack held: paraphrased spam is about an eighth of spam, too little for the slice gain to move overall recall." The prediction stays as written.
- The whole overall interval lies inside the 1-point margin, so D4's reversal condition is met. A point estimate inside the margin with an interval reaching past it would have been inconclusive instead. D5, "Incumbent stays the primary adapter", supersedes D4 with status Proposed and evidence: measurement, E1.
- The candidate as primary adapter moves to Alternatives with E1 as the retiring evidence.
- The paraphrased-slice gain raises a new bet: the candidate as a second stage on the incumbent's low-margin messages. It becomes E3, owned by evaluation-design, with a prediction written now. E2 stays queued but now serves E3 instead of D4, because a second stage must still fit the latency budget.
- Status, Summary, and the mechanism figure's adapter labels change in the same edit.
