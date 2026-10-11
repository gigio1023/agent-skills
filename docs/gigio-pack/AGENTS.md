# Gigio Pack repository guidance

Maintain the project-context and adaptive-work skills described in README.md. Current principles are in docs/principles.md; current load-bearing rules are in docs/rule-ledger.md. Historical decisions retain provenance but do not override later user-approved changes.

## Authoring

- Public skills and documentation are English. Keep Markdown prose as natural paragraphs without fixed-column source wrapping.
- Use established field language. Do not invent framework terminology or require a fixed thinking sequence.
- Keep skills self-contained with colocated resources. References are loaded for a named decision, not all at once.
- Preserve original records, unrelated changes, and private design material. docs/design/ is private historical input, not publication content.
- This repository has no terminology index. Use curate-terminology only when a change introduces, disputes, or bans a term; do not create a glossary for maintenance work with no such term.
- Update README, affected references, instructions, and current rule documentation together when responsibilities change.
- Document craft, explicit editorial defaults, and internal sharing (recipients, source access, sharing pass, delivery) belong to copydesk in agent-skills; the pack's share-internal-doc was retired into it on 2026-09-24.
- No runtime framework, daemon, mandatory project database, or model-evaluation scaffolding in skill payloads.

## Work and authority

A project can span repositories and non-code work. User-owned direction is separate from maintained findings. Plan only through the next useful decision, adapt bounded work to results, and ask before a direction change or long new activity unless already authorized. Preserve narrower resource and side-effect limits.

The four core skills have separate request triggers. A request covering several steps already grants those steps; do not require repeated confirmation. Relevant specialist skills can be used within the task. An explicit user choice about delegation governs; without one, the lead decides within the active harness policy.

Harness, Git, delegation, and Python helpers are maintained in agent-skills. Research methods are maintained in research-credo. Do not restore local copies to repair a missing installation.

## Validation and publication

Discover all nine packages with the Skills CLI, validate their metadata and resource links, and check changed templates and examples. Static review does not demonstrate model behavior. Model comparisons require a corresponding request.

Commit only when requested; a PR request includes scoped commits and push. Use conventional English titles and concise PR bodies. Non-trivial commits explain Context, Changes, Results, and Validation. PRs are draft by default. Publication does not authorize merging, global installation, or cleanup of unrelated worktrees.

## Tests

A useful test protects a meaningful caller-visible contract and derives expected results independently from the implementation under test. Use requirements, documented contracts, independent calculations, or reproduced bugs. Copying expected values from the code merely repeats its assumptions; writing a test after the implementation does not itself make the test invalid.

- Verify features end to end. Run the real entry point on real or fixed input and leave an artifact another person can rerun and compare, such as an output file, log, report, or screenshot. Give the command and the artifact path in the final message.
- Choose focused cases from plausible failures and the behavior callers depend on. Use an isolated test when it can establish a contract more directly or cover a failure path the entry-point run does not exercise.
- For a bug fix, reproduce the failure before the fix when feasible and retain the cases needed to protect the corrected contract.
- Public APIs, CLI behavior, parser rejection, compatibility, cancellation, and resource cleanup can warrant tests, as can security, financial, data-loss, and reported-number risks. Avoid redundant tests that add no useful regression signal.
- Diagnose a test that fails during refactoring. Fix a behavior regression in the code; adapt stale setup or implementation-specific assertions while preserving the public contract. Remove a test only when its contract is obsolete, redundant, or has no independent value, and explain why. A failure alone is not evidence that the test should be deleted.
- Test observable outcomes rather than internal helper layout, fakes built only for the test, or exact prompt and message wording without a specified contract. Exact values, serialized text, and formatting can be valid assertions when an API, protocol, documented CLI, or consumer depends on them.

End-to-end path here: the Skills CLI discovery and validation in Validation and publication above. Skill payloads carry no test scaffolding. Documentation-only edits need package and consistency checks; model trials require a separate request.
