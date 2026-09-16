---
name: technical-report-writing
description: >
  Use when writing or revising technical reports, engineering proposals,
  design docs, RFCs, ADRs, experiment reports, or project documentation in
  Markdown, HTML, editable documents, or PDF. Teaches factual prose,
  explanation, evidence, comparison, and document production through public
  examples. NOT for marketing or PR copy, or prose polish alone.
---

# Technical Report Writing

Write a document the reader can use to explain a system, evaluate a result, or choose an action. Make the important point easy to find and the reasoning worth reading. Use concrete subjects, exact operations, useful examples, and evidence proportionate to the claim. A dry register is direct and complete, with enough technical detail to understand why the result or design matters.

Infer the reader, task, source material, and medium from the request and project. Preserve established terminology, source files, and required templates. A review returns findings; a writing request returns the requested artifact. Recover available inputs before asking about consequential gaps.

## Build the explanation from evidence

1. **Choose the reader's entry point.** Open a report with its important finding, a proposal with the changed behavior and reason, a procedure with the task, and an explanation with the concrete problem or example that makes the concept useful. Select the entry point for this document rather than imposing one outline.
2. **Connect the facts.** Give each paragraph a job: trace a mechanism, interpret an observation, compare alternatives, or justify a choice. Supply the relation between evidence and conclusion. When evidence leaves a choice unresolved, identify the observation that would distinguish the alternatives.
3. **Show the system acting.** Name the actor, input, operation, state change, and output that matter. Trace one request or record through the relevant components. Introduce precise semantics after the example has given the reader something to attach them to.
4. **Make comparisons fair and useful.** Give alternatives the same decision dimensions. Preserve each credible option's advantage, then explain which constraint decides this case. For measurements, retain the baseline, population, units, and conditions needed to read the difference.
5. **State each claim at its supported strength.** Use present tense for specified behavior, past tense for a completed observation, explicit proposal language for a proposed change, and conditional wording for a hypothesis. Put a material qualification beside its claim. Strong writing instructions call for decisive author actions, not exaggerated certainty about facts.
6. **Spend detail on understanding.** Include the example, definition, counterexample, or failure path that resolves a likely reader question. Introduce unfamiliar or locally redefined terms at first useful use; use familiar technical vocabulary directly. Keep reproducibility detail retrievable without repeating it at every result.
7. **Give each form a distinct job.** Use prose for relationships, tables for parallel comparisons, steps for dependent actions, and figures for visible structure or behavior. Let the title orient or state the finding, the figure show the evidence, the caption supply local conditions, and the body explain the implication.

For example, in an independently constructed **synthetic proposal**:

> Store a completion record for each batch. On restart, retry batches without a completion record. A crash after saving output but before recording completion can replay the same batch, so key output writes by batch ID and make repeated writes idempotent.

The paragraph gives the proposed operation, the recovery path, and the implementation condition. It teaches the mechanism rather than praising reliability. In a real document, establish those semantics from its design and implementation.

## Choose useful examples and detail

For a new substantial document, read [voice and factual prose](references/voice-and-facts.md), the relevant [document form](references/document-forms.md), and the matching example below. For a small revision, load only what resolves the actual choice.

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

Read the document without the drafting conversation. Can the reader state the main point, explain its support, find the condition that changes its interpretation, and perform the intended next task? Retain details that help those answers; remove author-facing self-description and duplicated explanation.

Render and inspect the actual requested output, including figures, links, text, tables, and page boundaries. Deliver the artifact and editable source where applicable. Match source access to authorized recipients. Public packages contain public-source analysis or independently synthetic examples, not private records, internal metrics, logs, or personal paths. Publication requires the corresponding user request.
