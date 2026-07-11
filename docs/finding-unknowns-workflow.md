# Finding Unknowns Workflow — Design Record

Written 2026-07-11. Status: Tier 0 deployed; the `unknowns-pass` skill is
built in this repository at `skills/productivity/unknowns-pass/`. This
document records the investigation, decisions, and rationale behind absorbing
Tariq Shihipar's "Finding your unknowns" article into a personal workflow. An
agent in a future session should be able to pick up the work from this
document alone.

## 1. Origin and Problem Statement

Source: [A field guide to Claude Fable 5: Finding your unknowns](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns)
(official Anthropic blog, 2026-07-06, published alongside the AI Engineer
World's Fair keynote). The gap between the map (prompts, specs, mental model)
and the territory (the actual codebase, real-world constraints) is what the
article calls unknowns, and it argues that work quality is now bottlenecked
not by the model but by the user's ability to clarify those unknowns. Eight
patterns across three phases:

- Pre-implementation: blind spot pass / brainstorm / prototype / interview /
  reference / implementation plan
- During implementation: implementation notes (recording deviations)
- Post-implementation: pitch and explainer / quiz

(The article groups brainstorm and prototype into one section, but they do
different jobs: brainstorming is divergent option exploration, prototyping is
taste confirmation. This record counts them separately.)

**The user's pain**: the techniques are skipped every time not out of
ignorance but out of tedium. The cost is immediate (annoying questions) while
the reward arrives later and probabilistically — an asymmetry willpower
cannot beat. Result: massive token consumption with low-quality output.

**Diagnosis**: what's missing is not technique but initiation. At the time of
the audit the active environment was entirely pull-only — all 34 installed
skills required explicit invocation, all 7 hooks were Orca telemetry (no
context injection), no global `~/.claude/CLAUDE.md`, and `~/.codex/AGENTS.md`
existed but was zero bytes.

## 2. Investigation Summary (as of 2026-07-11)

### External prior art — already turned into skills at least 5 times

| Implementation | Shape | Stars | Status |
| --- | --- | --- | --- |
| Neeeophytee/finding-unknowns-skills | 8-skill pack + one-file CLAUDE.md/AGENTS.md | 162 | 6 days old, active |
| bozhouDev/finding-unknowns-skills | single CLAUDE.md behavior instructions | 48 | untouched since creation |
| tankadoko/unknowns-field-guide-skill | compressed single skill + one CLAUDE.md router line | 9 | untouched |
| GreatMark/fable-field-guide-skills | plugin | 5 | untouched |
| PH5h5W6d2L/fable-mode | Fable working-style instruction skill | 3 | untouched |

Pre-merge quiz prior art: dkamm/pr-quiz (207 stars, predates the article,
dormant), sphinx-ci (7 stars), Gater (commercial). Verdict: 1:1 ports are
already taken and the niche is crowded but shallow (built, then abandoned).
Nothing is mature enough to adopt — if building, build our own, and only with
a real difference.

### Local harness assets (~/git/harness)

- **Superpowers** (252k stars): the only genuine push precedent. A
  SessionStart hook force-injects skill guidance into every session, and its
  brainstorming skill enforces "HARD-GATE" (that repository's own term: no
  implementation before approval, no exceptions). Maximal process — a bad fit
  for this user. Only the push pattern was borrowed.
- **everything-claude-code `intent-driven-development`**: the best
  engineering quality in the set. Reconnaissance first, depth scaled to risk,
  "does not block implementation by default," an AC `[revised]` protocol
  during implementation. Its output is acceptance criteria, orthogonal to
  unknowns discovery — a complement, not an overlap. Adoption candidate if
  high-risk changes become frequent.
- **mattpocock-skills**: `grilling` (a 12-line ultra-light interview) and
  `prototype` (the best taste-probe implementation — throwaway hygiene, URL
  parameter variant switching, verdict capture). Both are engineering-shaped
  and don't fit non-engineering domains. Adoption deferred.
- **flow-next**: has `flow-next-interview` and friends, but they are locked
  into the flowctl/.flow framework. Partial adoption is not possible.
- **Common blank spot across every repository**: the blindspot direction —
  the agent teaching the human their unknown unknowns — exists nowhere.
  deep-interview's inverted interview points the other way (the human
  corrects the agent's understanding).

### Official steering division of labor (Anthropic, 2026-06-18)

CLAUDE.md = always-loaded facts and norms (recommended under 200 lines);
skills = procedures loaded on invocation; `.claude/rules/` = hard constraints
re-injected on every compaction; hooks = deterministic automation. So "short
router in the global file, procedure in a skill" matches the official
recommendation.

## 3. User Profile and Scope Principles

**Domains are an open set.** Game development, research projects, job
changes, life planning, money management, investment strategy and portfolio
management are all just examples; this list does not bound the system. The
design assumes new domains keep arriving.

Two classification axes hold up:

1. **Engineering vs non-engineering.** The essential difference is not domain
   identity but **how the result is verified**. Engineering work has
   executable verification (tests, builds, renders); non-engineering output
   cannot be tested directly, so **the user's understanding is the only
   acceptance criterion** — which is why explainer+quiz is quality
   verification itself, not a formality.
2. **Domain lanes.** A recurring domain like games can graduate into its own
   lane (a dedicated skill set). Research can split into a lane the same way.

The common working mode is **novice-entry**: touching a domain the user has
no expertise in, deeply and broadly, to generate ideas. The launch-video
anecdote in the article is the general form of this mode — start from what
you know → learn how the domain works → explore options → react to something
concrete → switch back to learning when you realize you don't know what
"good" looks like → launch from a brief.

## 4. Architecture: Three Layers

```text
Layer 0  push line (domain-agnostic)        ← deployed (2026-07-11)
         initiation + technique choice + effort limits + lane routing
Layer 1  unknowns-pass skill (domain-agnostic) ← built (2026-07-11)
         how to run each technique well + launch brief template
Layer 2  domain lanes (open set)             ← promoted only when a domain recurs
         game-*, (research?), (investment?), ...
```

- **Layer 0 — push line**: global instructions in every harness. When a
  large/ambiguous/unfamiliar request arrives without a spec, plan, or
  reference, propose the single cheapest technique before executing. Five
  techniques: blindspot brief / option map (divergent brainstorm) / throwaway
  variants (taste) / mini-interview (≤7 questions, options plus a
  recommendation, hardest-to-reverse first) / reference request. Rules: never
  ask for discoverable facts, confirm the starting point once, effort limits
  (≤7 questions, ≤3 variants, ≤1 artifact), route to domain lanes first,
  compress into a launch brief. During work keep a deviation log (4 fields);
  after work in an unfamiliar domain offer explainer+quiz. NOT for: small
  edits, well-specified work, "just do it."
- **Layer 1 — unknowns-pass (built)**: the push line owns initiation, so the
  skill owns execution guidance only — a table classifying the dominant
  unknown (technique selection), how to run each of the five techniques well,
  the verification split (executable vs comprehension-checked), the launch
  brief template, and scenario-based quiz question structure. Location:
  `skills/productivity/unknowns-pass/`.
- **Layer 2 — domain lanes**: the existing lane is games (game-direction →
  production → review); a partial lane is investment (toss-portfolio-state +
  fable5-judgment); general deep discovery is deep-interview (explicit
  invocation only). **Promotion rule**: when a domain (a) recurs and (b) the
  generic techniques prove insufficient for it, promote it to a dedicated
  lane.
  Finding: the `toss-portfolio-state` description references an uninstalled
  skill, `investment-decision-support` (dangling) — a natural candidate name
  if the investment lane is promoted. A research lane (working name
  research-direction) is also a promotion candidate.

## 5. What Is Deployed (Tier 0 v2, 2026-07-11)

Single canonical source plus symlinks/mirror:

```text
~/.agents/AGENTS.md            ← canonical source (edit here only)
├── ~/.claude/CLAUDE.md        → symlink (Claude Code)
├── ~/.codex/AGENTS.md         → symlink (Codex; the previous empty file was
│                                 backed up as AGENTS.md.bak-empty)
└── Cursor User Rule           → mirror (id 16793847; Cursor does not read
                                  global rules from files, so it is registered
                                  via the cursor-app-control MCP cursor_dialog
                                  tool. Re-sync after editing the canonical file)
```

v1 → v2 changes (reflecting the user profile): scope widened from code to all
substantial work; brainstorm (option map) separated from taste variants,
taking the techniques from 4 to 5; "hardest-to-reverse decisions first" added
to the priorities; domain-lane routing added; the notes file generalized to
`decision-log.md` for non-code work; post-work comprehension check
(explainer+quiz) added.

Known risks and responses:

- **False triggering** → defended by the NOT clause in the line; tune while
  observing. The worst case is the user turning the line off because it fires
  too often, so keep it conservative.
- **Compliance decay in long sessions** → Claude Code has an escalation path:
  promote the line into `.claude/rules/`, which is re-injected on every
  compaction.

## 6. What We Decided Not to Build or Adopt

| Item | Reason |
| --- | --- |
| 8-skill 1:1 pack | At least 4 external implementations exist. Overlapping skills should merge per skill-builder practice, so a pack is an antipattern. Eight pull skills are just eight things to skip |
| standalone quiz skill | Plenty of prior art. Fable already does this well from the article's bare prompt. The discipline problem is solved by one push-line clause |
| standalone pitch/explainer skill | Not the bottleneck. engineering-docs + humanize-doc covers it manually |
| standalone deviation-ledger skill | A 4-field instruction embedded in the push line is enough. flow-next plan-sync is prior art |
| adopting mattpocock grilling | 12 lines, redundant with the push line. With deep-interview installed it would make three interview skills and only blur the trigger boundaries |
| adopting mattpocock prototype | Best-in-class quality but engineering-shaped only. Revisit if the engineering share of work grows |
| adopting Superpowers | No implementation before approval, and maximal process throughout — the opposite of this user's temperament |
| adopting any external pack | Nothing is mature (§2). Even the most popular one is a week-old personal repository |

## 7. Decision History and Next Actions

Decisions confirmed in the 2026-07-11 interview (deep-interview):

- **Dropped the observation period; build now**: the original plan was
  "observe for 1–2 weeks, then decide," but a missed trigger is invisible —
  you have to notice that the line should have fired to record that it
  didn't — so manual observation was self-contradictory. The user chose to
  build immediately.
- **One skill with a verification split**: splitting into an engineering
  skill and a non-engineering skill would duplicate most of the body. A
  single `unknowns-pass` keeps Tariq's lifecycle (techniques before, notes
  during, a check after) and only diverges on plan ordering, the notes file,
  and the final check depending on how the result is verified (executable vs
  comprehension-checked). Non-engineering domains (investment, research,
  career, life planning, money management) are absorbed through trigger
  vocabulary in the description and the in-body split, not separate lanes.
