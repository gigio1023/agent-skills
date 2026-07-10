---
name: commit-and-push
description: >
  Use when the user explicitly asks to commit, split commits, stage and commit,
  push, sync a branch, or commit directly to the default branch. Triggers on
  "commit", "push", "git push", "커밋", "분할 커밋", "push 해줘",
  "stage and commit", and "direct commit". Keeps unrelated worktree changes
  untouched and limits the default result to commits plus branch push. NOT for
  opening or rewriting a PR (use draft-pr), full CI certification, or
  issue/PR comments and edits unless the user explicitly includes them.
---

# Commit and Push

Produce logically scoped commits and push the requested branch without
absorbing unrelated user changes. Report the commits, pushed ref, verification
evidence, and any remaining worktree state.

## Workflow

1. Inspect before mutating:

   ```bash
   git rev-parse --show-toplevel
   git status -sb
   git branch --show-current
   git remote -v
   git diff --stat
   git diff
   git diff --cached
   ```

2. Read repository instructions such as `CONTRIBUTING.md` and inspect recent
   commit style. Repository and user conventions override this skill's fallback.
3. Lock scope from the request and diff. Preserve unrelated tracked,
   untracked, staged, and unstaged changes. Stage explicit paths; use
   `git add -A` only when the whole worktree clearly belongs to the request.
4. Run focused, relevant checks before committing. Keep required evidence and
   failures; do not expand into an unrelated full-CI campaign unless requested
   or repository policy requires it.
5. Split changes into independently revertible units. Keep implementation and
   its tests together; order prerequisite commits before dependents.
6. Commit each unit, then inspect what actually landed:

   ```bash
   git diff --cached --stat
   git diff --cached
   git commit -m "<message>"
   git show --stat --oneline HEAD
   ```

7. Fetch and reconcile the selected upstream remote before push (often
   `origin`, but do not assume the name):

   ```bash
   git fetch <remote>
   git status -sb
   ```

   If the upstream advanced, rebase the local commits onto it. With a dirty
   worktree, finish only the intended commits first; do not hide unrelated work
   in an automatic stash. Resolve conflicts only when repository intent is
   clear, rerun affected checks, and abort with `git rebase --abort` if safe
   resolution needs user or product judgment.
8. Push the current branch. Use tracking when needed:

   ```bash
   git push -u <remote> HEAD
   ```

   If an already-pushed, clearly user-owned topic branch was rebased, use
   `git push --force-with-lease`, never plain `--force`. Ask before rewriting a
   shared or ambiguous branch.
9. Verify the result:

   ```bash
   git status -sb
   git log --oneline -n 5
   ```

   Confirm the pushed branch/upstream and retain any unrelated worktree changes.

## Commit Shape

One commit should represent one logical change that can be reviewed and
reverted on its own. Avoid splitting by arbitrary file count or layer when the
files implement one behavior.

Use the repository's message convention. If none exists, use:

```text
<type>(<scope>): <imperative subject>

<why this change is needed and any non-obvious consequence>
```

Fallback types are `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `ci`,
`perf`, and `style`. Default to concise English when the repository and user do
not establish another language. Add a body only when rationale, risk, or a
reference would otherwise be lost. Do not add agent branding,
`Co-Authored-By`, or author lines unless explicitly requested.

For a direct default-branch commit without a PR, include enough rationale and
verification in the commit body for the log to stand alone, but do not generate
a ceremonial report or file-by-file inventory.

## Side-Effect Boundary

The default authorization from a commit/push request covers the scoped Git
commits and their branch push. It does not cover issue comments, issue/PR body
or title edits, releases, tags, or other remote mutations. Perform those only
when the same request explicitly includes them, and use the corresponding
specialized skill.

## Output Contract

Lead with whether commit and push succeeded. Include:

- each new commit hash and subject;
- the remote and branch pushed, including whether tracking or
  `--force-with-lease` was used;
- checks run and their result, plus anything not run that materially limits
  confidence;
- remaining staged, unstaged, or untracked changes;
- the exact blocker and smallest next action if the push did not complete.

## Gotchas

- Do not run `git pull --rebase` blindly in a mixed worktree. Inspect, preserve
  unrelated changes, and reconcile remote history at a safe point.
- A pre-commit hook failure means the commit did not succeed. Fix only in-scope
  failures, restage the intended paths, and retry; do not bypass hooks unless
  the user explicitly accepts that risk.
- Never amend, squash, rebase, or force-push a shared branch merely to make the
  history prettier.
- Do not claim a push succeeded from local commit output. Verify the push and
  final branch status.
- If the repository uses `jj` or another VCS layer, stop before Git mutations
  and use the repository-specific publish path.
