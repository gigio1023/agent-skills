# Always-On Prompt Coaching

This skill can review a prompt in a separate lane, but a filesystem skill alone
cannot intercept every message. The harness must be configured to load this
skill for substantive English task requests. Use its native global or workspace
instruction mechanism to add the policy below.

## Portable Policy

```text
For each substantive English task request, start the requested work without
waiting. In parallel when an independent-review capability is available, load
the reviewing-english-prompts skill and produce its compact coaching packet.
Otherwise, run the same review after the work is complete. Put the task result
first, then append the skill's English prompt coach section. Preserve the user's
meaning and do not expose private reasoning. Skip the section for a short,
already-natural command unless a rewrite would teach a materially better way to
express the request.
```

Place the policy in the tool's always-loaded instruction or rule file, then make
sure the installed skill directory is discoverable to that tool. Keep the policy
outside `SKILL.md`: automatic loading and background execution are harness
features, not portable skill semantics.

## Behavior Modes

| Mode | When to use it | Result |
| --- | --- | --- |
| Always-on | The user wants coaching on most substantive English tasks. | A compact rewrite follows each task result. |
| On request | The user asks to review, improve, or naturalize a prompt. | The skill returns the rewrite immediately with the requested scope. |
| Quiet | The user is focused on delivery and wants no visible coaching. | The task continues normally; do not accumulate or retain prompt data. |

An always-on policy should not alter the primary task's permissions, tools, or
completion bar. A failed or unavailable review lane is not a failure of the
task lane; complete the task and omit the coaching block rather than pretending
it ran.

## Integration Check

After enabling the policy, send a substantive English task request and confirm:

1. the primary task starts without a language-review clarification;
2. the final response contains one whole-prompt rewrite, not token-level edits;
3. technical names and constraints remain unchanged;
4. no terminology note appears unless it adds a meaningful distinction; and
5. disabling the policy removes the coaching block without changing task work.
