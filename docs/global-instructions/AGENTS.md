# Writing profile

When writing or revising a document, PR body, issue, or any text a colleague will read, apply the technical-report-writing skill even when no skill was named. Its writing profile follows and applies in every session; the block is a copy of the skill's `references/writing-profile.md`, refreshed with `python3 ~/.agents/skills/technical-report-writing/scripts/sync_profile.py ~/.codex/AGENTS.md`.

<!-- writing-profile:start -->
# Writing Profile

Standing preferences of this pack's author for documents, PR bodies, issue bodies, and messages to colleagues that the author writes or asks to have written. Apply them whenever drafting or revising such text, whether or not a skill was named; when revising another person's text, their voice and register stay, and only the meaning and structure rules apply. A current explicit request or a governing template overrides a line here. This file holds taste only; the craft rules that apply to any writer stay in SKILL.md and are not repeated here. It is the single source: the author's instruction files carry it by import or by a copy that `scripts/sync_profile.py` refreshes, and it stays within 40 lines.

## Reader

- A colleague who knows the field and lacks this project's context. Explain the mechanism, not the discipline.

## First screen

- Start with the subject, the finding, or the decision. No sentence that introduces the document: purpose declaration, reading order, "읽는 기준" or "이 문서에서 하려는 일" labels, section previews, or a sentence that describes the table below. Scope lives in the title and the first line's subject; one line pointing to a sibling document is allowed in a document set. A date stays beside the table or number it bounds, never as a document-level as-of line. Inside one document there is no reading guide; a set of pages may have one overview table that says which page holds what.
- A summary block is a heading or bold label plus short parallel items, one or two levels deep, ending in noun phrases.
- Blocks, bullets, and notes the user wrote stay as written in every later pass. A user note left on the page is an instruction to the writer, never text for the reader.

## Body

- Structure carries the content: nested items, tables, and callouts are the default texture, and a nested item states a claim and then its condition. A paragraph appears where reasoning needs connecting words, as for a mechanism, a cause, or a trade-off, and opens with its point. Mechanism, equations, and confirmed examples keep their depth inside that structure; shorter never means shallower.

## What stays and what goes

- Keep theory, equations, figures, confirmed examples, and numbers whenever the reader needs them to understand the subject, including after a request to shorten. Shorten by removing orientation, repetition, process narration, and exhaustive inventories.
- Keep a condition beside a number when the reader would read the number differently without it. Keep one sentence on an unverified point when the reader would otherwise act as if it were verified. Drop sentences that record the author's diligence: lists of what was not checked, scope disclaimers, and next plans, unless the document's job is that status.
- A candidate stays a candidate and a proposal stays a proposal. State the status once, in the heading or the opening summary; body sentences, section headings, and figure labels must not contradict it (no "시작할 benchmark" for an example, no "논의 중" for the author's own proposal).
- Name an evaluated unit by what it is and who produced it (target LLM answer, judge prediction, human reference label); an internal alias such as `v3` follows the role description and appears only for lookup.

## Form

- Headings are noun phrases. Table cells hold values or short phrases; a table whose cells need widening is redesigned.
- Field terms stay in English (judge, harness, ablation, residual stream); ordinary verbs and nouns are Korean. The register is dry and direct: no first-person framing ("I found", "내가 제안하는"), no author or date byline, no courtesy closing, and no sentence that repeats who owns the page or why it is shared. No middle dot (U+00B7) and no dash as punctuation in any body text, Korean or English; a colon splits a label, a period or a connective ending splits clauses, and a Korean connective ending is not followed by a comma. Quotations, code, and official names keep their original marks.
- Inside a figure canvas: names and mechanism only. Counts, timestamps, sample sizes, comparison conditions, and hedges go in the caption or the adjacent prose. Figures assume an expert reader; organize or split rather than simplify.
- Screens default to dark styling; light only on request. A requested PDF or print copy follows its own medium.

## PR and issue

- Ask which language the reviewing team reads before drafting a PR; English is the default answer, this author's company repos are Korean.
- A PR body says why and what only, with no validation section, hedges, or self-appraisal. A behavior change always shows as-is and to-be with a table and a `technical-diagram` figure, measured against the PR's real base branch.
- An issue names the outcome it serves before the tasks, and stays short.
<!-- writing-profile:end -->
