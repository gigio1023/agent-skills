# Handoff Source Priority

Use this precedence order when compiling facts:

1. Direct execution evidence  
   - command outputs, test logs, build logs, query results, timestamps.
2. Repository state evidence  
   - `git status`, `git diff`, commit history, changed file content.
3. Tracker evidence  
   - issue/task status, review comments, linked decisions.
4. Structured workspace docs  
   - `plan.md`, `progress.md` or `task.md`, `result.md`, runbooks.
5. Unstructured session notes  
   - ad-hoc notes, narrative summaries.
6. Memory-only statements  
   - uncited claims from prior conversation.

If sources conflict, resolve using this procedure:

1. Prefer higher-priority source.
2. If same priority, prefer newer timestamp.
3. If still tied, prefer source with explicit path, command, or line reference.
4. If unresolved, record a `conflict` entry and set handoff status to at least `partial`.
5. If unresolved conflict blocks next action, set status to `blocked`.

Citation rules:

- Every completion claim must include at least one evidence reference.
- If no evidence exists, classify claim as `unknown` and do not mark complete.
- Never silently merge contradictory claims.
