# Sources And Rule Provenance

Checked 2026-09-05. Format specifications, runtime contracts, authoring advice, and example implementations serve different purposes. This is a scoped synthesis, not a complete API snapshot.

## Contents

- Format and runtime
- Authoring sources
- Local decisions
- Freshness

## Format And Runtime

[Agent Skills specification](https://agentskills.io/specification) defines required name/description metadata and optional license, compatibility, metadata, and experimental allowed-tools fields. Name syntax and folder identity are format requirements. Its approximate 5,000-token and 500-line guidance is authoring advice; it does not impose an 8KB file limit.

[Claude Code skills](https://code.claude.com/docs/en/skills) documents native invocation, hooks, and execution controls. The current runtime even permits omitted frontmatter fields; this package's portable validator intentionally requires name/description. Native fields need runtime-specific review.

[Anthropic authoring guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) also restricts reserved names and XML in metadata. The validator's optional claude-code target applies those restrictions, not the full native schema. It is not a runtime-conformance certification.

[OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills) describes on-demand instructions and native agents/openai.yaml metadata. Its initial skill-list budget is 2% of context, with an 8,000-character fallback when the context size is unknown. That catalog budget does not limit individual files; selected skills load their full instructions.

## Authoring Sources

### Thariq Shihipar

[How we use skills](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills) is dated June 3, 2026 on the official blog. A March 17 posting is visible in an [archive of his X post](https://x.noodl3.net/trq212/status/2033949937936085378); direct X retrieval was unavailable. The blog date should not be treated as the first publication date. Its byline identifies an Anthropic member of technical staff working on Claude Code, not a team-lead title.

Later writing and implementation broaden the advice beyond that skills article. Dates below refer to official blog publication or the indicated artifact, not search-index crawl dates. Adaptations are in [authoring patterns](skill-tips.md).

| Source | What it supports and where it stops |
| --- | --- |
| [Seeing like an agent](https://claude.com/blog/seeing-like-an-agent), April 10, 2026 | Design tools around observed model behavior; revisit action and retrieval interfaces. It does not require a particular tool count. |
| [Session management](https://claude.com/blog/using-claude-code-session-management-and-1m-context), April 15, 2026 | Choose continuation, compaction, reset, or isolation from task relevance and context needs. Native commands and context sizes are host-specific. |
| [Prompt caching](https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything), April 30, 2026 | Stable prefixes and dynamic updates matter to Claude's harness. Apply cache details to supported adapters, not as portable tool/model-switching prohibitions. |
| [HTML artifacts](https://claude.com/blog/using-claude-code-the-unreasonable-effectiveness-of-html), May 20, 2026 | Human-readable, interactive references and exported decisions; explicitly a personal preference, not a required format. |
| [Dynamic workflows](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code), June 2, 2026; coauthored with Sid Bidasaria | Task-shaped orchestration and adaptable workflow templates. Coordination and token cost must earn their place; native features need host support. |
| [Finding your unknowns](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns), July 6, 2026 | Discover missing requirements with references, exploration, prototypes, or questions; revise from discoveries during work. Personal habits such as interviews, fresh sessions, and quizzes are not universal gates. |
| [Context engineering for Claude 5](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models), July 24, 2026 | Audit overlapping instructions, design expressive interfaces, and supply rich references. The reported >80% reduction with no measurable coding-evaluation loss applies to their system prompt and models, not a quota or a result for our skills. |
| [ELI5 source](https://github.com/anthropics/claude-plugins-community/blob/794af9e63d07fad17087dcab61f21f44cb48effd/eli5/skills/eli5/SKILL.md), August 21, 2026 | A small audience-and-format skill. This revision and authorship were checked through GitHub history; the source is 10 lines and 321 bytes. Size and existence establish neither accuracy nor comparative performance. |

The July 19 [Peter Yang interview page](https://creatoreconomy.so/p/how-i-plan-build-and-run-loops-with-claude-code-thariq-shihipar) publicly lists related planning, artifacts, and verification topics. Only its public introduction and takeaways were inspected, not subscriber-only content; the guidance here is grounded in the direct articles and code above.

These operational lessons are not format validation requirements. A short skill can encode a recurring preference without a complicated workflow. Important task invariants still need precise instructions. Model-specific claims should not be silently transferred to another model or runtime.

### Anthropic

The [authoring guide](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) supports clear discovery, selective detail, and control matched to task fragility. Contents maps and size advice address usability, not runtime rejection.

The [engineering introduction](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) explains filesystem disclosure, code reuse, actual-task feedback, and inspection of code/dependencies/external access. Static scanning cannot establish that an arbitrary package is secure.

### Agent Skills creator guidance

[Best practices](https://agentskills.io/skill-creation/best-practices) starts with real expertise and project artifacts. It favors coherent scope, moderate detail, specific retrieval conditions, and defaults instead of exhaustive menus. Its examples are patterns to adapt rather than a compulsory workflow.

### Maintained implementations

- [Anthropic skill-creator](https://github.com/anthropics/skills/blob/41bbe19d1a1a7eaab5e7bb9050a417e5c6cffc8f/skills/skill-creator/SKILL.md): iteration and user-reviewed comparative runs; it also allows skipping evaluations when the user does not want them. Its runner and directory layout are implementation choices.
- [OpenAI skill-creator](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/SKILL.md): separate reusable code, references, output assets, and native UI metadata; do not promote one implementation's preferred layout into a format rule.

These revisions were resolved on the check date. Reading them does not authorize installing or executing their workflows.

## Local Decisions

| Rule | Classification and rationale |
| --- | --- |
| Remove 8KB warning | Unsourced heuristic introduced in [agent-skills PR 4](https://github.com/gigio1023/agent-skills/pull/4) |
| File above 500 lines | Organization advisory, not format failure |
| Long reference without contents map | Advisory; headings/search hints can suffice |
| Cross-links between references | Valid; broken direct links fail, auxiliary paths need context review |
| No Gotchas heading | Valid; include useful exceptions, not filler |
| Standard optional metadata | Type-checked; native/unknown fields require review |
| Actual YAML parser | Local choice to accept valid quoting and structured metadata |
| Model evaluations opt-in | Workflow preference, separate from script regression tests |
| Mutable state outside installed files | Protect data during package replacement |
| Naming without mandatory scoring | Preserve working names unless change has value |
| Minimal authoring path | Audience and result preferences can be sufficient; no mandatory resources or workflow |
| Diagnose before adding rules | Repair the missing information, retrieval, interface, or conflicting instruction |
| Inspect relevant co-loaded guidance | Resolve duplication at its source within authorized edit scope |
| Revisit workaround rules on relevant change | Retain condition and evidence where useful; no deletion percentage or expiration ritual |

The [validation contract](validation.md) gives executable checks and coverage limits. Other pack skills may prefer two fields as a conservative authoring default; that is not a general prohibition on optional standard metadata.

## Freshness

Reopen a relevant source when changing version-sensitive behavior, investigating reported drift, or reconciling the installed runtime. Record what was checked. Do not mark an entire snapshot current after checking only one section.

If verification is unavailable, identify that claim. Avoid unsupported benchmark numbers, ecosystem counts, and fixed expiration rituals. No model-performance comparison was performed for this maintenance revision.
