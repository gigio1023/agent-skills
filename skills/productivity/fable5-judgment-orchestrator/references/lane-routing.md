# Lane Routing

Use this reference before assigning work to Fable 5, GPT-5.6 Sol, another
worker, or a deterministic tool path.

## Route By Task Shape

| Lane | Default owner | Use when | Output |
|------|---------------|----------|--------|
| Judgment lead | Fable 5 | Framing, trade-offs, ambiguity, conflict resolution, recommendation | Decision with evidence and reversal condition |
| Sustained end-to-end work | Fable 5 | One coherent context is more valuable than splitting the task | Verified artifact or analysis |
| Fresh-context verifier | Fable 5 worker or strongest equivalent | A consequential long run needs specification checking or anchoring resistance | Findings tied to evidence |
| Repository/tool-heavy support | GPT-5.6 Sol or strongest configured Codex lane | Bounded codebase work, implementation, source collection, or executable checks benefit from that harness | Patch or compact evidence packet |
| Routine/high-volume support | Suitable lower-cost model | The task is bounded and the lane can meet the same contract | Compact result with caveats |
| Structured reduction | Deterministic code or programmatic tool path | Filtering, joining, ranking, deduplication, aggregation, or repeated validation needs no fresh judgment between calls | Small schema with evidence fields |
| Direct tool call | Lead model | One result is small, sequential, approval-sensitive, citation-bearing, or changes the next decision | Native result preserved for judgment |

These are defaults, not entitlements. Inspect the current harness and configured
models. If a named lane is unavailable, use the strongest suitable equivalent.

## Routing Test

Ask in order:

1. Can the lead finish this coherently without delaying other useful work? If
   yes, keep it direct.
2. Is the work independent enough to justify coordination overhead? If no, keep
   it sequential.
3. Does the lane need semantic judgment between results? If yes, use a model
   lane; if no, a deterministic reduction may be better.
4. Would a fresh context materially reduce anchoring or catch specification
   drift? If yes, add a verifier.
5. Will a cheaper or specialized lane still meet the evidence and quality bar?
   If yes, use it; otherwise keep the stronger lane.

## Evidence Packet

```text
Objective: Answer this bounded question: <question>.

Scope: Inspect <sources/files/repos>. Exclude <what another lane owns>.

Evidence: Prefer primary sources and direct inspection. Record dates and URLs
for current facts; record paths and relevant locations for local claims.

Output:
- Short answer or completed artifact
- Sources/files/tools inspected
- Decisive facts or verification results
- Weak, conflicting, or missing evidence
- Confidence and caveats

Stop when: The assigned question is answered to the stated evidence bar, or a
specific blocker makes further work non-productive.
```

## Long-Context Packet

```text
Objective: Read this large context and extract decision-relevant findings.

Focus: <questions the lead needs answered>. Preserve contradictions and source
locations. Do not make the final recommendation.

Output:
- Key findings
- Relevant passages or file locations
- Contradictions and omissions
- What the lead should examine personally
- Confidence
```

## Bad Routing

- Delegating because the lead model is expensive when the handoff loses crucial
  context or judgment quality.
- Asking several workers the same broad question without distinct sources,
  lenses, or ownership.
- Using programmatic tool calling for approval-sensitive actions, citations,
  native artifacts, or adaptive semantic judgment.
- Waiting idly for a worker when the lead has non-overlapping work to do.
- Launching another wave when the missing fact would not change the decision.
