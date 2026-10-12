# Interview Method

Use this reference when the core workflow needs a more precise root, starting point, blind-spot scan, recognition question, round shape, question lens, or closure audit.

## Contents

1. Root by work type
2. Starting point and blind-spot scan
3. Opening modes
4. Decision tree and frontier
5. Ambiguity ledger
6. Routing facts, investigations, and decisions
7. Recognition questions for unknown knowns
8. Writing a round
9. Pressure
10. Milestones and closure
11. Worked shapes

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

## 2. Starting Point and Blind-Spot Scan

### Starting point

The user's position decides how wide the scan goes and how much each question explains. Read it from the request and context before asking.

| Signal | Likely position | Effect on the interview |
| --- | --- | --- |
| A hunch in a sentence, no artifacts | Exploring | Wider scan, root round, terms of art defined |
| A draft plan or design | Shaping | Inverted opening, scan for what the draft omits |
| A near-final plan, "check before I start" | Committing | Scan weighted to irreversible steps, short rounds |
| New to the field or codebase | Novice | Standard pitfalls and achievable options lead the findings |
| Long practice in the field | Expert | Only what the stated plan misses, no tutorial |

State an inferred position in one line at the top of the first round so the user can correct it, as section 8 shows. Ask before the first round only when the position is unclear and would change that round, in one short message that also invites notes, earlier attempts, or references: what the user already knows and has tried is context the scan should not repeat back.

### Blind-spot scan

The scan applies the find-unknowns lens to the root, so the first round can carry what the user has not considered alongside what they know is open. Name the field and the class of effort, recall how comparable efforts went and failed, run a quick premortem, and sweep each dimension, dismissing quickly the ones that plainly do not apply:

- the goal behind the request and what would make a correct-looking result useless;
- constraints the request does not state: deadlines, budgets, access, compatibility, policy;
- affected people whose incentives differ from the user's;
- failure modes and the worst plausible case;
- cost, irreversibility, and order of steps;
- second-order effects downstream;
- assumptions the user and the agent share;
- the checks an experienced practitioner runs first;
- what is achievable: options, tools, or results the user may not know exist, and limits that put an expected result out of reach.

Report the findings that change the result, not the coverage. Section 8 shows them opening a round. When `find-unknowns` is installed, its method holds the full sweep; the interview applies it as a lens and writes no separate launch brief.

When an answer opens territory the first scan did not cover, run the same sweep on that territory only, before recomputing the frontier. In the rate-limiting round of section 8, an answer revealing that some clients are external partners under contract opens new territory: contractual rate commitments, how a rejection reaches a partner, and who approves a quota change.

Source note: the four kinds of unknowns, the blind-spot pass that starts from the user's own context, and recognition through options, references, and prototypes are adapted from Thariq Shihipar, ["A field guide to Claude Fable 5: Finding your unknowns"](https://claude.com/resources/articles/a-field-guide-to-claude-fable-finding-your-unknowns) (Anthropic, 2026-07-06), rewritten here; the [harness source notes](harness-source-notes.md#unknowns-revision-2026-10-12) record what this skill changed.

## 3. Opening Modes

### Sparse context: root round

Do not open with a questionnaire covering everything conceivable. Open with the scan's consequential findings, then the root decisions for the work type plus any independent consequential decision already on the frontier. Section 8 shows a root round for a systems change.

### Rich context: inverted interview

When the conversation, brief, or repository already contains substantial context, synthesize before questioning. Keep the synthesis short enough to audit:

1. **Confirmed facts:** directly supported by the user or evidence.
2. **Inferred assumptions:** plausible, but not accepted.
3. **Unresolved ambiguities:** missing facts or conflicting interpretations.
4. **Human-only decisions:** scope, priority, policy, preference, or tradeoff.

The scan's consequential findings follow the synthesis as things the user may not have considered. The human-only decisions on the frontier, including any a finding raised, become the first round, each in the standard question shape. Close the round with one line inviting correction: "If any numbered fact or assumption is wrong in a way that would change the result, say which." This prevents blank-slate questions and detects intent drift before drilling down.

### Brownfield: evidence-backed interview

Inspect the smallest relevant repository surface first: governing instructions, nearby docs, public interfaces, current behavior, tests, and analogous code. Ask a decision only when evidence leaves a real branch, and put the evidence in the question's reason line:

