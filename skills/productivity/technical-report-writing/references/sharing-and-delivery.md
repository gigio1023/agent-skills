# Sharing and Delivery

Read this when a document is about to leave the author's machine, when its recipients or distribution change, and again after any rewrite of a shared copy. It carries the recipient, source-access, sharing-pass, and delivery rules that lived in Gigio Pack's `share-internal-doc` until 2026-09-24; the sharing pass is user-set policy from two review rounds over nine shared reports in September 2026. Document craft stays in SKILL.md and is not repeated here.

## Latest shared copy

When colleagues or the user have edited the shared copy, retrieve that version before any revision or republication and treat it as the current baseline. Reconcile differences with the local source before rebuilding; intentional deletions and intervening edits stay. Familiarity with the original draft is not evidence that the shared copy is unchanged.

## Recipients and sources

- Match detail and attribution to the audience. Page ownership or the sharing message already names the author; no introductory byline, no "the author's synthesis" paragraph, and no sentence that repeats why the page is shared.
- Keep an action owner or observation date when it changes meaning. Preserve relevant events and accountability without personal evaluation, and add no explanation whose only job is to show caution.
- Every claim the reader must verify cites a source the reader can open: a Slack permalink, a Notion page, a GitHub blob pinned to a commit, an issue, a public source. Inspect the destinations: a bare Markdown filename linked as a website, a localhost address, a `vscode://` link, and a private local path are not team citations. Replace them with an authorized link or with the supported explanation itself. No folder inventory and no blanket source disclaimer; when essential access is unavailable, state that concrete limitation once.
- Restricted working records do not travel with the document.

| Distribution | Links allowed | Pass depth |
| --- | --- | --- |
| Author only | Anything, including local paths | Credential hygiene |
| Team | Links the team opens with normal access; internal key and system names stay | Passages about named colleagues, claims stated beyond the record |
| Whole company (Notion, all-hands) | Company-wide links only; no author-machine path | Everything below |
| Outside the company | Public sources only | Not covered here |

## Sharing pass

Two questions, answered separately; clearing one does not clear the other.

1. Would this embarrass the company: customer defects tied to names, unresolved security items, unpublished deals, competitor remarks, confidential coordinates.
2. Would this embarrass the person posting it: personal positioning, political calculus about when to raise a concern, judgments about a colleague's honesty or a paper's transparency, a new hire acting as auditor, methodology that reads as surveillance (counting private messages read, searching channels one is not a member of).

For internal sharing the author narrowed an over-eager pass: internal key names were fine, and the substance to tighten was claims whose scope or date was stated more strongly than the record supports (a founding month written as fact when only a quarter was confirmed). Genuine past failures are not deleted because they may have been fixed since.

### People

| Keep | Change |
| --- | --- |
| Real names on facts: owner, author, speaker, decision maker | Sentences that read as evaluations of attitude, ability, or workload, rewritten as structural statements ("검토 요청이 한 채널에 몰려 있습니다" rather than "이 팀은 응답이 느립니다") |
| Customer company names and internal ticket numbers, because the person acting on the item needs them | Names of individual customer contacts |
| Unaddressed security items, flagged with a handling notice | Coordinates that would let a reader find the confidential data itself |

Return findings to their original source so the document is not the judge ("지난 분기 보고서는 이 구간을 진단했습니다" rather than "검사한 표본 대부분에 결함이 있었습니다"). Where two conventions exist, describe both. Turn open questions into action guidance ("문의가 오면 원본 문서로 답합니다") instead of doubt. Named colleagues see their passages before wider circulation; this is a review obligation to honor, not authority to contact people the user did not name.

### Always remove

- Credentials and secrets, including cookies and tokens visible in screenshots; write `[REDACTED]`.
- Coordinates of confidential data: repository names, file paths, Notion page titles, channel names that lead to it.
- Author, role, and result figures of submissions under anonymous review.
- Reproducible bypass values: user-agent strings, system prompt text, OAuth client identifiers, working attack prompts or payloads. Technique family, counts, sources, and judge design may stay; CBRN operational detail never does.
- Personal HR information: probation, employment terms, leave.
- Competitor mockery quoted with the speaker's name.
- Uncensored-model techniques and offensive tooling detail in defensive documents.

### Depersonalize

- Second-person address and "about my role" framing ("<이름>님께 제안된", "<이름>님의 역할은") become role language: "신규 입사자", "AI Engineer".
- Wall-clock timestamps that reveal when the author worked become relative gaps; a sentence naming the specific small models used becomes a role description. Generalize; do not leave a hole.
- Session narration ("복구했다", "헤드리스", "폴백", "빌드 스크립트") moves to a methods appendix in the reader's language, or goes.
- Statements that assume the conversation ("이번 주", "오늘 푸시", "1차 리포트 대비") become statements verifiable inside the document.
- Removed coordinates go to the security owner in a separate handoff, never with the document.

A build script that regenerates the shared copy from the original has held up better than editing the original: span rules between anchors plus literal replacements, and a forbidden-token check that fails the build when a personal name, `/Users/`, `vscode://`, an external `<script src>`, or a local relative link survives. Publication is staged: private page first, wider circulation after the pass and after named people have seen their passages. If Korean text corrupts during a publish, stop the batch.

## Delivery

Inspect the actual destination after rendering, conversion, or publication: complete content, visible row and column labels, readable cells, list hierarchy, equations, figure size and numbering, captions, and working source links. For a collapsible document, check the initial view and representative expanded content. Distinguish a retrieved-content check from a visual check, and never report a rendered view as inspected when only its source was read. Re-fetch what was published and diff it against the source; a Notion replacement of 192 items once applied only 100 silently.

Publication needs its own authorization: preparing a document does not authorize sending, publishing, committing, or installing anything, and an existing grant is reused instead of asked for again. Return the artifact, its path or URL, and any material delivery limitation. The originals stay unchanged.
