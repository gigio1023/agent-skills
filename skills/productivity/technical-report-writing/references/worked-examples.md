# Worked Examples

Use these to inspect sentence, paragraph, table, figure, and caption decisions, not only the document outline. Structural repairs and synthetic rewrites are independently constructed teaching examples; their numbers and events are not measurements of a real system or anonymized company records. The public readings analyze the cited documents.

For prose and displays working together, start with [finished examples](finished-examples.md); for a single explanatory paragraph, use [writing patterns](writing-patterns.md). Use the contrasts here to diagnose why a sentence or display is less useful, then retain the action and result demonstrated by the stronger version.

## Contents

- Structural repairs: [paragraph table](#paragraph-table), [table-split](#table-split), [heading-and-cell-phrases](#heading-and-cell-phrases), [figure-split](#figure-split), [genre-transfer](#genre-transfer).
- Reader context: [row identity](#row-identity), [internal aliases](#internal-aliases), [list hierarchy](#list-hierarchy).
- Public readings: [PEP 703](#pep-703-separate-the-measured-cost-from-the-intended-benefit), [Rust RFC](#rust-rfc-2394-give-a-concrete-mental-model-before-precise-semantics), [MapReduce](#mapreduce-explain-an-experimental-curve-through-system-behavior), [Circuit Tracing](#circuit-tracing-tie-a-limitation-to-a-counterexample).
- Prose: [mechanism](#replace-praise-with-the-mechanism), [proposal status](#keep-a-proposal-from-sounding-implemented), [observation and explanation](#separate-an-observation-from-its-explanation), [alternative](#compare-an-alternative-fairly), [failure sequence](#keep-the-failure-sequence-and-remove-blame).
- Evidence display: [comparison conditions](#preserve-the-comparison-conditions-in-a-compact-result), [table](#make-a-table-carry-repeated-context-once), [caption](#give-a-caption-a-job-distinct-from-the-title).
- Concision and language: [self-description](#remove-report-self-description), [definition](#define-the-measurement-not-the-familiar-word), [Korean relations](#restore-the-relation-in-korean).

## Structural repairs

These examples are independently synthetic. They teach editorial decisions without reproducing private documents, source identities, measurements, or incident details.

### Paragraph table

**Reader:** an engineer comparing two document-indexing configurations.

**Before:**

| Item | Content |
| --- | --- |
| Method | Documents are indexed either during the upload request or later by a worker. The second configuration writes a durable job first. |
| Result | Direct indexing takes 800 ms before acknowledging upload. Queued indexing takes 80 ms to acknowledge and 3 seconds to make the document searchable. |
| Meaning | Queued indexing acknowledges earlier, but users must wait for the worker before their document appears in search. |

The rows are different parts of an argument. The grid does not provide a comparison.

**After:**

**Upload and search latency**

| Configuration | Upload acknowledgment | Search availability |
| --- | ---: | ---: |
| Direct indexing | 800 ms | 800 ms |
| Queued indexing | 80 ms | 3 s |

Queued indexing acknowledges the upload after saving a durable job. A worker then updates the search index. This shortens the upload wait while delaying search availability.

The compact table compares values; the short paragraph explains why they differ. The heading is a noun phrase. No paragraph explaining how to read the columns is needed.

### Table split

**Reader:** a team selecting an export path for two independent needs: output behavior and maintenance responsibility.

**Before:**

| Path | Output and delivery | Scheduling and ownership |
| --- | --- | --- |
| On demand | CSV is generated when requested and returned by HTTP; each export covers the selected account. | No schedule is used; the API team maintains the handler. |
| Scheduled | A daily Parquet file covers all accounts and is written to object storage. | The scheduler runs nightly; the data team maintains the worker. |

**After:**

**Export behavior**

| Path | Format | Delivery | Coverage |
| --- | --- | --- | --- |
| On demand | CSV | HTTP response | Selected account |
| Scheduled | Parquet | Object storage | All accounts |

**Maintenance**

| Path | Trigger | Owner |
| --- | --- | --- |
| On demand | Request | API team |
| Scheduled | Nightly schedule | Data team |

Stable path names connect the views. Choose the first table alone when the reader only needs the output contract. The second table earns its place only when maintenance affects the choice.

### Heading and cell phrases

**Before heading:** “Why does the worker retry the same job?”

**After heading:** “Job retries”

**Before cell under “Retry policy”:** “The worker retries a failed job at most three times.”

**After cell:** “Up to 3 retries”

**Explanatory sentence:** “The worker retries the job when the result is not acknowledged before the lease expires.”

Headings and cells remain compact while the sentence supplies the operation and condition. Do not apply a complete-sentence prose rule to labels.

The same distinction applies in Korean: use “작업 재시도” as the heading and “최대 3회” in the retry-limit cell. Keep the relation explicit in prose: “워커는 리스가 만료될 때까지 처리 결과가 확인되지 않으면 작업을 다시 시도한다.”

### Figure split

**Before:** one diagram combines a request path, a database schema, a release timeline, and two latency charts. Small type and four legends make every element fit, but the reader must infer which parts explain runtime behavior.

**After figure plan:**

| View | Question | Contents |
| --- | --- | --- |
| Request lifecycle | Where does a request wait? | Client, queue, worker; submit/dequeue/acknowledge edges |
| Queue latency | Which configuration reduces waiting? | Matched baseline/candidate distributions |

Explain the durable job record beside the lifecycle only if it is needed to understand recovery. Keep the full schema in the implementation reference. Omit the release timeline when it does not explain either result.

The first view establishes the mechanism; the second provides the comparison. A reader can follow either without interpreting unrelated deployment or history panels. A pair of matched distributions belongs together because comparing them is the task.

### Genre transfer

**Synthetic factual input:** a stale queue lease prevented a job from being reassigned; the operator reset the lease; the job then completed.

**Factual incident record:**

- **Observation:** Job retained an expired lease.
- **Response:** Operator reset the lease.
- **Result:** Another worker completed the job.

**Technical explanation:**

The queue records the worker assigned to a job in a lease. When that worker stops, the lease must expire before the queue assigns another worker. If reassignment still treats the expired lease as active, the job remains blocked.

**Proposal:**

Allow reassignment after lease expiry and give each assignment a new generation number. Reject acknowledgments from older generations so a delayed worker cannot complete a reassigned job. Increasing the lease duration alone would delay recovery without handling stale acknowledgments.

The factual record is enough for its reporting task. The explanation adds the missing mechanism; the proposal adds the changed behavior and the reason to choose it. Reusing the incident bullets for all three would remove necessary content.

### Row identity

**Before:** the columns name delivery options, but blank row headings leave the reader to infer that the rows are requirements.

| | Live updates | Daily digest |
| --- | --- | --- |
| | Yes | No |
| | No | Yes |

**After:**

| Requirement / Delivery option | Live updates | Daily digest |
| --- | --- | --- |
| Immediate notice | Yes | No |
| One scheduled message | No | Yes |

The corner heading names both dimensions, and each row states the requirement being assessed. If row labels already existed but their dimension was unnamed, repair the header alone. Do not add a paragraph decoding row order.

### Internal aliases

**Before:** “Run the classifier on review-set-r3. This is our gold-standard dataset.”

**After:** “Evaluate the classifier on the labeled support-ticket dataset (internal ID: `review-set-r3`). Labels come from a mix of human review and automated rules.”

The source for this teaching case establishes mixed label origins, not a gold-standard validation process. The edit explains the role and preserves the lookup ID without asserting that all labels were validated. Use “labeled dataset” in subsequent explanation. Omit the internal ID altogether when the reader will not need it.

### List hierarchy

**Before:**

- Search rollout: build the index, check phrase queries and category filters, compare incremental updates with a full rebuild, enable a pilot, check latency, and disable the pilot if results are incomplete.

**After:**

- Index correctness
  - Build the initial index.
  - Compare incremental updates with a full rebuild.
  - Check query behavior.
    - Phrase queries preserve word order.
    - Category filters exclude other categories.
- Pilot rollout
  - Enable search for the pilot group after correctness checks pass.
  - Measure request latency under pilot traffic.
  - Disable the pilot if indexed results are incomplete.

The hierarchy distinguishes two workstreams, their actions, and the cases within one check. It uses a third level only for that real subdivision. A short, independent observation can remain a single-level bullet; causal reasoning may still read better as a paragraph.

## Public documents: read the writing operation

### PEP 703: separate the measured cost from the intended benefit

In [Performance](https://peps.python.org/pep-0703/#performance), the author first identifies the configuration whose overhead is measured, then separates single-threaded and multithreaded cases in a table. The table names pyperformance 1.0.6 and the hardware; the following paragraph identifies baseline revision `018be4c` and explains the implementation factors behind the overhead. A nearby statement keeps the result from being applied to the default build.

The useful pattern is not “always add a limitations section.” It is: identify the changed configuration, expose the comparable rows, attach the baseline, and explain the mechanism. The current reader should not have to infer that a proposed ability to exploit more cores and measured interpreter overhead are different quantities. Preserve the historical setting; these numbers are not a claim about current Python releases.

### Rust RFC 2394: give a concrete mental model before precise semantics

The [guide-level explanation](https://github.com/rust-lang/rfcs/blob/f17e8623ee2e2854570dcdb936a9f4ab08c0fcd4/text/2394-async_await.md#guide-level-explanation) explains that calling an async function constructs a future rather than immediately executing the body, then shows a small example and the observable print order. The reference-level explanation describes the generated type, state, trait bounds, and lifetime capture. The alternatives section explains why the exposed return type was chosen, including the ergonomic cost of the alternative.

Borrow the progression from observable behavior to the semantics needed to implement or review it. Do not copy this RFC's provisional `await!` syntax into current code. Its postponed decisions and rejected alternatives are different categories; preserve that distinction without narrating what RFC categories mean in every proposal.

### MapReduce: explain an experimental curve through system behavior

In [section 5, especially Figure 3](https://storage.googleapis.com/gweb-research2023-media/pubtools/4449.pdf), the authors first state the computations and cluster configuration. The normal, no-backup, and worker-failure executions then share corresponding input, shuffle, and output plots. The text connects features of the curves to task scheduling, intermediate data movement, and output replication. Startup overhead is included when total elapsed time is reported.

Borrow the chain from experimental setup to a visible change and then to its supported mechanism. A bare “faster” headline would discard the useful explanation. A dashboard can use aligned panels for the same comparison; a PDF can retain the panels and explanatory paragraph without an interactive shell.

### Circuit Tracing: tie a limitation to a counterexample

In [Missing Attention Circuits](https://transformer-circuits.pub/2025/attribution-graphs/methods.html), the authors describe what follows from fixing attention patterns, then use cases where the graph misses the computation of interest. The validation discussion distinguishes claims derived from a replacement model from interventions in the underlying model.

Borrow the local chain: methodological choice → what remains observable → what can be missed → a concrete counterexample or validation test. Do not copy every enthusiastic phrase or analogy. The point is to preserve information that changes the interpretation, not to pad a report with disclaimers about all possible limitations.

## Synthetic rewrites

### Replace praise with the mechanism

Before: “The platform provides robust and seamless recovery through an advanced orchestration layer.”

After: “The coordinator requeues an unacknowledged batch after its lease expires. A worker commits the output before acknowledging the batch, so a retry must tolerate output that already exists.”

The rewrite names actors, state, ordering, and the consequence. It does not claim that all recovery paths work. The second sentence belongs because it changes the implementation requirement, not because every paragraph needs a caveat.

### Keep a proposal from sounding implemented

Before: “The service stores a cursor after each commit and supports safe resumption.”

After, when the design is only proposed: “Store the cursor after the batch commit. On restart, resume from the last durable cursor and replay any unacknowledged batch. This requires an idempotent output write.”

The paragraph states the proposed behavior and the condition that makes it usable. “Safe” is replaced by the actual replay semantics. If the system already implements this behavior, describe it in the present tense and cite its implementation or specification.

### Separate an observation from its explanation

Before: “The cache eliminated the bottleneck and proved that network traffic was the cause.”

After: “With the cache enabled, the replay issued fewer remote reads. The run did not measure network wait separately, so it does not establish whether the latency change came from network wait or server-side work.”

The second sentence names the competing explanations that affect the conclusion. Do not weaken the first observation with several vague hedges, or treat the missing measurement as evidence that neither explanation is true.

### Preserve the comparison conditions in a compact result

Synthetic setup: two configurations each receive the same 100 requests. The baseline completes 92 and the candidate completes 96. Successful-request median latency is 240 ms and 180 ms, respectively; the other requests time out.

Before: “The candidate is 25% faster and significantly more reliable.”

After: “On the same 100-request replay, successful-request median latency was 240 ms for the baseline and 180 ms for the candidate, a 25% reduction. The baseline completed 92 requests and the candidate completed 96. Timed-out requests are excluded from the latency medians.”

The synthetic arithmetic supports the relative reduction, not statistical significance, causality, or a population-wide reliability claim. The timeout note is short and adjacent because it changes the meaning of the medians. No generic statement about the report's scope is needed.

### Make a table carry repeated context once

Using the same synthetic setup:

| Configuration | Completed / attempted | Successful-request median latency (ms) |
| --- | ---: | ---: |
| Baseline | 92 / 100 | 240 |
| Candidate | 96 / 100 | 180 |

Note: timed-out requests are excluded from latency medians.

The columns expose both denominators and the latency population. A neighboring paragraph should explain the decision or uncertainty rather than repeat all six values. A “verified” column would add no measurement. Keep the full failed-request definition in methods only if the short note is insufficient.

### Give a caption a job distinct from the title

Title: “Worker completion times with and without backup tasks”

Caption: “The right panel has a longer tail after speculative backup tasks are disabled. Input partitioning and all other tested settings are unchanged.”

The synthetic title names the comparison, while the caption states the pattern and its conditions. The body would explain how the tail affects total completion time if the supplied data supports that consequence. Do not add another sentence telling readers that the chart demonstrates the importance of robust orchestration.

### Compare an alternative fairly

Before: “A managed queue is the best choice because it is scalable, reliable, and easy to maintain.”

After: “Use the managed queue for the retry log because the consumers already use its delivery and retention interface. An in-process queue avoids network calls, but its contents disappear when the process exits; retaining the retry log across restarts would require a second persistence mechanism.”

The alternative retains a real advantage. The decision follows from a stated durability requirement rather than unsupported scoring or a claim that one option is universally better. If delivery guarantees or retention are not known, verify them before writing this rationale.

### Keep the failure sequence and remove blame

Before: “An operator mistake caused a major outage, showing that our process needs improvement.”

After: “The rollout replaced the routing rule before the new backend passed its readiness check. Requests then reached an unavailable backend. The rollout procedure has no gate between those steps.”

The synthetic explanation names the sequence and the missing control. A real postmortem would support it with the relevant events and distinguish a confirmed sequence from a suspected cause. An action such as “gate the routing change on backend readiness and test the failed-readiness path” is more specific than “improve the process.”

### Remove report self-description

Before: “This document is a static snapshot rather than a live operational dashboard. It includes prepared and verified items but does not establish production readiness.”

After, when readers only need the result: “The configuration check passed. The service has not been exercised under load.”

If the date matters, display the data date once. If production readiness is not part of the reader's decision, omit that topic instead of explaining its exclusion. If readiness does matter, name the missing test rather than adding a general disclaimer.

### Define the measurement, not the familiar word

Before: “Latency is the time a request takes. The metric must be interpreted with awareness of its definition.”

After: “Latency is measured from enqueue to final response, including retries.”

Keep this definition when it differs from what the intended audience would assume. If a table heading or established methods section already carries the boundary, avoid repeating it.

### Restore the relation in Korean

Before: “재시도 안정성 확보 및 처리 일관성 보장.”

After: “Worker는 출력 저장이 끝난 뒤 batch를 acknowledge한다. 재시도할 때 이미 저장된 출력이 있을 수 있으므로 같은 batch를 다시 써도 결과가 달라지지 않아야 한다.”

The rewrite restores who acts, in what order, and what must hold. It preserves technical identifiers rather than replacing them with unclear formal nouns. It also replaces a guarantee with the condition the implementation must satisfy.

Before: “필터 변경 시 결과 해석 범위 상이함에 유의해야 한다.”

After: “필터를 변경하면 제목과 비율도 선택한 데이터로 다시 계산한다.”

For an implementation document, this is a concrete behavior requirement. In a reader-facing dashboard, implement it rather than displaying the instruction as prose. If the headline intentionally describes a fixed analysis, separate that analysis from the filtered view.

Before: “본 검토는 준비 작업의 완료를 의미하며 실질적인 운영 가능성을 보장하는 것은 아니다.”

After: “설정 파일 검사를 마쳤다. 부하 테스트는 아직 실행하지 않았다.”

The result is clear without teaching a taxonomy of completion. Retain the second sentence when the reader could otherwise act as if load behavior had been tested; delete it when it is irrelevant to the requested document.
