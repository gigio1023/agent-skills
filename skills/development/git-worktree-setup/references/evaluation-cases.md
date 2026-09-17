# Git Worktree Setup Evaluation Cases

Use the same repository fixtures and success rubric when evaluating this skill in Codex and Claude Code. Record unavailable runtime combinations instead of inferring behavioral parity from static review.

## Positive Triggers

1. "Implement this plan in an isolated worktree."
   - Detect current state, create or reuse isolation, and report path and branch.
2. "Before editing, check whether this Codex workspace is already a worktree."
   - Perform read-only detection and avoid creating nested isolation.
3. "Set up a separate branch workspace for this feature, but do not commit."
   - Respect the no-commit boundary while preparing and validating the workspace.

## Near Misses

1. "Show me every worktree in this repository."
   - List state directly; do not load a creation workflow.
2. "The feature is done; remove its worktree and push the branch."
   - Route to finishing, cleanup, and publication workflows instead.

## Behavior Fixtures

| Fixture | Required behavior |
| --- | --- |
| Normal checkout | Obtain consent unless isolation was already requested; default to Git creation under the repository's `.worktrees/` directory |
| Existing linked worktree | Reuse it and report whether HEAD is named or detached |
| Submodule checkout | Do not misclassify the submodule as a linked worktree |
| Dirty checkout | Preserve unrelated changes and stop if base selection is unsafe |
| Existing branch worktree | Reuse or report it; never force or overwrite |
| Creation policy | Honor an explicit Git or native choice; otherwise use Git under `.worktrees/`, adding an exact local exclude rather than moving outside the repository |
| Creation denied | Report the exact failure; do not silently work in place |
| Failing baseline | Preserve the command and failure as pre-existing evidence |

## Acceptance Rubric

- No nested worktree is created.
- No commit, push, rebase, cleanup, or tracked ignore edit occurs without matching authority.
- An explicit mechanism or directory policy wins; otherwise Git creation stays under the repository's `.worktrees/` directory and uses a local exclude rather than silently choosing a sibling, home-directory, or global path.
- The final report distinguishes workspace readiness from test success.
- The normal workflow remains usable without harness-specific tool names or installation paths.
