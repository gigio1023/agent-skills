# Harness Source Notes

Research refreshed on 2026-07-10 from the local checkouts under `~/git/harness`.
Every repository was updated with a fast-forward-only pull before review. The
revisions below make the research basis reproducible; they are not runtime
dependencies of the skill.

## Primary Source

[Q00/ouroboros](https://github.com/Q00/ouroboros) at `98d3d66d4123` is the
primary method source. Reviewed `skills/interview/SKILL.md`, the Socratic agent,
context-first and interview-hardening RFCs, convergence contracts, and the
ambiguity/ontology implementation. The portable skill keeps:

- one focused Socratic question per turn;
- inverted, context-first intake for rich prior material;
- facts-versus-human-decisions routing and explicit provenance;
- separate ambiguity tracks, pressure passes, and breadth checks;
- ontological, root-cause, lateral, and closure lenses;
- explicit user confirmation before crystallizing the brief.

The portable skill intentionally drops Ouroboros-specific state files, commands,
agent names, mandatory subagents, and synthetic numeric convergence thresholds.

## Comparative Harness Review

| Repository and revision | Material reviewed | Durable contribution |
| --- | --- | --- |
| [NomaDamas/Codexplain](https://github.com/NomaDamas/Codexplain) `0e9a987fb8b9` | `README.md`, explanation UX method | Answer-first, scan-friendly summaries that preserve exact evidence and uncertainty |
| [obra/Superpowers](https://github.com/obra/Superpowers) `d884ae04edeb` | `skills/brainstorming/SKILL.md` | Inspect context first, one question at a time, alternatives and approval before implementation |
| [santifer/career-ops](https://github.com/santifer/career-ops) `267dfb707987` | interview practice and debrief modes | Adaptive follow-up, evidence-backed claims, honest gap capture; also defines the job-rehearsal near-miss boundary |
| [Yeachan-Heo/clawhip](https://github.com/Yeachan-Heo/clawhip) `b9fc36d7b765` | native event and question-request contracts | Keep question payloads bounded and public-safe; preserve approval and routing identity |
| [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) `40927950c49f` | planner and spec-miner agents | Ground requirements in repository evidence, dependencies, risks, edge cases, and verifiable behavior |
| [gmickel/flow-next](https://github.com/gmickel/flow-next) `e38604ebd3a7` | interview/prospect skills and question banks | Classify facts before asking, show stakes and option consequences, track skipped decisions and branch depth |
| [safishamsi/graphify](https://github.com/safishamsi/graphify) `dae602ccd1a3` | graph query and extraction references | Distinguish extracted evidence from inference and make source expansion auditable |
| [garrytan/gstack](https://github.com/garrytan/gstack) `7c9df1c568a9` | `office-hours` and `spec` skills | Smart-skip answered questions, pressure-test polished answers, challenge premises, and force explicit choices |
| [mattpocock/skills](https://github.com/mattpocock/skills) `d574778f94cf` | grilling, grill-me, and to-spec skills | Walk a decision tree in dependency order, inspect facts, keep interview separate from execution |
| [Yeachan-Heo/oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) `95c9d2121fa2` | deep-interview skill and prompt builder | Target the weakest material dimension, cite brownfield evidence, preserve an explicit handoff gate |
| [Yeachan-Heo/oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex) `5d43a5bf6f00` | deep-interview skill, planner, and gate code | Preflight context, non-goals and decision-boundary gates, pressure ladder, and explicit execution contract |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) `14a0d79548d4` | `ponytail-review` skill | Remove ceremony that does not change the result; keep findings and output contracts compact |
| [frankbria/ralph-claude-code](https://github.com/frankbria/ralph-claude-code) `75c88e88c2db` | specification workshop and requirements guide | Use value, implementation, and verification perspectives plus concrete Given/When/Then failure scenarios |

## Synthesis Decisions

- Ouroboros remains the center; comparative sources sharpen question ergonomics,
  provenance, evidence, adversarial review, and stop rules.
- The skill asks one question per turn even though some compared workflows batch
  questions. Deep interviews benefit from allowing each answer to redirect the
  next branch.
- Numeric ambiguity scores were rejected. Topic-independent weights imply a
  precision the interviewer cannot justify; qualitative materiality gates are
  observable and portable.
- Harness-specific question tools, state stores, slash commands, and file paths
  were rejected. Native structured input is useful when available, but the
  question contract must also work in plain chat.
- User autonomy overrides workflows that insist on more questions after the user
  asks to stop. Early closure preserves open decisions and their impact.
- Automatic transcript, spec, or code generation was rejected. The default is a
  chat brief; durable or downstream mutations require explicit user authority.
- Job-interview coaching was kept out of scope despite useful patterns in
  career-ops. The subject here is the user's intent, product, plan, workflow, or
  decision—not their performance as a candidate.
