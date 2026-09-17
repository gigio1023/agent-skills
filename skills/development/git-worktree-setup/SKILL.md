---
name: git-worktree-setup
description: >
  Use when implementation should be isolated from the current checkout, a plan
  calls for a separate branch workspace such as `gigio-execute-plan` isolating
  parallel workers, or worktree state must be detected before editing. Reuses
  existing isolation or creates a worktree through the harness or Git. NOT for
  merely listing worktrees, deleting them, or publishing a finished branch.
---

# Git Worktree Setup

Start implementation in an isolated workspace without taking ownership of a worktree that the user or harness already manages.

## Quick Path

1. Read repository instructions and inspect Git state before changing anything.
2. Detect whether the current checkout is already a linked worktree, including the submodule exception below. Reuse it when it is.
3. If isolation is not already present, create it when the user has asked for a worktree or the active mission already grants isolation. Do not ask again for the same scope; an inspection-only request still does not grant creation.
4. Honor an explicit creation mechanism or directory policy. Otherwise create a Git worktree under the repository's `.worktrees/` directory. Use native creation when the user asks for harness-managed lifecycle behavior.
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

When `git_dir` differs from `git_common` and `superproject` is empty, the current checkout is already a linked worktree. Keep working there; do not create a nested or replacement worktree. An empty `branch` means detached HEAD, which is valid when the harness owns the workspace and should be reported as such.

A non-empty `superproject` identifies a submodule, not worktree isolation. Treat that checkout as a normal repository for this decision.

## Choose the Creation Mechanism

An explicit user or repository choice between harness-native creation and `git worktree` wins. Choose native creation when the requested result depends on harness-managed placement, handoff, restoration, or cleanup. Continue setup inside the workspace it returns and treat that workspace as externally managed.

Without an explicit mechanism, use `git worktree` and keep its directory inside the repository. Git creation does not by itself prevent a named branch from being discovered by ordinary Git and PR tooling. It may not gain harness-only lifecycle controls.

For Git creation:

1. Choose a base revision and branch name from the user's request and repository conventions. Do not invent a remote update, rebase, or branch rewrite.
2. Prefer an explicit project-local directory policy, then an existing `.worktrees/` or `worktrees/` directory. Otherwise use `.worktrees/` at the repository root. Keep every generated path beneath that directory. Do not choose a sibling, home-directory, or global location unless the user or repository explicitly names it.
3. Before using a project-local directory, check the exact path with `git check-ignore`. If it is not ignored, add the exact directory to the repository's local Git exclude file. Do not edit `.gitignore` or relocate the worktree outside the repository merely to keep it untracked. If local exclusion is unavailable, report the blocker instead of choosing a new location. Never create a commit merely to ignore the worktree directory.
4. Check `git worktree list --porcelain` and branch refs before creation. Reuse an existing matching worktree; never force, delete, or overwrite one.
5. Create a new branch with:

   ```bash
   git worktree add <path> -b <branch> <start-point>
   ```

   For an existing branch that is not checked out elsewhere, omit `-b`.

If sandbox or filesystem policy blocks creation, report the failed mechanism. Work in place only when the user accepts losing isolation or their instructions already authorize that fallback.

## Prepare and Verify

Inside the selected workspace, read project setup instructions and inspect lockfiles or tool configuration before installing dependencies. Use the repository's package manager and documented command; do not infer `npm`, Poetry, or another tool from a generic manifest alone.

Run the smallest project-appropriate check that establishes a baseline before implementation. Reuse an existing baseline only when its revision, relevant files, and environment match this workspace. Record the exact command and result. If the baseline fails, separate the pre-existing failure from later work and ask for direction only when proceeding would make attribution unsafe or require broader changes.

## Authority and Ownership

- Detecting and reporting worktree state is read-only. Creating a branch and worktree requires an explicit request or consent.
- Worktree creation does not authorize commits, pushes, rebases, tracked config edits, dependency upgrades, or cleanup.
- Treat a native, detached-HEAD, or otherwise externally created worktree as externally managed. Do not remove it during this workflow.
- Treat a Git worktree created by this workflow as workflow-owned, but do not remove it unless a later request explicitly authorizes cleanup.
- Preserve unrelated dirty state. If it prevents a safe base selection, report the conflict instead of moving or stashing someone else's changes.

## Output

Report:

- absolute workspace path;
- branch name or detached-HEAD state;
- reused, native-created, or Git-created mechanism;
- chosen start point when a workspace was created;
- setup and baseline commands actually run, with results;
- any permission failure, pre-existing test failure, or ownership caveat.

The workspace is ready only when its location and Git state are verified. Test success is reported separately and must not be implied when checks were skipped.

## Gotchas

- `git_dir != git_common` also occurs in submodules; keep the superproject guard.
- PR discovery depends on the branch, remote, and PR provider, not on who created the worktree. Harness-managed cleanup and handoff can still require native creation.
- A branch already checked out in another worktree cannot be checked out again.
- Dependency setup may modify lockfiles or generated files; inspect status after setup and report unexpected changes.

For maintenance fixtures and the upstream adaptation record, read `references/evaluation-cases.md` and `references/source-notes.md`.
