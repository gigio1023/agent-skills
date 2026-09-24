# PR Body Guidance

Read this before writing a new body or rewriting one. A repository template is authoritative even when its headings differ from the fallback here; this file then governs only how the template's fields are filled.

## Contents

- Reader test
- Default shape
- Headings in the PR language
- Structure
- Tables
- Before and after
- One more section
- Cut list
- Validation and checks
- Examples
- Where this shape comes from

## Reader Test

A reviewer skims the body once, before the diff. It succeeds when it answers three questions in under a minute:

- Why does this change exist? The problem, the intent, and the decision the code cannot show.
- What will I see changed? Outcomes and behavior, not a file inventory.
- What do I have to decide or do? A breaking change, a tradeoff to weigh, a screenshot to judge. Often nothing, and then nothing is written.

The title describes the whole diff in one specific sentence. If it cannot, report the scope mismatch; a longer body does not make unrelated changes coherent.

## Default Shape

Use this only when the repository has no template:

```markdown
## Context

One short paragraph: the problem or constraint, who or what it affects, and the decision behind the change. Understandable without the authoring session or a linked thread.

## Changes

- One bullet per reviewer-visible outcome.
  - Nest one level when several outcomes belong to one component or theme.
- Name an intentionally unchanged behavior or boundary when a reviewer would otherwise look for it.
```

A small change needs no headings: two or three sentences that give the why and the what. Do not pad a one-line fix into two sections.

## Headings In The PR Language

Title, headings, and prose share the language settled with the user. Translate the two fallback headings; keep a template's headings exactly as written. Conventional prefixes such as `fix:` and `docs:`, identifiers, commands, paths, and quoted text stay as they are.

| Language | Context | Changes |
| --- | --- | --- |
| English | `## Context` | `## Changes` |
| Korean | `## 배경` | `## 변경 사항` |

For another language, use the plain equivalents of "context" and "changes" that the team's existing PRs already use.

## Structure

Structure is what lets a body be read in one pass; length is what stops it being read.

- Prefer bullets over paragraphs for anything with more than one item, and a table when the items share attributes the reviewer will compare; see Tables below. Keep each bullet to one outcome and one or two sentences.
- Nest one level when four or more items fall into groups a reviewer would recognize, such as a component, a user-facing surface, or a migration step. Do not nest deeper.
- Put the decision the code cannot show first in Context. History, alternatives not taken, and background the reviewer already has stay out.
- Put issue references and design links next to the claim they support. The body must still make sense if the link is unavailable or the reader lacks access.

## Tables

A table lets the reviewer compare several items on the same attributes without re-reading bullets. Use one when that comparison is the point: settings with their old and new defaults, endpoints with their new status, options weighed with the chosen one marked. Items read in sequence, items with a single attribute, and a single item stay in bullets or a sentence. Before And After below is the one case where a table is always used, because as-is against to-be is always a side-by-side comparison.

Design the grid before filling it:

- Columns are the attributes the reviewer compares, one per column, named in the header. Drop a column that would read the same in every row or stay empty in most rows, and state that fact once above the table. Two to four columns is the usual range.
- Rows are the items, one per row, in the order the reviewer would scan them: by impact, by their order in the diff, or alphabetically when nothing else orders them.
- Cells hold a value, an identifier, or a short phrase. A cell that wants a full sentence, a list, or a qualifying clause shows that the attribute is not tabular; keep the fact in the cell and move the point to a bullet beneath the table.

Headers follow the PR language; identifiers, values, and code stay as written. A table with one data column is a list and a table with one row is a sentence; write those as such.

A table that earns its place:

```markdown
- Tighten the default timeouts so a stalled upstream fails the request instead of holding the worker.

| Setting | Before | After |
| --- | --- | --- |
| `connect_timeout` | 30s | 5s |
| `read_timeout` | 120s | 30s |
| `retry_budget` | unlimited | 3 |

- Explicit values in `config.yaml` are kept; only the defaults change.
```

In Korean the header row reads `| 설정 | 이전 | 이후 |` and the rest of the table does not change.

The same content as a table that should have been prose:

```markdown
| Setting | Change |
| --- | --- |
| `connect_timeout` | Reduced from 30s to 5s because the upstream normally answers within a second and a stalled connection held the worker for the full 30s during the incident on the 3rd. |
| `read_timeout` | Reduced from 120s to 30s for the same reason. |
```

One data column and a sentence per cell: the reason belongs in Context, and the values belong in the three-column table above.

## Before And After

Every PR that changes behavior, structure, a default, or a data flow shows both states explicitly in one table, because the reviewer judges the diff against that comparison. Rows are the things that change; columns are Before and After, plus at most one attribute column. Cells stay values or short phrases. Headers follow the PR language: `| Item | Before | After |` in English, `| 항목 | 이전 | 이후 |` in Korean.

