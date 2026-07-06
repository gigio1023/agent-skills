# Lane Routing

Use this reference before spawning workers, asking a companion harness, or
deciding which work should stay in Fable 5 context.

## Default Routing

| Lane | Default owner | Use when | Output |
|------|---------------|----------|--------|
| Final judgment | Fable 5 | Recommendation, critique, issue map, conflict resolution, confidence | Decision plus caveats |
| Missed-fact review | Fable 5 after evidence lanes | Looking for the important thing the team may have ignored | Missing/weak evidence list |
| Long-context reading | Configured long-context model | Large docs, many files, long transcripts, broad analysis | Compact findings with references |
| Token-heavy collection | Configured Codex support lane | Web search, local inventory, `rg` extraction, source lookup, repo issue scan | Evidence packet |
| High-reasoning support lane | Strongest configured support model | Difficult bounded analysis that benefits from isolated reasoning | Argument, evidence, caveats |
| Narrow verification | Any suitable worker/tool | Tests, builds, link checks, command output, version checks | Pass/fail plus key output |

If the available models or harnesses differ from these defaults, use the
strongest configured equivalent and state the substitution when it matters.

## Keep In Fable 5

- The decision rule: what evidence would actually change the answer.
- The issue graph: how subquestions, risks, and stakeholders connect.
- The final trade-off: upside, downside, reversibility, timing, opportunity
  cost, and user-fit.
- The skeptical pass: what assumption is too convenient, what source is weak,
  what framing is missing.

## Good Support-Lane Packets

```text
Objective: Collect evidence for this bounded question: <question>.

Scope: Inspect <sources/files/repos/domains>. Exclude <what another lane owns>.

Method: Prefer primary sources and direct inspection. For web/current facts,
record dates and URLs. For local files, include paths and line references.

Output:
- Short answer
- Sources/files inspected
- Decisive facts
- Weak or conflicting evidence
- Confidence and caveats

Stop when: You have enough evidence for Fable 5 to decide whether this point
matters.
```

## Good Long-Context Packets

```text
Objective: Read this large context and extract decision-relevant findings.

Context: <long docs/files/transcripts/JDs/specs>.

Focus: <questions Fable 5 needs answered>. Do not make the final
recommendation.

Output:
- Key findings
- Relevant passages or file references
- Contradictions and omissions
- What Fable 5 should examine personally
- Confidence
```

## Bad Delegation

- Asking a worker to "decide what I should do" without a defined lens.
- Sending the whole conversation when only a bounded source lookup is needed.
- Letting a worker's confidence replace Fable 5's own synthesis.
- Running another wave because it feels thorough when the missing evidence would
  not change the decision.
