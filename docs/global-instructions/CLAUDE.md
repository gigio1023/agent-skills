# Subagent fan-out budget

The main conversation may run up to 10 subagents at once. **If you are yourself a
subagent, spawn at most 2 at once**, at any depth, and prefer 1.

When a wave would need more than 2 lanes, do the extra work yourself and return
one summary, or run a second wave once the first returns. A wider nested wave is
rarely worth it: each layer multiplies token spend across the whole tree, and
each layer adds another round of summarization between the evidence and the
answer that reaches the user.

Hard limits enforced by the harness, for planning purposes: 10 concurrent
subagents per session, and nesting stops two layers below the main
conversation.

# Writing profile

When writing or revising a document, PR body, issue, or any text a colleague will read, apply the copydesk skill even when no skill was named. Its writing profile is imported below and applies in every session.

@~/.agents/skills/copydesk/references/writing-profile.md
