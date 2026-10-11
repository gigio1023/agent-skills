# Interview Method

Use this reference when the core workflow needs a more precise root, round shape, question lens, or closure audit.

## Contents

1. Root by work type
2. Opening modes
3. Decision tree and frontier
4. Ambiguity ledger
5. Routing facts, investigations, and decisions
6. Writing a round
7. Pressure
8. Milestones and closure
9. Worked shapes

## 1. Root by Work Type

The root is the set of decisions every other answer depends on. Pick it from the work type before the first round.

| Work type | Usual root | Ask when it changes the result |
| --- | --- | --- |
| System or infrastructure change | Goal, binding constraints, failure model, result that would change direction | Deployment, inputs, permissions, failure cost, migration window |
| Research direction or study | Question and the decision it informs, result that would change direction, data and compute limits | Baselines, datasets, evaluation conditions |
| Security or safety work | Protected assets and boundary, threat model, acceptable residual risk, result that would change direction | Deployment, permissions, inputs reaching the boundary, cost of a miss versus a false alarm |
| Product feature | Who uses it, in which situation, outcome it should change | Screens, flows, edge cases |
| Plan, rollout, or process change | Outcome, what must not break, decision owner, reversibility | Sequencing, rollback triggers, communication |
| Personal or organizational decision | Objective, options actually on the table, what would rule an option out | Timing, cost, who else is affected |

Usage scenes and screens are roots only for user-facing products. For other work they hang off the goal and failure model, if they matter at all. When the work type is unclear, ask it in the first round alongside the goal.

## 2. Opening Modes

### Sparse context: root round

Do not open with a questionnaire covering everything conceivable. Open with the root decisions for the work type plus any independent consequential decision already on the frontier. Section 6 shows a root round for a systems change.

### Rich context: inverted interview

When the conversation, brief, or repository already contains substantial context, synthesize before questioning. Keep the synthesis short enough to audit:

1. **Confirmed facts:** directly supported by the user or evidence.
2. **Inferred assumptions:** plausible, but not accepted.
3. **Unresolved ambiguities:** missing facts or conflicting interpretations.
4. **Human-only decisions:** scope, priority, policy, preference, or tradeoff.

The human-only decisions on the frontier become the first round, each in the standard question shape. Close the round with one line inviting correction: "If any numbered fact or assumption is wrong in a way that would change the result, say which." This prevents blank-slate questions and detects intent drift before drilling down.

### Brownfield: evidence-backed interview

Inspect the smallest relevant repository surface first: governing instructions, nearby docs, public interfaces, current behavior, tests, and analogous code. Ask a decision only when evidence leaves a real branch, and put the evidence in the question's reason line:

> `[from-code]` The existing import path retries network failures but treats validation failures as final. For the new batch path, should a validation failure reject the whole batch, or should valid items commit with an error report for the rest?

Avoid "How does the importer work?" when the code can answer it.

## 3. Decision Tree and Frontier

Build the tree from open decisions, not from a topic outline. A decision is a child of another when the right answer depends on how the parent is settled: canary percentages depend on whether the rollout uses a canary at all. Independent decisions are siblings and can share a round.

For each round:

1. Drop decisions already answered by the conversation, repository, or earlier rounds.
2. Mark what each remaining decision waits on. Decisions that wait on nothing still open form the frontier.
3. Move facts to inspection and empirical questions to the investigation list.
4. Keep the consequential frontier decisions and order them by impact.
5. Ask the round and wait.

After the answers, settled decisions unblock their children and can make whole branches moot: choosing no canary removes the canary-percentage questions. An answer that contradicts an earlier one reopens only the affected branch. Children of a decide-later decision stay open items unless the user adopts an explicit working assumption for the parent; questions asked under that assumption carry the label.

A pending fact lookup removes only its downstream decisions from the frontier. The tree stays internal; show the user the round and, when useful, which later questions an answer unlocks ("Q1 decides whether Q4 and Q5 come up at all").

