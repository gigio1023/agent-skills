---
name: pr-review-comment
description: >
  Use when the user wants code review findings validated against a Pull Request
  diff and posted as GitHub inline review comments, including "review and
  comment", "PR review comment", and "post review". Discovers an installed
  review skill or accepts supplied candidate findings, verifies code evidence
  and exact diff targets, previews the payload, and posts only after explicit
  approval. Works with github.com and GitHub Enterprise through the gh CLI. NOT
  for review-only feedback with no posting; use a code-review skill. NOT for
  validating or editing comments already posted on a PR.
---

# PR Review Comment

## Outcome Contract

- Outcome: material, code-supported findings attached to the correct diff side
  and commit, with a review body only when it helps the author act.
- Source order: user scope, target repo instructions, complete PR metadata and
  diff, existing review threads, code/callers/tests, candidate reviewer output,
  tone references.
- Authorization: collecting and drafting are read-only. Posting, replying,
  requesting changes, approving, or dismissing reviews are separate external
  mutations and require the user's explicit approval for that action.
- Done: posted review is read back from the target host and its URL, head SHA,
  event, and accepted comment count match the approved payload.

## Workflow

### 1. Identify And Freeze The Target

Resolve host, owner, repo, PR number, and repo-local instructions. Take the
host from the user's request or the repository's `origin` remote. For a GitHub
Enterprise host, prefix every `gh` call with `GH_HOST=<host>`.

Collect at least:

```json
{
  "host": "github.com",
  "owner": "example-org",
  "repo": "example",
  "number": 123,
  "author": "login",
  "base_ref": "main",
  "head_ref": "feat/example",
  "head_sha": "40-character SHA"
}
```

The `head_sha` is the optimistic lock for every later phase.

### 2. Collect The Complete Diff And Existing Threads

Use pagination for the files endpoint. Do not treat the first page as the whole
PR.

```bash
gh api --paginate "repos/{owner}/{repo}/pulls/{number}/files?per_page=100"
```

The REST `patch` field may be absent or truncated. When any changed file lacks
the needed hunk, obtain the complete diff with `gh pr diff` or a local
merge-base diff. If a complete target hunk still cannot be obtained, mark the
finding unverified and do not create an inline target.

Collect what reviewers already posted, so the new review does not repeat it:

```bash
gh api --paginate "repos/{owner}/{repo}/pulls/{number}/comments?per_page=100"
gh api --paginate "repos/{owner}/{repo}/pulls/{number}/reviews?per_page=100"
```

### 3. Obtain Candidate Findings

Use the review source the user named. Otherwise inspect the current harness and
installed skills, then choose the strongest applicable code-review skill.
Parallel review is useful only when independent correctness, security, or
repo-specific lanes materially expand coverage.

User-provided review text is candidate evidence, not an accepted verdict. It
goes through the same validation as delegated findings.

### 4. Validate Findings

For every candidate:

1. Restate the falsifiable code claim.
2. Inspect the changed code, nearest caller, relevant test, and repo rule.
3. Identify the precondition and a concrete failure or counterexample.
4. Classify it as `valid`, `partial`, `invalid`, or `needs-context`.
5. Deduplicate findings with the same cause and consequence. A point an
   existing review thread already makes on the same code is `already-raised`;
   do not repost it.
6. Draft only `valid` findings and the supported part of `partial` findings.

Style is not a finding unless it violates a repo rule or creates a material
correctness, security, operability, or maintainability cost.

### 5. Resolve Exact Diff Targets

Each inline draft uses this closed schema:

```json
{
  "path": "src/example.py",
  "side": "RIGHT",
  "line": 42,
  "start_side": "RIGHT",
  "start_line": 40,
  "body": "review comment",
  "expected_head_sha": "40-character SHA"
}
```

- Added or current lines use `RIGHT`; deleted lines use `LEFT`.
- Omit `start_line` and `start_side` for a single-line comment.
- Every target must exist in the collected diff. Never guess a line number: a
  finding without a verified diff target goes to the review body when it
  materially affects the PR; otherwise discard or file separately.
- Read `references/comment-format.md` and `references/voice-and-tone.md` before
  drafting. Keep evidence and fix direction, and remove review-process
  narration.

### 6. Preview And Approve

Show one approval packet:

- host, owner/repo, PR number, title, author, and expected head SHA
- event: `COMMENT`, `REQUEST_CHANGES`, or `APPROVE`
- every inline path, side, line range, and final body
- final review body, including why any finding is not inline
- discarded, `already-raised`, and `needs-context` candidates with reasons

Do not post until the user approves this exact packet. `REQUEST_CHANGES` is not
available on the reviewer's own PR.

### 7. Recheck, Post, And Read Back

Immediately before posting, fetch the current head SHA. If it differs from
`expected_head_sha`, stop, recollect the diff, and revalidate every target.

Write the approved JSON to a temporary file with the harness file-edit
mechanism, then post in one call:

```bash
gh api "repos/{owner}/{repo}/pulls/{number}/reviews" \
  --method POST --input "${PAYLOAD_FILE}"
```

Read the created review and comments back from the same host. Report the review
URL, event, commit ID, posted count, and any rejected target. Partial posting
is a failure that must remain visible.

## Replying To A Thread

A reply is a separate mutation. Preview the target comment URL and reply text,
obtain approval, post, and read back the reply URL.

## Gotchas

- Never post supplied reviewer output `as-is`. Validate its claim and target.
- Missing REST `patch` content does not mean unchanged code. Fetch the complete
  diff or mark the finding `needs-context`.
- A valid finding can still produce HTTP 422 when `side`, line, or head SHA is
  stale. Use the exact target schema and final head check.
- Submitted reviews and comments are externally visible and not reliably
  deletable. Approval applies to the exact payload, not a paraphrased summary.
- Do not combine `-f` fields with `--input`; post one JSON document.
- Do not spend comment space explaining reviewer tools, severity frameworks, or
  validation methodology. The code fact, consequence, and concrete alternative
  are the useful content.

## Reference Files

| File | Read when | Content |
|---|---|---|
| `references/comment-format.md` | Before target resolution and drafting | Inline/body roles, anti-patterns, code link format |
| `references/voice-and-tone.md` | Before the first draft | Human review voice, examples, posting self-check |
