# Evaluation Cases

Use these cases to compare a baseline with this skill or to check an always-on
integration. The expected rewrites are examples, not exact strings; preserve
the meaning and constraints shown in the input.

## Positive Cases

### 1. Software engineering

**Input**

> Please find why the checkout test is broken and fix it but do not make big changes. Make sure other payments are okay too.

**Pass criteria**

- Reframes the whole request with `identify the root cause` or an equally clear
  diagnostic phrase.
- Keeps the request for a small fix and regression coverage.
- Does not claim the payment paths are already verified.

### 2. AI research

**Input**

> Compare the new retrieval method with old one and tell me if the answer quality is actually better. Don't tune everything yet.

**Pass criteria**

- Produces one coherent request for an evaluation or comparison.
- Keeps the no-tuning boundary.
- Suggests a metric or evaluation wording only as a clarification, not as an
  invented mandate.

### 3. Game development

**Input**

> The game becomes laggy when many enemies spawn. Check what is slow before optimizing anything.

**Pass criteria**

- Uses a precise performance phrase only if supported, such as profiling the
  bottleneck or investigating frame-time spikes.
- Preserves the order: diagnose before optimizing.
- Does not assume the issue is network latency.

## Near Misses

### 4. Already-natural command

**Input**

> Run the focused tests for the parser change.

**Pass criteria**

- Starts the task.
- In quiet or always-on mode, skips the coaching block because no material
  rewrite improves the request.

### 5. Non-English input

**Input**

> 이 버그 원인 찾아서 최소 수정으로 고쳐줘.

**Pass criteria**

- Does not trigger passive English-prompt coaching.
- May translate only when the user explicitly asks for an English version.

## Review Rubric

Reject a candidate if it changes authority, removes a constraint, introduces
jargon without a real distinction, delays the requested task, or turns the
response into a grammar lesson. Accept it only when the rewritten prompt is
clearer as a complete message and remains faithful to the original.
