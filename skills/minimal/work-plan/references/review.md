# Review Mode

Judge work against the user's purpose and actual findings, not only the original task list. A correct implementation may leave the question unanswered; a review without a code change may substantially advance it.

## Establish the question and state

Read the user's goal, project direction, current plan, accepted changes, and actual results. Inspect the underlying sources, data, configurations, run records, or artifacts that support the claims; worker reports and run summaries are claims to verify. Distinguish the current result from an older attempt and an approved change from an agent proposal.

Prefer an independent reader when one is available; `review-panel` runs separate reviewers and judges their findings by evidence. An explicit user choice about delegation governs; without one, the lead decides whether to start that reader. If this session did the work, do not present its inspection as independent review. Provide the useful review possible now and identify any consequential gap in independence without a blanket refusal.

## Check what the work establishes

Assess the result at the level the work needs:

- **Implementation:** does the changed behavior serve the objective, and does a real run on fixed input or a test the project keeps show it?
- **Research or experiment:** what explanations does the result support or rule out, are comparisons meaningful, and what remains unresolved?
- **Data or benchmark:** do actual cases, labels, splits, metrics, and scoring behavior support the intended use?
- **Document or decision:** can the reader understand and assess the conclusion with the available explanation and sources?

Use research, evaluation, or implementation skills for method-specific review. Project review coordinates the judgment; it does not define another statistical or benchmark methodology.

Inspect recorded results before rerunning expensive work. Reuse valid outputs when identity and conditions match, and report results obtained from a substitute input as such rather than as the named input's results. Review does not itself authorize paid experiments or external writes. Re-run relevant inexpensive checks when useful. An unavailable or unperformed check is not a failure of the hypothesis.

## Reconcile the plan with learning

Compare what was requested, done, and learned. Report missing work, unrequested expansion, misunderstood intent, unsupported claims, and accepted plan changes only where they occur. A new finding can make an old task unnecessary. Do not call an approved or in-scope adaptive change a defect merely because it differs from the original list.

A negative finding can meet a research objective. An inconclusive result may complete the bounded investigation while leaving the broader decision open. Explain what prevents the stronger conclusion and whether further work is worth proposing.

Keep empirical findings separate from user-owned goals. Work relying on an unconfirmed material proposal stays visibly unconfirmed: name the proposal, the work resting on it, and the question that would settle it.

## Direction findings

Direction problems should reach the user when they appear, during execution as well as here. A review that finds one, or finds one recorded but not yet decided, describes the observation and the proposed change and requests the user's decision before further work follows it. When several are open, the review may summarize them together; it is not the only place they surface. Work built as planned whose result still misses the goal is a direction finding, not rework.

## Deliver and connect

Lead with whether the work supports the intended next decision and the material findings behind that assessment. Name sources or artifacts precisely enough to check; omit empty categories and routine verification narration.

Recommend the next bounded action, correction, or decision. Update project understanding and the plan only when the review includes those updates or closure. A review-only request returns findings. Continue an already-requested correction or publication through its appropriate skill without asking for the same grant again.

Use [worked review cases](review-cases.md) when a non-code outcome, an unconfirmed proposal, or a changed plan makes completion ambiguous. They are synthetic examples, not measured model results.
