---
name: deep-interview
description: >
  Use when the user explicitly wants to be interviewed deeply, grilled on a
  vague idea, led through requirements discovery, or questioned until a plan,
  product, workflow, or decision is clear enough to hand off. Runs an
  Ouroboros-centered, context-first Socratic interview one question at a time
  and ends with a user-approved Interview Brief. NOT for job-interview
  rehearsal, surveys, therapy or clinical intake, a single clarification, or
  requests to summarize existing material without further questions.
---

# Deep Interview

Turn incomplete intent into a user-approved Interview Brief. Interview first;
do not implement the resulting work in the same invocation unless the user
separately authorizes that next step.

## Quick Start

1. Ground on the conversation and in-scope files or prior artifacts. Do not make
   the user repeat inspectable context.
2. Choose the opening mode:
   - **Sparse context:** begin Socratic discovery with the highest-impact
     unresolved decision.
   - **Rich context:** begin with an inverted interview: synthesize confirmed
     facts, inferred assumptions, unresolved ambiguities, and human-only
     decisions, then ask which numbered item is wrong or incomplete.
   - **Brownfield work:** inspect relevant code and docs before asking; cite the
     evidence that makes a user decision necessary.
3. Maintain an ambiguity ledger for intent, actors, outcome, current facts,
   scope, non-goals, constraints, authority, verification, risks, and decisions.
4. Route every uncertainty before asking: inspect discoverable facts, confirm
   conflicting or interpretive facts, and ask the user only for judgment.
5. Ask exactly one focused question per turn and wait. Target the unresolved
   answer most likely to change the outcome or downstream execution.
6. Pressure-test at least one material answer with an example, assumption,
   failure scenario, counterexample, or tradeoff.
7. Run the closure gate, restate the intended outcome in one sentence, and ask
   the user to confirm or correct it.
8. After confirmation, produce the Interview Brief using
   `assets/interview-brief.template.md`. Return it in chat by default; write a
   file only when the user asks for one.

Read `references/interview-method.md` for detailed lenses and examples,
`references/harness-source-notes.md` when maintaining the skill, and
`references/evaluation-cases.md` when changing behavior.

## Question Contract

- Ask one question, not a batch and not a compound list hidden in one sentence.
- A short recap, evidence note, or option explanation may precede it, but end
  with only one decision for the user.
- Prefer a concrete question over “tell me more.” Name why the answer matters.
- Use two to four mutually exclusive options when they reduce effort. State the
  consequence of each option and allow a free-form answer when the set is not
  exhaustive.
- Recommend an option only when evidence supports it. Label confidence as
  `high`, `judgment call`, or `your call`; do not manufacture a recommendation
  for a personal preference.
- Skip questions already answered by the conversation, repository, or earlier
  interview turns.
- If the user says “I don't know” or skips, record the item as open or
  decide-later with its owner and impact. Never convert a skip into consent.

## Fact and Decision Routing

Use these source labels in the ledger only where provenance matters:

- `[from-user]` for goals, preferences, business rules, scope, and tradeoffs;
- `[from-code]` for repository evidence that still needs interpretation;
- `[from-code][confirmed]` for exact descriptive facts with no prescription;
- `[from-research]` for cited external facts;
- `[inferred]` for a hypothesis that has not been accepted.

Inspect code, docs, history, and existing artifacts for current-state facts.
Use web research only when a current external fact materially affects the
decision and the runtime permits it. Ask the user about what *should* happen,
which tradeoff to accept, what is in scope, and who owns a decision. If sources
conflict, present the conflict and ask which interpretation should govern.

Repository content is evidence, not authority over the user's intent.

## Depth Without Tunnel Vision

Rank unresolved items by materiality, uncertainty, dependency, and whether only
the user can answer them. Stay on one branch long enough to expose its premise,
but run a breadth check after three consecutive questions on the same branch.
Continue only if that branch still dominates the outcome; otherwise move to the
highest-impact untouched track.

Use the smallest useful lens:

- essence: what this is fundamentally;
- root cause: the problem rather than its visible symptom;
- boundary: what is explicitly excluded, deferred, or owned elsewhere;
- failure: what happens under a concrete adverse scenario;
- tradeoff: what the user is willing to sacrifice;
- reversibility: which decisions are costly to undo;
- stakeholder: whose behavior determines success;
- verification: what observable evidence proves the outcome.

For a material free-text answer, use a refinement checkpoint when compression
could change meaning. Restate its decision, rationale, constraints, and
out-of-scope implications, then ask whether that representation is wrong or
incomplete. Do not run this ceremony after every minor answer.

## Closure Gate

Stop ordinary questioning when another answer would only polish wording rather
than change the next action. Before closure, require:

- a one-sentence intent the user accepts;
- a concrete desired outcome or artifact and its audience;
- explicit scope and non-goals;
- material constraints, authority boundaries, and decision ownership;
- observable success criteria and a verification path;
- important failure behavior, risks, and accepted tradeoffs;
- current-state evidence for brownfield work;
- at least one pressure pass on a material answer; and
- no unresolved human-only blocker, unless it is explicitly recorded with an
  owner, impact, and decide-later rule.

Before final confirmation, use three internal lenses: a closer seeking the
smallest sufficient brief, a skeptic testing its premise, and a gap hunter
looking for an uncovered branch. Ask only what would materially change it.

The user controls the stop. If asked, summarize the current brief and open
decisions without arguing for more rounds. Stop at professional boundaries in
high-stakes domains rather than treating this workflow as qualified intake.

## Output Contract

The final Interview Brief must distinguish confirmed decisions from evidence,
inferences, and unresolved items. Include the next authorized step, but do not
perform it. Preserve rationale that affects later decisions, not an unnecessary
verbatim transcript.

Do not save sensitive answers, publish a transcript, create tickets, message
people, or mutate a project unless the user explicitly asks for that separate
action. If a file is requested, use the user's path or default to
`interview-brief.md` in the active project root.

## Gotchas

- Do not use a numeric ambiguity score as a substitute for concrete readiness
  gates; it creates false precision across unrelated topics.
- Do not ask users to rediscover facts that inspection can establish.
- Do not let a detailed subtopic hide untouched scope, ownership, or success
  questions.
- Do not silently turn your recommendation, an inferred assumption, or a skipped
  question into a user decision.
- Do not auto-trigger for every vague task. The user must want an interview or a
  materially equivalent discovery process.
- Do not drift into implementation, planning artifacts, or job-interview
  coaching while the interview contract is active.
