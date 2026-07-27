# Voice and Tone: Sound Like a Human Reviewer

## Contents

- Hard Bans
- What Human Reviewers Sound Like
- Inline Comment Shape
- Slop vs Human: Side by Side
- When to Allow Voice Markers
- Review Body: Guide the Author, Don't Summarize the Review
- Body Anti-patterns
- Non-English Reviews
- Self-Check Before Posting

This file exists because a typical AI-drafted PR review still reads as
machine-generated after the structural anti-patterns (severity tags, internal
IDs, methodology headers) are stripped. The remaining tells live in voice and
register. Apply this guide on the first draft, not as a cleanup pass after the
review already reads wrong. All examples in this file are synthetic.

## Hard Bans

These read as machine-generated. Avoid them even when one feels natural.

- **Tables inside inline comments.** Humans write prose in line comments.
  Tables appear only in the review body for cross-cutting summaries, and
  rarely even there.
- **Bold section labels inside short comments.** No `**Severity: HIGH**`, no
  `**Issue:**`, no `**Fix:**`, no `**Why it matters:**`. A three-sentence
  comment with bold section headers is one of the strongest tells.
- **Conventional-comments labels.** No `issue (blocking):`, `nitpick:`,
  `praise:`, `suggestion (non-blocking):`. Use them only when the target repo
  demonstrably uses that convention in its own review threads.
- **Decorative punctuation patterns.** Em-dash chains and middle dots read as
  generated text in many communities. Prefer `:` for definitions, `,` for
  clauses, and periods for sentence breaks.
- **Mechanical fragment chains.** `X → Y. Z so not W.` Write sentences, not
  arrow-glued tokens. More than one `→` per comment is a tell.
- **Filler lead-ins.** "One more thing", "Additionally", "Also worth noting"
  at the start of a comment. Cut them. Start with the fact.
- **Softening before refusing.** "Nice approach, but...", "I see where this is
  going, however..." If the answer is no, say no. Maintainers of large
  open-source projects refuse flat.

## What Human Reviewers Sound Like

Before drafting, read a few recent reviews written by maintainers of large
open-source projects; the register is consistent across ecosystems and looks
like this:

- **One claim, one to three sentences of prose.** Not a structured document.
- **Lead with the fact or the verdict.** "I think this behavior is wrong."
  "We are not adding this dependency." "This test is strange."
- **Backticks for code references.** `compare_digest`, `Config.reload`, not
  "the function defined on line 42" or "the variable above".
- **Assert what you observed; hedge only with evidence.** "this returns zero
  on every path" when you traced it, versus "looks like this never runs,
  since nothing logs from it" when you inferred it.
- **Direct refusal is a complete comment.** "We are not adding this
  dependency. `memchr` from the standard library already covers this."
- **A genuine question is a complete comment.** "What breaks if we skip the
  rename here? Resolution should already handle it."
- **End with a suggestion block, or name the alternative concretely in
  prose.** Never "consider refactoring".

## Inline Comment Shape

The default shape, used 90% of the time:

```markdown
{The fact or the verdict, in one sentence.} {Optional second sentence with the consequence or the evidence.} {Optional third sentence with the fix or the alternative.}

```suggestion
{optional one-liner code fix}
```
```

That's the whole template. No title line. No labels. No bold. No bullets
unless you are genuinely listing two parallel items.

