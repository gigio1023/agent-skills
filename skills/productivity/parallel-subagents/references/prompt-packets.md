# Prompt Packets

Use these packet shapes when delegating. Adapt wording to the harness and task.

## Contents

- Research packet
- Value judgment packet
- Code exploration packet
- Code worker packet
- Review packet

## Research Packet

```text
Objective: Answer this specific question: <question>.

Scope: Inspect <source types / domains / repos / files>. Do not cover <excluded
scope> because another lane owns it.

Method: Prefer primary sources and direct inspection. Treat popularity as a weak
signal. Flag AI-slop, stale, or unsupported sources.

Output:
- Short answer
- Sources inspected
- Key claims with evidence
- Discarded/weak sources
- Confidence and caveats
- Follow-up questions that would materially change the answer

Stop when: You have inspected the assigned scope deeply enough to support or
reject the relevant claims.
```

## Value Judgment Packet

```text
Objective: Argue from the <advocate/skeptic/operator/outsider> lens for this
decision: <decision>.

Context: <facts, constraints, user preferences, time horizon>.

Scope: Focus on <lens-specific issues>. Do not attempt a final recommendation;
the lead agent will synthesize.

Output:
- Strongest argument from this lens
- Evidence or assumptions
- Failure modes / upside / opportunity cost
- What would change your view
- Confidence

Stop when: The assigned lens has a defensible argument, its decisive assumptions
are explicit, and further work is unlikely to change that argument materially.
```

## Code Exploration Packet

```text
Objective: Answer this codebase question: <question>.

Scope: Read <paths/modules>. Do not edit files.

Output:
- Direct answer
- Relevant files and line references
- Existing patterns to follow
- Risks or hidden contracts
- Suggested implementation boundary

Stop when: The codebase question is answered with direct file evidence, or a
specific missing dependency prevents a reliable answer.
```

## Code Worker Packet

```text
Objective: Implement <bounded change>.

Ownership: You own <files/modules>. Avoid touching <files/modules> unless
strictly necessary and report it.

Coordination: Other agents or the user may be editing the repo. Do not revert
changes you did not make. Keep changes minimal and compatible.

Verification: Run <tests/checks> if available. If not run, explain why.

Output:
- Files changed
- Behavior changed
- Verification performed
- Remaining risk

Stop when: The bounded change and required verification are complete, or a
concrete blocker requires authority or information outside this packet.
```

## Review Packet

```text
Objective: Review <artifact/diff/plan/research synthesis> for <risk class>.

Scope: Focus on material issues. Avoid generic style comments unless they affect
behavior, correctness, trust, or maintainability.

Output:
- Findings ordered by severity
- Evidence or file/source references
- Suggested fix or follow-up
- Anything you intentionally did not review

Stop when: The assigned risk class has been covered deeply enough to identify
material findings; do not continue only to manufacture style nits.
```
