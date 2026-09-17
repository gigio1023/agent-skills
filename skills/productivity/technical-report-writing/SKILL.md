---
name: technical-report-writing
description: >
  Write, revise, or review reader-facing documents: reports, guides,
  proposals, memos, posts, design docs, and project documentation for
  internal or external readers, in any language or medium. Use for
  information selection, explanation, prose editing, and document production;
  sharing authorization and specialized interface implementation remain separate.
---

# Technical Report Writing

Write for the reader's question, background knowledge, and intended use. Choose information before polishing its expression. Make the important point easy to find and give the reasoning, examples, and evidence needed to understand or use it. A dry technical register suits engineering reports; a guide, personal post, or proposal can need a different voice.

Infer the reader, task, source material, language, and medium from the request and project. Preserve established terminology, source files, required templates, and the author's intended voice. A review returns findings; an authoring or revision request returns the requested text or artifact. Recover available inputs before asking about consequential gaps. Editing a document does not authorize changing its underlying system or publishing it.

## Select what the reader needs

Keep content that helps the reader understand, compare, verify, decide, or act. Accuracy alone does not require retaining a sentence. Delete redundant definitions, routine UI tours, generic caveats, and self-assessment when they do no work for this reader. Judge their function in context, not the author's presumed motive or whether the text sounds AI-generated.

Preserve the accuracy, attribution, and evidential strength of retained claims, together with facts or conditions whose omission would materially change their interpretation or use. Failures, adverse results, populations, denominators, comparison conditions, uncertainty, and responsibilities are examples to consider, not a mandatory list to restate. Omit their explanation when the intended reader can already infer it from the passage or appropriate source and no consequential misunderstanding results. Keep core definitions and interpretation-changing conditions accessible; preserve any actually required notice. Removing an unsupported judgment must not erase the observed action or accountable next step.

Choose the useful edit: retain a good passage, rewrite necessary but unclear information locally, delete unnecessary information, or relocate detail for an identifiable reader task. Deletion needs no replacement disclaimer, footnote, or automatic appendix. Place a needed qualification where it resolves the reader's likely misunderstanding. Do not repeat it beside every claim when surrounding text, a shared method, or the relevant code or document already makes the condition clear.

Distinguish the report from its production record. Include build details, timestamps, revisions, and verification receipts when the reader needs them to compare, reproduce, audit, or act. A Sources section is a useful destination when it serves that task, not a compulsory home for everything removed. Preserve underlying evidence under its own retention rules; editing the report does not authorize deleting records.

When the choice is unclear, [reader-value decisions](references/reader-value.md) gives a functional diagnosis and paired examples where changing the reader's task changes the right edit.

## Build the explanation from evidence

Use the actions that fit the document. A mechanism explanation needs a system path; a personal account or lookup page may not need systems, measurements, or an argument at all.

1. **Choose the reader's entry point.** Open a report with its important finding, a proposal with the changed behavior and reason, a procedure with the task, and an explanation with the concrete problem or example that makes the concept useful. Select the entry point for this document rather than imposing one outline.
2. **Connect the facts.** Give each paragraph a job: trace a mechanism, interpret an observation, compare alternatives, or justify a choice. Supply the relation between evidence and conclusion. When evidence leaves a choice unresolved, identify the observation that would distinguish the alternatives.
3. **Show the system acting.** Name the actor, input, operation, state change, and output that matter. Trace one request or record through the relevant components. Introduce precise semantics after the example has given the reader something to attach them to.
4. **Make comparisons fair and useful.** Give alternatives the same decision dimensions. Preserve each credible option's advantage, then explain which constraint decides this case. For measurements, retain the baseline, population, units, and conditions needed to read the difference.
5. **State each claim at its supported strength.** Use present tense for specified behavior, past tense for a completed observation, explicit proposal language for a proposed change, and conditional wording for a hypothesis. Keep a qualification accessible where it is needed to interpret the claim. Strong writing instructions call for decisive author actions, not exaggerated certainty about facts.
6. **Spend detail on understanding.** Include the example, definition, counterexample, or failure path that resolves a likely reader question. Introduce unfamiliar or locally redefined terms at first useful use; use familiar vocabulary directly. Match depth to the reader, not an arbitrary length target.
7. **Make the useful content visible.** Give the opening's explanation, finding, or task and its decisive support enough space in any medium. Use prose for relationships, tables for parallel comparisons, steps for dependent actions, and figures when visible structure or behavior is easier to understand than text. Titles, captions, and body text should contribute different information. A document need not become a dashboard or contain a figure.

