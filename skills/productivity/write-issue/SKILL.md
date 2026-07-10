---
name: write-issue
description: >
  Use when the user wants a GitHub issue or issue comment drafted, created,
  audited, or rewritten in actionable Korean. Triggers on "이슈 만들어줘",
  "이슈 작성", "issue 생성", "이슈 내용 정리", "이슈 문구 수정", and
  requests to repair escaped-newline or English-heavy issue bodies. Preserves
  useful existing context and uses real Markdown files for GitHub mutations.
  NOT for PR titles/bodies (use write-pr/draft-pr), code review comments, or
  Jira issues.
---

# Write Issue

Produce a GitHub issue that a teammate can understand and act on without the
agent conversation. Lead with the outcome and keep required context, caveats,
and actions; remove raw dumps and filler.

## Quick Start

1. Decide whether the user wants copy only or an actual GitHub mutation. Before
   creating, editing, or commenting, check repository conventions, `gh` auth,
   and the existing issue when applicable:

   ```bash
   gh auth status
   gh issue view <number> --json number,title,body,url,state,assignees
   ```

2. Preserve useful human context, links, decisions, and acceptance criteria.
   Rewrite only the parts that are broken, stale, or requested; do not replace
   a maintained issue with a generic template.
3. Write the body to a real temporary file. Never pass multiline Markdown
   inline or through process substitution:

   ```bash
   tmp_issue_body="$(mktemp -t issue-body.XXXXXX.md)"
   cat > "$tmp_issue_body" <<'EOF'
   ## 배경
   - 왜 필요한지 1-2줄로 설명합니다.

   ## 목표
   - 완료 후 달라지는 상태를 적습니다.

   ## 범위
   | 포함 | 제외 |
   | --- | --- |
   |  |  |

   ## 작업 목록
   - [ ] 실행 가능한 작업을 적습니다.

   ## 완료 기준
   - 측정하거나 확인할 수 있는 기준을 적습니다.
   EOF
   ```

4. Return the draft for a writing-only request. If mutation was requested, use
   the reviewed file:

   ```bash
   gh issue create --title "<title>" --body-file "$tmp_issue_body"
   gh issue edit <number> --body-file "$tmp_issue_body"
   gh issue comment <number> --body-file "$tmp_issue_body"
   ```

   Use only the command matching the request. Add `--title "<title>"` to an edit
   only when a title change was requested. For a comment, write only the
   requested update instead of reusing the full issue template. Delete the
   temporary file after a successful mutation.

## Content Contract

- Write Korean-first prose; retain necessary English product, API, and code
  terms. At least one substantive Korean sentence must remain.
- Make the action and done state explicit. Use checkboxes for implementation
  work; do not manufacture a checklist for a pure question or discussion issue.
- Prefer concrete modules, interfaces, or repository-visible links over vague
  phrases such as "여러 파일".
- Keep background to the facts needed to decide or execute the issue.
- Use Markdown links for repository-visible documents. Do not publish local
  workspace paths or filenames that recipients cannot access.
- Do not add, remove, or change assignees unless the user explicitly requests it.
  Repository automation may assign the issue after creation; do not preempt it.
- Omit emoji and avoid tilde ranges that GitHub may render as strikethrough.

## Context and Markdown Safety

Do not republish an existing raw body as an `Original body` dump or a full
Markdown code block. Summarize or rewrite it while preserving important facts.

The final title/body/comment must not expose conversation-only context:

- unexplained section numbers or local shorthand;
- `plan.md`, `handoff.md`, or other workspace-only paths;
- session labels, workstream codenames, or undefined abbreviations;
- literal escaped control sequences such as `\n`, `\r\n`, or `\t`.

A teammate who receives only the issue URL should understand the objective and
next action within about 30 seconds.

## Auditing Existing Issues

Use the bundled read-only scanner when the user asks to find malformed issue
bodies:

```bash
python3 scripts/audit_issue_bodies.py \
  --repo <owner/repo> --author <login> --state open --json
```

Exit code `0` means no findings; exit code `2` means findings were detected,
not that the scanner crashed. Treat `escaped_newline=true` or
`english_heavy=true` as review candidates, then inspect each issue before
editing. A scan does not authorize bulk rewrites.

## Output Contract

For a draft, return the proposed title and rendered body. For a GitHub mutation,
lead with the issue URL and state whether it was created, edited, or commented
on; mention assignee changes and preserved context when relevant. On failure,
report the exact auth/repository/command blocker and the smallest next action.

## Pre-Publish Gate

- Real line breaks are present; no literal escaped control sequences remain.
- Korean-first content explains background, goal, scope, action, and done state
  at the depth appropriate to the issue.
- Links and paths are accessible to repository readers.
- Existing useful context was preserved.
- The requested command uses `--body-file` with a real file.
- Title, assignee, and target issue/repository are verified before mutation.

## Gotchas

- Process substitution such as `--body-file <(cat <<EOF ...)` can produce empty
  or truncated content across shells and `gh` versions. Use a real file.
- `english_heavy` is a heuristic, not permission to rewrite. Inspect context and
  preserve accepted technical English.
- Editing an issue body can erase screenshots, task history, and decisions.
  Read the current body first and make the smallest requested change.
- This skill does not edit PR bodies or comments. Route those to `write-pr` or
  `draft-pr` instead of expanding scope.
