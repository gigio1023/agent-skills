# [Module or system name] design

- Status: [WIP | In Review | Approved | Obsolete, superseded by link]
- Owner: [role]
- Updated: [date]
- Target: [deliverable form and date, when delivery is bound to one; omit otherwise]
- Links: [code at revision], [plan], [result records]

## Summary

- **What:** [what is being built, in one sentence]
- **How:** [how it works, in one or two sentences]
- **Key open item:** [the undecided item that matters most]
- **Next measurement:** [queue ID and the decision it would change]

## Context and Scope

[Background facts and the system boundary. Omit when the reader already has them.]

## Goals and Non-goals

- **Goals:** [each with a completion condition a reviewer can check; for a learned component, the metric, population, and difference, or a note that the evaluation design fixes them; for delivery bound to a date, the outcome, deliverable form, and scope promised by that date]
- **Non-goals:** [plausible goals excluded on purpose, each with its reason, including scope that will not fit the target date; omit when none would surprise a reader]

## Design

[Mechanism figure when the reader needs to see how it works. Then components, the path of a representative request or episode, state, failure behavior, and for a learned component its data sources, promotion of a new revision, and how a quality drop would be noticed. For an agent loop, the code that enforces each permission and budget, and, when episodes persist or touch external state, the restart and side-effect semantics.]

## Interfaces and Seams

| Interface | Fixed contract | Adapters | Production adapter |
| --- | --- | --- | --- |
| [name] | [link to definition] | [baseline, incumbent, candidate, fake] | [which] |

[Output meaning, failure behavior, and where the operating point lives, beside the table. A single adapter gets its reason.]

## Threat Model

[Only when the setting is adversarial: assets, trust boundaries, adversary access and budget and whether it adapts, objective categories in and out of scope with reasons, assumptions, residual risk. Methodology language only.]

## Operating Boundary

[Only when the system itself attacks: authorized targets and scope, budgets, containment, the never-do list, evidence handling, and the role that authorizes changes, each limit with the code that enforces it. Keep the threat model beside it when target responses are untrusted input that matters. Methodology language only.]

## Verification Split

| Component | Side | Verified by | Where | Status |
| --- | --- | --- | --- | --- |
| [component] | [Deterministic, or Learned or judging] | [real-run check, contract test, or evaluation] | [check artifact, test path, or evaluation record] | [exists, or queued with ID] |

Essential contracts:

- **[Contract]:** [why a break would pass a real run unnoticed and be costly, unsafe, or felt outside the module]; tested from the contract by an author who has not seen the implementation.

[Most deterministic parts have only a real-run check. Record any test requirement from the project's policy or CI with its source.]

## Alternatives Considered

- **[Option]:** [its advantage]; [why it loses under these goals, or the evidence that retired it]

## Open Questions

- **Before review**
  - [Question?]
    - Blocks: [what]; settled by: [owner judgment, queue ID, or reading]
- **During implementation**
- **Outside this design**

## Experiment Queue

| ID | Bet | Changes | Owner skill | Status | Result |
| --- | --- | --- | --- | --- | --- |
| E1 | [bet] | [D-number or question] | [ml-experiment, evaluation-design, or load-testing] | [queued] | [link or none yet] |

## Decision Log

### D1. [Decision as a noun phrase]

- Status: [Proposed | Accepted | Superseded by Dn], [date]
- Evidence: [kind], [location]; [kind], [location]
- Reverse if: [observable condition and what the design would do]
- Prediction, [date]: [for a bet, before the result exists]
- Critique, [date]: [when critiqued: status, deciding measurement as queue ID, open attacks]
- Hindsight: [appended when the result arrives]

## References

- [What it is], [when produced]: [why a reviewer would open it]
