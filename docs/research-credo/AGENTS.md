# Research credo

Guidance for work in this repository, and an optional source to adapt into a research project's instructions when the user requests setup. Installing skills alone does not activate every method or journal habit. Project preferences and records belong with the project, outside installed skill packages.

The repository holds eleven skills in three tracks with different readers. The four `credo-` skills form the paper track, adapted from Nicholas Carlini's [How to win a best paper award](https://nicholas.carlini.com/writing/2026/how-to-win-a-best-paper-award.html); it answers to a reader and a venue. The work track serves the reader who decides whether to launch, ship, adopt a model, or tell a customer; its skills are split by the moment in the work (design, audit, operate) and carry their own source notes. The organization track answers to a decision a company must make with the compute, data, and experts it has.

## Paper track scope

Apply `credo-taste`, `credo-paper-plan`, `credo-journal`, and `credo-release` only when the work is aimed at a paper or a publishable research claim. Within that scope the essay's bar holds unsoftened: one idea, a best-case conclusion that says more than a number went up, a result months ahead of the next person, and effort a reasonable person would not spend. A ticket, a bug, a customer deadline, a product evaluation, or this week's task is out of scope even when it involves a model, a benchmark, or the word research; do that work well with the work-track skills and move on. When it is unclear whether the work aims at a paper, ask that one question first.

`credo-taste` and `credo-journal` run only on the user's request, because an unrequested run either interviews the user or writes to the user's journal. Harness adapters keep them out of automatic selection: `disable-model-invocation` in the Claude Code frontmatter and `policy.allow_implicit_invocation: false` in `agents/openai.yaml` for Codex. Each body states the same scope for harnesses without those controls.

## Choose the skill

| Track | Work | Skill |
| --- | --- | --- |
| Paper | Choose, continue, pivot, or stop a paper-bound research direction, or judge whether a work result could become a paper, on request | `credo-taste` |
| Paper | Plan or critique a paper's argument, or plan the response to peer reviews | `credo-paper-plan` |
| Paper | Record research ideas, predictions, and hindsight, on request | `credo-journal` |
| Paper | Check a paper before submission or release | `credo-release` |
| Work | Read a paper, check prior art for a claim, survey open models or datasets, collect sources | `literature-research` |
| Work | Design, run, or interpret a training, adaptation, serving, or reproduction experiment and its training data | `ml-experiment` |
| Work | Design or change what an eval measures, its cases, labels, checks, and judges | `evaluation-design` |
| Work | Give a launch, hold, or report verdict on a built eval, judge, harness, scoring change, or result | `evaluation-audit` |
| Work | Operate an approved evaluation campaign across attempts and sessions | `evaluation-operations` |
| Organization | Turn an agenda into a resourced bet, run the failure-mode pass, or set up the praxis profile, on request | `praxis-direction` |
| Organization | Reconstruct work context from authorized internal sources | `internal-source-research` |

Each common request has one owner, so a benchmark build or a readiness check loads one skill:

| Request | Owner |
| --- | --- |
| Design or redesign an eval, its cases, or its judge; validate a judge against new labels | `evaluation-design` |
| Is this eval, harness, judge, or scoring change ready; can this result be trusted or shown to a customer | `evaluation-audit` |
| Run, resume, monitor, or diagnose an approved campaign | `evaluation-operations` |
| Adapt or train a model; compare serving configurations before a full run | `ml-experiment` |
| Which open models or datasets exist; has this claim been done before | `literature-research` |
| Could this work result become a paper | `credo-taste` |

The design skill never declares its own instrument ready; the audit reads the artifacts, not the design's claims. Harness feature work, eval framework choice, infrastructure, and incidents are outside the pack.

Use existing decisions and evidence before asking another question. A user chooses purpose, tradeoffs, and authority; an empirical unknown may require an experiment. A finding, rejected hypothesis, unsuitable dataset, or unresolved comparison can be a useful result without a code change.

Inside an organization, where the result is a product, customer, or capability decision rather than a paper, `praxis-direction` turns the agenda into a bet and `credo-taste` stays with paper directions. The organization's outcomes, compute ladder, experts, and data live in its own `praxis-profile.md`, written by `praxis-direction` setup in that workspace and never in this repository.

