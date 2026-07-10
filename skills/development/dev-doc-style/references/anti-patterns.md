# Documentation Anti-Patterns

Use this list to diagnose a concrete readability problem. Do not report a
pattern unless it harms the page in context.

## Buried Outcome

The current command, decision, or supported behavior appears only after history
or meta commentary.

Repair: lead with the current outcome, then retain only background that changes
interpretation.

## Mixed Reader Jobs

A page combines onboarding, exhaustive reference, architecture rationale, and
project status with no clear primary reader.

Repair: identify the primary job. Move unrelated depth only when there is a
maintained destination and navigation can be updated safely.

## Bullet as Paragraph

One bullet holds several independent facts, conditions, and links.

Repair: split parallel facts, add a real grouping parent, or return to prose if
the ideas form an argument.

## Decorative Structure

Tables, diagrams, callouts, or nested lists repeat simple prose without making a
comparison, sequence, hierarchy, or warning clearer.

Repair: keep the smallest surface that communicates the relationship.

## Lost Condition

A brevity edit removes words such as "when", "may", "optional", or a version
limit and turns a conditional claim into an unconditional one.

Repair: restore the condition near the affected behavior.

## False Single Source

Repeated content is deleted from a standalone guide in favor of a link that the
reader cannot access or that lacks the needed detail.

Repair: deduplicate volatile detail, not essential local context. Keep a concise
summary where the reader needs it.

## Unlabeled or Brittle Link

"Here", a raw path in prose, or a renamed heading leaves the destination unclear
or breaks an inbound anchor.

Repair: use descriptive link text and search inbound references before renaming
headings.

## Meta Prose

Phrases such as "this section discusses" delay the actual claim.

Repair: state the claim, instruction, or reason directly. Keep scope statements
when they genuinely define what the page excludes.

## Unverified Example

A polished command or output looks authoritative but was copied, invented, or
not run against the repository.

Repair: verify it or label its status and placeholders explicitly.

## Style-Only Churn

A broad rewrite changes terminology and voice while fixing one localized
structure problem.

Repair: constrain the diff. Preserve intentional author voice and project
vocabulary unless the user requested a full style pass.
