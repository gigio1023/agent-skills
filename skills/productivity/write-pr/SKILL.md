---
name: write-pr
description: >
  Use when the user wants a Korean reviewer-facing GitHub PR title or body
  drafted, rewritten, or cleaned up, especially with Jira or GitHub Enterprise
  conventions. Triggers on "PR 본문", "PR 작성", "PR description 업데이트",
  "PR 문구 수정", and requests for a concise Korean PR summary. Produces a
  respectful body sized to the change and centered on why it exists and what
  outcome it creates. NOT for branch creation, commits, rebasing,
  pushing, or generic PR publication (compose with draft-pr), issue writing
  (use write-issue), or review comments.
---

# Write PR

Produce a concise Korean title and body that let a reviewer understand why the
PR matters and what changes after merge. This skill owns the copy contract;
when the request also asks to create or update the actual GitHub PR, compose it
with `draft-pr` for repository and publication operations.

## Quick Start

1. Read the user request, repository PR template, existing PR body when editing,
   linked issue/Jira context, and the net diff or commit range. Preserve useful
   screenshots, links, release notes, and human reviewer context.
2. Write the body to a real temporary Markdown file. Do not use process
   substitution for `--body-file`:

   ```bash
   tmp_pr_body="$(mktemp -t pr-body.XXXXXX.md)"
   cat > "$tmp_pr_body" <<'EOF'
   Jira: https://issues.example.com/browse/PROJ-123

   ## 배경
   왜 이 작업이 필요한지 1-2문장으로 설명합니다.

   ## 변경 요약
   - 의미 단위 변경을 적습니다.

   ## 결과
   - 머지 후 사용자나 시스템에서 달라지는 점을 적습니다.
   EOF
   ```

   Jira 줄은 사용자가 실제 Jira URL이나 이슈를 제공한 경우에만 둡니다.
3. Check length and revise from reviewer impact outward:

   ```bash
   wc -l "$tmp_pr_body"
   ```

   For a routine PR, target about 20 lines or fewer and keep a small PR near 10.
   This is a heuristic, not a ceiling: retain required template sections,
   migration steps, risks, caveats, links, and reviewer actions. Use
   `references/anti-patterns.md` when the draft is repetitive rather than merely
   long.
4. Return the title/body for a writing-only request. If the user asked to mutate
   GitHub, hand the file to the `draft-pr` flow and use `--body-file`.

## Body Contract

Use this fallback shape when the repository does not require another template:

```markdown
## 배경
작업이 필요한 사실과 동기를 1-2문장으로 씁니다.

## 변경 요약
- 파일이 아니라 의미 단위로 2-4개 이내를 씁니다.

## 결과
- 머지 후 관찰 가능한 영향이나 운영 조치를 1-3개로 씁니다.
```

Keep required repository-template sections, but remove unused placeholders.
The core content rules are:

- All prose is Korean honorific style (`-습니다`, `-합니다`, `-됩니다`);
  compact noun-phrase bullets are allowed.
- Explain motivation and outcome before implementation detail. Leave file,
  function, line, and change-count inventories to the diff.
- Do not add a generic verification/test section or stale claims such as
  "pytest passed". CI is the source for routine test status. If a repository
  template requires a test section, satisfy the template with specific,
  current evidence or the repository's accepted not-run form.
- Put a breaking effect in one `결과` bullet: `기존 X -> 변경 Y. 운영 조치 Z`.
  Do not create a duplicate `Breaking Changes` section.
- Use one nested-bullet level only when a change has multiple related aspects;
  a second level is a signal to split or compress the PR.
- Keep follow-ups, postmortem detail, and long link collections in their own
  issue or document.
- Remove agent branding, session names, local paths, unexplained internal
  abbreviations, and conversation-only references.
- Do not use emoji, em dash (`—`), middle dot (`·`), bullet glyph (`•`), or
  tilde ranges that GitHub can render as strikethrough. Use hyphens, commas, and
  Korean wording instead.

## Title and Link Rules

Follow repository title conventions first. Otherwise use a concise title that
states the net change.

- When a Jira issue is supplied, put its full URL at the top of the body and
  include `[PROJ-123]` in the title so common Jira development-panel link rules
  can match it. Do not invent an issue URL from a key alone.
- Add `Closes #N` only for the intended GitHub issue. Jira and GitHub issue
  references can coexist.
- Do not copy a vague branch name or add agent prefixes to the title.

## Publication Commands

Use these only when the request explicitly includes GitHub mutation and after
the `draft-pr` preflight has identified the PR/base/head:

```bash
gh pr edit <number> --body-file "$tmp_pr_body"
```

Add `--title "<title>"` only when the request includes a title change.

For GitHub Enterprise, set `GH_HOST`; older compatible `gh` builds may not
support `--hostname`:

```bash
GH_HOST=github.example.com gh pr edit <number> --body-file "$tmp_pr_body"
```

Delete the temporary file after successful publication. Do not overwrite an
existing title unless the user requested a title rewrite or it is clearly a
placeholder.

## Output Contract

For writing-only work, return the proposed title and rendered body, plus any
missing Jira/issue fact that prevents an exact link. For a published update,
lead with the PR URL and say whether the title, body, or both changed. Preserve
required facts, caveats, links, and reviewer actions; trim filler and process
narration.

## Pre-Publish Gate

- A routine body is near or below 20 lines; every extra section or bullet earns
  its place through required context, risk, migration, or reviewer action.
- `배경` and `결과` answer why the PR exists and what changes after merge.
- Prose uses Korean honorific endings.
- No generic test section remains unless the repository template requires it;
  no file/function inventory, session-only reference, agent footer, emoji, or
  forbidden punctuation remains.
- Jira URL/title key and `Closes #N` are present only when verified and intended.
- Existing screenshots, links, and reviewer context that still matter are
  preserved.

## Reference Files

| File | Read when | Content |
| --- | --- | --- |
| `references/anti-patterns.md` | Reviewing a draft or removing repetition without losing required context | Bad/good mappings and compression order |
| `references/examples.md` | Tone or section balance remains unclear | Compact positive and negative examples |

## Gotchas

- `--body-file <(cat <<EOF ...)` can yield an empty or truncated body across
  shells and `gh` versions. Write a real file first.
- `GH_HOST=... gh ...` is more portable for GitHub Enterprise than assuming a
  `--hostname` flag.
- `변경 요약` says what was done; `결과` says what reviewers or users receive.
  Do not repeat the same bullet under both.
- A long breaking change is not a reason to add more sections. If it cannot be
  explained in one or two result bullets, consider whether the PR scope itself
  should be split.
- Preserve repository-required templates and meaningful human content; concise
  does not mean deleting required facts or caveats.
- Bare "PR 작성" requests produce copy only. Use `draft-pr` only when the user
  explicitly asks to create, open, publish, or update the remote PR.