- **The push line stays generic**: it does not name a specific skill
  (avoiding Cursor re-sync burden and coupling). The skill is discovered
  through its description triggers.
- **Distribution path**: build in this repository → merge to main → install
  via the install-skill-pack procedure.

Remaining actions:

1. **Domain lane promotion**: if a domain (research, investment, ...) recurs
   and the generic techniques prove insufficient, evaluate promotion per the
   rule in §4.
2. **When editing the canonical file**: edit `~/.agents/AGENTS.md` → re-sync
   the Cursor user rule (cursor_dialog update, id 16793847). The symlinked
   harnesses update automatically.

## 8. Usage Scenarios (examples — this list does not bound the scope)

- **Domain with a lane (games)**: "I want to make a game but have no design
  experience" → routing sends it to game-direction (taste interview + concept
  slate are already specialized there). The generic layer fires only for
  sub-domains the lane doesn't cover ("I don't know what a shader is" →
  blindspot brief).
- **Non-engineering without a lane (investment strategy)**: establish facts
  with toss-portfolio-state → blindspot brief (the questions an expert would
  ask, the landmines) → option map (conservative through aggressive
  candidates) → reactions → mini-interview (decisions only a human can make,
  like risk tolerance; hardest-to-reverse first) → launch brief (effectively
  an investment policy document) → decision-log during operation → quiz
  before committing money (the real acceptance step in this domain).
- **Exploratory work without a lane (research ideas)**: option map is the
  main technique — explore the area, diverge into 5–10 directions, reactions
  fix the scope → launch a fresh session from the brief → when output
  arrives, confirm understanding with explainer+quiz.
- **Judgment-heavy work (job change / life planning)**: enter with option map
  + blindspot brief → the user explicitly invokes deep-interview when depth
  is needed → final judgment goes to fable5-judgment. Nothing new to build;
  the push line only handles the entry.
- **Negative (must not fire)**: typo fixes, well-specified implementation,
  "just do it."

## Reference Links

- Source article: https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns
- Steering guide: https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more
- External prior art: https://github.com/Neeeophytee/finding-unknowns-skills ,
  https://github.com/bozhouDev/finding-unknowns-skills ,
  https://github.com/tankadoko/unknowns-field-guide-skill ,
  https://github.com/dkamm/pr-quiz
