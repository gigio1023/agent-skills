# Interfaces, Seams, and the Verification Split

Read this when writing the Interfaces and seams or Verification split sections, when deciding whether a component should sit behind a seam, or when a component's side of the split is unclear.

## Contents

- Vocabulary
- Where a seam belongs
- Learned and judging components
- Agent loops
- The interface as test and evaluation surface
- Classifying components
- Worked example: a message spam classifier
- Source note

## Vocabulary

Use these terms the same way throughout the document so a reviewer can tell which slot each part fills.

- **Module:** a unit that callers use through an interface while its implementation stays behind it, at any scale: a function, a service, or a model-backed component together with its wrappers.
- **Interface:** what a caller has to know to use the module without surprises: types, invariants, ordering, error modes, latency and cost budgets, and, for a learned component, the meaning of its output.
- **Seam:** the place where behavior can change without editing the callers. The interface lives at the seam, and where to place it is a design decision of its own.
- **Adapter:** a concrete implementation that fills a seam. The word names a role, not a size: a fine-tuned model, a rule baseline, and an in-memory fake can all be adapters of one interface.
- **Depth:** how much behavior callers get per unit of interface they must learn. A deep module hides much behind a small interface; a shallow one makes callers learn nearly as much as it contains.

## Where A Seam Belongs

Put a seam where something actually varies across implementations. A seam with one adapter is hypothetical: it adds indirection and leaves nothing to compare. A seam with two adapters is real. A deterministic component with one implementation is written as plain code with no seam.

Apply the deletion test to each module the design introduces: imagine removing it. If its complexity would reappear in every caller, the module earns its place. If the complexity would disappear, the module was a pass-through and the design is simpler without it.

Keep each interface small. Fewer entry points and simpler parameters mean fewer contract tests, a smaller evaluation surface, and less to change when a candidate is swapped.

## Learned And Judging Components

A learned or judging component is the clearest case for a real seam, because the design expects to compare candidates over its life. The second adapter is usually cheap and earns its place: a rule or majority-class baseline that gives evaluation a floor, the incumbent model, or a fake that returns fixed outputs for tests.

- Shape the interface from what callers need. Each adapter normalizes its raw output (text, logits, tool calls) into the interface type, and a normalization failure is an adapter error with a defined interface outcome.
- Define the meaning callers rely on: the label set, whether a score only ranks or is a calibrated probability, whether an abstain or unknown outcome exists, and any reason or evidence field a caller reads. Evaluation measures exactly these, and two candidates whose outputs mean different things cannot be compared.
- Define failure behavior at the interface: timeout, malformed output, unavailable provider, exhausted budget, and the caller's fallback for each.
- Keep prompts, templates, decoding settings, model revision, and preprocessing inside the adapter as configuration, recorded per adapter revision so every result binds to an identifiable adapter.
- Say where the operating point lives. If the adapter returns a score and the caller applies the threshold, one evaluation run can compare candidates at matched operating points, and swapping a candidate means choosing the caller's threshold again unless scores are calibrated. If the adapter returns only a label, the threshold is adapter configuration, chosen for each candidate on data kept apart from the reporting set, and each evaluation run sees one operating point.

## Agent Loops

For a component that acts through an agent loop, the interface is the task contract and the outcome. The contract states the goal, the inputs, the allowed actions, the budget in turns, tokens, and wall time, and the termination conditions. The outcome is the end state the loop leaves behind, with the agent's success claim and trace as supporting records. The loop itself (model, prompt, scaffold) is the adapter, so a scripted policy for known flows and a model-driven loop can sit behind the same contract and be compared.

Each tool the loop calls is its own seam, with a production adapter and a controlled one such as a recorded environment or an in-memory fake. The controlled adapters let tests check tool code and budget enforcement deterministically and let evaluation run episodes in a reproducible environment. For a web-navigation agent, for example, a snapshot of the target site behind the browsing tool's interface lets the same episode run against two loop adapters. Score the end state, not the agent's account of it.

## The Interface As Test And Evaluation Surface

