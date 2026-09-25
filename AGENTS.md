# Agent instructions

## Tests

A test written after the code, with expected values read off that code, repeats the implementation: it passes by construction, misses the bugs it shares with the code, and breaks on every refactor. Do not write such tests unless the user asks for a specific one.

- Verify features end to end. Run the real entry point on real or fixed input and leave an artifact another person can rerun and compare, such as an output file, log, report, or screenshot. Give the command and the artifact path in the final message.
- When a unit needs an isolated test, first list the ways it can fail, take expected values from the spec or a hand calculation, and only then write the code.
- A bug fix may add one test that reproduces the bug and fails before the fix.
- Keep or add a test only if losing it would let a security, money, data-loss, or reported-number bug ship unnoticed and no end-to-end run covers it.
- If a refactor that keeps behavior breaks a test, the test was checking implementation. Delete it instead of rewriting it and list it in the PR.
- Do not test constants, prompt or message strings, output formatting, internal helpers, or fakes built for the test itself.

End-to-end path here: run each changed bundled script on a sample input, then discover and validate the packages with the Skills CLI. Tests that meet the keep bar: scripts that overwrite user files, such as `skills/productivity/copydesk/scripts/sync_profile.py`, and scripts that handle account data or credentials, such as `toss-portfolio-state`.
