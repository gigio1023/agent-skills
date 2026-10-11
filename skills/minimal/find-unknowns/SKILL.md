---
name: find-unknowns
description: >
  Use when the user starts substantial work in territory they don't know well:
  a new project, research direction, investment or money-management strategy,
  career or life plan, product or game idea, or an unfamiliar part of a
  codebase, with no spec, plan, or reference yet; or when they ask for an
  unknowns pass, blind spot pass, option map, throwaway variants, or a launch
  brief. Uses bounded, adaptive discovery, compresses what
  was learned into a launch brief, and, when the user cannot test the result
  directly, explains consequential decisions and offers a comprehension check.
  NOT for well-specified or small tasks, multi-round
  Socratic discovery (use deep-interview), final decision synthesis (left to
  the agent's own judgment), or packaging session state (use session-handoff).
---

# Find Unknowns

Surface consequential unknowns before expensive work starts. Begin with the cheapest useful technique and adapt to what it reveals within the same objective and authorized resources. Finish with a launch brief, then continue any next action the user has already authorized. A brief does not create new authority.

## Quick Start

1. Establish the starting point. Inspect available files, repository context, and prior artifacts before asking for facts. If the user's familiarity with the domain is unclear, make the brief self-contained. Ask only when familiarity changes a material decision or the useful discovery technique.
2. Choose a technique for the consequential unknown:

   | Dominant unknown | Signal | Technique |
   | --- | --- | --- |
   | Unknown unknowns | New domain; doesn't know what to ask or what "good" looks like | Blindspot brief |
   | Unsettled scope or direction | "Something in this area"; competing ways to attack | Option map |
   | Unknown knowns (taste) | "I'll know it when I see it" | Throwaway variants |
   | Known unknowns | Nameable open questions | Mini-interview |
   | Inexpressible want | Can't describe it, but an example exists somewhere | Reference request |

3. Use the result to decide whether another short technique or check would change the next decision. Switch or combine techniques within the same objective and grant without a new approval. Ask before changing direction, exceeding resources or access, taking a new external action, or starting a long new activity unless already authorized.
4. Identify evidence that can verify the result and the consequences the user needs to understand. Use that to order the next useful work.
5. Compress the useful findings and open decisions into a launch brief. Adapt [the template](assets/launch-brief.template.md) when it helps; its headings and tables are optional.

Keep discovery proportional to the decision. Choose enough questions, examples, or artifacts to expose meaningful differences, and stop when another small check would no longer change the next action. If the remaining work needs sustained interviewing or a substantial investigation, describe that need without silently expanding the pass.

## Running Each Technique Well

**Blindspot brief.** Teach what changes the user's choices for this task: how the domain works, how experts judge results, relevant failure points and prior art, and missing vocabulary. Ground the explanation in the user's starting point. Suggest a revised prompt when it would make the next request more precise.

**Option map.** Inspect relevant code, files, or sources before proposing directions. Compare materially different options by the tradeoffs that affect the decision, including cost and the unknown each resolves. Keep the set small enough to compare without omitting a consequential alternative. Capture the user's accepted and rejected options as scope decisions in their words.

**Throwaway variants.** Make concrete alternatives that expose the uncertain choice, such as mockups, strawman documents, or sample plans. Label them as throwaway and label synthetic data. Choose a comparison format the user can judge easily; polish and production wiring add little to this decision. Save artifacts only within the task's file authority. Capture preferences the user's reactions actually establish. If comparison criteria remain unclear, use a short explanation or reference comparison to establish them.

**Mini-interview.** Ask only questions whose answers could change the next work or a costly decision. Give concrete options and a recommended default when useful. Never ask for a fact available through inspection or search. Separate user choices from empirical uncertainty: a cheap authorized check can resolve the latter; an experiment needing new resources belongs in the next bounded work proposal. "I don't know" leaves an open item with a decide-later rule, never consent. When user-only choices need sustained conversation, offer `deep-interview` and let the user choose that expansion.

**Reference request.** Reuse an available example before asking for another. Prefer inspectable source for code and a concrete artifact for other domains, such as a portfolio, paper, video, contract, or finished game. Explain the transferable features. Distinguish observed features and proposed choices from decisions the user has made.

## How The Result Gets Verified

**Directly testable work.** Identify tests, builds, renders, source checks, or measured outcomes that can establish the result. Order work around the uncertainties most likely to change the next decision while respecting real dependencies.

**Work the user cannot test directly.** Explain the evidence, consequences, and unresolved decisions behind a strategy or recommendation. Put consequential uncertainty before costly commitments. Offer a scenario-based comprehension check when useful or requested. Understanding does not establish factual correctness or replace permission or professional review. An optional comprehension check does not block an already-authorized action.

Keep consequential findings and changed decisions in the project's existing records when record maintenance is authorized. Record the evidence, what changed, and any condition for revisiting it. A discovery pass does not require a new notes file or a fixed deviation format.

## When Not To Run This

- A domain-specific skill that covers the territory wins over these generic techniques; run the pass only for sub-areas it does not cover.
- Sustained multi-round discovery the user explicitly wants belongs to `deep-interview`, not this pass.
- When the unknowns are already resolved and only a difficult judgment call remains, that is decision synthesis, not an unknowns pass.
- Skip entirely for small or mechanical edits, well-specified work, or when the user says "just do it."

## Launch Brief

The brief carries what the next action needs: the objective and limits, relevant starting point, confirmed decisions with rationale, findings with evidence, consequential open items, and the next useful action with its acceptance criteria. Use the format that makes those facts clear. Return it in chat by default; write a file when the user asks. Preparing for a possible new session alone does not authorize a file.

Continue the next action when it is already authorized. If the user requests a plan file, use `gigio-write-plan` and the existing brief without another discovery round. If the user requests durable project setup, use `gigio-project-setup`. A missing PROJECT.md does not trigger setup, and accepting a brief does not require either skill.

Plan only far enough to reach the next useful decision. Unresolved empirical questions can be the work; unresolved user choices block only the work that depends on them.

## Gotchas

- Do not let a blindspot brief become an unanchored lecture; every section must change how the user would prompt this task.
- Do not polish throwaway variants or wire them into real systems.
- Do not convert your recommended defaults into user decisions; unanswered items stay open.
