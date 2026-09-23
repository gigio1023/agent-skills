---
name: technical-report-writing
description: >
  Write, revise, or review reader-facing reports, guides, proposals, memos,
  posts, design docs, and project documentation in any language or medium.
  Use for information selection, document structure, concise tables,
  explanatory visuals, prose, and production. Owns document craft;
  share-internal-doc adds recipient suitability and authorized delivery.
  NOT for ordinary chat or specialized interface implementation alone.
---

# Technical Report Writing

Produce a document that a reader without the drafting conversation can understand and use. Select and organize the information before polishing sentences. Default to clear noun-phrase headings, short readable blocks, compact comparisons, and focused visuals. Preserve the explanation needed to understand the subject; a concise document can still be substantial.

Infer the reader, task, sources, language, and medium from the request and project. Use available inputs before asking about consequential gaps. Preserve established terms, source files, required templates, and the author's intended voice. A review returns findings; authoring or revision returns the requested text or artifact. Change the underlying system or publish only when separately authorized. A current explicit style request or governing template takes precedence over these editorial defaults.

For a user-edited document, compare the current copy, which remains the revision baseline, with an earlier version when available to learn which functions the user removed and retained, as described in [authoring and revision](references/authoring-and-revision.md).

## Document structure

Choose the content and form for each reader question. Use lists for parallel facts, steps for dependent actions, tables for comparable attributes or exact lookup, charts for quantitative patterns, and diagrams for relationships or behavior. Use short connected paragraphs to explain causes, mechanisms, implications, and trade-offs. Let the reader's purpose determine section boundaries. Keep a separate section when it answers a distinct question or supports a different decision; merge source categories, case retellings, and background topics that do not. Split a bullet that bundles several subjects. Use second- or third-level bullets when they express real groups and supporting details; keep independent peers at the same level. Give each parent a useful meaning and each leaf one point. Formatting does not replace explanation.

Use clear noun phrases for section headings, table titles, and figure titles. Name the subject or comparison: “Recovery paths,” not “How does the system recover?” or “This approach makes recovery safer.” Put the finding in the opening sentence or caption. Keep headings specific enough to predict their contents; replace labels such as “Start,” “Three conclusions,” and a generic “Overview.”

Organize for the document's purpose. A factual incident record can use an overview, chronology, grouped observations, and response. A technical introduction needs the problem, a concrete example, and enough mechanism to explain it. A proposal needs the changed behavior, alternatives, and the reason to choose. An incident report stays concise; a technical explanation keeps its reasoning instead of becoming an inventory of facts. Define terms near first use; add a glossary or prerequisite chapter only for a real lookup need.

For a new or restructured document, decide which question each section and visual answers before filling it. Keep the planning exercise out of the document; add a fixed outline or review pause only when requested. Use [information design](references/information-design.md) for block selection and split decisions, and [document forms](references/document-forms.md) for genre-specific depth.

In a long explanation, the visible path carries the subject, the useful result with its interpretation conditions, the mechanism, and the key figures. Named collapsible sections hold necessary optional depth, such as prerequisites and derivations, at the point of need. When the reader asks to keep detailed theory or figure explanations, keep the derivations, intermediate steps, and explanations at that optional depth; a summary and a local link do not replace them. Remove material that does not help this reader instead of hiding it. The title identifies the subject, an optional callout locates the scope, and the opening begins the explanation; each has a distinct job. Use [information design](references/information-design.md) to choose depth for readers with different backgrounds.

## Tables and visuals

Design a table before populating it: identify the comparison or lookup, row items, and shared attributes. Name the row entity in its header, label every row, and name the compared attributes. A matrix names both dimensions visibly, so no meaning rests on a blank corner or row position. Split the table when columns answer different questions or rows mix unlike kinds of information. Remove a column with no useful variation. Omit the table when a list or short explanation does the job better. An “Item / Content” grid containing paragraphs is usually prose constrained by cell borders.

Keep cells to values, identifiers, or short phrases; use a short sentence only when needed for meaning. Every row should participate in the same comparison or lookup. Move shared context into headers or one nearby note. Put reasoning and extended explanation outside the grid. If many cells need paragraphs, redesign the table rather than shrinking the type or adjusting column widths. Preserve a condition that changes a value's meaning. A compact two-column lookup is valid; neither a column count nor a word quota determines quality.

