# Writing Patterns

Choose a pattern by the reader's task. Each pattern names a writing action, shows what the finished prose can look like, and gives a reader check. All example paragraphs below are independently constructed **synthetic examples**, not excerpts, measured results, or anonymized company incidents. Public sources illustrate the writing technique.

## Contents

- [Explain a mechanism](#explain-a-mechanism)
- [Recommend a design](#recommend-a-design)
- [Report a measured difference](#report-a-measured-difference)
- [Explain a failure](#explain-a-failure)
- [Describe a migration](#describe-a-migration)
- [Write a periodic review](#write-a-periodic-review)
- [Teach a concept or procedure](#teach-a-concept-or-procedure)
- [Keep a living reference useful](#keep-a-living-reference-useful)

## Explain a mechanism

**Use when:** the reader recognizes the components but cannot explain their behavior together.

**Write:** start with one concrete input. Follow ownership and state through the components, then introduce the general rule. Add the failure branch that reveals an important invariant. Keep the component names stable between text, code, and diagram.

> The client submits a batch ID and its records. The coordinator leases that batch to one worker. The worker stores the output under the batch ID, then acknowledges completion. If the lease expires first, the coordinator can assign the batch again. Repeating the output write must therefore preserve the already stored result.

**Reader check:** can a reader identify what survives a crash, what can repeat, and which component acts next?

**Read:** [FoundationDB architecture](https://apple.github.io/foundationdb/architecture.html), role sections; [Figma multiplayer](https://www.figma.com/blog/how-figmas-multiplayer-technology-works/), the discussion of OT/CRDT influences and document structure. Figma describes a custom centralized system inspired by multiple CRDTs, not adoption of OT. Transfer the explanation of assumptions and relaxed requirements, not an algorithm label detached from its conditions.

## Recommend a design

**Use when:** the reader must choose between plausible approaches.

**Write:** establish the current constraint, explain the proposed change, and compare alternatives along the dimensions that decide the choice. Preserve the losing alternative's real advantage. Put a concrete consequence after the decision.

> Use the existing durable queue for the retry log. Consumers already use its delivery interface, and pending work must survive a process restart. An in-process queue avoids a network call, but satisfying the same durability requirement would add a separate persistence mechanism. The durable queue keeps recovery on the interface the consumers already implement.

**Reader check:** can the reader state why this option fits this situation and which changed requirement could favor another option?

**Read:** [CockroachDB distributed SQL RFC](https://github.com/cockroachdb/cockroach/blob/master/docs/RFCS/20160421_distributed_sql.md), alternatives and numbered examples; [Vercel CDN metadata](https://vercel.com/blog/how-we-cut-cdn-metadata-lookup-latency-by-91-percent), the section explaining why further shard reduction was not worth a rollout. Transfer common comparison dimensions and a reason to stop, not a compulsory scorecard.

## Report a measured difference

**Use when:** a result must support an engineering judgment.

**Write:** name the comparison and the measured difference, put the decisive conditions beside it, and show the cost or contrary result that changes the judgment. Separate the observation from its proposed explanation.

Synthetic input: the same replay contains 100 requests per configuration. Baseline completes 92; candidate completes 96. Successful-request median latency is 240 ms and 180 ms, respectively; other requests time out.

> The candidate's successful-request median latency was 180 ms, compared with 240 ms for the baseline, a 25% reduction on the same replay. It completed 96 of 100 requests; the baseline completed 92. The latency medians exclude timeouts. Repeated trials are needed to estimate run-to-run variation before using this difference as a release criterion.

The final sentence earns its place when release selection is the reader's task. For a narrow record of one replay, the measured observation can be sufficient.

**Reader check:** can the reader identify what was measured, the comparison population, and what the evidence supports? Can they distinguish a lower latency from a claim of statistical significance?

**Read:** [Jepsen etcd 3.4.3](https://jepsen.io/analyses/etcd-3.4.3), consistency documentation, test design, and results; [PEP 703](https://peps.python.org/pep-0703/#performance), configuration-specific performance; [LINE JVM profiling](https://engineering.linecorp.com/en/blog/profiling-a-simple-performance-issue-in-a-jvm-based-server/), the interpretation of profiling samples. Translate a broad promise into an observable test before writing its result.

## Explain a failure

**Use when:** the reader needs to understand an incident and prevent its mechanism recurring.

**Write:** open with user-visible impact and recovery state. Trace trigger, latent condition, propagation, mitigation, and evidence. Keep investigation time distinct from event time. Show the observation that changed a hypothesis rather than reproducing the whole investigation transcript.

> Requests reached an unavailable backend after the rollout changed the routing rule. The rollout log places the route change before the readiness check completed. Reverting the route restored responses. Add a gate that keeps the old route while readiness is pending, then exercise the failed-readiness path before the next rollout.

**Reader check:** can the reader connect a corrective action to a specific failure mechanism and tell what would demonstrate completion?

**Read:** [Slack's incident on 2-22-22](https://slack.engineering/slacks-incident-on-2-22-22/), mitigation and datastore-load analysis; [Brandur's Postgres queue investigation](https://brandur.org/postgres-queues), test bench and dead tuples; [Etsy's debriefing guide](https://www.etsy.com/codeascraft/debriefing-facilitation-guide), questions that recover the information available to responders. Use a dry register while retaining the investigation's useful reasoning.

## Describe a migration

**Use when:** a reader must implement, operate, or assess a staged change.

**Write:** show the old and new behavior, then describe stages with their concrete state, check, and recovery action. Put compatibility changes before the affected operation. Explain a validation gap where test and production conditions differ.

> First, separate the schema domains in application queries and enforce the boundary in CI. Keep the data on the existing cluster during this stage. Move a domain only after its queries satisfy the boundary and the migration's consistency checks pass. This separates query compatibility work from physical data movement.

This example demonstrates staged reasoning, not a complete executable database migration procedure.

**Reader check:** can the reader tell what changes at each stage and what evidence permits the next stage?

**Read:** [GitHub database partitioning](https://github.blog/engineering/infrastructure/partitioning-githubs-relational-databases-scale/), virtual partitions and SQL linters; [GitHub MySQL upgrade](https://github.blog/engineering/infrastructure/upgrading-github-com-to-mysql-8-0/), upgrade plan, rollback, and production-only query failures; [NAVER's Oracle-to-MySQL migration](https://d2.naver.com/helloworld/6512234), consistency and performance validation. Keep workload rates separate from partition counts.

## Write a periodic review

**Use when:** readers revisit measures and actions at a regular interval.

**Write:** relate the previous action to this period's observation, identify the relevant comparison, and propose the next action where the evidence calls for one. Attach human commentary to the same period and population as the data.

> The retry limit changed before this week's replay. The candidate completed 96 of 100 requests, compared with 92 for the baseline. All four remaining requests timed out. Inspect those requests before increasing the limit again; the current results do not identify whether another retry would complete them.

**Reader check:** can the reader connect the action, current evidence, and next useful investigation without interpreting a wall of KPI cards?

**Read:** [Evidence weekly review](https://business-review-demo.netlify.app/weekly-reports/2021/52), previous actions, measures with commentary, and next actions; [Wikimedia Movement Metrics](https://upload.wikimedia.org/wikipedia/commons/a/ab/February_2025_Wikimedia_movement_metrics.pdf), metric explanations, definition changes, and missing-data notes. Borrow Evidence's organization, not its inconsistent demo chronology or unsupported causal comments.

## Teach a concept or procedure

**Use when:** a reader needs a mental model or a task they can perform.

**Write:** begin with a small concrete example, tell the reader what to observe, then explain the rule. Add complexity when it answers the next question. For a procedure, place the expected result and failure branch beside the operation. For a visual explanation, name the input being changed and the output to compare.

> Start with one worker and a queue containing two jobs. Follow the first job from assignment to acknowledgement. Now delay its acknowledgement until the lease expires. Compare which worker owns the job and which output already exists. This case explains why a retry needs an idempotent write.

For an existing system, construct and exercise an authorized example before presenting it as a verified procedure. For a static document, show both states with labels rather than instructing the reader to drag a nonexistent control.

**Reader check:** can the reader explain the general rule from the example and repeat the relevant task?

**Read:** [Red Blob Games A* introduction](https://www.redblobgames.com/pathfinding/a-star/introduction.html), paired algorithm conditions; [Bartosz Ciechanowski's GPS](https://ciechanow.ski/gps/), a simple model refined in stages; [Reuters' blockchain explanation](https://www.reuters.com/graphics/TECHNOLOGY-BLOCKCHAIN/010070P11GN/index.html), one transaction followed through the explanation. Preserve the technical relation when adapting analogies.

## Keep a living reference useful

**Use when:** readers return for exact interfaces, current behavior, or changes between versions.

**Write:** organize by lookup task. Keep names, defaults, valid values, and errors precise. Link historical rationale to the current specification. Put a changed default with its effect and migration option. State data extraction time or archive status when freshness changes use.

> The new configuration defaults to bounded retries. Existing callers that rely on unlimited retries must set that policy explicitly before upgrading. The configuration reference describes the current default; the decision record explains why it changed.

**Reader check:** can the reader find the current rule and distinguish it from a historical proposal or result?

**Read:** [SQLite 3.45.0 release notes](https://www.sqlite.org/releaselog/3_45_0.html), defaults and build identity; [CPython Argument Clinic](https://devguide.python.org/development-tools/clinic/), task-specific documentation modes; [Eurostat population structure](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Population_structure_and_ageing), extraction and planned-update dates. An update timestamp is useful metadata, not a substitute for keeping the content current.
