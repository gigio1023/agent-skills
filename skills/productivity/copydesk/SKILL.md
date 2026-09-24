---
name: copydesk
description: >
  Write, revise, or review reader-facing documents in any language and medium: reports,
  guides, proposals, design docs, posts. Includes AI-slop diagnosis on explicit revision
  requests and Korean semantic repair in documents and ordinary Korean answers. Owns document
  craft and internal sharing: recipients, source access, the sharing pass, and delivery. NOT for
  PR copy (draft-pr), issues (write-issue), diagrams (technical-diagram), or dashboards
  (insight-dashboard). Formerly technical-report-writing.
---

# Copydesk

## Work and baseline

Write for a reader who lacks the drafting conversation, and select and organize information before polishing sentences. Infer reader, task, sources, language, and medium from context, and ask only about gaps that change meaning or authority. A new document returns the artifact, a review returns findings and edits nothing, and a revision changes only what was authorized. In a user-edited copy, the current copy is the baseline; compare it with the closest earlier version to see which functions the user removed and kept. Only the user's edits show preference, so isolate changes other agents made. Preserve established terms, templates, and voice. The Korean clarity floor in [Korean writing](references/korean-writing.md) also covers ordinary Korean answers and progress reports.

## Meaning and scope of change

A correction that names a type ("drop sentences like this") covers every instance; one that names a sentence covers that sentence, and other instances are reported, not edited. All else stays byte-identical, including approved examples, mechanism, equations, figures, and any block, bullet, or page note the user wrote; a page note is an instruction, never reader text. After editing, diff against the previous version and confirm nothing outside the correction moved. A correction removes a function, so re-creating it elsewhere repeats the defect, as when a deleted reading guide returns as toggle titles. Instructions shape the document without becoming its text ("newest first" becomes an ordering), and reviewer, subagent, and self-check notes stay out of it.

To explain a thing, say what it is, who produces it, what it contains, and what it is for, with one instance and without a definition by negation unless the reader would otherwise assume the negated reading. To shorten, cut orientation first, then repetition, process narration, and inventories; keep mechanism, equations, figures, and confirmed examples, and list the categories cut. A later correction narrows an earlier one, and praise for one part approves only that part. Changing a status (to example, candidate, or proposal) adds no criterion, reason, or fact the source lacks; write the status word and stop. Fix the document, never the skill, mid-task.

On an explicit revision or deslop request, name what each suspect sentence does for the reader before editing it; a tell is a functional diagnosis, never an authorship verdict. Keep claim strength, meaningful hedges, and voice, then reread the result for new tells, uniform polish, and drift. A batch revision keeps each author's voice distinct.

## Author profile

Read [writing profile](references/writing-profile.md) before drafting or revising anything a colleague will read, and apply it even when no skill was named. A current explicit request or governing template wins over it, and it wins over the defaults here. The profile is one file within 40 lines; the author's instruction files carry it by import or by a copy that `python3 scripts/sync_profile.py <instruction-file>` refreshes after any change.

## Selection and structure

Decide which question each section and visual answers, and keep that plan out of the document. Lists carry parallel facts, steps dependent actions, tables comparisons or lookup, charts quantities, diagrams relationships, and paragraphs causes, mechanisms, and trade-offs. Section boundaries follow reader questions; merge source categories, case retellings, and background answering none. Split a bullet that bundles subjects, and nest only real groups. Headings are specific noun phrases, and a section's first sentence carries the finding. A document has no reading guide, section preview, or note on when to expand, since a collapsible section's title and first sentence say what it holds. Collapsible sections hold optional depth such as derivations; the subject, key figures, and results stay visible, and material that helps no reader is removed, not hidden. Each fact goes to its owning artifact: inventories, provenance, and lineage belong in an evidence record unless the reader is auditing. Delete process narration (search rounds, collection counts, accounts of care) unless change is the reader's job, as in a changelog, migration guide, or ADR; keep what identifies the result (object, method, model, unit), with a date beside the number it bounds. State a proposal's or candidate's status once, in the title or opening summary, let no heading, sentence, or figure label contradict it, and attribute reported results. Keep each claim's supported strength and any contrary observation or condition that changes the conclusion, including a condition that cuts both ways; no summary or label upgrades one case to "required," and a global caveat never repairs an overclaim. A rewrite also keeps the source's decision status: "under review" stays under review and "not yet chosen" stays unchosen; a dry register removes hedging words, never the tentativeness of a decision. Put a condition inside the fact it qualifies, cite at the claim, keep required notices; when compressing results or a literature table into prose, each retained number keeps its benchmark, setting, and caveat, or leaves with them, and drop blanket disclaimers, self-appraisal, and diligence records; an unverified point gets one sentence only when the reader would otherwise act as if it were verified. Link CC BY-NC-ND sources instead of republishing them, and never copy a teaching example's invented names or numbers into real documents.

