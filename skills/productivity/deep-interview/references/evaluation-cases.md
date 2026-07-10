# Evaluation Cases

Use the same prompts with and without the candidate skill. Hold model, harness,
tools, effort, and evaluator fixed. A behavioral edit passes only if it improves
the positive cases without triggering on the negatives.

## Positive Cases

1. **Sparse idea**
   - Prompt: “Interview me deeply about a local-first expense tracker before we
     plan or build anything.”
   - Expect: one outcome/root-problem question, no feature questionnaire, no
     implementation.
2. **Rich prior context**
   - Prompt: “These notes already contain my product decisions. Interview me
     without making me repeat what is settled: `notes/product-brief.md`.”
   - Expect: inspect first, synthesize facts/assumptions/ambiguities/decisions,
     then ask one correction question.
3. **Brownfield decision**
   - Prompt: “Grill me on the rollout plan for this repository and find hidden
     assumptions before I hand it to another agent.”
   - Expect: inspect repository evidence, ask only a human decision, cite the
     evidence, track verification and failure behavior.
4. **Early stop**
   - Prompt after two rounds: “Stop here and summarize what we have.”
   - Expect: stop immediately, produce a partial brief, label open decisions and
     their impact, do not demand more answers.

## Near-Miss Negatives

1. “Run a mock behavioral job interview and score my answers.”
   - Expect: do not activate; this is candidate rehearsal.
2. “Summarize this conversation into a spec. Do not ask me questions.”
   - Expect: do not activate; honor the no-question instruction and route to a
     documentation or handoff workflow.

## Rubric

Score each positive case from 0 to 2 on each item:

- chooses the correct sparse, inverted, or brownfield opening;
- asks exactly one material question per turn;
- separates inspectable facts from user judgment;
- preserves provenance, uncertainty, skips, and contradictions;
- pressure-tests at least one material premise without tunnel vision;
- stops on user request and avoids unauthorized mutation;
- closes with an accurate, user-confirmed Interview Brief.

Pass criteria: no zero on authority or one-question behavior, at least 11/14 on
each positive case, and neither negative case activates. Record baseline and
candidate scores plus concrete failure excerpts outside the deployed skill.
