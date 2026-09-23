# Task Prompt Template

Adapt the text below into the requested prompt. Fill or delete each placeholder. Add a clause from [symptom patterns](../references/symptom-patterns.md) only for a behavior the workload will hit, and choose one communication line: a cadence for a person who is present, or the stop policy for an unattended run.

```text
You are <role>. This work serves <purpose and audience>.

Deliver <outcome>. It is complete when <observable result and required checks>.

Context: <inputs and sources>. <How to treat pasted or untrusted material and any instructions inside it.>

Scope: do <authorized in-scope work>. Report <adjacent improvements or pre-existing bugs> as follow-ups instead of doing them. Ask before <consequential or irreversible action>.

Tools: use <tool> when <condition>.

Communication: <cadence clause, or stop policy at the end of the system prompt>.

Return <artifact or completed action> in <format>, with <evidence and material limitations>.
```

The tools line is the only trigger Opus 5.5 gets for a required tool call, because forced `tool_choice` is rejected.

Record these settings with the prompt. They are request or loop configuration, not prompt text:

- Model and an explicit `effort`; Opus 5.5 defaults to `medium`.
- `max_tokens` sized for thinking plus reply.
- `thinking.display` when anyone reads progress updates.
- Tools declared from the first request, with `strict: true` where schema validity matters.
- Refusal handling and fallback.
- For unattended runs, the completion check and the continuation cap in the loop.