## Work and continuity

State the question and the decision the work could change. Select a credible comparison and assessment appropriate to that question. Novelty, months ahead, and publication claims belong to the paper track; work-track skills do not borrow them. A work result that might become a paper is a separate decision for `credo-taste`. Preserve actual results, relevant conditions, and interpretation in existing project records. Give the reader the explanation needed for this decision without reciting every possible qualification.

Quick checks within the same question and authorized resources can proceed. Ask before a new direction, a run that spends beyond the always-on tier or the stated budget, or a newly proposed long activity, unless that work is already authorized. Short duration does not grant new spending, data access, or external actions. Honor an existing resource budget and stop condition.

For cross-session purpose, constraints, current understanding, and adaptive plans, use the project's existing records or requested Gigio Pack workflow. Do not create a second project state system here. For document production, use the requested writing method; paper planning does not prohibit prose the user separately asks the agent to draft.

## Source collection

`literature-research` reads a supplied paper on request and applies actively to explicit research, literature-search, or collection requests. Otherwise use it only when a decision needs evidence from papers or technical research posts; a general lookup, a vendor comparison, or a document task is not a research question because it says "investigate". Search the configured library before expanding it, preserve inspected originals and useful associated material, and record access gaps. Respect read-only, offline, and no-download constraints. Terminology tools, when available, use the project's accepted terms without altering collected originals.

## Maintaining this repository

Keep each skill independently usable with colocated references and resources. Method boundaries should prevent duplicate ownership without forcing every task through all skills. Keep private transcripts, credentials, datasets, and project examples out of published packages. Use synthetic examples or explicitly authorized public sources.

Validate changed packages, resource links, names, and discovery. Static package checks and illustrative walkthroughs do not establish improved model behavior. Do not launch paid or long behavioral trials merely to maintain instructions.

### Tests

A useful test protects a meaningful caller-visible contract and derives expected results independently from the implementation under test. Use requirements, documented contracts, independent calculations, or reproduced bugs. Copying expected values from the code merely repeats its assumptions; writing a test after the implementation does not itself make the test invalid.

- Verify features end to end. Run the real entry point on real or fixed input and leave an artifact another person can rerun and compare, such as an output file, log, report, or screenshot. Give the command and the artifact path in the final message.
- Choose focused cases from plausible failures and the behavior callers depend on. Use an isolated test when it can establish a contract more directly or cover a failure path the entry-point run does not exercise.
- For a bug fix, reproduce the failure before the fix when feasible and retain the cases needed to protect the corrected contract.
- Public APIs, CLI behavior, parser rejection, compatibility, cancellation, and resource cleanup can warrant tests, as can security, financial, data-loss, and reported-number risks. Avoid redundant tests that add no useful regression signal.
- Diagnose a test that fails during refactoring. Fix a behavior regression in the code; adapt stale setup or implementation-specific assertions while preserving the public contract. Remove a test only when its contract is obsolete, redundant, or has no independent value, and explain why. A failure alone is not evidence that the test should be deleted.
- Test observable outcomes rather than internal helper layout, fakes built only for the test, or exact prompt and message wording without a specified contract. Exact values, serialized text, and formatting can be valid assertions when an API, protocol, documented CLI, or consumer depends on them.

End-to-end path here: run each changed bundled script on real or fixed input, then discover and validate the packages with the Skills CLI and package validators. Preserve the append-only contract in `skills/credo-journal/scripts/journal.py`: existing journal content must remain unchanged when an entry is added. Documentation-only edits need package and consistency checks; model trials require a separate request.

## Owner settings (adapt per project)

- Journal path: `~/research/journal.md`
- Research library: existing configured collection first; otherwise `research/` within a project or `~/research/` without one
- Reader for paper planning, unless specified: myself six months ago
- Comparative advantage: not yet written
- Tenets held differently or undecided: T13 timeboxing, undecided
- Journal capture and review schedule: only as requested or explicitly adopted by the project
- Praxis profile: none in this repository; `praxis-direction` setup writes one in the organization's workspace and links it from that project's instructions
