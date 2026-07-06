# Scenario Catalog

Use this catalog to decide whether `parallel-subagent-orchestrator` is the right
skill, to explain expected use cases to a user, or to design validation prompts
for the skill. Treat the examples as patterns, not a requirement to spawn many
agents.

## Research And Evidence

- Ecosystem scan: compare libraries, tools, products, vendors, package health,
  GitHub activity, issue quality, and maintenance risk.
- Web/news/current-facts research: split official sources, reporting, community
  evidence, and skeptic/slop review.
- Literature or standards review: split primary-source extraction, methodology
  critique, and applicability analysis.
- Company, job, or due-diligence research: split company fundamentals, role/JD
  fit, legitimacy signals, compensation/location constraints, and user-fit risk.
- Market or financial background research: split primary filings/data, market
  narrative, risk/counter-thesis, and decision implications.

## Judgment And Strategy

- Apply/skip, buy/wait, move/stay, build/buy, or choose-between-options
  decisions where advocate, skeptic, operator, and outsider lanes sharpen the
  final recommendation.
- Career, relocation, housing, or investment planning where the decision has
  real cost and uncertainty is spread across independent evidence sources.
- Product or architecture strategy where implementation feasibility, user value,
  risk, and reversibility need separate lenses.

## Coding And Verification

- Unknown codebase exploration before implementation: architecture lane, test
  lane, risk/contract lane, and implementation-boundary lane.
- Parallel implementation with clean ownership: separate modules, screens,
  scripts, tests, docs, migrations, or verification artifacts.
- Adversarial code review after an implementation or plan: correctness,
  security/safety, maintainability, performance, accessibility, and user-fit.
- Verification while implementation continues: test runner, browser/UI checks,
  build/export checks, smoke tests, and regression review.
- Migration or release planning: data model, rollout, rollback, docs, and
  operational risk lanes.

## Knowledge Work And Skill Design

- Agent skill design or optimization: trigger contract, workflow structure,
  progressive disclosure, validation prompts, and anti-regression review.
- Prompt-packet library design: define reusable worker contracts, output shapes,
  stop conditions, and evidence requirements.
- Multi-wave synthesis: first wave gathers breadth, second wave resolves
  conflicts, final wave verifies or implements narrow fixes.

## Harness-Specific Routing Hints

- Codex: native subagents often inherit the main session's model and settings.
  Adjust model or reasoning effort only when the harness exposes that choice and
  the user or companion skill gives a reason.
- Claude Code: native subagents, tasks, agent-team features, and installed
  cross-harness plugins vary by setup. Use visible capabilities rather than
  assuming a named worker exists.
- Companion routing skills can pin exact model preferences for a user or team.
  This skill should consume those preferences as policy input while staying
  focused on orchestration mechanics.

## Poor Fits

- Tiny sequential tasks where one pass is faster than framing and merging
  workers.
- Highly private or credential-sensitive work where splitting context creates
  unnecessary exposure.
- Code edits that require overlapping ownership unless the harness provides
  isolated worktrees and the user accepts integration overhead.
- Cases where the lead agent has not defined an output contract, evidence
  requirements, and a stop condition for each lane.