> `[from-code]` The existing import path retries network failures but treats validation failures as final. For the new batch path, should a validation failure reject the whole batch, or should valid items commit with an error report for the rest?

Avoid "How does the importer work?" when the code can answer it.

## 4. Decision Tree and Frontier

Build the tree from open decisions, not from a topic outline. A decision is a child of another when the right answer depends on how the parent is settled: canary percentages depend on whether the rollout uses a canary at all. Independent decisions are siblings and can share a round.

For each round:

1. Drop decisions already answered by the conversation, repository, or earlier rounds.
2. Mark what each remaining decision waits on. Decisions that wait on nothing still open form the frontier.
3. Move facts to inspection and empirical questions to the investigation list.
4. Keep the consequential frontier decisions and order them by impact.
5. Ask the round and wait.

After the answers, rescan any territory they opened (section 2), then let settled decisions unblock their children; they can make whole branches moot: choosing no canary removes the canary-percentage questions. An answer that contradicts an earlier one reopens only the affected branch. Children of a decide-later decision stay open items unless the user adopts an explicit working assumption for the parent; questions asked under that assumption carry the label.

A pending fact lookup removes only its downstream decisions from the frontier. The tree stays internal; show the user the round and, when useful, which later questions an answer unlocks ("Q1 decides whether Q4 and Q5 come up at all").

