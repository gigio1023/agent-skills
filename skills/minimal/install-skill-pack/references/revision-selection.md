# Revision Selection

Choose exactly one revision mode and prepare a reviewed checkout before installation. Keep the source supplied to the Skills CLI separate from the URL used for Git review.

## Inputs

- `source_repo`: the user's repository source without a fragment.
- `review_clone_url`: a cloneable URL for the same repository. Convert GitHub shorthand `owner/repo` to `https://github.com/owner/repo.git`; otherwise use the repository's HTTPS or SSH clone URL.
- `target_branch`: optional named branch.
- `target_commit`: optional exact full commit ID. It cannot be combined with a branch.

Create one disposable directory for all modes:

```bash
review_dir="$(mktemp -d "${TMPDIR:-/tmp}/skill-pack-review.XXXXXX")"
```

## Default Branch

Omit a ref from both the review clone and the CLI source. Git and the Skills CLI will use the remote's default branch.

```bash
git clone --depth 1 "$review_clone_url" "$review_dir/repo"
reviewed_sha="$(git -C "$review_dir/repo" rev-parse HEAD)"
install_source="$source_repo"
current_sha="$(git ls-remote "$review_clone_url" HEAD | awk 'NR == 1 {print $1}')"
test -n "$current_sha" && test "$current_sha" = "$reviewed_sha"
```

## Named Branch

Use the branch for both the review clone and the CLI source:

```bash
git clone --depth 1 --branch "$target_branch" \
  "$review_clone_url" "$review_dir/repo"
reviewed_sha="$(git -C "$review_dir/repo" rev-parse HEAD)"
install_source="$source_repo#$target_branch"
current_sha="$(
  git ls-remote "$review_clone_url" "refs/heads/$target_branch" |
    awk 'NR == 1 {print $1}'
)"
test -n "$current_sha" && test "$current_sha" = "$reviewed_sha"
```

The fragment is a Git branch ref. Keep skill selection in explicit `--skill` arguments; `@name` has different CLI semantics.

## Exact Commit

The CLI's remote `#ref` path can pass a raw commit ID to `git clone --branch`, which Git rejects. Fetch the exact commit into the review checkout and install from that local snapshot instead:

```bash
git init "$review_dir/repo"
git -C "$review_dir/repo" remote add origin "$review_clone_url"
git -C "$review_dir/repo" fetch --depth 1 origin "$target_commit"
git -C "$review_dir/repo" checkout --detach FETCH_HEAD
reviewed_sha="$(git -C "$review_dir/repo" rev-parse HEAD)"
test "$reviewed_sha" = "$target_commit"
install_source="$review_dir/repo"
```

Require the complete commit ID so the identity check is exact. In its default symlink mode, the Skills CLI materializes a canonical package copy and links non-universal agent destinations to it; it does not keep the disposable source checkout as the link target. Remove the checkout only after canonical content, agent links, and discovery all pass. A global install from this temporary local path is not tracked as a remotely updateable source. To reinstall the pinned version, repeat this workflow with the same commit.
