# Worked Drafts

Read this when the right shape for a draft is unclear. Every example is invented. Each shows the draft, the fields, and the one-line assignee decision, followed by why it is shaped that way. Copy the judgment, not the wording: the team's own convention still wins.

## Contents

- Bug relayed from chat, ownership ambiguous
- Wrong output in data or an evaluation
- Uncertain or research work, with its closing note
- Splitting one large in-progress issue
- Korean noun-phrase outline
- Overview table, a figure, and one collapsed block
- Local and server-only material with a pile of links

## Bug Relayed From Chat, Ownership Ambiguous

The user pastes a message from a support colleague and says "can you file this?". The user is not on the payments team.

```markdown
Title: `payment.succeeded` webhook delivered three times after a 503

> "Merchant says they got the payment.succeeded webhook three times for one
> charge after their endpoint returned a 503. They shipped the order three times."

Reported by support in the payments help channel: https://chat.example.com/archives/C042/p1726555

- Where: webhook delivery worker, production, one merchant so far
- Observed: three deliveries for one charge after a single 503. Event ids not checked yet.
- Expected: one delivery per event, or retries that reuse the event id so receivers can deduplicate
```

Fields: label `bug`, which the team already uses. No priority, cycle, or status set.

Assignee: left empty. The delivery worker belongs to the payments team and this is a report for their triage.

Why: the title states the symptom, because a report filed for another team's triage should not presume the fix. The reporter's words are quoted, attributed by role, and the conversation is linked, so nothing is lost in paraphrase. The draft does not invent a fact the reporter never gave. "Event ids not checked yet" tells the reader what to do next, so it is a fact and not a defensive disclaimer. There is no acceptance-criteria section and no background about how webhooks work.

## Wrong Output In Data Or An Evaluation

The user is running their own evaluation, found a systematic error, and will fix it. Because the fix is the author's own, the title names the target and the action instead of the symptom.

```markdown
Title: Fix day and month swap in receipt date extraction for en-GB receipts

| Input | Observed | Expected |
| --- | --- | --- |
| `Date: 03/04/2026` (locale en-GB) | `2026-03-04` | `2026-04-03` |

- 41 of 500 en-GB receipts in the evaluation set are affected, all with a day of 12 or lower
- Dataset revision: https://data.example.com/receipts-eval/revisions/18
- Parser settings: `doc-extraction: configs/date_parser.yaml` on `main`
```

Assignee: the author. It is the author's own evaluation work.

Why: one real input with observed and expected output says more than a description of the error class. The dataset revision is pinned, and the path names its repository and branch.

## Uncertain Or Research Work

The user wants to find out whether a reranker is worth its latency, and has named the candidates, the 1,200-query long-query set, the two metrics, and the shared experiment log. Had the user not supplied those, the draft would leave them out and the report would ask for them.

```markdown
Title: Reranker comparison table for long queries

Question: does a cross-encoder reranker raise recall@5 on queries over 30 tokens enough to justify its latency?

- Candidates: the current retriever alone, and with each of two cross-encoder rerankers
- Same 1,200-query long-query set and the same index snapshot for every run
- Deliverable: one table of recall@5 and p95 latency per candidate, with a recommendation
- Experiment log: https://docs.example.com/d/reranker-long-queries
```

Assignee: the author. No estimate, no sub-issues.

Closing note, added when the issue is closed:

```markdown
- Outcome: the larger reranker raises recall@5 from 0.71 to 0.78 at +140 ms p95. The smaller one is within run-to-run variation of the baseline.
- Decision: adopt neither for now, because the latency budget is 100 ms
- Table and runs: https://docs.example.com/d/reranker-long-queries
```

Why: the title names a deliverable, so the issue can be closed whatever the answer turns out to be, including "neither". The reasoning and the runs live in the experiment log. The issue carries two or three lines of outcome and the link.

## Splitting One Large In-Progress Issue

"Migrate the evaluation harness to the new runner" has been in progress for two weeks and the user asks to split it. Three separate lumps have shown up in the work so far.

Parent: left exactly as it is. It stays the record of the final outcome.

Sub-issues created:

- Port dataset loaders to the new runner
- Check metric parity between the old and new runner on the regression set
- Add the new runner to the nightly CI job, blocked by the loader port (set as a relation, not written in the body)

Not created:

- "Finish the migration". It names the parent's outcome again and has no separate work of its own.
- "Write migration docs". Nobody has started it and its size is a guess. It is mentioned in the report so the user can add it when it becomes real.

Assignee: the author on all three, set explicitly on each sub-issue. The user is doing this work.

Report line: "You already have three issues in progress, so I created all three sub-issues as not started. Tell me which one you are on now and I will move it, which makes four."

Why: sub-issues come from lumps that exist, not from a plan of what the work might contain. A sub-issue restates the parent when it names the parent's outcome again without work of its own. A real last step is different: a cutover with its own date and rollback steps becomes a sub-issue once that work exists. The in-progress count is raised with the user instead of silently growing.

## Korean Noun-Phrase Outline

A task the author will do, in a Korean tracker. The title is a noun phrase naming the target and the action. Bullet items end in a noun or read `label: value`, and established English terms stay in English.

```markdown
Title: 결제 webhook 5xx 응답 시 재시도 추가

- 대상: `payments-api`의 webhook 발송 worker
- 현상: 수신 서버의 503 응답에 재시도 없이 실패 처리
- 작업
  - 5xx와 timeout에 exponential backoff 재시도 3회
  - 재시도 소진 시 dead-letter queue 적재
  - 재시도 횟수 metric 추가
- 제보 원문 (지원팀 채널): https://chat.example.com/archives/C042/p1726555
```