Source note: the design-tree and frontier framing is adapted from the `grilling` skill in [mattpocock/skills at 49dd158](https://github.com/mattpocock/skills/tree/49dd158/skills/productivity/grilling) (MIT License, Copyright (c) 2026 Matt Pocock), rewritten here; the [harness source notes](harness-source-notes.md) record what this skill changed.

## 4. Ambiguity Ledger

Maintain the ledger internally and show the smallest useful slice when it helps the user correct the record.

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
| Investigations | Each empirical question has a settling check and a route |
| Open decisions | Each blocker or deferral has an owner, impact, and decide-later rule |

Do not force every interview to fill every conceivable track. A track is material only if its answer could change the brief or the next authorized step.

## 5. Routing Facts, Investigations, and Decisions

Classify the needed information before composing a question.

| Class | Action | Example |
| --- | --- | --- |
| Discoverable fact | Inspect and record | Current API shape, file path, existing test |
| Conflicting fact | Show evidence; ask which meaning governs | Docs promise A; code does B |
| External fact | Research when current and material | Current platform limit or standard |
| Empirical question | Record an investigation item and route it | Throughput under peak load, accuracy after quantization |
| Human decision | Ask | Priority, policy, scope, acceptable failure |
| Mixed | State facts, then ask the decision | Existing retry behavior plus desired new rule |

An investigation item records the question, what would settle it (the measurement, trial, or experiment and its rough cost), the decisions waiting on it, the route (`ml-experiment`, `evaluation-design`, or the experiment queue of the plan or design document (`design-doc`)), and the user's rule for each plausible outcome when they gave one.

Descriptive evidence never decides a prescriptive question by itself. Existing code can show the current pattern; only the user or delegated authority decides whether that pattern should continue.

## 6. Writing a Round

A root round for a synthetic systems change, "add per-client rate limiting in front of an internal API gateway":

```markdown
Round 1. Root decisions; quotas and counter storage come after these.

**Q1. Primary goal.** Protecting backend capacity and enforcing fair use between clients lead to different limit keys and different behavior under load.
- A. Protect capacity: global and per-route limits, shed load under pressure.
- B. Fair use: per-client quotas, predictable rejections.
- C. Both, with capacity protection taking precedence.
Recommended: C (judgment call), because overload is the failure that takes every client down. Go with C?

**Q2. Behavior when the limiter itself fails.** Failing open keeps traffic flowing without protection; failing closed protects the backend but turns a limiter outage into an API outage.
- A. Fail open and alert.
- B. Fail closed.
Recommended: A (judgment call) for an internal gateway where availability matters more than strict quotas. Fail open and alert?

**Q3. Rule if the added latency is too high.** The added latency is an investigation item (load test under peak traffic), but what to do with the result is your decision.
- A. Switch to local approximate counters.
- B. Accept the latency.
Recommended: A (judgment call), because exact global counts are rarely needed for an internal limit. Use approximate counters if the budget is exceeded?

Not asked yet: per-client quota values (depend on Q1); counter storage (depends on Q2 and on what the gateway already runs, which I am checking).
```

Avoid:

- "Tell me more."
- unrelated decisions fused into one question;
- options that differ only in wording;
- a dependent question in the same round as its prerequisite;
- an implementation choice before intent and boundaries are clear;
- praise or filler that obscures the decisions.

## 7. Pressure

The first polished answer is not always the operational answer. For at least one material claim, choose one pressure move and put it in the next round, marked as a follow-up to the earlier answer:

- request a specific example or counterexample;
- ask what evidence would falsify the claim;
- expose the dependency that must remain true;
- force a choice between two desirable outcomes;
- name what must be excluded to preserve the priority;
- run a failure scenario through the proposed boundary;
- ask whether the stated solution addresses the root cause or only a symptom.

Do not keep pushing because discomfort itself looks productive. Stop a branch when the next answer would not alter scope, policy, verification, or execution.

## 8. Milestones and Closure

Use qualitative milestones rather than a synthetic score:

- **Initial:** the topic exists, but intent or outcome is still unstable.
- **Shaped:** intent, actors, and major boundaries are coherent.
- **Testable:** success, failure behavior, and verification are observable.
- **Ready:** the next authorized action is determined and no unresolved human-only blocker prevents it.

At a milestone transition, check from a lateral angle: what fact would change the recommendation, what is the smallest sufficient version, which boundary or dependency could make this infeasible, and which independent branch has received no pressure.

Ready does not require an empty frontier. Branches the next action does not touch go into the brief as open items with owner, impact, and decide-later rule, or as investigation items. Offer the one-sentence intent for confirmation unless the user already accepted the same material meaning. A correction reopens only the affected ledger tracks, not the whole interview.

## 9. Worked Shapes

### Refinement checkpoint

> I am recording your answer as: decision, retain existing customers during migration; rationale, continuity outweighs cleanup speed; constraint, no forced reauthentication; non-goal, redesigning account recovery. Is any part of that wrong or materially incomplete?

### Concrete failure question

> The unresolved boundary is partial success. If 99 records import and one is malformed, should the user receive 99 committed records plus an error report, or should the entire import remain unchanged?

### Decide-later capture

> I will mark the identity provider choice as decide later, owned by the security lead, with the impact that the rollout cannot enter production until it is settled. Is that the correct boundary for the brief?

### Investigation item capture

> Whether the nightly batch finishes inside the maintenance window is a measurement, not a decision, so I am listing it as an investigation item: a timed run on a copy of last month's data, routed to the plan's experiment queue. Your rule if it overruns was to split the batch by region.

### Final confirmation

> One-sentence intent: "Enable support staff to correct customer addresses in one audited workflow without broad account-edit permissions." Does this state the outcome you want the next agent to preserve?
