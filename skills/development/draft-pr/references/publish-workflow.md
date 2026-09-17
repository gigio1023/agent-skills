# Publication Workflow

Read this before mutating Git state or creating, updating, or merging a pull request. The user must already have requested the corresponding external write.

## Contents

- Preflight
- Provider adapter
- Base and existing PR
- Commit and push
- Create or update the PR
- GitHub with `gh`
- Forgejo with `fj`
- Explicit squash merge

## Preflight

```bash
git rev-parse --show-toplevel
git status -sb
git branch --show-current
git remote -v
git remote get-url --push <head-remote>
```

Select the branch's head remote from the user's instruction, its configured push remote, or an unambiguous repository convention, in that order. Resolve its host and head repository. Resolve the PR target separately from the user's instruction, an existing PR, or an unambiguous target remote; only default the target remote and repository to the head when this is not a fork workflow. When an SSH alias, custom port, or reverse proxy makes the web origin ambiguous, use an existing repository setting or ask for the exact forge URL. Do not guess.

Confirm a provider adapter and its authenticated user before any Git mutation. Stop when provider authentication fails. An assignment-only failure after a PR write does not invalidate that write; leave assignees unchanged and report it.

If the current branch is the remote default branch, create a descriptive topic branch without a model or agent prefix.

## Provider Adapter

Use the row matching the selected publication remote. Bind every provider command to the exact host, head repository, and target repository; ambient CLI defaults may point at a different account or remote.

| Remote | Adapter and preflight |
| --- | --- |
| GitHub or GitHub Enterprise | Require `gh`, run `gh auth status --hostname <host>`, set `implementer_login="$(gh api user --hostname <host> --jq '.login')"`, and pass the exact target repository with `--repo` or `-R`. Stop if authentication or repository resolution fails. |
| Forgejo | Require `fj`, run `fj version`, authenticate with `fj -H <host> whoami`, and bind PR commands to the exact host plus target repository. Confirm the installed version's live help exposes every command used below. Stop before Git mutation when `fj` is missing or unauthenticated. |
| Gitea-compatible private forge | Use its documented API, authenticated browser, or an already-configured compatible CLI. Verify capabilities against that instance instead of assuming Forgejo parity. |
| Plain Git server or unknown forge | No PR adapter is established. Stop before mutation. Use commit-and-push only when the user asked for a push without a PR. |

For a private Forgejo host, `git push` authentication does not authenticate `fj`. If `whoami` fails, stop and tell the user to create a token in Forgejo's `Settings > Applications` and register it once through the interactive command:

```bash
fj -H <host> auth add-token
```

