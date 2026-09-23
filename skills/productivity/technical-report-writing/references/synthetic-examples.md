# Synthetic Examples

Use these contrasts to diagnose why a sentence, table, or figure is less useful, then keep the operation the stronger version demonstrates. Every example is independently constructed: its names, numbers, and events are not measurements of a real system or anonymized company records, and they are never copied into a real document. For prose and displays working together in one document, start with [finished examples](finished-examples.md).

## Contents

- Structural repairs: [paragraph table](#paragraph-table), [table split](#table-split), [heading and cell phrases](#heading-and-cell-phrases), [figure split](#figure-split), [genre transfer](#genre-transfer), [row identity](#row-identity), [internal aliases](#internal-aliases), [list hierarchy](#list-hierarchy).
- Prose rewrites: [observation and explanation](#separate-an-observation-from-its-explanation), [broad promise](#turn-a-broad-promise-into-an-observable-test), [alternative](#compare-an-alternative-fairly), [failure sequence](#keep-the-failure-sequence-without-blame), [untested condition](#name-the-untested-condition-readers-would-assume), [definition](#define-the-measurement-not-the-familiar-word), [Korean relations](#restore-the-relation-in-korean).

## Structural repairs

### Paragraph table

**Reader:** an engineer comparing two document-indexing configurations.

**Before:**

| Item | Content |
| --- | --- |
| Method | Documents are indexed either during the upload request or later by a worker. The second configuration writes a durable job first. |
| Result | Direct indexing takes 800 ms before acknowledging upload. Queued indexing takes 80 ms to acknowledge and 3 seconds to make the document searchable. |
| Meaning | Queued indexing acknowledges earlier, but users must wait for the worker before their document appears in search. |

The rows are different parts of an argument; the grid compares nothing.

**After:**

**Upload and search latency**

| Configuration | Upload acknowledgment | Search availability |
| --- | ---: | ---: |
| Direct indexing | 800 ms | 800 ms |
| Queued indexing | 80 ms | 3 s |

Queued indexing acknowledges the upload after saving a durable job. A worker then updates the search index. This shortens the upload wait while delaying search availability.

The table compares values; the paragraph explains why they differ. No paragraph explaining how to read the columns is needed.

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

Stable path names connect the views. The second table earns its place only when maintenance affects the choice.

### Heading and cell phrases

**Before heading:** “Why does the worker retry the same job?” **After:** “Job retries”

**Before cell under “Retry policy”:** “The worker retries a failed job at most three times.” **After:** “Up to 3 retries”

**Explanatory sentence:** “The worker retries the job when the result is not acknowledged before the lease expires.”

Headings and cells stay compact while the sentence supplies the operation and condition. Do not apply a complete-sentence prose rule to labels. In Korean, use “작업 재시도” as the heading and “최대 3회” in the cell, and keep the relation in prose: “워커는 리스가 만료될 때까지 처리 결과가 확인되지 않으면 작업을 다시 시도한다.”

### Figure split

**Before:** one diagram combines a request path, a database schema, a release timeline, and two latency charts. Small type and four legends make everything fit, but the reader must infer which parts explain runtime behavior.

**After figure plan:**

| View | Question | Contents |
| --- | --- | --- |
| Request lifecycle | Where does a request wait? | Client, queue, worker; submit, dequeue, and acknowledge edges |
| Queue latency | Which configuration reduces waiting? | Matched baseline and candidate distributions |

Explain the durable job record beside the lifecycle only if recovery needs it. Keep the full schema in the implementation reference. Omit the release timeline when it explains neither result. The matched distributions belong together because comparing them is the task.

### Genre transfer

**Synthetic input:** a stale queue lease prevented a job from being reassigned; the operator reset the lease; the job then completed.

**Factual incident record:**

- **Observation:** Job retained an expired lease.
- **Response:** Operator reset the lease.
- **Result:** Another worker completed the job.

**Technical explanation:** The queue records the worker assigned to a job in a lease. When that worker stops, the lease must expire before the queue assigns another worker. If reassignment still treats the expired lease as active, the job remains blocked.

**Proposal:** Allow reassignment after lease expiry and give each assignment a new generation number. Reject acknowledgments from older generations so a delayed worker cannot complete a reassigned job. A longer lease alone would delay recovery without handling stale acknowledgments.

The record is enough for its reporting task. The explanation adds the mechanism; the proposal adds the changed behavior and the reason to choose it. Reusing the incident bullets for all three would remove necessary content.

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

The corner heading names both dimensions, and each row states the requirement assessed. If row labels existed but their dimension was unnamed, repair the header alone.

### Internal aliases

**Before:** “Run the classifier on review-set-r3. This is our gold-standard dataset.”

**After:** “Evaluate the classifier on the labeled support-ticket dataset (internal ID: `review-set-r3`). Labels come from a mix of human review and automated rules.”

The source establishes mixed label origins, not a validation process. The edit states the role and keeps the lookup ID without claiming that every label was validated. Use “labeled dataset” afterward, and omit the ID when readers will not look it up.

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

The hierarchy separates two workstreams, their actions, and the cases within one check; the third level exists only for that subdivision. Causal reasoning may still read better as a paragraph.

## Prose rewrites

### Separate an observation from its explanation

**Before:** “The cache eliminated the bottleneck and proved that network traffic was the cause.”

**After:** “With the cache enabled, the replay issued fewer remote reads. The run did not measure network wait separately, so it does not establish whether the latency change came from network wait or server-side work.”

The second sentence names the competing explanations that affect the conclusion. Do not weaken the observation with vague hedges, or treat the missing measurement as evidence that neither explanation holds.

### Turn a broad promise into an observable test

**Before:** “The pipeline guarantees exactly-once processing.”

**Test first:** stop the worker after it writes output and before it acknowledges, let the coordinator reassign the batch, and count output rows per input record.

**After:** “When the worker stopped between the output write and its acknowledgment, the reassigned batch left one output row for each of the 500 records; the second write replaced the first under the same batch ID.”

The promise becomes behavior a reader can check, and the sentence reports that behavior. Design the test before writing the result. If it has not run, state the check that remains instead of the promise.

### Compare an alternative fairly

**Before:** “A managed queue is the best choice because it is scalable, reliable, and easy to maintain.”

**After:** “Use the managed queue for the retry log because the consumers already use its delivery and retention interface and pending retries must survive a restart. An in-process queue avoids a network call per message, but meeting the same durability requirement would add a second persistence mechanism.”

The losing option keeps its real advantage, and the choice follows from a stated requirement. The reader can name the change that would reverse it: if retries could be dropped on restart, the in-process queue wins. Verify delivery and retention behavior before writing this rationale.

### Keep the failure sequence without blame

**Before:** “An operator mistake caused a major outage, showing that our process needs improvement.”

**After:** “Requests reached an unavailable backend after the rollout replaced the routing rule. The rollout log places the route change before the backend's readiness check completed; the procedure has no gate between those steps. Reverting the route restored responses.”

The rewrite names the sequence and the missing control instead of a person. Event times come from the records; when the team learned each fact is investigation time and stays separate. A real postmortem distinguishes a confirmed sequence from a suspected cause. “Gate the route change on backend readiness and exercise the failed-readiness path” is an action; “improve the process” is not.

### Name the untested condition readers would assume

**Before:** “This document is a static snapshot rather than a live operational dashboard. It includes prepared and verified items but does not establish production readiness.”

**After:** “The configuration check passed. The service has not been run under load.” In Korean: “설정 파일 검사를 마쳤다. 부하 테스트는 아직 실행하지 않았다.”

Keep the second sentence when a reader could otherwise act as if load behavior had been tested, for example in a launch decision. Delete it when load is not part of the reader's decision; a list of everything the author did not check is cover, not a limit.

### Define the measurement, not the familiar word

**Before:** “Latency is the time a request takes. The metric must be interpreted with awareness of its definition.”

**After:** “Latency is measured from enqueue to final response, including retries.”

Keep this definition when it differs from what the intended audience would assume. If a table heading or methods section already carries the boundary, do not repeat it.

### Restore the relation in Korean

**Before:** “재시도 안정성 확보 및 처리 일관성 보장.”

**After:** “워커는 출력을 모두 저장한 뒤에 batch 처리 완료 응답(ack)을 보낸다. 재시도하면 이미 저장된 출력이 남아 있을 수 있으므로, 같은 batch를 다시 써도 결과가 달라지지 않아야 한다.”

The rewrite restores who acts, in what order, and what must hold. It keeps the technical identifiers, uses Korean verbs for ordinary actions, and replaces a guarantee with the condition the implementation must satisfy.