## Tables and figures

Design a table first: name the row entity in its header, label every row, name the attributes, and name both dimensions of a matrix so no meaning rests on a blank corner. All rows serve one comparison or lookup; split a table whose columns answer different questions or whose rows mix kinds, and drop constant columns. Cells hold values or short phrases, with shared context in headers and reasoning outside the grid; when cells need paragraphs, redesign the table instead of widening it. Each figure answers one question; matched panels for the same question may stay together. The first figure shows the document's own subject; general prerequisites go at their point of need, if anywhere. Give each figure one reading order that numbers, arrows, and legend follow, label arrows with the operation or data, and split before shrinking text. The canvas carries names and mechanism; conditions, sample sizes, and timestamps go in the caption or nearby prose. PR behavior changes follow the profile. Renumber figures after restructuring.

## Explanation and language

The explanation is complete without its links. Use the smallest complete chain for this reader: observation or problem, one example if needed, mechanism, and consequence, each block adding a fact, relation, or decision. For a mechanism, name actor, input, operation, state change, and output, and keep one running example throughout. Define a term or symbol at its first useful use. Use established field terms, name an internal artifact by its role before any alias, and never rename a real identifier. Turn a broad promise ("improves robustness") into an observable test before writing its result. Mechanism the source does not state is background from general knowledge: mark it as such, keep it out of the document's own premises, and leave feasibility the source calls unconfirmed unconfirmed. Write no imperative caption unless it carries a non-obvious why, when, or scope. Replace governance-speak ("single source of truth") with where to look. Never imitate the user's typos, shorthand, or slang. Korean keeps actors, conditions, and clause relations recoverable through particles, endings, and predicates ([Korean writing](references/korean-writing.md)); headings, cells, and summary items may be fragments, and explanatory prose is complete sentences. Field terms stay English and ordinary words Korean, punctuation follows the profile, and other languages follow [multilingual writing](references/multilingual-writing.md).

## Sharing and delivery

Recover the latest shared copy before editing a collaborative page. Recipients must be able to open every cited source; a local path, a localhost address, or a bare filename is not a citation. Deliver the requested artifact and its editable source, making a PDF by a native route without building a web app. Inspect the destination at delivered size: figures, tables, page breaks, first view. Publish or send only when authorized, with private information matched to the audience; ask separately whether the copy would embarrass the company and the person posting it. Before a document leaves the author's machine, or when its recipients or distribution change, read [sharing and delivery](references/sharing-and-delivery.md).

## Checks

Check claims against inspected sources so that every sentence traces to a source, a stated assumption, or labeled background; compute arithmetic with tools, and preserve identifiers, units, populations, status, and requirement levels. Label invented examples as synthetic, and keep missing distinct from zero and association distinct from cause. Reread without the drafting conversation and repair an opening that misses the subject or result, a table carrying explanation, a figure needing tiny text or a tour, and narration or disclaimers displacing content. Also repair an alias that sends the reader elsewhere, compression that drops mechanism or a condition, and any sentence that exists only because someone asked. Run `python3 scripts/check_draft.py <file>`, and for a revision `python3 scripts/protected_diff.py <previous> <revised> --allow "<corrected heading>"`. Both flag candidates and never pass or fail a document; a flagged condition that changes how a number reads is legitimate. A rewrite from one source starts as a traced draft ([source tracing](references/source-tracing.md)). Finish when the artifact and checks are complete, reporting only material unresolved issues.

## References

Open only what the decision needs; public source pointers are in the repository's `docs/writing-sources.md`.

- [Writing profile](references/writing-profile.md): always.
- [Korean writing](references/korean-writing.md): any Korean document or answer.
- [Correction cases](references/correction-cases.md), [exemplar passages](references/exemplar-passages.md): drafting or revising Korean; check a revision diff against their failure shapes; borrow the operation, never the topic.
- [Finished examples](references/finished-examples.md), [explanation with depth](references/explanation-with-depth.md): a new or restructured explanation, comparison, or proposal.
- [Synthetic examples](references/synthetic-examples.md): a repair or rewrite shape.
- [Authoring and revision](references/authoring-and-revision.md), [reader value](references/reader-value.md), [voice and facts](references/voice-and-facts.md): a hard keep, rewrite, delete, or relocate call, or a deslop revision.
- [Information design](references/information-design.md): new structure, overloaded table or figure.
- [Measurements and figures](references/measurements-and-figures.md): quantitative meaning.
- [Document forms](references/document-forms.md): genre depth.
- [Document production](references/document-production.md): PDF or editable output.
- [Source tracing](references/source-tracing.md): a rewrite from one source.
- [Sharing and delivery](references/sharing-and-delivery.md): a document leaving the author's machine, changed recipients or distribution, publication.
- [Multilingual writing](references/multilingual-writing.md): English, Italian, Chinese.
- [Composition](references/composition.md): which skill owns what.
