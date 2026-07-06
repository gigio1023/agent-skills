# Source Notes

Last reviewed: 2026-06-29.

This skill is a synthesis, not a verbatim copy. Keep it compact and judgment-oriented.

## Sources Considered

- OpenAI Developers, "Designing delightful frontends with GPT-5.4": useful for current OpenAI-facing frontend prompting patterns: clear constraints, strong visual anchors, structured narratives, design systems, and a frontend skill that emphasizes art direction, hierarchy, imagery, and motion.
  https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4

- OpenAI API prompting docs: relevant meta-rule that prompts/instructions should be treated like application code, versioned, reviewed, tested, and kept close to product behavior.
  https://developers.openai.com/api/docs/guides/prompting

- Anthropic public `frontend-design` skill: strong taste layer for avoiding templated defaults and grounding design in subject matter. Use the principle, not the exact text.
  https://github.com/anthropics/skills/tree/main/skills/frontend-design

- Anthropic public skills guidance: supports progressive disclosure and keeping the trigger description strong while moving detailed material into references.
  https://github.com/anthropics/skills

- Vercel Web Interface Guidelines: strong implementation QA checklist for accessibility, focus, forms, animation, typography, content handling, performance, navigation, layout, theming, i18n, and anti-patterns.
  https://github.com/vercel-labs/web-interface-guidelines
  https://github.com/vercel-labs/agent-skills

- Microsoft `frontend-design-review` skill: useful framing around frictionless action, craft, trust, and design review, but too broad to copy directly into this general design skill.
  https://github.com/microsoft/skills

- StyleSeed: useful distinction between design judgment and token dumps, plus coherence rules for color, rhythm, state, and density. Avoid importing brand skins or many hard numeric rules into the general skill because they can become a new template.
  https://github.com/bitjaru/styleseed

## Selection Criteria

Prefer guidance that:
- Improves decisions across multiple frameworks and output formats.
- Explains when to choose a pattern, not just what the pattern is.
- Produces verifiable behavior: screenshots, responsive checks, accessibility checks, build/lint/test.
- Prevents common AI-generated UI failures without forcing every design into the same aesthetic.

Reject or quarantine guidance that:
- Is mostly trend-chasing or inspirational wording.
- Requires a single brand skin, component library, or visual style for all outputs.
- Adds long rule lists that the agent will follow mechanically without judgment.
- Optimizes only for landing pages while harming tools, reports, dashboards, or documents.

## Architecture Decision

Keep one `frontend-design` skill as the shared art-direction and quality layer. Add references by surface or verification type. Do not create React/Vue/HTML-specific design skills unless repeated failures prove that implementation details need separate local runbooks.
