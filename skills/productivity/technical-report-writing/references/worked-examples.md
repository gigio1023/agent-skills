# Worked Examples

Use these to inspect the actual sentence, paragraph, table, and caption decisions, not only the document outline. The first section analyzes public documents. Every example in the second section is synthetic and constructed for teaching; its numbers and events are not measurements of a real system or anonymized company records.

## Contents

- Public readings: [PEP 703](#pep-703-separate-the-measured-cost-from-the-intended-benefit), [Rust RFC](#rust-rfc-2394-give-a-concrete-mental-model-before-precise-semantics), [MapReduce](#mapreduce-explain-an-experimental-curve-through-system-behavior), [Circuit Tracing](#circuit-tracing-tie-a-limitation-to-a-counterexample).
- Prose: [mechanism](#replace-praise-with-the-mechanism), [proposal status](#keep-a-proposal-from-sounding-implemented), [observation and explanation](#separate-an-observation-from-its-explanation), [alternative](#compare-an-alternative-fairly), [failure sequence](#keep-the-failure-sequence-and-remove-blame).
- Evidence display: [comparison conditions](#preserve-the-comparison-conditions-in-a-compact-result), [table](#make-a-table-carry-repeated-context-once), [caption](#give-a-caption-a-job-distinct-from-the-title).
- Concision and language: [self-description](#remove-report-self-description), [definition](#define-the-measurement-not-the-familiar-word), [Korean relations](#restore-the-relation-in-korean).

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

Title: “The tail grows when backup tasks are disabled.”

Caption: “Completion time by worker for the same input partitioning. The right panel disables speculative backup tasks; all other tested settings are unchanged.”

The synthetic title carries the observed pattern, while the caption identifies the comparison. The body would explain how the tail affects total completion time if the supplied data supports that consequence. Do not add another sentence telling readers that the chart demonstrates the importance of robust orchestration.

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
