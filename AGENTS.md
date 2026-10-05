# Agent instructions

## Tests

A useful test protects a meaningful caller-visible contract and derives expected results independently from the implementation under test. Use requirements, documented contracts, independent calculations, or reproduced bugs. Copying expected values from the code merely repeats its assumptions; writing a test after the implementation does not itself make the test invalid.

- Verify features end to end. Run the real entry point on real or fixed input and leave an artifact another person can rerun and compare, such as an output file, log, report, or screenshot. Give the command and the artifact path in the final message.
- Choose focused cases from plausible failures and the behavior callers depend on. Use an isolated test when it can establish a contract more directly or cover a failure path the entry-point run does not exercise.
- For a bug fix, reproduce the failure before the fix when feasible and retain the cases needed to protect the corrected contract.
- Public APIs, CLI behavior, parser rejection, compatibility, cancellation, and resource cleanup can warrant tests, as can security, financial, data-loss, and reported-number risks. Avoid redundant tests that add no useful regression signal.
- Diagnose a test that fails during refactoring. Fix a behavior regression in the code; adapt stale setup or implementation-specific assertions while preserving the public contract. Remove a test only when its contract is obsolete, redundant, or has no independent value, and explain why. A failure alone is not evidence that the test should be deleted.
- Test observable outcomes rather than internal helper layout, fakes built only for the test, or exact prompt and message wording without a specified contract. Exact values, serialized text, and formatting can be valid assertions when an API, protocol, documented CLI, or consumer depends on them.

End-to-end path here: run each changed bundled script on real or fixed input, then discover and validate the affected packages with the Skills CLI and package validators. Relevant contracts include preserving user text in `skills/productivity/copydesk/scripts/sync_profile.py`, protecting account data in `toss-portfolio-state`, and maintaining documented parsing, output, and failure behavior in bundled tools. Documentation-only edits need package and consistency checks; model trials require a separate request.
