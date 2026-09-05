# Reference Research

Use this for Direct work and for Adapt or Review work only when the project does not provide enough design context. The goal is to extract decisions with evidence, not assemble a collage of attractive surfaces.

## Contents

- [Classify Supplied Material](#classify-supplied-material)
- [Frame The Search](#frame-the-search)
- [Select Sources](#select-sources)
- [Extract And Synthesize](#extract-and-synthesize)
- [Reject Weak Transfers](#reject-weak-transfers)
- [Stop And Fall Back](#stop-and-fall-back)

## Classify Supplied Material

Determine what role each user-provided screenshot, link, repository, or design file has before searching:

- **Target:** the user asks to match, recreate, or treat it as the design source. It belongs with the requirements. Preserve its material constraints and ask only when fidelity or reuse rights materially change the result.
- **Constraint:** it establishes brand, platform, component, content, or workflow rules. It bounds the solution even when it is not the desired appearance.
- **Inspiration:** it shows a quality, mood, or pattern to consider. It supplies evidence but does not override the product job or existing contract.

Do not infer pixel fidelity from “inspired by,” and do not dilute a named target into a general mood board.

## Frame The Search

Write one sentence for the screen's user job and name the unresolved design decision. Search for that decision rather than a vibe adjective.

Useful query frames include:

- `<domain> <user task> interface` for shipped workflows;
- `<subject> visual archive`, `<subject> material`, or `<subject> diagram` for domain-native visual substance;
- `<interaction> accessibility pattern` or `<component> design system` for a tested behavior;
- `<surface> long content`, `<surface> empty state`, or `<surface> mobile` for state and responsive evidence.

Search only when the answer could change hierarchy, interaction, visual material, density, or a costly implementation decision.

## Select Sources

Use at most three source classes unless the request calls for deeper research:

1. A shipped product that supports the same user workflow.
2. Subject-native material such as real objects, maps, diagrams, archives, documents, imagery, or data conventions.
3. A standard or production design system that covers the risky interaction.

Prefer primary screens, repositories, and official guidance. Use galleries and brand reconstructions to discover candidates, then verify important decisions against the original product or a stronger source. A popular or polished page is not proof that its pattern fits the current task.

Record provenance for assets, code, fonts, and icons. Reuse them only when the license and project allow it. A reference can inform a decision without granting reuse rights.

## Extract And Synthesize

For each source, capture only:

```text
Transfer: the decision worth bringing into this work
Constraint: why it cannot be copied unchanged
Evidence: the screen, code, data, or guidance that supports the judgment
```

Then synthesize the evidence into the smallest build brief that answers:

- What establishes the reading order?
- What is the primary visual anchor and how does it come from the subject, data, product, or user task?
- What density and grouping fit the repeated work or reading behavior?
- Which states, viewports, and interactions carry the highest risk?

Translate references into relationships and behavior. Do not combine one source's palette, another source's radius, and a third source's hero treatment without a product reason tying them together.

## Reject Weak Transfers

Drop or revise a candidate decision when:

- it works only with content, assets, or data the project does not have;
- it reduces the primary task's speed, clarity, or information density;
- it copies brand identifiers or a distinctive composition without permission;
- it covers only a staged desktop happy path;
- its source is an unattributed reconstruction or generated analysis presented as official guidance;
- removing the surface styling leaves no useful hierarchy or interaction model.

## Stop And Fall Back

Stop when the evidence resolves the hierarchy, anchor, density, and risky states. More references after that point usually add noise.

If web search, a design catalog, or an optional MCP service is unavailable, use the existing product, user-provided material, bundled assets, and standards. Do not block the task or invent external evidence. State the missing source only when it leaves a material design decision uncertain.
