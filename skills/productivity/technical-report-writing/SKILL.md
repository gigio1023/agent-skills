---
name: technical-report-writing
description: >
  Use when writing or revising dry technical reports, engineering proposals,
  design docs, RFCs, ADRs, experiment reports, or project documentation in
  Markdown, HTML, editable documents, or PDF. Covers voice, factual statements,
  mechanisms, measurements, decisions, and production. NOT for marketing copy,
  PR copy, or prose polish alone (slop-aware-writing).
---

# Technical Report Writing

Produce an engineering document the reader can use to understand a system, evaluate a result, or make a decision. Use a restrained, factual register: concrete subjects, observable behavior, stated measurement conditions, and explicit reasons. Preserve technical depth while removing promotional framing, defensive repetition, and authoring-session narration.

Infer the reader, task, source material, document type, and delivery medium from the request and project. Preserve existing source files, terminology, and required templates. Review requests return findings; writing and revision requests return the requested artifact. Ask only when a missing input changes the result and cannot be recovered from authorized sources.

## Start with the engineering content

Read the evidence before drafting the claim. Establish the current behavior, proposed change or observed result, mechanism, relevant comparison, and consequence for this reader. These are questions for the author, not compulsory headings. A design proposal must not sound like an implemented system; a completed experiment must not be described as a prediction.

Write the most useful entry point for the genre: the result for a report, the changed behavior and reason for a proposal, the action for a procedure, or the concept a reader needs to learn. Build each substantive paragraph around a relation the evidence supports. A list of facts under a headline does not explain why they matter.

Use plain present tense for specified behavior, past tense for a completed measurement or incident, and explicit proposal language for future behavior. Name the component or actor that performs the action. First person is appropriate for an author's measured action or design choice; passive voice is appropriate when the actor is irrelevant and the object is the topic. Dry writing is not subjectless bureaucracy, uniformly short sentences, or unexplained noun fragments.

Keep known facts, estimates, hypotheses, and recommendations distinct in the wording that carries them. Put a material assumption, exclusion, or uncertainty beside the affected statement. Do not introduce a paragraph explaining how carefully the document separates these categories. Remove the generic disclaimer, not the condition that makes the claim true.

## Read the detail the task needs

| Decision | Reference |
| --- | --- |
| Drafting substantial technical prose, or repairing tone, causal language, definitions, and fact presentation | [Voice and factual prose](references/voice-and-facts.md) |
| Choosing the shape of a proposal, RFC, ADR, architecture explanation, experiment report, or operational document | [Engineering document forms](references/document-forms.md) |
| Reporting measurements, comparison tables, uncertainty, equations, or technical figures | [Measurements and figures](references/measurements-and-figures.md) |
| Needing sentence-, paragraph-, table-, and caption-level demonstrations | [Worked examples](references/worked-examples.md): public-source readings and independently constructed synthetic examples |
| Choosing a public technical exemplar or checking where a writing pattern comes from | [Source readings](references/source-readings.md): section-level analysis, transfer decisions, and source versions |
| Producing or converting a PDF or editable document | [Document production](references/document-production.md): native typesetting, analysis publishing, office, and browser routes |
| Combining this skill with internal sharing, dashboards, or frontend implementation | [Composition](references/composition.md) |

For a small edit, use the core and the relevant reference only. For a new technical document, read voice/facts and the relevant document form, then the examples or production detail that resolve actual choices. Do not load every source or force every genre through a single outline.

## Preserve the detail that does work

Explain component responsibilities, data or control flow, state changes, prerequisites, failure behavior, and trade-offs where they determine the reader's understanding. Keep exact API names, units, versions, and status distinctions. Define a term when its unfamiliar or nonstandard meaning changes the argument, not just because it is technical. Use ordinary domain terminology without a glossary tour.

Keep the reasoning behind a decision and the strongest relevant alternative. A rejected option needs its real advantage and the constraint that made another choice preferable. A negative result or limitation belongs when it changes interpretation or action. Generic assurances, cosmetic completion badges, repeated scope statements, and paragraphs describing what the report includes usually do not.

Use prose for explanation, tables for genuinely parallel attributes, steps for dependent actions, and figures for relationships that become clearer visually. Captions and notes supply distinct information; they should not repeat the same conclusion in the title, caption, card, and nearby paragraph. A short document may need no chart. A long technical argument should not be compressed to an arbitrary page limit.

## Verify and deliver

Check substantive claims against the inspected sources, and compute reported arithmetic with the project's tools. Recheck terminology, units, denominators, measurement conditions, and whether a stated cause has causal evidence. Verify a mechanism against the actual design or implementation, not the vocabulary of an admired source. Label invented teaching examples as synthetic; never present them as collected results.

Read the document without the drafting conversation. Check that the main point, its support, and its material conditions remain understandable. Remove detail that serves only the author. Inspect the actual requested output after rendering, including citations, tables, figures, text, and pagination. Deliver the artifact and editable source where applicable.

Match information to the authorized recipients. Public examples must come from public sources or be constructed independently of private cases. Keep private source maps, logs, customer details, internal metrics, and personal paths out of public packages and attachments; replacing names alone is not sufficient anonymization. Publication still requires the corresponding user request.