Use a token limited to the target repositories with [`write:repository`](https://forgejo.org/docs/latest/user/authentication/token-scope/). Add `write:issue` because assignment, labels, and comments use issue routes. Never pass a token as a command argument, read or copy `fj`'s token store, put a token in a Git remote or repository file, or report it. Authentication setup is a user action, not part of PR publication.

[`tea`](https://about.gitea.com/products/tea/) is a Gitea CLI. Do not substitute it for `fj` on the Forgejo path. Use it for Gitea only when it is already configured for the exact instance and its live help confirms the required behavior.

## Base And Existing PR

Prefer the user's explicit base. Otherwise, reuse an existing PR's base. On GitHub, list the current head branch in the exact target repository and filter the JSON by head owner and base when a fork or same-named branch is possible:

```bash
gh pr list --repo <host>/<target-owner>/<repo> \
  --head "<head-branch>" --state open \
  --json number,url,title,body,baseRefName,headRefName,headRepositoryOwner,isDraft,state,assignees
```

`gh pr list --head` accepts a branch name but not `<owner>:<branch>`. Do not assume its first result is the current fork branch; inspect `headRepositoryOwner.login`, `headRefName`, and `baseRefName`.

If no PR exists, query the remote default:

```bash
gh repo view <host>/<target-owner>/<repo> --json defaultBranchRef --jq '.defaultBranchRef.name'
```

On Forgejo, query the current tracked branch through the exact target remote:

```bash
fj -H <host> pr -R <target-remote> view
```

If `fj` cannot infer one PR or the workflow uses a fork, list candidates and then inspect an exact reference:

```bash
fj -H <host> pr search --repo <target-owner>/<repo> --state open
fj -H <host> pr view <target-owner>/<repo>#<index>
```

Resolve the default branch from the target remote's symbolic `HEAD` when the user and an existing PR did not name a base. Do not guess it from a local branch name.

Do not treat a same-named branch from a fork as the current branch. Preserve the existing PR's title, body, assignees, links, screenshots, and reviewer context unless the user requested a rewrite.

Fetch the target remote before comparing or publishing. Rebase only when the topic branch is behind, conflicted, or explicitly needs sync:

```bash
git fetch <target-remote>
git rebase <target-remote>/<base-branch>
```

Resolve conflicts intentionally, run focused checks, stage only resolved files, and continue. Abort when a safe resolution requires product judgment the user has not supplied. Use a merge commit only when the repository requires it or the user asks for one.

## Commit And Push

Inspect the diff and commit only the intended scope:

```bash
git diff --stat
git diff
```

Stage explicit paths when unrelated changes exist. Use `git add -A` only when the entire worktree belongs to the PR. Push a new or unchanged topic branch with `git push -u <head-remote> HEAD`. After rebasing an already-pushed, clearly user-owned topic branch, use `git push --force-with-lease`; ask before rewriting a shared or ambiguous branch.

## Create Or Update The PR

Write real Markdown to a temporary file. Do not rely on generated fill text or a multiline shell argument for final content.

```bash
tmp_pr_body="$(mktemp -t draft-pr-body.XXXXXX.md)"
```

### GitHub with `gh`

Create a new draft:

```bash
pr_ref="$(gh pr create --repo <host>/<target-owner>/<repo> --draft --base "<base-branch>" --head "<head-owner>:<head-branch>" --title "<concise title>" --body-file "$tmp_pr_body")"
```

Update an existing PR without changing its title unless requested:

```bash
pr_ref="<number>"
gh pr edit "$pr_ref" --repo <host>/<target-owner>/<repo> --body-file "$tmp_pr_body"
```

After the create or update succeeds, clean up the temporary file and add the authenticated user without removing existing assignees:

```bash
rm -f "$tmp_pr_body"
gh pr edit "$pr_ref" --repo <host>/<target-owner>/<repo> --add-assignee "$implementer_login"
```

Assignment failure does not invalidate a successful PR create or update. Report it separately. Verify the remote result rather than trusting command success:

```bash
gh pr view "$pr_ref" --repo <host>/<target-owner>/<repo> --json number,url,title,body,baseRefName,headRefName,isDraft,state,assignees
```

The create command prints the PR URL. Preserve it as `pr_ref`; do not parse a number from human-readable output. `--head <user>:<branch>` currently does not support an organization as the head owner. If that limitation applies, stop and use an explicitly selected API or browser path instead of changing the head repository.

Change readiness only when requested and verify it afterward:

```bash
gh pr ready "$pr_ref" --repo <host>/<target-owner>/<repo>
gh pr view "$pr_ref" --repo <host>/<target-owner>/<repo> --json number,url,isDraft,state
```

Use `gh pr ready "$pr_ref" --repo <host>/<target-owner>/<repo> --undo` for an explicitly requested return to draft. Do not use `gh pr create --dry-run` as a no-write probe because the command may still push Git changes. The GitHub commands in this section follow the current official [`gh pr` manual](https://cli.github.com/manual/gh_pr_create); confirm live help before relying on a newly added or host-specific flag.

### Forgejo with `fj`

`fj` 0.6.0 creates PRs with a positional title and supports `--body-file` on create. It has no dedicated draft flag, so use `WIP:` only after confirming the instance recognizes the default work-in-progress prefix:

```bash
fj -H <host> pr create "WIP: <concise title>" \
  --repo <target-owner>/<repo> \
  --base "<base-branch>" \
  --head "<head-owner>:<head-branch>" \
  --body-file "$tmp_pr_body"
```

The create output provides the PR number. Form the exact reference as `<target-owner>/<repo>#<index>`, then verify it and assign the authenticated user without removing existing assignees:

```bash
fj -H <host> pr view <target-owner>/<repo>#<index>
fj -H <host> pr assign --pr <target-owner>/<repo>#<index> "$implementer_login"
fj -H <host> pr view <target-owner>/<repo>#<index> assignees
```

Confirm the displayed state is `draft` and the base and head match. Build the PR URL from the resolved web origin and verified repository and index. If the instance uses another work-in-progress prefix, stop unless the user selected a compatible API or browser fallback.

For an authorized body update, preserve the old body before replacing it. Current `fj` has no `--body-file` for edit, so pass the already-reviewed file as one quoted argument rather than hand-escaping Markdown:

```bash
pr_body="$(<"$tmp_pr_body")"
fj -H <host> pr edit <target-owner>/<repo>#<index> body "$pr_body"
fj -H <host> pr view <target-owner>/<repo>#<index>
```

Use `fj pr edit <ref> title "<title>"` only when the user authorized a title or readiness change. Delete the temporary body file after remote verification. Use REST or an authenticated browser only when the user explicitly requests that fallback and the live instance can verify the same host, repository, PR, and state.

## Explicit Squash Merge

Merge only when the user explicitly asks to merge the resolved PR. A request to create, update, mark ready, or check a PR is not merge authority. Resolve the exact host, target repository, and PR number again immediately before merging.

On Forgejo, inspect the PR, checks, and current reviews with exact references:

```bash
pr_ref="<target-owner>/<repo>#<index>"
fj -H <host> pr view "$pr_ref"
fj -H <host> pr status "$pr_ref"
fj -H <host> pr review "$pr_ref" list
```

Require an open ready PR, the expected base and head, `mergeable: yes`, no pending or unsuccessful required check, no unresolved requested change, and no unmet repository rule. Do not use `fj pr status --wait` in the normal path because it waits without a fixed deadline. If checks are pending, report them or poll only for a user-requested bounded wait.

`fj pr merge` performs the write without a confirmation prompt. Once every gate passes, use squash explicitly and do not set a custom title or message unless the user asked for one:

```bash
fj -H <host> pr merge "$pr_ref" --method squash
fj -H <host> pr status "$pr_ref"
```

Add `--delete` only when the user explicitly requested deletion of the remote head branch. Never retry with another merge method or an administrative bypass when squash is disabled or the server rejects the merge.

On GitHub, query the repository merge policy and the exact PR state. Capture the head OID immediately before the required-check gate:

```bash
gh repo view <host>/<target-owner>/<repo> --json squashMergeAllowed --jq '.squashMergeAllowed'
gh pr view "$pr_ref" --repo <host>/<target-owner>/<repo> \
  --json number,url,title,isDraft,state,mergeable,mergeStateStatus,reviewDecision,baseRefName,headRefName,headRefOid,statusCheckRollup
head_oid="$(gh pr view "$pr_ref" --repo <host>/<target-owner>/<repo> --json headRefOid --jq '.headRefOid')"
gh pr checks "$pr_ref" --repo <host>/<target-owner>/<repo> --required
```

Require `squashMergeAllowed: true`, a non-draft open PR, the expected base and head, a mergeable state, a satisfied review decision, and exit code 0 from `gh pr checks --required`. Exit code 8 means checks are pending; another nonzero result blocks the merge. Do not add `--watch` or `--auto` unless the user requested waiting or scheduled merging.

Use `--match-head-commit` to prevent merging a head that changed after the preflight:

```bash
gh pr merge "$pr_ref" --repo <host>/<target-owner>/<repo> \
  --squash --match-head-commit "$head_oid"
gh pr view "$pr_ref" --repo <host>/<target-owner>/<repo> \
  --json number,url,state,isDraft,mergedAt,mergeCommit,autoMergeRequest,baseRefName,headRefName
```

Add `--delete-branch` only when the user explicitly authorized deletion of both the local and remote head branch. Never use `--admin` as a retry. A protected base may place the PR in a merge queue instead of merging immediately. Report queued or scheduled state accurately and claim completion only when `mergedAt` is present. See the official [`gh pr checks`](https://cli.github.com/manual/gh_pr_checks) and [`gh pr merge`](https://cli.github.com/manual/gh_pr_merge) manuals for these flags and merge-queue behavior.
