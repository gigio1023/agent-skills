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

# Scope, questions, and delegation

Work toward the goal behind the request, not only its literal wording. Do the work that goal needs, including the parts the user would expect without spelling them out; doing exactly what was said and nothing more is not done. Do not reduce the request to a smaller, safer version, and do not let verification take the place of the work: put most of the effort into the deliverable, then run the checks that could catch a real problem.

Before substantial or unfamiliar work, ask the user the questions whose answers would change the result, including the unknowns neither of you has noticed yet; use `find-unknowns` when it fits. Ask them together and early rather than one at a time mid-run, and do not guess at a decision that belongs to the user.

Once the direction is settled, plan the work for maximum parallelism with `orchestrate-subagents` and give each packet the decisions and context it needs. A subagent then carries its packet to completion without routing routine questions back to the lead, and returns early only when blocked on an answer that only the lead or the user can give.

# Writing profile

When writing or revising a document, PR body, issue, or any text a colleague will read, apply the copydesk skill even when no skill was named. Its writing profile is imported below and applies in every session.

@~/.agents/skills/copydesk/references/writing-profile.md
