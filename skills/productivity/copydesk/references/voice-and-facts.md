# Voice and Factual Prose

Use while drafting or revising sentences and paragraphs, in any language. [Synthetic examples](synthetic-examples.md) show complete rewrites, and [multilingual writing](multilingual-writing.md) covers language-specific choices.

## Subjects, verbs, and register

Make the technical subject do the work: the scheduler assigns, the worker acknowledges, the client retries, the measurement records. Prefer the actual operation to a prestige synonym: a component does not merely “enable seamless orchestration” when it queues jobs and retries failures. Keep an established term such as backpressure or linearizability when it names the behavior precisely. Replace vague praise with the invariant, mechanism, or observed result that would justify it.

Use present tense for defined behavior and mechanisms, past tense for an observation at a known revision, and proposal language for a design that has not been implemented. State the result or change directly: “The replay recorded…” or “Store the cursor after the commit.” A heading such as “Proposed cursor storage” can establish proposal status without repeating “we propose” in each paragraph. Do not hide a proposal behind “the system supports” or turn a team's belief into a community consensus.

Default to subject-centered prose in technical and shared reports. Remove “my findings,” “the author's synthesis,” and ornamental author/date introductions when page metadata or the sharing context already supplies them. An observation date, source attribution, or action owner can still change the meaning and belongs with the relevant fact. Keep required bylines in their metadata position. First-person voice is appropriate when explicitly requested, required by the destination's genre, or needed to distinguish firsthand testimony or responsibility; merely permitting it is not a reason to add a narrator.

Replace governance-speak with the actor and action. Document-architecture nouns such as “single source of truth,” “authoritative document,” “단일 source,” and “권위 문서” carry the author's filing system into the prose, while the reader needs what happens and where to look: “Retry limits are defined in `retry.md`,” not “`retry.md` is the single source for retry policy.” Treat abstract nouns of process the same way: “the service owner approves the change,” not “change governance applies.”

## Controlled sentences

The author's documents use controlled language at about 80% of [ASD-STE100](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf) Issue 9 (2025-01-15): its sentence and paragraph rules, without its approved-word dictionary. Rule numbers in parentheses point into that standard. The rules hold in English and Korean. Headings, table cells, labels, quotations, and code are exempt. In another person's text, their sentence style stays ([authoring and revision](authoring-and-revision.md#preserve-the-intended-voice)).

1. **One claim per sentence.** A sentence states one fact, one action, or one relation (4.1). Split at the second claim, and keep the relation as a word: so, because, then. Korean: 연결어미(`-고`, `-며`, `-는데`, `-지만`, `-어서`)는 한 문장에 하나까지 쓴다. 둘째 연결어미에서 문장을 끊고 관계는 `그래서`, `이때`, `그러나`로 잇는다.
2. **One instruction per sentence, condition first.** Write an instruction in the imperative, with one action unless two actions occur at the same time (5.2, 5.3). A condition the reader must know first opens the sentence (5.4): "If the queue is full, stop the producer." Korean: "queue가 가득 차면 producer를 멈춘다."
3. **The actor is the subject.** Use the active voice. Use the passive only when the actor is unknown or adds nothing and the object is the topic (3.6): "The buffer is released after the callback returns." Korean: 문단의 첫 문장과 행위자가 바뀌는 문장에는 주어를 쓴다. 같은 행위자가 이어지는 문장에서는 주어를 생략해도 된다. `~에 의해`와 `되어진다`는 능동으로 바꾼다(A-8, A-9).
4. **One term per concept, one meaning per term.** Choose one name for a concept and repeat it (1.11, 9.4). Rotating "platform", "solution", and "engine" for one component makes the reader count components. Korean: 같은 개념은 문서 끝까지 같은 표기로 쓴다.
5. **Short sentences.** Aim for at most 20 words in an instruction and 25 in a description (5.1, 6.3). A longer sentence is a signal to check rule 1. Korean has no word count, so the connective limit in rule 1 does this job.
6. **One topic per paragraph.** The first sentence states the topic, and a paragraph has at most six sentences (6.5, 6.6).
7. **At most three nouns in a row.** Unpack a longer stack with a preposition (2.1). Korean: 조사를 되살리거나 절로 푼다([명사열 풀기](korean-writing.md#명료성-기준)).
8. **Each point once, stated positively.** Write what a thing is or does. Add a negation only when the reader would otherwise assume the negated reading. A rule stated once does not return as a warning, a summary, or an example of what not to write.

Keep every word the grammar needs: articles, particles, endings, and predicates (4.2, 4.5). The rules shorten sentences; mechanism, conditions, and numbers stay.

**English description.** Before, 47 words and four claims: "The cache layer, which is responsible for reducing load on the database, is not a source of truth, and entries may be evicted at any time by the eviction policy, so callers should always be prepared to re-fetch data from the database if a miss is encountered."

> The cache reduces database load. The eviction policy can remove a cache entry at any time. If the cache has no entry for a key, the caller reads the value from the database.

The defensive "not a source of truth" goes, because the third sentence states its consequence.

**Korean description.** Before, 연결어미 여섯 개: "이 job은 실패하면 scheduler에 의해 재시도되는데, 재시도 횟수는 설정 파일에서 관리되고 있으며 최대 횟수에 도달하면 dead-letter queue로 이동되므로 운영자의 확인이 필요하지만 알림은 자동으로 발송되지 않는다."

> job이 실패하면 scheduler가 job을 다시 실행한다. 최대 재시도 횟수는 설정 파일이 정한다. 재시도가 이 횟수에 이르면 scheduler가 job을 dead-letter queue로 옮긴다. 이때 알림은 가지 않는다. 그래서 운영자가 dead-letter queue를 직접 확인해야 한다.

알림이 없다는 부정은 독자가 알림을 기대할 만한 자리라 남겼다.

## Keep each author's voice in revision

When one pass revises texts by several people, or one author's notes written in different registers, keep each text's own register, stance, and recurring choices; do not converge them toward one safe middle voice. Keep hedges that mark genuine doubt, keep the author's first person and explicit causal chains, and do not swap plain words for rarer synonyms to sound polished.

## Make each paragraph carry a relation

Choose a paragraph's job: describe behavior, explain a mechanism, report an observation, compare alternatives, or justify a decision. Start where the reader can orient, then supply the evidence or technical sequence, and include the consequence if it is not already apparent. This is a reasoning pattern, not a mandatory three-sentence form.

Move from a known component or problem to the new detail. Keep a condition next to the action it constrains. When a system has multiple steps, describe the ordered state changes rather than joining component names with arrows and leaving their relationship implicit. A paragraph can end after the mechanism is clear; it does not need an inspirational takeaway.

A transition must name a real relation. “Because” requires a causal explanation; “therefore” requires an inference supported by the preceding statements. If the source shows only co-occurrence, report it without manufacturing the missing experiment.

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

A caption or lead-in that only restates the command or code below it, such as “다음 명령어로 의존성을 설치합니다” above `uv sync`, is deleted. Keep it when it says why, when, for whom, or with what scope the command runs, which the command itself does not show.
