# Writing profile

When writing or revising a document, PR body, issue, or any text a colleague will read, apply the copydesk skill even when no skill was named. Its writing profile follows and applies in every session; the block is a copy of the skill's `references/writing-profile.md`, refreshed with `python3 ~/.agents/skills/copydesk/scripts/sync_profile.py ~/.codex/AGENTS.md`.

<!-- writing-profile:start -->
# Writing Profile

Standing preferences for documents, PR bodies, issues, and messages this author writes or asks to have written. Apply them when drafting or revising colleague-facing text. Another author's text keeps its voice and register unless a change is requested. A current explicit request or governing template takes precedence. This file holds taste; reusable craft principles live in SKILL.md. Instruction files import it or carry a copy refreshed by `scripts/sync_profile.py`.

## Reader

- A colleague who knows the field and lacks this project's context. Explain the mechanism and the reason for a decision at the depth that reader needs.

## First screen

- Start with the subject, finding, or decision. Remove preambles that announce the document, repeat its title, or describe the visible table layout. A document set may have an overview that helps the reader choose a page. Put a date beside the result it bounds.
- A summary block uses a short heading or bold label and parallel items. Noun phrases suit labels and compact results; use sentences when conditions or reasoning need them.
- Preserve passages explicitly marked to stay as written. A local correction leaves unrelated prose intact. A broad revision may reshape user-authored prose while keeping its meaning and intentional omissions. A user note to the writer guides the edit and stays out of the reader's copy.

## Body

- Choose prose, lists, tables, and figures for the reader's question. Use tables for comparable attributes, figures for relationships that benefit from a display, and paragraphs for connected explanation. Nest items when the hierarchy carries meaning.
- Keep actors, actions, references, and conditions clear. Preserve natural causal and contrastive sentences; length alone is not a defect. Use consistent terms for the same concept while retaining distinctions between different concepts. Remove repeated framing and padding without dropping grammar or reasoning.

## Content

- Keep useful theory, mechanisms, equations, figures, confirmed examples, and numbers when shortening. Cut repetition, redundant orientation, process narration, and inventories that do not serve the reader. Keep the conditions and uncertainty needed to interpret a claim.
- A candidate stays a candidate and a proposal stays a proposal. Establish status where readers encounter the claim; headings, body, and figure labels must agree. Do not invent team discussion or approval to remove first-person framing.
- Name evaluated units by role and producer, such as target LLM answer, judge prediction, or human reference label. Add an internal alias only when it helps lookup.

## Form

- Prefer specific noun-phrase headings and concise table cells. Put extended reasoning beside the table.
- Keep established field terms in English, such as judge, harness, ablation, and residual stream. Write ordinary verbs and nouns in natural Korean. The register is dry and direct. Remove ornamental first-person framing, bylines, courtesy closings, and self-appraisal; retain attribution or responsibility when it matters.
- Avoid middle dots and dashes as prose punctuation. Use periods, colons, or natural clause connections. Quotations, code, official names, and notation keep their original marks. Choose Korean commas by sentence structure rather than inserting them automatically after connective endings.
- Figure labels carry the names, operations, and quantities needed to understand the visual. Put supporting setup, timestamps, and extended qualifications in a caption or adjacent prose. Keep a condition on the canvas when readers need it to distinguish a branch or interpret a value.
- Screens and figures default to light and should remain legible in dark contexts. Follow the host surface, an existing document's theme, or an explicit request when it sets the delivered theme. PDF and print follow their own medium.

## PR and issue

- Resolve the reviewing team's language from the current request and repository context. Ask only when it remains unclear; English is the fallback and this author's company repositories use Korean.
- A PR body says why and what. Keep validation logs and routine self-appraisal out of it. Retain meaningful conditions and uncertainty. A behavior change uses an as-is/to-be table against the real base branch; add a diagram only when requested. A required repository template takes precedence.
- An issue names the outcome before the tasks and stays short. Use complete sentences for causes, conditions, and mechanisms. `draft-pr` and `write-issue` own their workflows; copydesk supplies shared writing principles.
<!-- writing-profile:end -->