Give each chart or diagram one primary comparison, relationship, or mechanism. Separate unrelated questions and levels of detail; matched panels may belong together when they answer the same question. Do not combine a process, component inventory, historical timeline, benchmark, and deployment catalog merely because all concern one subject. The first figure shows the document's own subject and its relationships. A figure of general prerequisites, such as a generic Transformer block in a refusal-direction guide, is background; place it at the point of need, if at all. Plan one reading order that numbers, arrows, and legend all indicate, then labels and useful size. Split or remove detail before adding more boxes, legends, footnotes, or smaller text.

Use visuals where they reduce the reader's work, without a mandatory figure count. Show real entities and label arrows with the operation or data. Keep titles, labels, captions, and nearby text complementary. Number figures in reading order after restructuring. Read [measurements and figures](references/measurements-and-figures.md) for quantitative meaning and [worked examples](references/worked-examples.md) for complete structural repairs.

## Content and evidence

Keep what helps the reader understand, compare, verify, decide, or act. Assign information to the artifact that owns it. A reader-facing document normally owns the core finding, enough mechanism to understand it, conditions that change its meaning, and representative evidence. A local evidence or methods record can own exhaustive inventories, full provenance, alternate examples, and implementation lineage. An audit, evidence inventory, or reproduction protocol reverses that default when those details are the reader's task. Delete process narration, meaning how the author searched or worked, unless requested: search rounds, collection counts, source-folder inventories, local preservation steps, and accounts of care. Result-identifying information stays: what was evaluated, the method, model, unit, and observation date. Explain the subject's method when needed; how the author found that method is a different topic.

Exclude blanket disclaimers, self-protective wording, self-appraisal, routine reading instructions, and table tours. Do not replace a deleted paragraph with another disclaimer or automatically move it to an appendix. Attach usable citations to the relevant claims. State a material condition or uncertainty inside the specific fact it qualifies, without prefacing the entire document with a warning. Keep an actually required notice in its required place.

State findings and proposals directly: “Use a bounded queue” or “Proposed retry policy,” rather than “I found” or “I propose.” Omit ornamental bylines, “the author's synthesis” introductions, and prose that repeats page ownership or sharing context. Keep dates that bound an observation, attribution that distinguishes a source or responsible actor, and required publication metadata. Use an author-centered voice only when explicitly requested or essential to the genre or meaning; a proposal heading establishes proposal status, and the opening summary carries that status wherever it states the proposed change.

Preserve the supported strength of retained claims. Attribute reported results, distinguish proposals from implementation, and retain contrary observations and comparison conditions that change the conclusion. Do not upgrade one case to “the only method,” “required,” or “proven” through summarization or a diagram label. A global caveat cannot repair an overclaim. Preserve original evidence in its owning location when removing report prose. Use [reader-value decisions](references/reader-value.md) for a difficult retain, rewrite, delete, or relocate decision.

## Revision discipline

Change only the passages a correction names. Untouched sentences, approved examples, mechanism, equations, and figures stay byte-identical unless the correction covers them; after editing, diff against the previous version and confirm nothing outside the correction moved. A correction removes a function, not only a sentence; re-creating it elsewhere repeats the defect, as when a deleted reading guide returns as toggle titles, a “기초 읽기” block, or an opening route sentence. The user's instruction shapes the document without becoming its text: “newest first” becomes an ordering, never a sentence stating the ordering, and “this is my proposal” becomes a proposal heading, never “내가 제안하는.” Reviewer, subagent, and self-check notes stay in the checking record, including a caveat such as “not 180 independent samples.”

To explain a thing, say what it is, who produces it, what it contains, and what it is used for, with one concrete instance and no definition by negation or added qualification. To shorten, remove orientation, repetition, process narration, exhaustive inventories, and duplicate tables first; keep mechanism, equations, the subject's figures, and examples the user confirmed, then diff and list the categories removed. A later correction narrows an earlier request, and praise for one part approves only that part. Fix the document itself instead of editing the skill or recording new rules mid-task.

## Explanation and language

Open with the useful finding, task, recommendation, or concrete problem for this reader. Supply the context and reasoning needed to understand it in this document. Links support verification and deeper inspection; the main explanation is complete without them.