Tests, evaluations, and callers cross the same seam. Contract checks at the interface (output schema, error modes, timeouts, budget enforcement) run against every adapter, the candidate included. Quality evaluation calls the interface with the production configuration of the adapter under test. An evaluation that scores something callers never receive, such as raw model text before normalization or an intermediate score, measures a different system, and the document gives the reason when it does so.

## Classifying Components

The split asks one question of each component: can a rule decide whether its output is correct for a given input?

- **Yes, deterministic.** Parsing, schema validation, normalization of model output, routing on a verdict, budget enforcement, retries, storage, and access checks written as code. Tests verify these under the project's test policy. Nondeterminism from concurrency or timing does not move a component to the evaluation side.
- **No, judging or learned.** Correctness is a judgment over a distribution: a model's labels or scores, a judge's verdicts, a ranking, generated text, an agent's task success. Evaluation designed with `evaluation-design` verifies these.

Edge cases:

- A wrapper around a learned component splits at the seam. The wrapper is tested with a fake adapter; the adapter's quality is evaluated.
- Hand-written code whose correctness no rule states, such as a tuned scoring heuristic, is on the evaluation side for its quality, even though tests can still check that it computes what it was written to compute.
- A judge used inside the system, such as a model that grades candidate answers before one is returned, is a learned component. It needs the validation `evaluation-design` gives an evaluation judge.
- A rule that encodes policy, such as which labels send a message to review, is deterministic. Whether that policy produces the intended outcome in deployment is an evaluation question about the whole module.
- A latency or cost budget is verified by neither unit tests nor quality evaluation. State it as a goal with its measuring conditions (percentile, load, hardware); when candidates differ on it, queue a serving comparison for `ml-experiment`.

## Worked Example: A Message Spam Classifier

Synthetic. A messaging service routes each incoming message to the inbox, a spam folder, or a human review queue.

- **Interface:** `classify(message, sender_history) -> Verdict`. A `Verdict` holds a score that only ranks, an abstain flag, and a reason code from a fixed list. A call that exceeds 150 ms returns an abstaining verdict with reason `timeout`, and the router sends every abstention to review. The router applies the spam threshold to the score, so evaluation compares candidates at matched false-positive rates and the threshold is router configuration, chosen again when a candidate is adopted.
- **Adapters:** a keyword and sender-reputation rule set, which is also the fallback; the incumbent gradient-boosted model; a small language-model candidate; and a fixed-output fake for tests. The candidate's prompt, model revision, and output parser are its adapter configuration.
- **Seam not drawn:** message parsing has one implementation and nothing that varies, so it is plain code.

| Component | Side | Verified by | Where | Status |
| --- | --- | --- | --- | --- |
| Message parsing | Deterministic | Unit tests | `tests/parse/` | Exists |
| Timeout and abstain path | Deterministic | Contract test, every adapter | `tests/contract/` | Exists |
| Verdict routing | Deterministic | Unit tests | `tests/router/` | Exists |
| Rule set implementation | Deterministic | Unit tests | `tests/rules/` | Exists |
| Rule set label quality | Learned or judging | Paired evaluation, as floor | `evals/spam-paired/` | Queued, E1 |
| Candidate label quality | Learned or judging | Paired evaluation vs incumbent | `evals/spam-paired/` | Queued, E1 |

The 150 ms budget is not a row: it is a goal measured on the target hardware, and whether the candidate meets it is a serving comparison queued as E2.

## Source Note

The vocabulary of modules, interfaces, seams, adapters, and depth, the deletion test, the rule that one adapter makes a hypothetical seam and two make a real one, and the interface as the test surface are adapted from the `codebase-design` skill in [mattpocock/skills at 49dd158](https://github.com/mattpocock/skills/tree/49dd158/skills/engineering/codebase-design) (MIT License, Copyright (c) 2026 Matt Pocock), which credits the seam to Michael Feathers and deep modules to John Ousterhout. The ideas are rewritten here, not copied. This skill extends them to learned and judging components: the second adapter as an evaluation baseline, output meaning and operating point as part of the interface, agent tools behind their own seams, and evaluation crossing the same seam as tests.
