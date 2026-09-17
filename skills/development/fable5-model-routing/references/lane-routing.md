# Lane Routing

Use this reference before assigning work to Fable, another Claude model, a configured GPT-5.6 or Codex lane, or a deterministic tool path. Fable means Claude Fable 5 or Claude Fable 5.1.

## Contents

- Difficulty Tiers
- Setting Model and Effort in the Harness
- Route By Task Shape
- Routing Test
- Phase Boundary
- Evidence Packet
- Long-Context Packet
- Bad Routing

## Difficulty Tiers

Place each lane by three signals: whether success can be judged from the packet without inventing a premise or decision rule; whether the next move depends on interpreting intermediate results; and how costly a wrong or shallow result is. The defaults below name Claude Code aliases as examples. Inspect the harness's configured models and agent definitions and substitute the equivalent tier.

| Tier | Signals | Default model | Default effort | Examples |
|------|---------|---------------|----------------|----------|
| Mechanical collection | Success is obvious from the packet; no interpretation between steps; cheap to redo | Fastest configured model (`haiku`) | `low` where supported; Haiku 4.5 takes no effort parameter | Inventory files or symbols, run a documented check and report its output, fetch named pages, deduplicate or aggregate structured results |
| Bounded execution | Stable specification with an explicit coverage and source bar; some interpretation but no new decision rule | Mid-tier model (`sonnet`), or the configured GPT-5.6 Sol or Codex lane for repository-heavy work | `medium`; `high` when a multi-file change must be correct the first time | Scoped implementation, evidence collection against a stated bar, test runs with failure triage, document summarization with citations |
| Judgment-adjacent support | Fresh context matters, or contradictions and omissions must be preserved; the lead has bounded the question but not the answer | Strongest non-lead model (`opus`), or Fable itself when the verifier must match the lead's capability | `high`; `xhigh` only when a long autonomous run has shown a measured gain | Fresh-context specification review, adversarial critique, long-context extraction, ambiguous interpretation the lead has framed |
| Judgment core | Decision rule, framing, conflict resolution, recommendation | The lead (Fable) | Session effort | Not delegated |

Effort rules that cut across tiers:

- Effort level names do not correspond to the same amount of thinking across models. Derive the level for the lane's model; do not copy the lead's setting.
- `high` is the API default wherever effort is supported; Haiku 4.5 does not support the parameter, so a Haiku lane has no effort to set. `xhigh` is meant for long-running agentic work with token budgets in the millions; `max` removes constraints and is prone to overthinking on routine or structured-output work. Neither belongs on a lane without a measured reason.
- Lower effort produces fewer and more consolidated tool calls, less preamble, and terser confirmations, which is what a mechanical lane wants.
- At `low`, Fable 5.1 calls search and retrieval tools less often and answers from memory more. For a lane whose value is fresh information, raise the effort or add a verification instruction to the packet.
- Fable at `low` is often competitive on cost per task with Opus- or Sonnet-class models at higher effort while scoring higher. Where the harness can set a subagent's effort, include that configuration in the comparison before defaulting to a smaller model.
- When two tiers both seem plausible, take the cheaper one only if a failure is cheap to detect and redo; otherwise take the higher.

## Setting Model and Effort in the Harness

The policy is harness-neutral; the mechanics are not. Confirm the current harness's controls before promising an assignment.

**Claude Code.** The spawn call sets the model: the Agent tool's `model` argument accepts `sonnet`, `opus`, `haiku`, `fable`, a full model ID, or `inherit`. As of v2.1.271 the spawn call carries no effort argument; a subagent's effort comes from its agent definition's `effort` field (`low`, `medium`, `high`, `xhigh`, `max`) in `.claude/agents/*.md` or `~/.claude/agents/*.md`, which overrides the session level but not the `CLAUDE_CODE_EFFORT_LEVEL` variable or `maxEffortLevel`. A subagent without such a definition inherits the session's effort. So pick the model per invocation, pick the effort by choosing an agent definition that carries it, and when none does, state that the lane runs at inherited effort and steer inside the packet: "Answer directly without deliberating." for a mechanical lane, "This task involves multistep reasoning. Think carefully before responding." for a heavier one. Built-in agent types and locally configured agents, including proxy-pinned ones, carry their own model and tool limits; read their descriptions before choosing. If `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` pins every subagent to one model, report that instead of describing the intended assignment. When a recurring lane needs an effort no definition provides, propose the definition to the user; do not create user configuration unasked.

**Cursor.** Subagent files under `.cursor/agents/` or the user directory carry a `model` field: `inherit`, the default, or a model ID with bracketed parameters such as `claude-opus-5[effort=high]`. Effort therefore travels with the model string in the definition, and where the session exposes no per-invocation choice, the assignment is which definition to run.

**Codex.** Out of scope for this skill. Codex subagents inherit the main session's model and settings unless the harness exposes a choice and the user gives a reason.