Build understanding through the subject itself. Use the smallest complete explanatory chain for this reader: a concrete observation or problem, one representative example when needed, the mechanism, and the consequence or choice. Add another example only when it changes the interpretation or decision. Use these moves in the order the reader needs, without turning them into sections. Each substantive block should add a new fact, relationship, example, warrant, or decision. After a paragraph, the reader should be able to explain more, rather than know what a later chapter promises.

Name the actor, input, operation, state change, and output when explaining a mechanism. Keep the same representative request or record through the explanation so readers can connect the parts. Put a symbol's meaning beside its first useful operation and a comparison condition beside the result it qualifies. Spend detail on the distinction or failure path that resolves a real reader question. For a long or introductory explanation, see [an explanation with optional depth](references/explanation-with-depth.md): a clear opening, mathematical example, and expandable foundation working together.

Use established field terminology and explain unfamiliar meanings at first useful use. Keep detailed term provenance, naming history, and source-specific distinctions in an endnote, glossary, or linked record unless it changes how the reader interprets the term. Name an unfamiliar internal artifact by its actual role before introducing a local alias; include the exact alias only when readers need it for lookup or coordination. Use the meaningful term in subsequent explanation. Do not replace opaque shorthand with a new slogan, rename a real identifier, or imply verification or quality that the source does not establish. Keep ordinary connecting language natural in the reader's language. Explanatory prose uses complete sentences; headings, labels, and cells use concise, unambiguous phrases.

Read only the reference needed for the current decision:

- [Correction cases](references/correction-cases.md) and [exemplar passages](references/exemplar-passages.md): read before drafting or revising a Korean technical document; check a revision diff against the failure shapes, and borrow the operation, never the topic, from the quoted passages.
- [Authoring and revision](references/authoring-and-revision.md): source grounding, scope, and preservation of voice.
- [Voice and factual prose](references/voice-and-facts.md): actors, logical relations, supported claims, and citation placement.
- [Multilingual writing](references/multilingual-writing.md): language-specific meaning and expression.
- [Writing patterns](references/writing-patterns.md): mechanisms, investigations, proposals, and progress.
- [Finished examples](references/finished-examples.md): for a new or restructured explanation, measured comparison, or proposal, choose the matching sample to see prose, tables, lists, and a diagram working together.
- [Document production](references/document-production.md): the existing source or a suitable native PDF/editable-document route; no web application is needed solely to produce a PDF.
- [Composition](references/composition.md): internal sharing, analytical views, and specialist production without repeated intake or editorial passes.
- [Example library](references/example-library.md) and [source readings](references/source-readings.md): public source pointers for a specific technique question.

Borrow the useful operation from an example, not its whole outline, density, or style. Explicit user preferences remain operative across genres unless overridden, including where an optional reference differs.

## Reader and delivery checks

Check claims against inspected sources and compute arithmetic with tools. Preserve identifiers, units, populations, proposal status, and requirement levels. Label invented teaching examples as synthetic. Keep missing data distinct from zero and temporal association distinct from demonstrated cause.

Read the actual document without the drafting conversation and repair these failures before delivery:

- The opening or headings do not identify the subject, useful result, or task.
- A table's cells contain the explanation, its row meaning is implicit, its rows mix categories, or its columns serve unrelated questions.
- A diagram needs tiny text, several competing reading paths, or an accompanying tour to explain its organization.
- Research narration, author self-introduction, repeated “I propose” framing, generic disclaimers, or table tours displace content.
- An opaque local alias or missing context forces the reader to visit another document or a distant glossary to understand the main point.
- A long flat bullet bundles multiple subjects, or nesting adds indentation without a meaningful group.
- Compression removes the mechanism, rationale, attribution, or condition needed for this genre.
- A sentence exists because the user asked for something or a reviewer flagged something, and gives the reader nothing new.

Inspect the destination at its delivered size, including figures, citations, table wrapping, page boundaries, and the initial view. Keep Markdown source paragraphs unwrapped; rendered line width is a separate layout choice. Deliver the requested artifact and editable source where applicable. Match private information and source access to the authorized audience, and publish or send only when authorized. Finish when the artifact and applicable checks are complete; report only material unresolved issues.
