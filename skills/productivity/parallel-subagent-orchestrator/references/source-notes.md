# Source Notes

Last reviewed: 2026-06-29.

This skill was designed from the user's repeated need for sustained parallel
subagent work across coding, research, literature review, and value judgment,
plus public patterns from current agent ecosystems.

## Sources That Shaped The Skill

- OpenAI Codex subagent docs: subagents are useful for independent work, but
  spawning should respect the current harness and user intent. This shaped the
  explicit "lead agent owns the decision" and Codex consent cautions.
- Anthropic multi-agent research writing: lead-worker decomposition, clear
  objectives, independent source lanes, and synthesis are more important than
  raw agent count. This shaped the claim/evidence synthesis gate.
- Anthropic/Claude skills guidance: skills should use progressive disclosure,
  gotchas, and folder structure rather than cramming every rule into SKILL.md.
- Claude Code subagent and agent-team docs: context isolation, specialized
  roles, and fresh work packets are valuable, but team systems have coordination
  costs. This shaped the "smallest useful first wave" rule.
- flow-next and cc-sdd: durable specs, task boundaries, re-anchored workers,
  independent review, and receipts are strong patterns for long-running coding
  work.
- codex-subagents-mcp: archived, so not adopted directly, but its ideas around
  file-backed agent definitions, validation, and isolation influenced the
  harness-neutral adapter thinking.

## Patterns Accepted

- One portable orchestration skill instead of separate Codex/Claude/Cursor/etc.
  skills. The policy is stable; the mechanics are harness-specific.
- Companion routing skills may provide exact model preferences for a user or
  team. This skill consumes those preferences but does not hardcode them.
- First-wave breadth followed by narrower follow-up waves.
- Explicit output contracts for every delegated task.
- Evidence/confidence/conflict synthesis rather than summary concatenation.
- Skeptic lanes for noisy web/GitHub/tool research.
- Disjoint ownership for parallel code edits.

## Patterns Rejected

- Large catalogs of named specialist agents as the default interface. They look
  powerful but are brittle across harnesses and often encourage overdelegation.
- User-specific model policy embedded in this harness-neutral skill. Exact
  model preferences belong in companion routing skills such as
  `fable5-judgment-orchestrator`.
- Star-count-driven tool selection. Popularity is useful only as an adoption
  signal.
- Automatic background self-improvement or scheduled skill rewriting. Skill
  updates should be deliberate and evidence-backed.
- Pretending to run parallel work where the harness does not provide delegation.