Source note: the design-tree and frontier framing is adapted from the `grilling` skill in [mattpocock/skills at 49dd158](https://github.com/mattpocock/skills/tree/49dd158/skills/productivity/grilling) (MIT License, Copyright (c) 2026 Matt Pocock), rewritten here; the [harness source notes](harness-source-notes.md) record what this skill changed.

## 5. Ambiguity Ledger

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
| Tacit criteria | Each criterion the user recognizes on sight was shown and chosen, or is listed as still to be recognized |
| Blind spots | The territory the next action touches was scanned, including territory answers opened, with limits recorded |
| Investigations | Each empirical question has a settling check and a route |
| Open decisions | Each blocker or deferral has an owner, impact, and decide-later rule |

Do not force every interview to fill every conceivable track. A track is material only if its answer could change the brief or the next authorized step.

## 6. Routing Facts, Investigations, and Decisions

Classify the needed information before composing a question.

| Class | Action | Example |
| --- | --- | --- |
| Discoverable fact | Inspect and record | Current API shape, file path, existing test |
| Conflicting fact | Show evidence; ask which meaning governs | Docs promise A; code does B |
| External fact | Research when current and material | Current platform limit or standard |
| Empirical question | Record an investigation item and route it | Throughput under peak load, accuracy after quantization |
| Human decision | Ask | Priority, policy, scope, acceptable failure |
| Tacit criterion | Show options or a reference; ask which | Report format, naming style, level of detail |
| Mixed | State facts, then ask the decision | Existing retry behavior plus desired new rule |

An investigation item records the question, what would settle it (the measurement, trial, or experiment and its rough cost), the decisions waiting on it, the route (`ml-experiment`, `evaluation-design`, a next action in the plan (`work-plan`), or the experiment queue of the design document (`design-doc`)), and the user's rule for each plausible outcome when they gave one.

Descriptive evidence never decides a prescriptive question by itself. Existing code can show the current pattern; only the user or delegated authority decides whether that pattern should continue.

## 7. Recognition Questions for Unknown Knowns

A criterion is probably tacit when the user says they will know it when they see it, answers with adjectives such as "clean" or "not too much", or rejects results without saying why, and when it concerns a format, layout, tone, naming style, or level of detail. Asking for a description then produces an answer the user did not mean. Ask for recognition instead, cheapest first:

1. **Reference.** Point to existing code or artifacts in the repository that already embody a candidate, such as a module's error messages or an earlier report, and ask whether it is the model. For code work, source code is the strongest reference, because it carries details nobody would think to state.
2. **Samples in the round.** Write two to four short options that differ on the uncertain criterion and as little else as possible, small enough to judge in seconds. Label synthetic data.
3. **Runnable prototype or variant.** Use one only when samples cannot show the criterion, as with interaction, timing, or a rendered layout, and only with the user's consent; offer it with its cost and the question it settles. When `find-unknowns` is installed, its throwaway-variant rules apply.

A recognition question keeps the standard shape:

```markdown
**Q4. Shape of the nightly build-time report.** You said you would know it when you see it, so here are three samples on the same synthetic data.
- A. One line per target, slowest first: `//svc/api  142s  +38s vs main`
- B. Grouped by package with a subtotal, regressions marked
- C. JSON lines for a dashboard, no text view
Recommended: A (judgment call), because the usual reader scans for the one regression. Closest to A? If a report already in the repository looks right, point me at it instead.
```

Record what the reaction establishes in the user's words, including what was wrong with the rejected options, and do not generalize beyond it. If the user cannot choose, the criterion may be undecided rather than tacit: ask what the result is for or who reads it, then show options against that purpose. A criterion still unrecognized at closure goes into the brief with what would be shown next.

## 8. Writing a Round

A root round for a synthetic systems change, "add per-client rate limiting in front of an internal API gateway":

```markdown
Assumed starting point: you know the gateway well and have not run a limiter in front of it. Correct me if not.

Things you may not have considered:
- Clients that retry on rejection without backoff turn a limit into a burst of retries. I would return a retry-after hint; I am reading how the client libraries retry.
- The gateway release in the repository may already include a rate-limiting module, which would make this configuration rather than new code. I am checking.
- Scheduled jobs that share one client identity would hit a per-client limit together on the hour. Q1 decides whether that matters.

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

## 9. Pressure

The first polished answer is not always the operational answer. For at least one material claim, choose one pressure move and put it in the next round, marked as a follow-up to the earlier answer:

- request a specific example or counterexample;
- ask what evidence would falsify the claim;
- expose the dependency that must remain true;
- force a choice between two desirable outcomes;
- name what must be excluded to preserve the priority;
- run a failure scenario through the proposed boundary;
- ask whether the stated solution addresses the root cause or only a symptom.

Do not keep pushing because discomfort itself looks productive. Stop a branch when the next answer would not alter scope, policy, verification, or execution.

## 10. Milestones and Closure

Use qualitative milestones rather than a synthetic score:

- **Initial:** the topic exists, but intent or outcome is still unstable.
- **Shaped:** intent, actors, and major boundaries are coherent.
- **Testable:** success, failure behavior, and verification are observable.
- **Ready:** the next authorized action is determined and no unresolved human-only blocker prevents it.

At a milestone transition, check from a lateral angle: what fact would change the recommendation, what is the smallest sufficient version, which boundary or dependency could make this infeasible, which independent branch has received no pressure, and which territory the answers opened has not been scanned.

Ready does not require an empty frontier. Branches the next action does not touch go into the brief as open items with owner, impact, and decide-later rule, or as investigation items; tacit criteria not yet recognized go in with what would be shown next. Offer the one-sentence intent for confirmation unless the user already accepted the same material meaning. A correction reopens only the affected ledger tracks, not the whole interview.

## 11. Worked Shapes

### Refinement checkpoint

> I am recording your answer as: decision, retain existing customers during migration; rationale, continuity outweighs cleanup speed; constraint, no forced reauthentication; non-goal, redesigning account recovery. Is any part of that wrong or materially incomplete?

### Concrete failure question

> The unresolved boundary is partial success. If 99 records import and one is malformed, should the user receive 99 committed records plus an error report, or should the entire import remain unchanged?

### Decide-later capture

> I will mark the identity provider choice as decide later, owned by the security lead, with the impact that the rollout cannot enter production until it is settled. Is that the correct boundary for the brief?

### Investigation item capture

> Whether the nightly batch finishes inside the maintenance window is a measurement, not a decision, so I am listing it as an investigation item: a timed run on a copy of last month's data, routed to the plan as a next action. Your rule if it overruns was to split the batch by region.

### Still-to-recognize capture

> The column set for the build-time report is still to be recognized: you rejected B and C, and A was close but not right. I am listing it with the next step of two variants of A on last week's data; it blocks only the report template. Is that the right boundary?

### Final confirmation

> One-sentence intent: "Enable support staff to correct customer addresses in one audited workflow without broad account-edit permissions." Does this state the outcome you want the next agent to preserve?
