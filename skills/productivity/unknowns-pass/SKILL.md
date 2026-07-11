---
name: unknowns-pass
description: >
  Use when the user starts substantial work in territory they don't know well —
  a new project, research direction, investment or money-management strategy,
  career or life plan, product or game idea, or an unfamiliar part of a
  codebase — with no spec, plan, or reference yet; or when they ask for an
  unknowns pass, blind spot pass, option map, throwaway variants, or a launch
  brief. Surfaces unknowns with the single cheapest technique, compresses what
  was learned into a launch brief, and, when the user cannot test the result
  directly, checks their understanding with an explainer and quiz before the
  result is adopted. NOT for well-specified or small tasks, multi-round
  Socratic discovery (use deep-interview), final decision synthesis (use
  fable5-judgment), or packaging session state (use handoff-prompt).
---

# Unknowns Pass

Close the gap between what the user asked for and what reality will demand by
making unknowns explicit before the expensive work starts. One pass is one
technique plus one launch brief. The pass ends at the brief; executing the
plan needs separate authorization.

## Quick Start

1. Establish the starting point. Inspect whatever is inspectable — files,
   repository, prior artifacts — before asking anything. If the user's
   familiarity with the domain is unclear, ask once; a novice in the domain
   changes what every technique must cover.
2. Classify the dominant unknown and pick exactly one technique:

   | Dominant unknown | Signal | Technique |
   | --- | --- | --- |
   | Unknown unknowns | New domain; doesn't know what to ask or what "good" looks like | Blindspot brief |
   | Unsettled scope or direction | "Something in this area"; competing ways to attack | Option map |
   | Unknown knowns (taste) | "I'll know it when I see it" | Throwaway variants |
   | Known unknowns | Nameable open questions | Mini-interview |
   | Inexpressible want | Can't describe it, but an example exists somewhere | Reference request |

3. Run the technique well (next section). Run a second one only when the
   first reveals the need and the user agrees.
4. Work out how the result will be verified (below); that changes the plan
   order, the notes file, and the final check.
5. Compress everything learned into a launch brief using
   `assets/launch-brief.template.md`.

Keep the pass light: one technique, at most 7 questions, at most 3 variants,
at most 1 artifact. Go deeper only when the user asks.

## Running Each Technique Well

**Blindspot brief.** Teach the user enough to prompt well, grounded in their
stated starting point — not a generic tutorial. Cover: how the domain actually
works, what "good" looks like and how experts judge it, the landmines and
common failure points, relevant prior art, the questions an expert would ask
about this specific task, and the vocabulary the user was missing. End with a
suggested re-prompt written in that new vocabulary.

**Option map.** Explore the territory first — search the codebase, files, or
the web; never brainstorm from a blank page. Then lay out 5–10 candidate
directions ordered from cheapest to most ambitious, each with one line on what
it costs and which unknown it resolves. The user's reactions are the real
output: capture each accept or reject as a scope statement in their words.

**Throwaway variants.** Two or three wildly different concrete versions —
mockups, strawman documents, sample plans — with no wiring, no persistence, no
polish, labeled as throwaway. After the user reacts, verbalize what each
reaction reveals as one sentence and fold those sentences into the spec. If
the user cannot judge which variant is better, stop: they don't know what
"good" looks like yet, so switch to a blindspot brief.

**Mini-interview.** At most 7 questions, each with concrete options and a
recommended default. Prioritize answers that would change the direction or are
costly to reverse. Never ask for a fact you can discover by inspection or
search. "I don't know" is an answer: record it as an open item with a
decide-later rule, never as consent.

**Reference request.** Ask for one reference. For code, source beats prose
beats screenshots — point at the folder and say what to look for. For other
domains, a concrete example (a portfolio, paper, video, contract document, a
finished game) beats any description. Extract the transferable ideas, state
them back, and confirm before treating them as decisions.

## How The Result Gets Verified

**Executable work** — tests, builds, renders, or measurable outcomes can
verify the result. Order the launch brief plan with the decisions most likely
to change first: data models, interfaces, user-facing flows; put mechanical
work at the bottom. During execution keep `implementation-notes.md`.

**Comprehension-checked work** — strategies, plans, decisions, or any result
the user cannot test directly. The user's own understanding is what accepts
the result. Order the plan by how hard each decision is to undo, hardest
first. During execution keep `decision-log.md`. Before the irreversible step —
committing money, sending the application, adopting the plan, merging —
deliver a short explainer plus a quiz the user must pass. Quiz questions are
scenario-based ("what happens to X if Y"), not recall, and must cover every
logged deviation and every decision the user did not make personally.

Deviation entries in either notes file use four fields: what the plan said →
what reality revealed → the conservative choice taken → when to revisit.

## When Not To Run This

- A domain-specific skill that covers the territory wins over these generic
  techniques; run the pass only for sub-areas it does not cover.
- Sustained multi-round discovery the user explicitly wants belongs to a
  dedicated interview workflow, not this pass.
- When the unknowns are already resolved and only a difficult judgment call
  remains, that is decision synthesis, not an unknowns pass.
- Skip entirely for small or mechanical edits, well-specified work, or when
  the user says "just do it."

## Launch Brief

Fill `assets/launch-brief.template.md`. The brief must let a fresh session
execute without rereading this conversation: starting point, confirmed
decisions with rationale, resolved unknowns with evidence, open items with
decide-later rules, the ordered plan, the notes-file instruction, and the
acceptance criteria. Return it in chat by default; write a file when the user
asks or when it will seed a new session.

## Gotchas

- Do not run several techniques in parallel or preemptively; the value is in
  picking the single cheapest one.
- Do not let a blindspot brief become an unanchored lecture; every section
  must change how the user would prompt this task.
- Do not polish throwaway variants or wire them into real systems.
- Do not convert your recommended defaults into user decisions; unanswered
  items stay open.
- Do not start executing the plan in the same pass without explicit
  authorization.
