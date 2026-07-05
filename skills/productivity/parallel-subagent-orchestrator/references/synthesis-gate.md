# Synthesis Gate

Use this before presenting a result from parallel work.

## Merge Claims, Not Summaries

Build the answer from claims and evidence:

| Claim | Source / agent | Evidence type | Confidence | Caveat | Action |
|-------|----------------|---------------|------------|--------|--------|
| What appears true | Where it came from | Direct / inferred / opinion | High / medium / low | What could break it | Use / verify / reject |

Do not paste each subagent's summary in sequence. That preserves labor, not
judgment.

## Conflict Handling

When agents disagree:

1. Check whether they answered the same question. Apparent conflicts often come
   from different scopes, dates, versions, or assumptions.
2. Prefer primary sources, executable evidence, and direct inspection over
   community repetition.
3. If both sides have evidence, state the conflict and decide what would resolve
   it.
4. Launch a follow-up wave only if the conflict affects the final decision.

## Gap Scan

Before finalizing, ask:

- Did every important branch of the user's question receive coverage?
- Are any claims unsupported by a source, file, test, or explicit inference?
- Did all subagents share the same hidden premise?
- Is there a missing stakeholder, time horizon, or risk lens?
- Would a second wave likely change the answer enough to justify cost?

## Follow-Up Wave Criteria

Launch another wave when:

- A high-impact conflict remains unresolved.
- A source-of-truth was not inspected.
- The result depends on current facts that were not checked.
- Implementation workers exposed an integration risk.
- A reviewer found a material issue and a bounded owner can fix it.

Do not launch another wave when:

- Remaining uncertainty is low impact.
- The user asked for a quick answer.
- The missing information is unknowable from available tools.
- More agents would duplicate the same search path.

## Final Output Shape

For research and judgment:

- Recommendation or answer first.
- Evidence that actually moved the decision.
- Major caveats and uncertainty.
- What was delegated and how results were synthesized.

For coding:

- What changed.
- Which worker or lane owned which area, if relevant.
- Verification performed.
- Remaining risk or tests not run.

For plans:

- Proposed decomposition.
- Dependencies and ordering.
- What should be parallel and what should stay sequential.
