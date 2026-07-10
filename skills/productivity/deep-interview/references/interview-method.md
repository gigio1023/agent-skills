# Deep Interview Method

Use this reference when the core workflow needs a more precise opening,
question lens, or closure audit.

## Contents

1. Opening modes
2. Ambiguity ledger
3. Routing facts and decisions
4. Designing one strong question
5. Pressure and breadth
6. Milestones and closure
7. Worked turn shapes

## 1. Opening Modes

### Sparse context: Socratic discovery

Do not begin with a questionnaire. Identify the most consequential unknown and
ask one question that exposes it. Early questions normally establish the real
problem, desired change, or user who experiences it before implementation
detail.

Useful opening shape:

> The first branch is whether this is meant to change an observable outcome or
> mainly produce an artifact. What would be different in the world if this
> worked?

### Rich context: inverted interview

When the conversation, brief, or repository already contains substantial
context, synthesize before questioning. Keep the opening short enough to audit:

1. **Confirmed facts** — directly supported by the user or evidence.
2. **Inferred assumptions** — plausible, but not accepted.
3. **Unresolved ambiguities** — missing facts or conflicting interpretations.
4. **Human-only decisions** — scope, priority, policy, preference, or tradeoff.

Then ask one correction question, such as: “Which numbered item is wrong or
missing in a way that would change the result?” This prevents blank-slate
questions and detects intent drift before drilling down.

### Brownfield: evidence-backed interview

Inspect the smallest relevant repository surface first: governing instructions,
nearby docs, public interfaces, current behavior, tests, and analogous code.
Ask a confirmation or decision question only when evidence leaves a real branch.

Good shape:

> `[from-code]` The existing import path retries network failures but treats
> validation failures as final. For the new batch path, should partial validation
> failures reject the whole batch or preserve valid items?

Avoid “How does the importer work?” when the code can answer it.

## 2. Ambiguity Ledger

Maintain the ledger internally and show the smallest useful slice when it helps
the user correct the record.

| Track | Ready when |
| --- | --- |
| Intent and why now | The underlying change and urgency are explicit |
| Actors and audience | The affected people and brief consumer are named |
| Desired outcome | The end state or artifact is concrete |
| Current state | Relevant facts are grounded in evidence |
| Scope and non-goals | Included, excluded, and deferred work are explicit |
| Constraints | Time, compatibility, policy, budget, and quality limits are known |
| Authority | The user, agent, and other owners have clear decision boundaries |
| Success and verification | Observable checks distinguish done from plausible |
| Risks and failure behavior | Material adverse cases have an expected response |
| Open decisions | Each blocker or deferral has an owner and impact |

Do not force every interview to fill every conceivable category. A track is
material only if its answer could change the brief or the next authorized step.

## 3. Routing Facts and Decisions

Classify the needed information before composing a question.

| Class | Action | Example |
| --- | --- | --- |
| Discoverable fact | Inspect and record | Current API shape, file path, existing test |
| Conflicting fact | Show evidence and ask which meaning governs | Docs promise A; code does B |
| External fact | Research when current and material | Current platform limit or standard |
| Human decision | Ask | Priority, policy, scope, acceptable failure |
| Mixed | State facts, then ask one decision | Existing retry behavior plus desired new rule |

Descriptive evidence never decides a prescriptive question by itself. Existing
code can show the current pattern; only the user or delegated authority decides
whether that pattern should continue.

## 4. Designing One Strong Question

Select the next question using four factors:

1. **Materiality** — would a different answer change the outcome?
2. **Uncertainty** — is the current answer absent, vague, or contradictory?
3. **Dependency** — does this answer unlock several later decisions?
4. **Human necessity** — is user judgment actually required?

A strong question has one decision, a concrete frame, and visible stakes. When
options help, keep them neutral and mutually exclusive:

> This determines whether the first release optimizes learning or operational
> completeness. I recommend the single-team pilot (`judgment call`) because the
> success signal is still unproven. Should the first boundary be one team, one
> workflow across all teams, or a production-complete rollout?

Use `high` only for a recommendation strongly grounded in constraints or
evidence. Use `judgment call` when reasonable people could choose differently.
Use `your call` for taste, values, or risk appetite; do not anchor the answer.

Avoid:

- “Tell me more.”
- three unrelated questions in one turn;
- options that differ only in wording;
- an “other” option when a free-form answer is impossible to use;
- asking for an implementation choice before intent and boundaries are clear;
- praise or filler that obscures the next decision.

## 5. Pressure and Breadth

The first polished answer is not always the operational answer. For at least one
material claim, choose one pressure move:

- request a specific example or counterexample;
- ask what evidence would falsify the claim;
- expose the dependency that must remain true;
- force a choice between two desirable outcomes;
- name what must be excluded to preserve the priority;
- run a failure scenario through the proposed boundary;
- ask whether the stated solution addresses the root cause or only a symptom.

Do not keep pushing because discomfort itself looks productive. Stop a branch
when the next answer would not alter scope, policy, verification, or execution.

Track independent branches. After three consecutive questions on one branch,
compare it with untouched tracks. A deep answer about one component does not
make sibling components clear. Conversely, rotating after every answer produces
breadth without insight; pressure-test the active premise before moving on.

## 6. Milestones and Closure

Use qualitative milestones rather than a synthetic score:

- **Initial:** the topic exists, but intent or outcome is still unstable.
- **Shaped:** intent, actors, and major boundaries are coherent.
- **Testable:** success, failure behavior, and verification are observable.
- **Ready:** no unresolved human-only blocker prevents the next authorized step.

At a milestone transition, briefly inspect from a lateral perspective:

- researcher: what fact would change the recommendation?
- simplifier: what is the smallest sufficient version?
- architect: which boundary or dependency could make this infeasible?
- breadth keeper: which independent track has received no pressure?
- closer: what single remaining decision blocks a faithful brief?

At closure, use closer, skeptic, and gap-hunter lenses internally. Ask another
question only if it would materially change the brief. Then offer the
one-sentence goal for confirmation. A correction reopens only the affected
ledger tracks, not the whole interview.

## 7. Worked Turn Shapes

### Refinement checkpoint

> I am recording your answer as: decision — retain existing customers during
> migration; rationale — continuity outweighs cleanup speed; constraint — no
> forced reauthentication; non-goal — redesigning account recovery. Is any part
> of that representation wrong or materially incomplete?

### Concrete failure question

> The unresolved boundary is partial success. If 99 records import and one is
> malformed, should the user receive 99 committed records plus an error report,
> or should the entire import remain unchanged?

### Decide-later capture

> I will mark SSO provider choice as “decide later,” owned by the security lead,
> with the impact that rollout cannot enter production. Is that the correct
> boundary for the brief?

### Final confirmation

> One-sentence intent: “Enable support staff to correct customer addresses in
> one audited workflow without broad account-edit permissions.” Does this state
> the outcome you want the next agent to preserve?