The link line says what the link is. A bare `참고:` followed by a URL would not.

Not this, which narrates in past-tense sentences:

```markdown
수신 서버가 503을 반환했을 때 재시도를 하지 않고 실패 처리했습니다. 그래서 재시도 로직을 추가했고 metric도 넣었습니다.
```

## Overview Table, A Figure, And One Collapsed Block

The author is moving three nightly evaluation suites to a new runner and wants one issue a teammate can take in at a glance. The content is the same three fields over three suites, the hand-off between the runner and the result store is what people keep getting wrong, and the failing log is long but needed by whoever picks up the blocked suite. The draft is shown in GitHub's form; the collapsible form differs by tracker.

````markdown
Title: Move nightly evaluation suites to the batch runner

Nightly runs hit the 6 hour limit on the old runner twice last week.

| Suite | Nightly runtime now | State on the new runner |
| --- | --- | --- |
| Retrieval | 2 h 10 min | Runs, results match |
| Summarization | 3 h 40 min | Runs, 2 metrics differ |
| Long context | 5 h 50 min | Fails at result upload |

![Runner, queue, and result store](./nightly-flow.png)
Figure: the batch runner writes results to the queue and a separate worker uploads them to the result store, so an upload failure does not fail the run.

- Find why ROUGE-L and BERTScore differ on Summarization (tokenizer version is the first suspect)
- Fix the upload step for result files over 2 GB, which is what Long context produces
- Switch the nightly schedule once all three suites match

<details>
<summary>Upload failure log for Long context: the worker times out after 300 s on a 2.3 GB file</summary>

```text
02:14:07 upload start results/long-context/2026-09-16.parquet size=2.3GB
02:19:07 error: request timed out after 300s
02:19:07 retry 1/3 ...
```

</details>
````

Fields: no estimate. The figure is attached with the tracker's upload function, so the image reference resolves for every reader.

Assignee: the author. It is the author's own migration.

Why: the table comes right after the purpose sentence because three suites share three fields, every column has a header, the first column names each row, and no cell is longer than a few words. The figure earns its place because the hand-off it shows is the part readers misunderstand, and one visible line says what it shows. Only the log is collapsed: whoever takes the upload fix needs it, most readers do not, its summary line already gives the conclusion, and the tasks and findings stay visible. With the block closed the issue still reads complete. Had there been one suite, a sentence would replace the table; had the flow been a straight line, the figure would be dropped.

## Local And Server-Only Material With A Pile Of Links

The author analysed webhook latency and asks for an issue, saying "add these links". The report and plan are on the author's machine, the run output is on a batch server the team cannot log in to, and the links are a handful of loosely related pages. A first draft that points at all of it and states nothing:

```markdown
Title: Webhook latency

Details in the report: research/webhook-latency/REPORT.md
Plan: .plans/webhook-retry.md
Results: /data/runs/webhook-latency/2026-09-02/
Dashboard: http://10.0.3.17:3000/d/webhooks
An agent session ran the latency script in a local worktree; see the session notes.

Related:
- https://git.example.com/acme/payments-api/pull/398
- https://git.example.com/acme/payments-api/pull/412
- https://docs.example.com/d/queue-design-2024
- https://docs.example.com/d/webhooks-overview
- https://chat.example.com/archives/C042/p1726001
```

Running the check on each reference:

| Reference | Claim or action it supports | Opens for readers | Result |
| --- | --- | --- | --- |
| `research/.../REPORT.md`, `.plans/...` | The findings, but it stands in for them | No, author's machine only | Facts moved into the body, path removed, stated as not yet shared |
| `/data/runs/...` | The measurements | No. A bare path names no host or access condition, and the team cannot reach that server | Same |
| Dashboard on `10.0.3.17` | Lets a reader check the latency number | Only on the VPN | Kept, with the access condition beside it |
| Pull request 412 | The change the regression is attributed to | Yes | Kept, and the sentence says what it is |
| Pull request 398, two background documents, chat thread | None. Merely related | Yes | Dropped |
| "An agent session ran..." | None. Authoring context | Not applicable | Dropped |

The corrected draft:

```markdown
Title: Retry payment webhooks on 5xx responses

- p95 delivery latency rose from 0.8 s to 4.2 s after the queue change in pull request 412 (https://git.example.com/acme/payments-api/pull/412), measured over 7 days of production logs from 2 September
- Deliveries that receive a 5xx are never retried. They are 3.1% of all deliveries in that window.
- Live latency panel, to check the first number: http://10.0.3.17:3000/d/webhooks (VPN required)
- The analysis notes and the raw run output exist only on the author's machine and the batch server. There is no shared copy yet.
```

Shown to the user together with the draft before posting, because the check dropped links the user asked to include: "I put the two numbers into the issue and said plainly that the report and run output have no shared copy yet; tell me if you want them moved somewhere shared first. I dropped four links (pull request 398, two background documents, the chat thread) because no statement in the issue depends on them. I kept the dashboard with its VPN condition."

Why: the issue now commits to its findings in its own text, so a reader who opens nothing still knows what was found. Each remaining link is named and says why one would open it, and every sentence still reads correctly with its link removed. What is not shared is stated instead of hidden behind a path. The date and measurement window stay because a reader needs them to interpret the numbers; which agent ran what does not.