For example, in an independently constructed **synthetic proposal**:

> Store a completion record for each batch. On restart, retry batches without a completion record. A crash after saving output but before recording completion can replay the same batch, so key output writes by batch ID and make repeated writes idempotent.

The paragraph gives the proposed operation, the recovery path, and the implementation condition. It teaches the mechanism rather than praising reliability. In a real document, establish those semantics from its design and implementation.

## Choose useful examples and detail

Read only the reference that resolves the current writing decision. A substantial document can benefit from a nearby finished example; a sentence edit does not need the full library.

- **Choose between new writing, local editing, and structural revision:** [authoring and revision](references/authoring-and-revision.md) covers source grounding, scope, and preserving voice while repairing the reader's problem.
- **Build sentences and paragraphs:** [voice and factual prose](references/voice-and-facts.md) covers subjects, logical connections, claim strength, and detail placement.
- **Resolve language-specific meaning or voice:** [multilingual writing](references/multilingual-writing.md) provides conditional English, Korean, Italian, and Chinese guidance; use the same meaning checks for other languages.
- **Choose the document's structure:** [document forms](references/document-forms.md), including guides, memos, posts, and engineering forms. Use the reader's task and governing template, not every listed section.
- **Explain, compare, investigate, or report progress:** [writing patterns](references/writing-patterns.md) pairs reader situations with writing actions, finished examples, and reader checks.
- **Inspect sentence, paragraph, table, and caption craft:** [worked examples](references/worked-examples.md) contains public close readings and synthetic rewrites.
- **Find a nearby public work:** [example library](references/example-library.md) groups design documents, engineering investigations, and visual explanations by task. Read the relevant passage before borrowing its technique.
- **Understand the original technical and editorial basis:** [source readings](references/source-readings.md) retains section-level analysis of papers, specifications, and documentation guides.
- **Present numbers, uncertainty, equations, or figures:** [measurements and figures](references/measurements-and-figures.md).
- **Produce a PDF or editable document:** [document production](references/document-production.md). Start with Typst for an unconstrained print-first report, DOCX when recipient editing decides the medium, or the project's existing source. PDF needs no shadcn intermediate.
- **Combine internal sharing, data views, and frontend work:** [composition](references/composition.md). Use optional companions for their specialty without restarting intake or requiring the entire pack.

Borrow the source's explanatory operation and adapt its depth to the reader. Keep the project's architecture, evidence, and voice authoritative. A useful public example can motivate a technique without establishing a universal heading, chart count, governance process, or current API.

## Verify the reader's result

Check claims against inspected sources and compute arithmetic with tools. Preserve measurement boundaries, exact identifiers, requirement levels, and proposal status. Label invented teaching examples as synthetic; never present them as collected results. Keep a missing measurement distinct from zero and a temporal association distinct from a demonstrated cause.

Read the document without the drafting conversation. Check the actual reader-facing content before delivery:

- Does the opening make the useful explanation, finding, comparison, or task easy to find, with its decisive support given room?
- Does each production or verification detail help this reader interpret, reproduce, audit, or act?
- Can this reader correctly interpret each claim or view using its wording, surrounding context, and appropriate supporting material, without redundant qualifications?
- Do definitions, UI instructions, headings, and captions add information the intended reader needs?
- Are paragraphs organized by meaning, with facts, logical relations, voice, and material limits intact?

Use these questions to repair the artifact, not to print a checklist or a self-congratulatory completion paragraph. In Markdown, keep natural prose paragraphs without fixed-column source wrapping. Preserve list structure, code, and intentional hard breaks. Rendered line width is a separate layout choice: inspect it for the medium and reader instead of treating unwrapped source as a requirement for unlimited screen width.

Inspect the final text in its destination context; render generated outputs and check figures, links, tables, page boundaries, and the initial view where relevant. Deliver the artifact and editable source where applicable. Include private personal or organizational information only within the authorized audience and purpose; permission to inspect a source is not permission to disclose it. Match source access to recipients, and publish or send only when authorized. Finish when the requested artifact and applicable checks are complete; report only material unresolved issues in the delivery note.
