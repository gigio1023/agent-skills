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
Cognitive latitude is part of the grant too: how far Codex should
investigate, judge, recommend, or opine is the host's call — write it
into the packet rather than leaving it implied.

Choose a broad judgment grant, not an exhaustive permission table. The host
may ask Codex to execute fixed decisions, decide within named bounds, or own
investigation, judgment, and decisions end to end. Name the consequential
choices reserved to the host; ordinary reversible choices inside scope may
stay implicit. If the packet grants a decision, Codex should make it rather
than returning it for ceremonial approval.

Internal parallelism is a standing recommendation inside a delegated run.
Codex may freely decide whether to spawn subagents, how many to use, and how
to coordinate them without asking the host for each dispatch. Prefer parallel
subagents for independent investigation, implementation, or verification
branches; keep dependencies and conflicting writes sequential. This freedom
does not widen the packet's scope, sandbox, or external authority.

The response contract is always file-backed. Ask Codex to put the complete
report in its final response. The launcher captures that response directly as
`report.md` with `-o`; the packet does not need to know the run path, and the
model does not need write access merely to hand findings back. No finding,
decision, caveat, or verification result may exist only in a progress event.

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

## Judgment authority
Choose the broad grant: execute fixed decisions; decide within named bounds;
or own investigation, judgment, and decisions end to end. Name only the
consequential decisions reserved to the host. Ordinary reversible choices
inside scope belong to Codex unless stated otherwise.

## Authority and pause conditions
What it may run or edit, and which external effects are intended — network
calls, MCP tools, credentials. When it must stop and report instead of
proceeding (destructive actions, contract changes, missing information).
Internal subagents: encouraged. Choose freely whether to use them, how many,
and how to coordinate them. Parallelize independent branches; keep dependent
steps and conflicting writes sequential. Do not ask the host to approve each
internal dispatch.

## Verification
Exact commands to run, and what output counts as passing.

## Response contract
Return the complete report as your final response, covering: ... (findings,
changed files, commands run with results, deviations from this packet,
anything left unverified). The launcher captures it as report.md, so do not
write a separate handoff file or leave material results only in progress.
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

## Judgment authority
Implement the already-decided empty-input behavior. You own ordinary reversible
implementation choices inside the two-file scope.

## Authority and pause conditions
You may edit the two files above and run pytest. If the fix requires an API
change, stop and report options instead.
Internal subagents are allowed, but this task is small and sequential enough
to handle directly unless a useful independent check emerges.

## Verification
`python -m pytest tests/test_parser.py -q` → all passing.

## Response contract
Return a concise complete report: list changed files, include the final pytest
summary line, and note any deviation. The launcher captures it as report.md.
```

## Review and investigation packets

The same shape works for missions that change nothing in the workspace. Use
`read-only`: `-o` is a CLI output capture, so the model does not need workspace
write authority to produce `report.md`.

- **Investigation**: objective = the question; verification = the evidence
  the answer must cite (paths, line numbers, command output).
- **Review**: point at the diff or branch; response contract = findings
  ranked by severity, each with file:line and a concrete failure scenario.
  A fresh thread gives an independent perspective; resume the original
  thread only when continuity matters more than independence.

A read-only mission stays read-only on resume: reuse the original run's
sandbox unless the user has since granted more. "Now apply the fix you
proposed" is new authority — say so in the packet and in your reply.
