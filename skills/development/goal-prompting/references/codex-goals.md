# Codex Goals

Use this reference when the target is Codex or when translating a goal into or out of Codex.

## Current Contract

Codex Goal mode attaches a persistent objective to the active chat and automatically continues work toward it. The objective becomes both the first prompt and the completion criteria. Current public guidance recommends three core elements when they apply:

- outcome: the result that should exist;
- constraints: required boundaries, compatibility needs, or approaches to avoid;
- verification: tests, measurements, or review criteria that prove completion.

The objective must be non-empty and no longer than 4,000 characters. Put longer supporting detail in a file and point the objective to it. Keep the terminal outcome and decisive verification in the objective itself.

Goal mode does not expand sandbox, approval, network, or tool permissions. A goal can still pause for a decision or unavailable authority.

## Draft Shape

Use prose or compact labels according to complexity:

```text
/goal <outcome>. Start with <material context>. Preserve <critical constraints>. Done when <observable evidence>. Stop and ask if <real blocker or approval gate>.
```

Do not include every field when it is empty. For an already well-scoped task, one outcome sentence plus verification may be enough.

## Native Goal State

When the current Codex surface exposes goal-state capabilities and the user explicitly asks to activate the goal:

1. Inspect the existing goal before setting another.
2. Continue a matching active goal. Do not duplicate or silently replace an unfinished conflicting goal.
3. Use a token budget only when the user explicitly requested one. Do not translate a turn or time clause into a token budget automatically.
4. Mark completion only after the objective's evidence exists. Follow the current runtime contract for blocked, paused, resumed, or cleared states.

When authoring from Claude Code or another harness, return the `/goal` payload for the user to paste into Codex. Do not claim that the remote goal state changed.

## Codex-Specific Checks

- Is the objective a durable result rather than “keep working” or “make progress”?
- Can Codex verify the result using the named workspace, sources, commands, or review criteria?
- Are external writes, destructive actions, deployment, publication, or branch rewrites separately authorized?
- Does a referenced plan or goal file support the objective without becoming the only statement of done?
- If the route is unsettled, should the user refine the work in plan mode before starting the goal?

## Translation From Claude Code

Keep transcript-visible proof because it remains useful. Remove assumptions about Claude Code's separate evaluator, Stop hooks, trust dialog, Haiku model, or turn-count accounting. Retain a user-requested bound as a constraint, but do not invent a native token budget from it.
