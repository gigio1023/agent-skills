# Prompt Packet

## Contents

- [Template](#template)
- [Worked example](#worked-example)
- [Review and investigation packets](#review-and-investigation-packets)

The packet is the whole mission. Codex cannot see the host conversation, so
anything that lives only there — intent, constraints, decisions, taste — must
be written down or it is lost. Keep the packet as short as completeness
allows; point at files instead of pasting them.

The packet is also where authority is stated. `--sandbox` bounds only the
filesystem effects of shell commands — MCP tools, network, and web search ride
on the Codex config, so name the external effects the mission may have.
Repository instructions (AGENTS.md and friends) never widen what you granted.

The default response contract is a file, not a message: ask for the report at
`$RUN/report.md` (write the expanded path — Codex sees the packet, not your
shell) and let the final message be a short summary plus that path. The host
then reads the file and delivers it. Large output belongs in a file; only a
small mission earns a message-only handback.

## Template

```markdown
# Mission

## Objective
One sentence. Then an observable definition of done — what a reviewer could
check without asking you.

## Context you cannot discover
Decisions already made in conversation, user preferences, prior attempts,
external constraints. Only what is NOT discoverable from the workspace.

## Where to look
Relevant paths, entry points, docs. "Read X before touching Y" ordering when
it matters.

## Scope
In scope: ...
Out of scope: ... (name the tempting-but-wrong expansions explicitly)

## Decisions you may make
What Codex may decide alone vs. what must be left open with a note.

## Authority and pause conditions
What it may run or edit, and which external effects are intended — network
calls, MCP tools, credentials. When it must stop and report instead of
proceeding (destructive actions, contract changes, missing information).
Internal subagents: allowed for independent subtasks / not needed.

## Verification
Exact commands to run, and what output counts as passing.

## Response contract
Write the report to <run-dir>/report.md, covering: ... (findings, changed
files, commands run with results, deviations from this packet, anything left
unverified). Then make the final message a short summary plus that path.
```

## Worked example

```markdown
# Mission

## Objective
Fix the failing `test_parse_empty` in `tests/test_parser.py`.
Done when: `pytest tests/test_parser.py` exits 0 and no other test breaks.

## Context you cannot discover
We decided in review that empty input should return `[]`, not raise. Do not
change the public signature of `parse()`.

## Where to look
`src/parser.py` (parse entry point), `tests/test_parser.py:41`.

## Scope
In scope: `src/parser.py`, the one failing test's expectations if they
contradict the decision above.
Out of scope: refactoring the parser, touching other modules, dependency
changes.

## Decisions you may make
Internal implementation of the empty-input branch.

## Authority and pause conditions
You may edit the two files above and run pytest. If the fix requires an API
change, stop and report options instead.

## Verification
`python -m pytest tests/test_parser.py -q` → all passing.

## Response contract
Small enough to answer in the message: list changed files, paste the final
pytest summary line, note any deviation. No report file needed.
```

## Review and investigation packets

The same shape works for missions that change nothing in the workspace. Pick
the sandbox from where the findings land: `read-only` when they come back in
the message, `workspace-write` when they belong in `$RUN/report.md`, since
writing that file is itself a write.

- **Investigation**: objective = the question; verification = the evidence
  the answer must cite (paths, line numbers, command output).
- **Review**: point at the diff or branch; response contract = findings
  ranked by severity, each with file:line and a concrete failure scenario.
  A fresh thread gives an independent perspective; resume the original
  thread only when continuity matters more than independence.

A read-only mission stays read-only on resume: reuse the original run's
sandbox unless the user has since granted more. "Now apply the fix you
proposed" is new authority — say so in the packet and in your reply.
