# Voice and Factual Prose

Use while drafting or revising sentences and paragraphs. The technical examples use a restrained engineering register; adapt the voice to the requested genre and author instead of imposing that register on every document. Apply the same factual discipline across languages while keeping their natural syntax. See [synthetic examples](synthetic-examples.md) for complete rewrites and [multilingual writing](multilingual-writing.md) for language-specific choices; public source pointers are kept in the repository's docs/writing-sources.md.

## Write the reader's understanding

Choose relevant information before choosing the sentence, then identify the relation the reader needs. State a component's operation, show the observation that changes a hypothesis, compare the cost that decides an alternative, or explain the condition that limits a result. [Synthetic examples](synthetic-examples.md) show several of these actions as before-and-after rewrites. Use an example to guide the work, then let the evidence and reader determine the paragraph's final shape. A fluent sentence can still be unnecessary; use [reader-value decisions](reader-value.md) when selection is the problem.

Trace a request through its state changes so the reader can predict the next operation. Compare alternatives on common dimensions and explain the constraint that decides this case. Keep technical precision inside the sentence that needs it. These concrete actions give clarity and balance an observable result.

## Subjects, verbs, and register

Make the technical subject do the work: the scheduler assigns, the worker acknowledges, the client retries, the measurement records. Prefer the actual operation to a prestige synonym: a component does not merely “enable seamless orchestration” when it queues jobs and retries failures. Keep an established term such as backpressure or linearizability when it names the behavior precisely. Replace vague praise with the invariant, mechanism, or observed result that would justify it.

Use present tense for defined behavior and mechanisms, past tense for an observation at a known revision, and proposal language for a design that has not been implemented. State the result or change directly: “The replay recorded…” or “Store the cursor after the commit.” A heading such as “Proposed cursor storage” can establish proposal status without repeating “we propose” in each paragraph. Do not hide a proposal behind “the system supports” or turn a team's belief into a community consensus.

Default to subject-centered prose in technical and shared reports. Remove “my findings,” “the author's synthesis,” and ornamental author/date introductions when page metadata or the sharing context already supplies them. An observation date, source attribution, or action owner can still change the meaning and belongs with the relevant fact. Keep required bylines in their metadata position. First-person voice is appropriate when explicitly requested, required by the destination's genre, or needed to distinguish firsthand testimony or responsibility; merely permitting it is not a reason to add a narrator.

Use passive voice when the object is the topic and the actor adds nothing: “The buffer is released after the callback returns” can be exact. Restore the actor if it determines ownership or responsibility. Avoid empty framing such as “it is important to note” and “it can be seen that” when the following proposition can stand alone.

Do not simulate dryness with noun piles, missing predicates, legalistic qualifiers, or identical short sentences. A long sentence is useful when it carries one tightly connected condition and action; split it when the reader must hold unrelated facts in memory. In Korean prose, retain particles that identify the subject, object, comparison, and condition. This sentence guidance does not require full sentences in headings, labels, or table cells: use clear noun phrases and compact values there. Preserve established English identifiers; do not translate an API into a new name to make a sentence sound formal.

Replace governance-speak with the actor and action. Document-architecture nouns such as “single source of truth,” “authoritative document,” “단일 source,” and “권위 문서” carry the author's filing system into the prose, while the reader needs what happens and where to look: “Retry limits are defined in `retry.md`,” not “`retry.md` is the single source for retry policy.” Treat abstract nouns of process the same way: “the service owner approves the change,” not “change governance applies.”

## Keep each author's voice in revision

When one pass revises texts by several people, or one author's notes written in different registers, keep each text's own register, stance, and recurring choices; do not converge them toward one safe middle voice. Keep hedges that mark genuine doubt, keep the author's first person and explicit causal chains, and do not swap plain words for rarer synonyms to sound polished.

## Make each paragraph carry a relation

Choose a paragraph's job: describe behavior, explain a mechanism, report an observation, compare alternatives, or justify a decision. Start where the reader can orient, then supply the evidence or technical sequence, and include the consequence if it is not already apparent. This is a reasoning pattern, not a mandatory three-sentence form.

Move from a known component or problem to the new detail. Keep a condition next to the action it constrains. When a system has multiple steps, describe the ordered state changes rather than joining component names with arrows and leaving their relationship implicit. A paragraph can end after the mechanism is clear; it does not need an inspirational takeaway.

