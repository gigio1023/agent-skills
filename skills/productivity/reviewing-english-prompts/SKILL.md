---
name: reviewing-english-prompts
description: >
  Use when a user wants an English task prompt reviewed or quietly coached while
  the requested work continues, especially for software engineering, AI
  research, and game-development work. Rewrites the complete request in clear,
  natural technical English and recommends precise domain terms when useful.
  NOT for translating non-English text, proofreading prose word by word, or
  changing the user's task requirements.
---

# Reviewing English Prompts

Help a user develop the habit of expressing technical work naturally in English
without making the task harder to execute. Preserve the user's actual request;
the coaching lane is a review, not a reinterpretation or a new requirement.

## Quick Path

1. Read the whole English request before judging individual words. Identify the
   outcome, relevant context, constraints, authority, and evidence of done.
2. Start or continue the requested work immediately. Do not make the user wait
   for a language review.
3. Re-express the request as one natural, direct prompt. Preserve the priority,
   scope, uncertainty, and level of urgency. Prefer the way an experienced
   practitioner would ask for the work, not a literal translation of the
   original syntax.
4. Add up to three terminology or wording notes only when they make the request
   more precise, more idiomatic, or easier to act on in its technical domain.
5. Return the coaching result after the task result. If the request is already
   concise and natural, say so briefly instead of inventing edits.

## Coaching Contract

### Preserve Meaning

Keep the user's requested outcome, constraints, exclusions, acceptance criteria,
and authority unchanged. In particular, do not turn a request to inspect into a
request to edit, soften a firm constraint, add a deadline, or substitute a
different technical approach.

When the wording is ambiguous, write a faithful paraphrase that retains the
ambiguity, then note the one decision that would make it actionable. Do not
silently guess.

### Rewrite the Prompt, Not Every Token

Treat the prompt as a small piece of working communication. Use a clear subject
and direct verb, put the desired outcome before implementation details, and
group related constraints together. Omit filler that adds no decision value.

Prefer a plain, idiomatic request over either of these extremes:

- literal Korean-to-English phrasing;
- inflated consultant or specification language when the user is simply asking
  an agent to do work.

Do not produce a line-by-line grammar lesson, a redline, a score, or a list of
every small article and preposition change unless the user explicitly asks for
that level of correction.

### Use Domain Language Carefully

Infer the domain from the request and repository context. Use a conventional
technical term when it names a real distinction the original wording misses.
Read [terminology-guide.md](references/terminology-guide.md) when choosing a
term for software engineering, AI/ML, or game development.

Technical precision is not a reason to make a prompt less natural. Keep exact
product names, APIs, identifiers, quoted errors, and code tokens unchanged.
Do not replace accepted team vocabulary merely because a synonym sounds more
formal.

### Keep the Main Work Moving

If the harness can run independent work in a background or delegated lane, send
the exact user prompt to a reviewer while the primary lane performs the task.
The reviewer returns only a coaching packet: a rewrite, optional terminology
notes, and an ambiguity flag. The primary lane owns task execution and the final
response.

If delegation is unavailable, execute the task first and review the original
prompt before writing the final response. Never claim that a review ran in the
background when it did not.

Read [always-on-setup.md](references/always-on-setup.md) when the user wants
this behavior applied automatically to ordinary English task requests.

## Output

Put the task result first. Then use this compact section only when coaching is
enabled for the request or harness:

```markdown
### English prompt coach

**Natural rewrite**

> <one complete, ready-to-send prompt>

**Precision note** *(only when useful)*

- `<original wording>` → `<preferred wording>` — <short reason>
```

For a prompt that needs no material rewrite, use `Natural and clear as written.`
Do not praise mechanically, restate the task result, or make the user compare
multiple near-identical versions. Offer one best rewrite; offer alternatives only
when they reflect a meaningful difference in technical intent or register.

## Authority and Privacy

- A coaching request authorizes analysis and a suggested rewrite, not edits to
  the user's prompt, files, settings, or agent configuration.
- The review lane may use the current prompt and task context only. It must not
  send the prompt to an external service merely to judge wording.
- Do not expose internal reasoning. Give the polished result and, when useful,
  a short reader-facing reason for a terminology recommendation.

## Validation

Before returning a rewrite, compare it with the original request:

- the same outcome, constraints, and boundaries remain;
- verbs and nouns are natural for the inferred domain;
- the prompt has one clear main request rather than a word-for-word gloss;
- identifiers, commands, API names, and quoted content are unchanged;
- any terminology note improves a real distinction rather than adding jargon.

Use [evaluation-cases.md](references/evaluation-cases.md) to test changes to
this skill or to calibrate a harness integration.

## Gotchas

- "Native" does not mean more formal, longer, or more idiomatic at the cost of
  the user's meaning.
- Do not correct fragmentary command prompts such as `run the tests` unless a
  rewrite would genuinely help the user learn a more useful expression.
- Do not turn a domain term into a prescribed implementation. For example,
  `root cause` describes a diagnosis goal; it does not authorize code changes.
- Keep the coaching block small. Its purpose is to build intuition while the
  user gets their work done, not to become a second task.
