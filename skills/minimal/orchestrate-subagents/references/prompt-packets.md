# Prompt Packets

Use these packet shapes when delegating. Adapt wording to the harness and task.

When the task definition already lives in a durable file, the packet carries its path plus the scalar config values the worker needs. Do not paraphrase the file's content into the packet.

Write each stop condition so the worker's last message is a result or a stated blocker with what remains, never a plan for what it will do next. The harness returns that last message to the lead as the result.

Give every packet that runs longer than a few minutes an expected duration and a progress artifact, and ask the worker to write findings to its output file as it goes rather than only at the end. The lead uses the artifact to tell a working agent from a stalled one, and a replacement worker can start from what is already written. See the dispatch loop in `SKILL.md`.

```text
Expected duration: <estimate, e.g. 20 minutes>.
Progress: Write <report path> incrementally: findings as you confirm them, then the final summary. Code changes stay in <your worktree> so the lead can see the diff grow.
```

The research, exploration, implementation, and review packets below require semantic judgment. Use Astra when assigning them to a GPT worker. The mechanical packet is the only Sol 6.1 shape; further GPT delegation preserves the same routing rule.

## Contents

- Mechanical collection packet
- Research packet
- Value judgment packet
- Code exploration packet
- Code worker packet
- Review packet
- Replacement packet

## Mechanical Collection Packet

```text
Objective: Produce <fixed output artifact> from <exact inputs>.

Inputs: <specified URLs, fixed queries, paths, or command inputs>.
Procedure: <exact commands or supplied deterministic transform>.
Output: <raw or mechanically transformed format>.
Acceptance: <count, hash, schema, or exact comparison>.
Authority: <permitted effects and user resource limits>.

Return the output, source locations, exit statuses, and failed or missing items.
Do not select sources, summarize meaning, diagnose results, assess confidence,
implement code, or choose a next action. Return an undefined result or mismatch
to Astra with the raw evidence and completed actions.
```

Use `small-model-handoff` when this executor needs a fuller command and authority contract. Prefer a script when it already performs the fixed operation.

## Research Packet

```text
Objective: Answer this specific question: <question>.

Scope: Inspect <source types / domains / repos / files>. Do not cover <excluded scope> because another subagent owns it.

Method: Prefer primary sources and direct inspection. Treat popularity as a weak signal. Flag AI-slop, stale, or unsupported sources.

Output:
- Short answer
- Sources inspected
- Key claims with evidence
- Discarded/weak sources
- Confidence and caveats
- Follow-up questions that would materially change the answer

Stop when: You have inspected the assigned scope deeply enough to support or reject the relevant claims.
```

## Value Judgment Packet

```text
Objective: Argue from the <advocate/skeptic/operator/outsider> lens for this decision: <decision>.

Context: <facts, constraints, user preferences, time horizon>.

Scope: Focus on <lens-specific issues>. Do not attempt a final recommendation; the lead agent will synthesize.

Output:
- Strongest argument from this lens
- Evidence or assumptions
- Failure modes / upside / opportunity cost
- What would change your view
- Confidence

Stop when: The assigned lens has a defensible argument, its decisive assumptions are explicit, and further work is unlikely to change that argument materially.
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

Stop when: The codebase question is answered with direct file evidence, or a specific missing dependency prevents a reliable answer.
```

## Code Worker Packet

```text
Objective: Implement <bounded change>.

Ownership: You own <files/modules>. Avoid touching <files/modules> unless strictly necessary and report it.

Coordination: Other agents or the user may be editing the repo. Do not revert changes you did not make. Keep changes minimal and compatible.

Limits: Do not spawn subagents. Never mark a failed task as done — report the failure.

Verification: Run <tests/checks> if available. If not run, explain why.

Expected duration and progress: <estimate>; keep changes in <worktree> and notes in <report path> as you go.

Output:
- Files changed
- Behavior changed
- Verification performed
- Remaining risk

Stop when: The bounded change and required verification are complete, or a concrete blocker requires authority or information outside this packet.
```

## Review Packet

```text
Objective: Review <artifact/diff/plan/research synthesis> for <risk class>.

Scope: Focus on material issues. Avoid generic style comments unless they affect behavior, correctness, trust, or maintainability.

Unit: <one branch, module, or claim group>. Other reviewers own the other units.

Expected duration and progress: <estimate>; append each confirmed finding to <report path> when you confirm it.

Output:
- Findings ordered by severity
- Evidence or file/source references
- Suggested fix or follow-up
- Anything you intentionally did not review

Stop when: The assigned risk class has been covered deeply enough to identify material findings.
```

## Replacement Packet

Use this when the lead stopped a stalled worker. The new worker starts from the stopped worker's artifacts, not from scratch and not from its transcript.

```text
Objective: Finish <original objective>. A previous worker stopped before finishing.

Original packet: <path or the original packet text>.
Already done: <artifact paths, diff location, report sections>; last observed change at <time>.
Direction it was taking: <its last stated step, if any>. Treat it as a hint, not a decision.
Remaining: <open items>.

Verify partial work before keeping it. Keep the original output paths so downstream packets still find them.

Expected duration and progress: <estimate>; write progress to <report path> as you go.

Stop when: The original stop condition is met, or a concrete blocker requires authority or information outside this packet.
```
