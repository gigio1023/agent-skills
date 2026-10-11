# Agent instructions

## Pack layout and authoring

- Packages live in two install sets: `skills/minimal/` is installed by default and `skills/additional/` on request. A set decides availability only; each skill's description and invocation settings decide when it runs. Say "install set", not "tier", which is reserved for routing difficulty.
- A minimal skill works without any additional or external skill. It may point to one with "when installed", but it does not require it.
- Public skills and documentation are English. Keep Markdown prose as natural paragraphs on one source line. Use established field language; do not invent framework terminology or require a fixed thinking sequence.
- Keep each skill self-contained with colocated references, scripts, and assets, loaded for a named decision rather than all at once. Keep private transcripts, credentials, datasets, and work-derived examples out of packages; use synthetic examples or authorized public sources.
- Preserve each skill's invocation contract. Skills whose unrequested run would interview the user, write to the user's records, or spend resources open only on request, stated in the description and the body. Harness controls (`disable-model-invocation`, `policy.allow_implicit_invocation: false` in `agents/openai.yaml`) also stop a natural-language request from loading the skill, so use them only for skills meant to be invoked by name, such as `credo-taste` and `credo-journal`.
- When responsibilities change, update the README catalog, affected references, the terminology index, and `docs/migration.md` together. No runtime framework, daemon, mandatory project database, or model-evaluation scaffolding in skill payloads.
- `docs/gigio-pack/` and `docs/research-credo/` are source records of the repositories absorbed on 2026-10-12. Current rules live here and in the skills; those records explain why older rules existed.

## Work and authority

- The user owns direction, tradeoffs, and authority; agents maintain findings and current understanding. Plan only through the next useful decision. A finding, rejected hypothesis, unsuitable dataset, or unresolved comparison can be a useful result without a code change.
- Quick checks within the same question and granted resources can proceed. Ask before a new direction, a newly proposed long activity, or spending beyond a stated budget, unless already authorized. A request that covers several steps grants those steps.
- An explicit user choice about delegation governs; otherwise the lead decides within the active harness policy.
- The `credo-` skills are the paper track: apply them only to work aimed at a paper or a publishable research claim. Product, customer, and capability decisions use the work-track skills and `praxis-direction`. A design skill never declares its own instrument ready; `evaluation-audit` reads the artifacts.

## Validation and publication

Discover all packages with the Skills CLI, validate their metadata and resource links, and check changed templates, examples, and scripts. Static review does not demonstrate model behavior; model comparisons require a corresponding request. Commit only when requested; a PR request includes scoped commits and push. Use conventional English titles and concise PR bodies that say why and what.

## Tests

A useful test protects a meaningful caller-visible contract and derives expected results independently from the implementation under test. Use requirements, documented contracts, independent calculations, or reproduced bugs. Copying expected values from the code merely repeats its assumptions; writing a test after the implementation does not itself make the test invalid.

- Verify features end to end. Run the real entry point on real or fixed input and leave an artifact another person can rerun and compare, such as an output file, log, report, or screenshot. Give the command and the artifact path in the final message.
- Choose focused cases from plausible failures and the behavior callers depend on. Use an isolated test when it can establish a contract more directly or cover a failure path the entry-point run does not exercise.
- For a bug fix, reproduce the failure before the fix when feasible and retain the cases needed to protect the corrected contract.
- Public APIs, CLI behavior, parser rejection, compatibility, cancellation, and resource cleanup can warrant tests, as can security, financial, data-loss, and reported-number risks. Avoid redundant tests that add no useful regression signal.
- Diagnose a test that fails during refactoring. Fix a behavior regression in the code; adapt stale setup or implementation-specific assertions while preserving the public contract. Remove a test only when its contract is obsolete, redundant, or has no independent value, and explain why. A failure alone is not evidence that the test should be deleted.
- Test observable outcomes rather than internal helper layout, fakes built only for the test, or exact prompt and message wording without a specified contract. Exact values, serialized text, and formatting can be valid assertions when an API, protocol, documented CLI, or consumer depends on them.

End-to-end path here: run each changed bundled script on real or fixed input, then discover and validate the affected packages with the Skills CLI and package validators. Relevant contracts include preserving user text in `skills/minimal/copydesk/scripts/sync_profile.py`, protecting account data in `toss-portfolio-state`, keeping `skills/additional/credo-journal/scripts/journal.py` append-only so existing journal content never changes when an entry is added, and maintaining documented parsing, output, and failure behavior in bundled tools. Documentation-only edits need package and consistency checks; model trials require a separate request.
