---
name: handoff-prompt-writer
description: >
  Use when the user wants a successor-ready handoff prompt, continuation prompt,
  next-agent prompt, session transfer file, or asks to package current work so
  another agent can continue without rereading the whole conversation. Creates
  one executable prompt file from intent, decisions, artifacts, live state,
  evidence, and remaining work. NOT for the paired handoff.md and
  context-pack.json contract produced by workspace-handoff-compiler.
---

# Handoff Prompt Writer

Create one self-contained prompt file that a successor agent can execute. The
default output is `handoff-prompt.md` in the active project root. Write the
file; do not stop at showing a draft in chat.

## Quick Start

1. Confirm the handoff scope from the current request. Use the user-specified
   output path, or default to `handoff-prompt.md`. For a multi-repo task, place
   it at the nearest common workspace root and label every repository.
2. Gather the smallest authoritative evidence set:
   - current user objective, intent, constraints, and explicit decisions;
   - relevant plans, progress notes, results, specifications, and logs;
   - live repository state, changed files, branch and revision, and diffs;
   - test, build, render, or command results that support completion claims;
   - unresolved questions, blockers, risks, and remaining work.
3. Reconcile conflicts. Current explicit user direction controls intent and
   scope. Live files, version-control state, and fresh tool output control
   implementation status. Treat older notes and conversation claims as context,
   not proof, when they disagree with inspectable state.
4. Fill `assets/handoff-prompt.template.md`. Replace every placeholder, remove
   empty optional rows, and keep the result addressed directly to the successor.
5. Point to exact files, commands, commits, and evidence instead of pasting long
   source material or a transcript.
6. Remove secrets, tokens, credentials, personal data, private reasoning, and
   irrelevant history. Preserve material caveats and authority boundaries.
7. Re-read the file cold. Verify that its first actions are executable and that
   every completed claim has inspectable evidence.

Read `references/source-notes.md` only when maintaining the handoff contract or
adapting it to a new agent runtime.

## Prompt Contract

The generated file must contain:

- a direct successor role and operating contract;
- the primary objective and observable definition of done;
- intent and background that explain why the work exists;
- in-scope, out-of-scope, and confirmation-required actions;
- current status, repository or artifact state, and important decisions;
- completed work paired with files, commands, tests, or other evidence;
- an artifact map with paths and why each item matters;
- remaining work ordered by dependency and impact;
- blockers, unknowns, risks, and what would resolve them;
- the first one to three executable actions;
- verification requirements and final delivery expectations.

Use `verified`, `inferred`, and `unknown` labels only where ambiguity matters.
Do not burden obvious facts with labels. A successor should know which claims it
can trust and which it must check.

## Evidence and Source Priority

Use this order for conflicts:

1. Current explicit user instruction for goal, scope, and authority.
2. Current filesystem, repository, external-system state, and fresh tool output.
3. Accepted specifications and maintained project artifacts.
4. Plans, progress notes, prior summaries, and conversation memory.

Do not infer intent from a diff when the user stated it directly. Do not claim
that work is complete because a plan says so or a file exists. State what was
not checked.

## Continuation Behavior

Write the handoff as an instruction to continue, not as a retrospective report.
The successor should be told to:

- re-ground on the named evidence before editing;
- preserve verified work and avoid repeating completed investigation;
- continue in scope without asking for routine reversible actions;
- pause only for destructive or irreversible actions, material scope changes,
  or information only the user can supply;
- validate outcomes before reporting them;
- update or replace stale handoff information if another transfer is needed.

If an existing handoff prompt is present, read it first. Preserve still-valid
context and user decisions, but replace stale status and evidence rather than
appending another conflicting summary.

## Output Contract

Return the path to the generated prompt, its overall continuation status, and
the first action encoded in it. Mention evidence gaps only when they affect the
successor's ability to proceed. The file itself is the deliverable.

## Gotchas

- Do not dump the conversation. Preserve decisions and consequences, not turns.
- Do not include hidden or private reasoning. Record concise rationale and
  evidence that another agent can inspect.
- Do not bury the next action after background. Make the start path explicit.
- Do not copy secrets from environment files, logs, authentication output, or
  tool results into the prompt.
- Do not silently combine unrelated repositories or tasks into one handoff.
- Do not use this skill when the user needs the stricter `handoff.md` plus
  `context-pack.json` parity contract.
