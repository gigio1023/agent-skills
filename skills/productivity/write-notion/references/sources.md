# Sources

Read this when a rule in `SKILL.md` is questioned or being changed. It lists the public sources behind the document shapes, says what kind of support each gives, and separates them from the local choices of this skill. Public sources were read on 2026-10-07.

## Contents

- How strong the support is
- Public sources
- Notion product facts
- Local choices

## How Strong The Support Is

The design doc sources are company handbooks, open-source governance templates, and practitioner accounts. They agree on a core (status in a header, a short summary, background facts, the proposed design, alternatives with reasons, and open questions) and differ on everything else, including names: design doc, RFC, RFD, KEP, PEP, and specification refer to overlapping genres. None measures whether a section order improves review outcomes. The security and evaluation sources are standards guidance and peer-reviewed reporting frameworks, not page templates. Treat the skeleton as a well-motivated default, which is why a team's own template wins over it.

## Public Sources

| Rule | Source | Kind of support |
| --- | --- | --- |
| Write a design doc before implementing a new system; Context is background facts, not requirements; non-goals are things that "could reasonably be goals, but are explicitly chosen not to be goals"; alternatives are among the most important sections; a short cross-cutting concerns section covers security, privacy, and observability; a one-to-three-page mini design doc suits a limited problem; skip the doc when it would only be an implementation manual | Malte Ubl, [Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/) | Practitioner account of one company's practice, not an official template |
| Header fields, the status values WIP, In Review, Approved, and Obsolete, a template readers can exit at any time, abandoned ideas kept with their reasons | HashiCorp, [Writing Practices and Culture](https://www.hashicorp.com/how-hashicorp-works/articles/writing-practices-and-culture), [RFC template](https://www.hashicorp.com/how-hashicorp-works/articles/rfc-template) | Published company practice. The live pages block automated fetches; they were read through a 2024 archived copy, so current wording may differ |
| Writing effort proportional to the change; templates that differ by domain; public templates with open-question sections and a milestones section | Gergely Orosz, [Companies Using RFCs or Design Docs and Examples of These](https://blog.pragmaticengineer.com/rfcs-and-design-docs/) | Secondhand practitioner reporting |
| Background as "indisputable facts, not opinion"; a definition of success | Sourcegraph handbook, [Requests for comments](https://github.com/sourcegraph/handbook/blob/main/content/company-info-and-process/communication/rfcs/index.md) | Company handbook |
| Security considerations for security-sensitive components; design documents updated as the work iterates | GitLab handbook, [Architecture design workflow](https://handbook.gitlab.com/handbook/engineering/architecture/workflow/) and [design document template](https://handbook.gitlab.com/handbook/engineering/architecture/design-documents/_template/) | Company handbook |
| Summary, Goals and Non-Goals, Risks and Mitigations, Test Plan, and Alternatives as sections | Kubernetes, [KEP template](https://github.com/kubernetes/enhancements/blob/master/keps/NNNN-kep-template/README.md) | Open-source governance template, far heavier than a team page needs |
| Open questions grouped by when they are resolved: before the proposal is accepted, during implementation, or out of scope | Rust, [RFC template](https://github.com/rust-lang/rfcs/blob/master/0000-template.md), "Unresolved questions" | Open-source template; the direct basis for grouping a question list by time |
| Rejected ideas recorded with the reason, so they are not reopened; open issues listed while in draft | Python, [PEP 1](https://peps.python.org/pep-0001/) and [PEP 12](https://peps.python.org/pep-0012/) | Open-source process and template |
| Viable options with benefits and drawbacks, the reasoning and data, and the determination; notes "timely rather than polished" | Oxide, [RFD 1](https://rfd.shared.oxide.computer/rfd/0001) | Company process, published |
| An implementation section that says who does what and when; open issues only when there are some | Go, [design doc template](https://github.com/golang/proposal/blob/master/design/TEMPLATE.md) | Open-source template |
| Decision record shape: context, decision, status, consequences, superseded rather than rewritten | Michael Nygard, [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions); [MADR](https://adr.github.io/madr/) | Practitioner proposal and a maintained template |
| Security considerations: what is in scope and out of scope "(and why!)", stated assumptions, remaining risk | IETF, [RFC 3552](https://www.rfc-editor.org/rfc/rfc3552), section 5 | Standards-body guidance for protocol documents |
| Metrics and decision thresholds with the reason for each, evaluation data described | Mitchell et al., [Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993); Gebru et al., [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) | Peer-reviewed reporting frameworks |
| Keep templates minimal and insist on exhaustive detail only for the riskiest projects | Will Larson, [Good engineering strategy is boring](https://lethain.com/good-engineering-strategy-is-boring/) | Practitioner opinion |

## Notion Product Facts

Tool names, parameters, the upload flow, and Notion Markdown syntax in [Notion Markdown mechanics](notion-markdown.md) come from the Notion MCP server's tool schemas and its enhanced Markdown specification resource (`notion://docs/enhanced-markdown-spec`), read through a connected server on 2026-10-07. Notion's public overview of the server is [Notion MCP](https://developers.notion.com/docs/mcp). These are facts about the product at that date; recheck the live schema before relying on a detail.

## Local Choices

These rules are this skill's own. They come from the pack owner's repeated corrections of real pages, so change them with the owner, not by appeal to a source.

- **Default section order.** The skeleton combines the sources above. Milestones and References are kept at the owner's request; Orosz's examples and the Go template include them. Non-goals stay in the default, following Google and the KEP, but are optional: they are omitted when no exclusion would surprise a reader, and the heading then reads "Goals". This matches `copydesk`'s guidance to list non-goals only when they prevent a consequential misunderstanding.
- **Layout.** Summary as nested bullets covering what, how, deadline scope, and the key undecided item; summary, context, goals, figures, and open questions visible; detail under toggle headings. `write-issue` treats collapsed sections as a last resort because an issue should be short. A design doc page is long and read at different depths, so toggles are the default here.
- **Open questions instead of disclaimers.** Undecided items are collected as questions; defensive wording is not scattered through the body. A question list is grouped by when it must be answered, following the Rust RFC template, and not by person unless asked.
- **Status words.** Measured options are labeled comparison evidence, and a selection is written as decided only when the owner decided it. The wording of claim strength itself belongs to `copydesk`.
- **People.** Roles, teams, and sources instead of names; a user mention for the one person the page must identify; few mentions because each can notify; no author names on internal evidence such as measurements, meeting records, or drafts, while published works keep their standard citation. The general rules now live in the writing profile; the skill keeps the Notion-specific part.
- **Terms.** Established field terms over coined local translations, and one term across text, tables, and figure labels, with figures re-rendered when a term changes.
- **Tables.** `header-row="true"` on every table, short cells with explanation in bullets below, and `colgroup` widths sized to content, with `fit-page-width` left unset. The column ranges and the total of about 700 for a default-width page are working values, not a Notion specification; the total in particular was not measured on a rendered page and should be confirmed there.
- **Figures.** One figure per reader question, light PNG from the figure skill, caption with the claim before the reading key, and re-render on any label change.
- **Observed editing failures.** In use before 2026-10-07, `update_content` could not target image blocks, and exact matching failed on long non-ASCII strings and on strings containing mention tags. The fallback of a fresh fetch and a whole-body `replace_content` that keeps child page tags and file sources follows from those failures and from the tool's own deletion safeguard. Revisit these rules when the Notion MCP server changes.
- **Verification after every structural edit.** The checklist collects the defects the owner corrected on published pages, so each check is cheap to run and catches a known way a page goes wrong after an edit.
