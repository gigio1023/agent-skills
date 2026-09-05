# Naming Agent Skills

Choose a stable handle. The description drives discovery, so renaming is not a substitute for correcting an unclear trigger.

## Format And Preference

The [open specification](https://agentskills.io/specification) defines syntax and directory identity. This pack prefers lowercase ASCII words separated by single hyphens for predictable tooling; the validator also accepts lowercase Unicode alphanumerics described in the specification. Quote numeric-looking names so YAML preserves their string type.

Anthropic's [authoring guide](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) suggests gerunds while accepting noun and action forms. A gerund is not required. Reserved-name rules depend on the target.

## Choose A Useful Handle

Use the user's established term when clear and distinct:

- Format/domain: pdf, frontend-design.
- Action/object: find-skills, deploy-service.
- Method: systematic-debugging.
- Recognizable policy: verification-before-completion.

Add qualifiers for actual ambiguity. Avoid temporary versions and implementation details unless they distinguish the capability. Do not add agent or skill merely to label a package.

Compare alternatives only when useful; no fixed candidate count, word count, scorecard, or popularity threshold is required.

## Rename Carefully

Keep working names unless requested or a real collision/discovery problem warrants change. Check siblings, directory identity, indexes, install references, and dependent links.

Review a normal trigger and nearby request that should select something else. A read-through is not proof of model routing; live trials require a requested behavioral evaluation.