If the fix needs more than one line of code, drop the ```suggestion block and
write the alternative as prose: "Pull `compare_digest` from `hmac` and use
that instead." Reviewers do this constantly when the fix isn't a single
substitution.

## Slop vs Human: Side by Side

Same finding, drafted both ways.

### Slop

> ### Timing attack in token comparison
>
> **Severity: HIGH**
>
> **Issue:** The token comparison on line 87 uses `==`, which short-circuits
> on the first byte mismatch. This leaks information about the secret via
> response timing.
>
> **Why it matters:** An attacker can recover the token byte-by-byte by
> measuring response times across many requests.
>
> **Fix:** Use a constant-time comparison.
>
> ```suggestion
> if not hmac.compare_digest(provided, expected):
> ```

Tells: severity tag, bold section headers, three labeled paragraphs,
methodology phrasing ("Why it matters"), reads like a textbook entry.

### Human

> `==` on the token leaks timing. Use `hmac.compare_digest` so the comparison
> is constant-time.
>
> ```suggestion
> if not hmac.compare_digest(provided, expected):
> ```

Two sentences, suggestion block, done.

### Another pair

**Slop:**
> ### Missing null check on optional field
>
> **Issue:** `user.profile` is optional per the type definition, but the code
> accesses `user.profile.avatar` directly on line 134 without a null check.
>
> **Why it matters:** Will raise `AttributeError` when a user without a
> profile is passed in.
>
> **Fix:** Guard with `if user.profile is not None`.

**Human:**
> `user.profile` is `Optional` in the schema but we're reading `.avatar` off
> it directly. Will crash for users that haven't set up a profile yet.

The fix direction is obvious from the diagnosis, no need to spell it out. If
it isn't obvious, add one sentence: "Easiest fix is an `if user.profile is
not None` guard."

## When to Allow Voice Markers

"Hey", "I think", "Wait", a single question mark. These are allowed sparingly,
about one per review. They signal you're reading the code and reacting, not
running a checklist. Overuse turns into performance.

Don't use them to soften refusals. Use them when you're genuinely puzzled by
something ("What is going on here?") or genuinely surprised ("Hey, I think
this code is dead: the index is built from `type_`, which never returns
either of these").

## Review Body: Guide the Author, Don't Summarize the Review

The PR-level body has a different job from inline comments, and the rules
above only cover inline. Inline comments answer "what's wrong with this
line"; the body answers "what should the author do next". Drafts that
summarize what you checked or what's wrong are reviewer-flexing: the author
can see the inline comments on their own.

A body should be one of three things, or nothing:

1. **Triage**: which of the inline comments block the merge, which are
   nice-to-have, which can be deferred. One sentence each.
2. **Items that can't be inline**: things that span the whole PR, or things
   outside the diff (post-merge checks, follow-up issues, deployment
   caveats). One short paragraph.
3. **A direct question or refusal at PR scope**: "I don't think this PR is
   ready, here's why" / "Why is this not split into two PRs?".

If you don't have any of those, leave the body empty. An empty body next to
four sharp inline comments is fine and common.

### Case Study: Same Body, Two Drafts

A synthetic before/after modeled on a real review cycle.

**Slop (draft):**

> Reviewed for backward compatibility and security, based on probing a
> staging deployment of this branch.
>
> `export_totals()` returns a zero-filled `UsageTotals` on every path, and
> the `ReportMeta` constructor omits `confidence`, so responses always carry
> `None` there. Both fields are optional in the schema, so nothing breaks,
> but any consumer using them for billing or quality tracking will read
> constants. Fixing this properly means threading the upstream usage payload
> through `Client.request_parsed`, and `confidence` first needs agreement on
> what `1.0` even means, so it doesn't really fit this migration. I would
> merge this PR as-is and track the two gaps in separate issues.
>
> After merge, it would be good to confirm the production `/status` response
> matches the docs. A `scripts/smoke_check.py`-style script could make this
> reusable for future deploys.

**Human (rewrite):**

> The blocking items are the API version and the request/response schemas;
> the rest of my comments are optional. After merge, please check the
> production `/status` response against the docs.

What the rewrite cut, and why:

- **The methodology lead-in.** How you reviewed does not help the author act.
- **The whole out-of-scope paragraph.** If the conclusion is "out of scope,
  track separately", the analysis belongs in that follow-up issue, not in the
  review body. The body shouldn't argue for a finding it's already deferring.
- **The speculative tooling suggestion.** If you actually want the script,
  file an issue. Don't drop "you could also do X" in the body.
- **Hedge stacking.** "doesn't really fit", "would be good to", "could make
  this reusable": several hedges in adjacent sentences turn into fog. Keep at
  most one, where it's load-bearing.

The rewrite kept what is actionable for the author: which comments block the
merge, and what to check after deploy.

### Body Anti-patterns

- "Reviewed this PR from the X perspective" or "based on running it in a
  deployed environment": meta-description of the review process. Cut.
- A full paragraph describing a problem that you then defer as out of scope:
  file the issue and stop writing about it here.
- Stacked soft asks ("might be worth...", "could be nice to...", "maybe
  consider...") across multiple sentences. Pick one ask, state it once.
- Repeating an inline comment's content in the body "for summary purposes".
  The author will read both. Don't double-bill.
- Listing what files you looked at, what tools you ran, or what your
  verification approach was. None of that helps the merge decision.

### Body Length Rule of Thumb

If the body is longer than the longest inline comment, it's almost certainly
wrong. The bulk of a review's content lives in inlines anchored to specific
lines; the body is a thin coordinating layer.

## Non-English Reviews

Everything above is language-independent. When the target repo reviews in
another language, additionally:

- Match the repo's existing formality register. Read a few merged PRs from
  the same repo before drafting, and mirror how its reviewers actually write.
- Apply the filler-lead-in, hedge-stacking, and softening bans to their local
  equivalents; every language has its own stock phrases for "please take a
  look when you get a chance".
- Keep code identifiers, error messages, and quoted output in their original
  language.

## Self-Check Before Posting

Run this checklist on every drafted comment. If any line answers "yes",
redraft.

- Does it have a title or a header line?
- Does it have `**Bold**` labels like `**Issue**`, `**Fix**`, `**Why**`?
- Does it have a severity tag anywhere?
- Does it use decorative punctuation (em-dash chains, middle dots), or `→`
  more than once?
- Does it start with a filler lead-in ("Additionally", "One more thing")?
- Does it end with a filler ask ("please take a look when you get a chance")?
- Is there a table?
- Are there more than 3 sentences without a code suggestion block?
- Does its formality or phrasing mismatch the repo's existing review threads?

Zero "yes" answers, then post.