If an exact requested model or level is unavailable, report that lane as blocked and continue independent authorized work; use an equivalent only when the user's routing policy permits substitution. Preserve a Fable lead the user asked for.

## Route By Task Shape

| Lane | Default owner | Use when | Output |
|------|---------------|----------|--------|
| Judgment lead | Fable | Framing, trade-offs, ambiguity, conflict resolution, recommendation | Decision with evidence and reversal condition |
| Judgment-dependent discovery | Fable | Source selection or interpretation changes the next question, premise, or option set | Stable frame, decisive evidence, and delegation specification |
| Sustained end-to-end work | Fable | One coherent context is more valuable than splitting the task | Verified artifact or analysis |
| Fresh-context verifier | Fable worker or strongest equivalent at `high` | A consequential long run needs specification checking or anchoring resistance | Findings tied to evidence |
| Repository/tool-heavy support | GPT-5.6 Sol or strongest configured Codex lane | Bounded codebase work, implementation, source collection, or executable checks benefit from that harness | Patch or compact evidence packet |
| Routine/high-volume support | Suitable lower-cost model at `low` or `medium` | The task is bounded and the lane can meet the same contract | Compact result with caveats |
| Structured reduction | Deterministic code or programmatic tool path | Filtering, joining, ranking, deduplication, aggregation, or repeated validation needs no fresh judgment between calls | Small schema with evidence fields |
| Direct tool call | Lead model | One result is small, sequential, approval-sensitive, citation-bearing, or changes the next decision | Native result preserved for judgment |

These are defaults, not entitlements. Inspect the current harness and configured models. Use a suitable equivalent only for an unspecified support lane or when the user's routing policy permits substitution.

## Routing Test

Ask in order:

1. Can the lead finish this coherently without delaying other useful work? If yes, keep it direct.
2. Is the work independent enough to justify coordination overhead? If no, keep it sequential.
3. Could a competent worker know what counts as success from the packet without inventing a premise, value judgment, source-quality rule, or next question? If no, Fable must investigate or specify further first.
4. Does the bounded work still need semantic judgment between results? If yes, use a capable model lane; if no, a deterministic reduction may be better.
5. Would a fresh context materially reduce anchoring or catch specification drift? If yes, add a verifier.
6. Which tier does the lane fall in, and what is the lowest model and effort that still meets its evidence bar? Assign that, and state it.

## Phase Boundary

Fable owns discovery until the handoff packet states:

- the current frame and material alternatives;
- the decision rule and evidence that could change it;
- bounded research questions or an executable action specification;
- source, coverage, and verification bars; and
- conditions that require escalation instead of local improvisation.

After that boundary, prefer GPT-5.6 Sol or the strongest suitable execution lane for large follow-on research, repository work, implementation, and tool-heavy action. A lower-cost lane may handle high-volume collection or straightforward web search when the coverage and source-selection rules are already explicit. Fable should inspect decisive evidence, not every routine result.

If a worker finds a new option, conflicting primary evidence, an invalid premise, or a consequential choice absent from the packet, stop that branch and return the reopened judgment to Fable. Once resolved, issue a revised packet and resume execution.

## Evidence Packet

```text
Objective: Answer this bounded question: <question>.

Scope: Inspect <sources/files/repos>. Exclude <what another lane owns>.

Decision boundary: Apply <fixed rules>. Do not resolve <reserved judgments>. Escalate if <premise breaks, new option appears, or evidence conflicts>.

Evidence: Prefer primary sources and direct inspection. Record dates and URLs for current facts; record paths and relevant locations for local claims.

Output:
- Short answer or completed artifact
- Sources/files/tools inspected
- Decisive facts or verification results
- Weak, conflicting, or missing evidence
- Confidence and caveats

Stop when: The assigned question is answered to the stated evidence bar, or a specific blocker makes further work non-productive.
```

## Long-Context Packet

```text
Objective: Read this large context and extract decision-relevant findings.

Focus: <questions the lead needs answered>. Preserve contradictions and source locations. Do not make the final recommendation.

Output:
- Key findings
- Relevant passages or file locations
- Contradictions and omissions
- What the lead should examine personally
- Confidence
```

## Bad Routing

- Delegating because the lead model is expensive when the handoff loses crucial context or judgment quality.
- Delegating broad discovery before the lead has defined what is material, then treating the worker's framing as neutral evidence.
- Asking several workers the same broad question without distinct sources, lenses, or ownership.
- Copying the lead's model and effort onto every lane, or letting every lane inherit them without a stated reason.
- Describing a model or effort the harness did not actually apply.
- Using programmatic tool calling for approval-sensitive actions, citations, native artifacts, or adaptive semantic judgment.
- Waiting idly for a worker when the lead has non-overlapping work to do.
- Launching another wave when the missing fact would not change the decision.
