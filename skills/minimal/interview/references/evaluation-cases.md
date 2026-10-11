# Evaluation Cases

Use the same prompts with and without the candidate skill. Hold model, harness, tools, effort, and evaluator fixed. A behavioral edit passes only if it improves the positive cases without triggering on the negatives.

## Positive Cases

1. **Sparse product idea**
   - Prompt: "Interview me about a local-first expense tracker before we plan or build anything."
   - Expect: a first round on product roots (who uses it, in which situation, what outcome should change), each question with why it matters, options, and a recommended default; no dependent question such as sync technology before multi-device scope is settled; no implementation.
2. **Rich prior context**
   - Prompt: "These notes already contain my product decisions. Interview me without making me repeat what is settled: `notes/product-brief.md`."
   - Expect: inspect first, give a numbered synthesis of facts, assumptions, ambiguities, and human-only decisions, then one round of the frontier human-only decisions plus an invitation to correct any numbered item; nothing already settled is re-asked.
3. **Brownfield rollout grilling**
   - Prompt: "Grill me on the rollout plan for this repository and find hidden assumptions before I hand it to another agent."
   - Expect: inspect repository evidence first; the first round batches the independent consequential decisions (for example rollout goal, tolerated blast radius, rollback trigger), each citing evidence, why it matters, options, and a default; dependent decisions (for example canary percentages before deciding whether to canary) wait for a later round; facts the repository answers are not asked; empirical questions such as whether a migration fits its window are recorded as investigation items; verification and failure behavior are tracked.
4. **Systems root**
   - Prompt: "Interview me about adding per-client rate limiting to our internal API gateway before I write the design doc."
   - Expect: the root round covers goal, binding constraints, failure behavior, and which result would change direction; no end-user usage scenes or screens; latency or throughput unknowns become investigation items with the user asked only for the rule to apply to each outcome.
5. **Explicit serial request**
   - Prompt: "Interview me about my thesis topic, one question at a time; I want to think through each answer."
   - Expect: exactly one question per turn, still with why it matters, options, and a default, choosing the highest-impact frontier question each turn.
6. **Early stop**
   - Prompt after two rounds: "Stop here and summarize what we have."
   - Expect: stop immediately, produce a partial brief, label open decisions with their impact and decide-later rule, and do not demand more answers.

## Near-Miss Negatives

1. "Run a mock behavioral job interview and score my answers."
   - Expect: do not activate; this is candidate rehearsal.
2. "Summarize this conversation into a spec. Do not ask me questions."
   - Expect: do not activate; honor the no-question instruction and route to a documentation or handoff workflow.
3. "Before I start this migration, do a quick blind-spot pass."
   - Expect: do not activate; this is a light unknowns pass (`find-unknowns`).
4. "Here is my idea for caching query results at the edge. Tear it apart."
   - Expect: do not activate; this asks for objections to one stated idea (`idea-critique`), not questions to the user.
5. "Write the plan for the next step of this migration."
   - Expect: do not activate; this is plan writing (`work-plan`).

## Rubric

Score each positive case from 0 to 2 on each item:

- chooses the root from the work type and the correct sparse, inverted, or brownfield opening;
- asks the independent consequential questions together with why, options, and a default, defers dependent questions, and goes serial only on explicit request;
- separates inspectable facts, investigation items, and user judgment;
- preserves provenance, uncertainty, skips, and contradictions, and never treats silence as consent;
- pressure-tests at least one material premise without tunnel vision;
- stops on user request and avoids unauthorized mutation;
- closes when the next authorized action is determined, with an accurate, user-confirmed Interview Brief that lists open items with decide-later rules.

Pass criteria: no zero on authority or on round structure, at least 11/14 on each positive case, and no negative case activates. Record baseline and candidate scores plus concrete failure excerpts outside the deployed skill.
