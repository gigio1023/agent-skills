# Voice and Factual Prose

Use while drafting or revising technical prose. The goal is a restrained engineering register, not a corporate brand voice. Apply the same factual discipline in Korean and English; let each language keep its natural syntax. See [worked examples](worked-examples.md) for complete rewrites and [source readings](source-readings.md) for the public basis.

## Write the reader's understanding

Choose the relation to explain before choosing the sentence. State a component's operation, show the observation that changes a hypothesis, compare the cost that decides an alternative, or explain the condition that limits a result. [Writing patterns](writing-patterns.md) pairs these actions with finished synthetic paragraphs and reader checks. Use a pattern to guide the work, then let the evidence and reader determine the paragraph's final shape.

Trace a request through its state changes so the reader can predict the next operation. Compare alternatives on common dimensions and explain the constraint that decides this case. Keep technical precision inside the sentence that needs it. These concrete actions give clarity and balance an observable result.

## Subjects, verbs, and register

Make the technical subject do the work: the scheduler assigns, the worker acknowledges, the client retries, the measurement records. Prefer the actual operation to a prestige synonym: a component does not merely “enable seamless orchestration” when it queues jobs and retries failures. Keep an established term such as backpressure or linearizability when it names the behavior precisely. Replace vague praise with the invariant, mechanism, or observed result that would justify it.

Use present tense for defined behavior and mechanisms, past tense for an observation at a known revision, and proposal language for a design that has not been implemented. Use “we measured” or “we propose” when authorship matters and the document convention permits it. Do not hide a proposal behind “the system supports” or turn a team's belief into a community consensus. Prefer a component subject over an author subject when describing runtime behavior.

Use passive voice when the object is the topic and the actor adds nothing: “The buffer is released after the callback returns” can be exact. Restore the actor if it determines ownership or responsibility. Neither active voice nor a first-person ban is a universal rule. Avoid empty framing such as “it is important to note” and “it can be seen that” when the following proposition can stand alone.

Do not simulate dryness with noun piles, missing predicates, legalistic qualifiers, or identical short sentences. A long sentence is useful when it carries one tightly connected condition and action; split it when the reader must hold unrelated facts in memory. In Korean, retain particles that identify the subject, object, comparison, and condition. Preserve established English identifiers; do not translate an API into a new name to make a sentence sound formal.

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

Explain an abstraction through its contract and an example: input, transformation, output, ownership, and relevant failure behavior. Use pseudocode when execution order or state transition is difficult to express unambiguously in prose. Explain what the pseudocode abstracts away only when the omission matters. A mechanism diagram and the surrounding text should use the same component names.

Distinguish an analogy from an implementation. If an analogy needs a paragraph explaining everything that does not map, use the actual mechanism instead. A familiar example can teach a concept, but it cannot provide evidence for the system being evaluated.

## Sources, citations, and detail placement

Place a citation where its scope is clear: beside the reported value, mechanism, comparison, or attributed claim. Prefer the paper's relevant section/table, a source permalink, or a maintained specification to a product home page. Preserve source versions when an API, policy, or result could change. Summarizing several sources does not make them independent evidence if they all repeat one experiment.

Keep a methods note that changes the interpretation on the main reading path. Put reproducibility detail in a methods section or appendix when the reader needs it but not at every mention. Delete reader-irrelevant caveats rather than creating a permanent appendix of deleted prose. A citation is not a request for readers to reconstruct the argument from scratch.

Headings should name the behavior, decision, or comparison that follows. Use neutral headings when there is no established result. Lists work for parallel observations; tables work when rows share meaningful dimensions. Do not convert an argument into a checklist to make it appear concise.