A transition must name a real relation. “Because” requires a causal explanation; “therefore” requires an inference supported by the preceding statements. If the source shows only co-occurrence, report it without manufacturing the missing experiment. Repeating the subject is better than cycling through “platform,” “solution,” “framework,” and “engine” for the same component.

## Express the status inside the fact

| What is known | Useful construction | Do not silently turn it into |
| --- | --- | --- |
| Observed behavior | “In the replay, the worker retried the rejected items.” | A guarantee for all workloads |
| Measured comparison | “At the tested concurrency, p95 latency was lower with the bounded queue.” | A universal performance advantage |
| Estimate | “The estimate uses completed requests and the observed mean payload size.” | A measured total |
| Hypothesis | “Queue contention may explain the tail; the run did not measure lock wait.” | A confirmed root cause |
| Proposal | “Store the cursor after the batch commit so a retry can resume from the last durable batch.” | Existing implementation behavior |
| Decision | “Use the bounded queue because the consumer's drain rate limits useful parallelism.” | A choice attributed to people who did not approve it |
| Unknown | “The trace ends before the worker exits.” | “The worker never exited.” |

State the actual gap rather than hedging every clause. “No measurements were collected above this concurrency” identifies the unsupported range. Repeated “may,” “potentially,” and “not guaranteed” language is not a substitute for naming the missing evidence. A status word should describe the subject's state, not the author's confidence in the document.

Preserve the force of requirements. In ordinary project prose, distinguish a required precondition from a recommended default and an optional choice. When the destination adopts BCP 14 terminology, preserve its convention and exact uppercase keywords; do not import standards boilerplate into a memo merely to make it sound authoritative. [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html) explains the uppercase convention.

## Technical explanation and definitions

Introduce a definition when the reader needs a nonstandard meaning, a precise measurement boundary, or a new abstraction to follow the next step. Put it at first useful use. An experienced audience does not need an explanation of what a dashboard, latency, or a caption is. It may need to know whether this latency includes queueing and retries.

An internal nickname is not a definition. Prefer the established domain term for what the artifact actually is; if none fits, use a plain functional description. Introduce an exact local alias once when lookup requires it, then use the meaningful name consistently. For example, “the labeled evaluation dataset (internal ID: `review-set-r3`)” explains the role while preserving the identifier. It does not claim that every label was reviewed by a person. Terms such as “gold standard,” “validated,” and “ground truth” require corresponding evidence or an explicitly defined convention; a local filename cannot establish those properties.

Explain an abstraction through its contract and an example: input, transformation, output, ownership, and relevant failure behavior. Use pseudocode when execution order or state transition is difficult to express unambiguously in prose. Explain what the pseudocode abstracts away only when the omission matters. A mechanism diagram and the surrounding text should use the same component names.

Distinguish an analogy from an implementation. If an analogy needs a paragraph explaining everything that does not map, use the actual mechanism instead. A familiar example can teach a concept, but it cannot provide evidence for the system being evaluated.

## Sources, citations, and detail placement

Place a citation where its scope is clear: beside the reported value, mechanism, comparison, or attributed claim. Prefer the paper's relevant section/table, a source permalink, or a maintained specification to a product home page. Preserve source versions when an API, policy, or result could change. Summarizing several sources does not make them independent evidence if they all repeat one experiment.

Keep an interpretation-changing method accessible in the actual reading context. Surrounding explanation, a clear label, or the appropriate code or document can already supply it; do not append the same note to every claim. Use a methods section, Sources section, appendix, or existing record for detail that an actual reproduction or audit task needs. Detail without that use can be deleted from the prose instead of permanently relocated. A citation is not a request for readers to reconstruct the argument from scratch.

Use clear noun-phrase section headings and visual titles that name the subject, behavior, or comparison. Put assertions and questions in the body, unless a governing template or explicit user request requires them as headings. Lists work for parallel observations; tables work when rows share meaningful dimensions. Keep reasoning in short connected explanations instead of forcing either paragraphs or nested bullets to carry every part of the document.

A caption or lead-in that only restates the command or code below it, such as “다음 명령어로 의존성을 설치합니다” above `uv sync`, is deleted. Keep it when it says why, when, for whom, or with what scope the command runs, which the command itself does not show.
