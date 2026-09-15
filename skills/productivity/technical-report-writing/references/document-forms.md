# Engineering Document Forms

Use when choosing or revising a technical document's structure. Begin with the reader's task and the governing project template. The questions below guide content selection; they are not a universal section checklist. Read a real exemplar through [source readings](source-readings.md) when its form is unfamiliar.

## Technical report or experiment report

The reader needs to know what was tested, what happened, why the result is informative, and what it changes. Open with the question and supported result. Then expose the decisive evidence and the method needed to interpret it. A report can lead with a negative result or an unresolved comparison; it does not need a positive product story.

Connect the chain: hypothesis or engineering question → tested intervention or comparison → measurement conditions → observed result → warranted interpretation. Put workload, baseline, version, trial unit, and exclusions where their absence would mislead. Separate the measured behavior from a suggested explanation. An ablation tests a component's contribution under its conditions; it does not by itself establish performance everywhere.

Explain why the selected workload represents the intended use and where it does not. A synthetic microbenchmark can isolate a mechanism but does not substitute for end-to-end behavior. Report relevant contrary results and side costs rather than compressing them into a single favorable aggregate. Preserve enough method detail to rerun or audit the result; link full configurations and raw results when their distribution is authorized.

End with the supported engineering implication or next discriminating test, not a ceremonial summary. If a recommendation is requested, make it and name the observation that would reverse it. [MapReduce](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/) separates programming model, implementation, configuration, and experiments; [Circuit Tracing](https://transformer-circuits.pub/2025/attribution-graphs/methods.html) separates the proxy model, validation, and method-specific failures.

## Design proposal, RFC, or enhancement proposal

The reader needs to assess a change before treating it as implementation fact. State the current behavior or constraint, the proposed behavior, and why the change is needed. Explain the mechanism in enough detail to reveal its trade-offs: responsibilities, interfaces, state, data flow, compatibility, and failure behavior as applicable.

Give a concrete usage example before reference-level detail when it helps the reader understand the new interface. Then specify the semantics that the example cannot settle: ordering, lifetime, ownership, concurrency, error handling, and migration. Keep guide-level explanation and exact specification aligned. Rust RFC 2394 demonstrates this two-level structure; its historical syntax is not a current API reference.

Compare plausible alternatives against the same important constraints. Include the status quo when it is a credible option. State an alternative's advantage before the reason it loses here. Avoid an arbitrary scorecard in which invented weights make the desired answer win.

A compatibility note belongs beside the changed interface, with migration or rollback steps where someone must act. Use separate non-goals only when they prevent a likely consequential misunderstanding or a governing template requires them. Do not enumerate everything the proposal does not attempt. A short project proposal does not inherit Kubernetes' release governance, approval gates, or every production-readiness question; use the relevant technical questions without importing an unrelated organization.

Keep unresolved questions that affect the design, with the evidence or decision needed to resolve them. A list of speculative future features is not an unresolved-questions section. Preserve proposal status, decision history, and supersession when the project uses them; a merged document is not automatically an implemented feature.

## Architecture or mechanism explanation

The reader needs a usable mental model of an existing system. Start with the boundary that matters to the explanation, not a catalog of every repository or infrastructure component. Show the components involved in the path being explained and name their responsibilities. Trace a representative request, record, or job through them.

Explain the invariants and transitions: what is stored durably, what is only in memory, when ownership changes, what can be repeated, and how the system behaves when a dependency is unavailable. Distinguish control flow from data movement. Show trust boundaries when security or access determines the interaction. A box labeled “security” cannot stand in for an actual authorization check.

Use a diagram where spatial relationships reduce prose. Label arrows with the action or data, then explain only what the figure cannot show. Keep the diagram's names consistent with the code and reader-facing terminology. Do not invent components to make a diagram look balanced or claim current behavior from an old design document without checking the implementation.

## Architecture decision record

An ADR records a consequential choice and why it made sense under the conditions at the time. State the decision question, relevant forces, considered options, chosen option and reason, and consequences. Keep a real drawback in the decision record so the next maintainer does not rediscover it as a surprise.

Write “We chose X because Y” when a choice was actually made; use proposed status when it was not. Preserve the accepted record and supersede it through the project's process instead of rewriting history to fit a new decision. An ADR is not a retrospective benchmark or a full system design. [MADR's own format decision](https://adr.github.io/madr/decisions/0000-use-markdown-architectural-decision-records.html) makes the question, options, and outcome inspectable.

## Incident report or postmortem

Lead with the affected service or behavior, user-visible impact, duration when known, and current recovery state. Separate the trigger from the conditions that let it become an incident. Explain the causal sequence with evidence, and mark a suspected link as suspected instead of filling it with a plausible story.

Include the timeline entries that locate detection, diagnosis, mitigation, recovery, and consequential decisions. Preserve time zones and distinguish a system event from when responders learned about it. Omit a transcript of routine activity. A change preceding recovery is not automatically the fix; explain what evidence connects them.

Actions should address the mechanism or detection gap and have an observable completion condition. Avoid “improve monitoring” without naming the signal and response it should enable. Keep accountable ownership appropriate to the recipients without blame or erasure. The Google SRE example demonstrates separation of impact, cause, trigger, resolution, actions, and timeline; it is a fictional teaching example, not an actual Google outage.

## Project overview, reference, or runbook

A project overview explains what the project does, where it fits, the main entry points, and how to perform the first relevant task. Preserve enough context for a newcomer without teaching familiar infrastructure. Point to the canonical code, API, and maintenance docs rather than duplicating changing information.

A reference organizes exact interfaces and behavior for lookup: parameter or field, type, valid values, default, effect, and relevant error. Describe interactions between fields where they matter. Do not bury a required condition in a motivational introduction.

A runbook organizes actions by the actual symptom or task. State prerequisites before the action they constrain, the command or operation, the observable result, and the next step on failure. Distinguish inspection from mutation. A command example that has not been exercised is not a verified procedure. Avoid documenting credentials or copying a private environment into a public example.
