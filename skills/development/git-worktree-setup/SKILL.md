---
name: git-worktree-setup
description: >
  Use when implementation should be isolated from the current checkout, a plan
  calls for a separate branch workspace, or worktree state must be detected
  before editing. Reuses existing isolation or creates a worktree through the
  harness or Git. NOT for merely listing worktrees, deleting them, or publishing
  a finished branch.
---

# Git Worktree Setup

Start implementation in an isolated workspace without taking ownership of a
worktree that the user or harness already manages.

## Quick Path

1. Read repository instructions and inspect Git state before changing anything.
2. Detect whether the current checkout is already a linked worktree, including
   the submodule exception below. Reuse it when it is.
3. If isolation is not already present, create it only when the user has asked
   for a worktree or consents to one.
4. Prefer the harness's native worktree capability. Fall back to `git worktree`
   only when no native capability exists.
5. Run repository-defined setup and the smallest meaningful baseline check.
6. Report the path, branch state, creation mechanism, and validation evidence.

## Detect Existing Isolation

Resolve both paths rather than comparing Git's sometimes-relative output:

```bash
git_dir=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
git_common=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
superproject=$(git rev-parse --show-superproject-working-tree 2>/dev/null)
branch=$(git branch --show-current)
```

When `git_dir` differs from `git_common` and `superproject` is empty, the current
checkout is already a linked worktree. Keep working there; do not create a
nested or replacement worktree. An empty `branch` means detached HEAD, which is
valid when the harness owns the workspace and should be reported as such.

A non-empty `superproject` identifies a submodule, not worktree isolation. Treat
that checkout as a normal repository for this decision.

## Choose the Creation Mechanism

Use an available native worktree capability first. Native creation lets the
harness track directory placement, branch state, and later cleanup. Once it
succeeds, continue setup inside the workspace it returns.

Use the Git fallback only when the runtime has no native worktree capability:

1. Choose a base revision and branch name from the user's request and repository
   conventions. Do not invent a remote update, rebase, or branch rewrite.
2. Prefer an explicit directory policy, then an existing `.worktrees/` or
   `worktrees/` directory. Otherwise use `.worktrees/` at the repository root.
3. Before using a project-local directory, check the exact path with
   `git check-ignore`. If it is not ignored, use a local exclude rule or another
   untracked location unless the requested change authorizes editing
   `.gitignore`. Never create a commit merely to ignore the worktree directory.
4. Check `git worktree list --porcelain` and branch refs before creation. Reuse
   an existing matching worktree; never force, delete, or overwrite one.
5. Create a new branch with:

   ```bash
   git worktree add <path> -b <branch> <start-point>
   ```

   For an existing branch that is not checked out elsewhere, omit `-b`.

If sandbox or filesystem policy blocks creation, report the failed mechanism.
Work in place only when the user accepts losing isolation or their instructions
already authorize that fallback.

## Prepare and Verify

Inside the selected workspace, read project setup instructions and inspect
lockfiles or tool configuration before installing dependencies. Use the
repository's package manager and documented command; do not infer `npm`, Poetry,
or another tool from a generic manifest alone.

Run the smallest project-appropriate check that establishes a baseline before
implementation. Record the exact command and result. If the baseline fails,
separate the pre-existing failure from later work and ask for direction only
when proceeding would make attribution unsafe or require broader changes.

## Authority and Ownership

- Detecting and reporting worktree state is read-only. Creating a branch and
  worktree requires an explicit request or consent.
- Worktree creation does not authorize commits, pushes, rebases, tracked config
  edits, dependency upgrades, or cleanup.
- Treat a native, detached-HEAD, or otherwise externally created worktree as
  externally managed. Do not remove it during this workflow.
- Preserve unrelated dirty state. If it prevents a safe base selection, report
  the conflict instead of moving or stashing someone else's changes.

## Output

Report:

- absolute workspace path;
- branch name or detached-HEAD state;
- reused, native-created, or Git-created mechanism;
- chosen start point when a workspace was created;
- setup and baseline commands actually run, with results;
- any permission failure, pre-existing test failure, or ownership caveat.

The workspace is ready only when its location and Git state are verified. Test
success is reported separately and must not be implied when checks were skipped.

## Gotchas

- `git_dir != git_common` also occurs in submodules; keep the superproject guard.
- Manual `git worktree add` can create state invisible to a harness that offers
  native worktree management.
- A worktree directory inside the repository must be ignored before creation.
- A branch already checked out in another worktree cannot be checked out again.
- Dependency setup may modify lockfiles or generated files; inspect status after
  setup and report unexpected changes.

For maintenance fixtures and the upstream adaptation record, read
`references/evaluation-cases.md` and `references/source-notes.md`.