The table is the whole comparison. Do not add a diagram, figure, or Mermaid block to the body unless the user asks for one for this PR; a figure drawn by default costs a skill run and an upload, and repeats what the table already says.

The Before side is the PR's actual base branch at the merge base, read from the code there, not from an earlier draft the author passed through or from memory. When the base is not the default branch, name it once above the table.

A pure refactor with no behavior change, a docs typo, or a one-line fix has nothing to compare. Say that in one sentence and skip the table.

```markdown
`integration/next` 기준입니다.

| 항목 | 이전 | 이후 |
| --- | --- | --- |
| 첫 배치의 503 | 즉시 실패 | backoff로 재시도 |
| retry 대상 배치 | 두 번째 배치부터 | 전체 배치 |
| 실패 에러 | 배치 인덱스 없음 | 배치 인덱스 포함 |
```

## One More Section

Add a third section only for these triggers, and keep it as short as the others:

| Section | Add when |
| --- | --- |
| Migration or breaking change | Adopters must act. State what breaks and how to adapt. |
| Screenshots | A visual change is hard to judge from code. Show before and after when both matter. |

Everything else that used to earn a section, such as a tradeoff to weigh, a performance number, a rollout order, or a review focus, is one bullet or one sentence where it belongs, or a template field when the template asks for it.

## Cut List

Sentences of these kinds add length and no information. Delete them, or replace them with the fact they were avoiding.

| Pattern | Example | Instead |
| --- | --- | --- |
| Hedge or disclaimer | "This should not affect other modules." | Check, then either say what it affects or say nothing. |
| Self-appraisal | "Thoroughly tested and carefully reviewed." | Nothing; the checks and the diff speak. |
| Courtesy filler | "Let me know if you'd like any changes." | Nothing. |
| Announcement | "This PR aims to improve…" | Start with the problem. |
| Process narration | "First I investigated the logs, then…" | The finding, not the path to it. |
| Restated diff | "Renamed `foo` to `bar` in `a.py`, `b.py`, and `c.py`." | The outcome the rename achieves, once. |
| Chat reference | "As discussed", "follow-up to our conversation" | The decision itself, stated for a reader who was not there. |
| Deferral padding | "Further improvements could be made in a future PR." | A concrete non-goal, only when a reviewer would otherwise ask for it. |

## Validation And Checks

Do not add a validation or testing section. Automated results live in the forge's checks and the commit history; a prose copy goes stale and attracts filler. Two exceptions:

- The repository template or contributor guide asks for one. Answer its field in one or two lines.
- A check the reviewer will hit is red or skipped for a known reason. State that in one line where it belongs; it is a fact, not a section.

## Examples

Before, a body that says little in many words:

```markdown
## Summary

This PR aims to improve the reliability of the export job. As discussed, the job was sometimes failing. I investigated the logs and found the issue and fixed it. I have thoroughly tested this change and it should not affect other jobs.

## Changes

- Updated `export_job.py`
- Updated `retry.py`
- Added tests

## Validation

- Ran the full test suite locally, all green.
- Manually triggered the job three times.

Let me know if you would like any changes.
```

After, the same change:

```markdown
## Context

The nightly export failed whenever the warehouse returned a 503 during the first batch, because the retry wrapper only covered later batches. Customers then received no file that day.

## Changes

- Retry the first batch with the same backoff as the rest, so a transient 503 delays the export instead of dropping it.
- Fail the job after the retry budget is spent, with the batch index in the error.
```

The same change when the team reads PRs in Korean:

```markdown
## 배경

warehouse가 첫 배치에서 503을 반환하면 nightly export가 실패했습니다. retry wrapper가 첫 배치를 감싸지 않았기 때문이고, 그날 고객은 파일을 받지 못했습니다.

## 변경 사항

- 첫 배치도 나머지 배치와 같은 backoff로 재시도합니다. 일시적인 503은 export를 지연시킬 뿐 중단시키지 않습니다.
- retry 예산을 다 쓰면 배치 인덱스를 담은 에러로 작업을 실패 처리합니다.
```

## Where This Shape Comes From

The why-then-what core follows Google's [CL description](https://google.github.io/eng-practices/review/developer/cl-descriptions.html) guidance: a first line that says what, a body that says why. The testing section that many public templates carry, such as [Kubernetes](https://github.com/kubernetes/kubernetes/blob/master/.github/PULL_REQUEST_TEMPLATE.md) and [React](https://github.com/react/react/blob/main/.github/PULL_REQUEST_TEMPLATE.md), is left out on purpose: in a team repository the forge's checks are the live record, and the section filled with reassurance rather than information. Follow such a template when the repository has one.
