# Voice and Tone: Sound Like a Human Reviewer

## Contents

- The First-Order Rule
- Hard Bans
- Labels Follow the Repo
- What Human Reviewers Sound Like
- More Human Signals
- Inline Comment Shape
- Slop vs Human: Side by Side
- When to Allow Voice Markers
- Review Body: Guide the Author, Don't Summarize the Review
- Body Anti-patterns
- Non-English Reviews
- Self-Check Before Posting
- Sources

This file exists because a typical AI-drafted PR review still reads as
machine-generated after the structural anti-patterns (severity tags, internal
IDs, methodology headers) are stripped. The remaining tells live in voice and
register. Apply this guide on the first draft, not as a cleanup pass.

Every quoted review comment below is real: collected from public PRs in
rust-lang/rust, tokio-rs/tokio, python/cpython, and pytorch/pytorch, and
verified verbatim against the GitHub API in July 2026. Each link is a
permalink to the original comment. The slop examples are synthetic, because
top repos rarely let slop get posted.

## The First-Order Rule

Comment on the code, never the developer. Google, CPython, and Kubernetes
reviewer guides all state this before saying anything about format.

- "The comparison isn't constant-time", not "you introduced a timing bug".
- It applies to praise too: praise the change ("these diagnostics are much
  easier to read"), not the person.

## Hard Bans

These read as machine-generated. Avoid them even when one feels natural.

- **Tables inside inline comments.** Humans write prose in line comments.
  Tables appear only in the review body for cross-cutting summaries, and
  rarely even there.
- **Bold section labels inside short comments.** No `**Severity: HIGH**`, no
  `**Issue:**`, no `**Fix:**`, no `**Why it matters:**`. Wikipedia's catalog
  of AI-writing signs names this exact bold-header-plus-colon list pattern.
- **Decorative punctuation patterns.** Em-dash chains and middle dots appear
  in community-collected AI-tell lists (see Sources). Prefer `:` for
  definitions, `,` for clauses, and periods for sentence breaks.
- **Mechanical fragment chains.** `X → Y. Z so not W.` Write sentences, not
  arrow-glued tokens. More than one `→` per comment is a tell.
- **Filler lead-ins.** "Additionally", "One more thing", "Also worth noting"
  at the start of a comment. Wikipedia's AI-tell catalog flags "Additionally"
  openers specifically. Start with the fact.
- **Diluted refusals.** If the answer is no, say no. Softening a question is
  human and even prescribed (Kubernetes suggests "Am I understanding this
  correctly?" over "Why did you do this?"). Softening a refusal into "great
  approach, but maybe we could consider..." is the tell.

## Labels Follow the Repo

A blanket ban on label prefixes would be wrong. Google's reviewer guide
prescribes `Nit:`, `Optional:`, and `FYI:`; rust-lang reviewers tag comments
with `Remark:`, `Question:`, and "(Not for this PR)"; teams that adopt
conventional-comments write `suggestion (non-blocking):` on purpose.

The rule: mirror the conventions visible in the repo's existing review
threads (the workflow already collects them), and import nothing those
threads don't use.

- The repo uses `Nit:` or similar prefixes: use them for exactly that
  purpose.
- The repo shows no labels: write plain prose. `Nit:` is still widely
  understood; anything beyond it starts to look imported.
- Bold severity scaffolds (`**Severity: HIGH**`) are banned everywhere; none
  of the surveyed communities write them.
- Severity must still be clear. Kubernetes requires reviewers to distinguish
  a nit from a change required for acceptance; do it with the repo's own
  prefixes or one triage sentence in the review body.

## What Human Reviewers Sound Like

Ten real comments, each showing a shape worth copying.

**Lead with the verdict.**

> **Darksonn**, [tokio-rs/tokio#8120](https://github.com/tokio-rs/tokio/pull/8120#discussion_r3201495853)
> "I think this behavior is wrong. It should only take from the LIFO slot if it has already checked *all* worker threads. The caller of this method probably has to loop twice."

**State the consequence, the fix, and the test you expect.**

> **pablogsal**, [python/cpython#154195](https://github.com/python/cpython/pull/154195#discussion_r3617731789)
> "This rejects valid task names above 256 KiB instead of truncating them, so async sampling can still fail. We should cap `read_len`, not `len`, and test this boundary."

**Refuse flat, point at the alternative.**

> **Darksonn**, [tokio-rs/tokio#8141](https://github.com/tokio-rs/tokio/pull/8141#discussion_r3232270494)
> "We are not adding this dependency. You can use `libc::memchr` similar to `tokio/src/util/memchr.rs` if you want to do this."

**Ground a refusal in project policy.**

> **zooba**, [python/cpython#152604](https://github.com/python/cpython/pull/152604#discussion_r3639323355)
> "No thanks, we don't use ntdll from CPython.
>
> We should be changing this function to return the version number controlled by the compatibility shims, because it will match the other compatibility behaviours that are associated with that version.
>
> The `platform` module exists to get the "real" version."

**Being genuinely puzzled is a complete review comment.**

> **RalfJung**, [rust-lang/rust#112464](https://github.com/rust-lang/rust/pull/112464#discussion_r3228536243)
> "This is a strange test. It says to only timeout after billions of years, yet apparently it expects the OS to timeout immediately. What is going on here? And why is there no comment explaining this?^^"

**React, then redirect.**

> **albanD**, [pytorch/pytorch#191019](https://github.com/pytorch/pytorch/pull/191019#discussion_r3647169467)
> "What?!
> Why take a data_ptr of a Tensor to make it into another Tensor? :p
> clone() or alias() should work here depending if you want a fresh Tensor or a view to the original."

**A nit is one line plus the replacement.**

> **malfet**, [pytorch/pytorch#183065](https://github.com/pytorch/pytorch/pull/183065#discussion_r3230614183)
> "Nit (to error out rather than silently fail on large tensors
> ```suggestion
>   const auto output_W = c10::checked_convert<int32_t>(output_c.size(2));
> ```"

**Use the repo's prefix, then say why the code misleads.**

> **pablogsal**, [python/cpython#153365](https://github.com/python/cpython/pull/153365#discussion_r3650274419)
> "Nit: can you add a short comment here noting that item 1 of the `CoroInfo` holds the waiter task address (that's what `parse_task` stores there)? The field is called `task_name`, so this is easy to misread."

**Mark inference as inference.**

> **lolbinarycat**, [rust-lang/rust#152449](https://github.com/rust-lang/rust/pull/152449#discussion_r3228824374)
> "Hey I think this code is dead.  The search index is built using `type_`, which never returns either of the new types.  Also, since `macro1` in the js test works correctly with filtering, I _think_ that means these two workaround types aren't needed?"

**Evidence first, then a concrete ask.**

> **zware**, [python/cpython#133964](https://github.com/python/cpython/pull/133964#discussion_r3228693351)
> "As far as I can tell, these tests are not run by regrtest and are mostly relevant to `libmpdec` rather than `_decimal`.  I mostly just don't see why they're *here*.  If they're important enough to keep, they're important enough to wire into regrtest."

Patterns to copy from the set:

- One claim, one to three sentences of prose, and the reasoning is part of
  the claim. Google's guide is explicit that brevity never excuses dropping
  the why.
- Backticks for code references. Markdown emphasis lands on the load-bearing
  word (*all*, *here*), never on section labels.
- Assert what you observed; hedge only with evidence ("As far as I can
  tell... not run by regrtest").
- A refusal or a question can be the entire comment.
- Prefer a suggestion block or a named alternative, but pointing out the
  problem and letting the author decide is also a valid complete comment.
  Google calls this balance out explicitly.
- Genuine praise appears occasionally and targets the change. Google and
  CPython both instruct reviewers to also say what is good; a long review
  with zero positive signal reads generated.

## More Human Signals

Verified one-off patterns worth imitating when they are true for you. Never
fake them.

Costs argued in concrete units:

> **Darksonn**, [tokio-rs/tokio#8222](https://github.com/tokio-rs/tokio/pull/8222#discussion_r3458194802)
> "No sleeps in tests unless absolutely necessary. They make the test suite slow. This test alone makes Tokio's CI job take 600 ms longer."

Citing what you ran, not just what you read:

> **serhiy-storchaka**, [python/cpython#154148](https://github.com/python/cpython/pull/154148#discussion_r3612210656)
> "I verified -- it is not slower, but slightly faster on both major fallback platforms: `acos(x)/pi` vs `2*asin(sqrt((1-x)/2))/pi` is 8.4 vs 7.0 ns/call with glibc (x86-64, gcc -O2) [...]"

Conceding when rebutted, and reversing your own earlier suggestion:

> **camelid**, [rust-lang/rust#158709](https://github.com/rust-lang/rust/pull/158709#discussion_r3646432396)
> "You're right, my bad. I read your code too quickly."

> **Darksonn**, [tokio-rs/tokio#8219](https://github.com/tokio-rs/tokio/pull/8219#discussion_r3467888085)
> "I know I suggested this name, but thinking more about it this is also not clearer."

For this skill that matters most in the reply flow: when the author rebuts a
finding and they are right, concede plainly instead of defending the original
comment.

Two more observations from the harvest:

- Real maintainer comments contain typos and informal register. Do not inject
  fake typos, but uniformly sanded prose across a whole review is itself a
  weak tell; stop polishing once the content is right.
- Some projects have started labeling agent-written comments explicitly. If
  the target repo has such a convention, follow it. This guide exists to make
  comments useful and readable, not to disguise their origin.

## Inline Comment Shape

The default shape, used 90% of the time:

```markdown
{The fact or the verdict, in one sentence.} {Optional second sentence with the consequence or the evidence.} {Optional third sentence with the fix or the alternative.}

```suggestion
{optional one-liner code fix}
```
```

That's the whole template. No title line. No labels beyond the repo's own
conventions. No bold. No bullets unless you are genuinely listing two
parallel items.

If the fix needs more than one line of code, drop the ```suggestion block and
write the alternative as prose, the way Darksonn's and zooba's refusals above
name the replacement path.

## Slop vs Human: Side by Side

Same finding, drafted both ways. These pairs are synthetic; the human drafts
mimic the register of the verified quotes above.

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

Two sentences, suggestion block, done. This is the same shape as malfet's
`checked_convert` nit above.

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

"Hey", "I think", "Wait", "What?!", a single question mark, an occasional
":p" or "?^^". The verified quotes above show all of these in real maintainer
comments. Use them sparingly, about one per review: they signal you read the
code and reacted, not that you ran a checklist. Overuse turns into
performance.

Don't use them to soften refusals. Use them when you are genuinely puzzled
(RalfJung's "What is going on here?") or genuinely surprised (lolbinarycat's
"Hey I think this code is dead").

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
3. **A direct question or refusal at PR scope**, like this real
   changes-requested body:

> **rtimpe**, [pytorch/pytorch#190578](https://github.com/pytorch/pytorch/pull/190578#pullrequestreview-4770190844)
> "I'd rather just review it all at once.  It's not clear why the sources you included would be needed to support `.set()`, for example.
>
> Is there another way to reduce the scope?  For example, could you start by supporting just `cv.set()`, without explicit token support?  I'd also encourage you to try using UDOV wherever possible - it's still not clear to me why we need a new VT for tokens, based on your included tests"

Praise plus one open focus point is also a complete, human body:

> **zooba**, [python/cpython#153700](https://github.com/python/cpython/pull/153700#pullrequestreview-4765860130)
> "Looks great overall, glad we kept going, this is really neat!
>
> Still have a question about guessing at ino values when we don't know them."

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
- Restating your own inline comments in the body "for summary purposes". The
  author will read both. (A repo that wants a PR-level summary of the change
  itself is a different, legitimate genre; this ban is about re-summarizing
  your own review.)
- Listing what files you looked at, what tools you ran, or what your
  verification approach was. None of that helps the merge decision.

### Body Length Rule of Thumb

If the body is longer than the longest inline comment, it's almost certainly
wrong. The bulk of a review's content lives in inlines anchored to specific
lines; the body is a thin coordinating layer. Both real bodies quoted above
are two sentences long.

## Non-English Reviews

Everything above is language-independent. When the target repo reviews in
another language, additionally:

- Match the repo's existing formality register. Read a few merged PRs from
  the same repo before drafting, and mirror how its reviewers actually write.
- Apply the filler-lead-in, hedge-stacking, and diluted-refusal bans to their
  local equivalents; every language has its own stock phrases for "please
  take a look when you get a chance".
- Keep code identifiers, error messages, and quoted output in their original
  language.

## Self-Check Before Posting

Run this checklist on every drafted comment. If any line answers "yes",
redraft.

- Does it criticize or praise the developer instead of the code?
- Does it have a title or a header line?
- Does it have `**Bold**` labels like `**Issue**`, `**Fix**`, `**Why**`?
- Does it use a severity scaffold or a label prefix that the repo's own
  threads don't use?
- Does it use decorative punctuation (em-dash chains, middle dots), or `→`
  more than once?
- Does it start with a filler lead-in ("Additionally", "One more thing")?
- Does it end with a filler ask ("please take a look when you get a chance")?
- Is there a table?
- Are there more than 3 sentences without a code suggestion block?
- If it refuses something, is the refusal diluted by compliments or stacked
  hedges?
- Does its formality or phrasing mismatch the repo's existing review threads?

Zero "yes" answers, then post.

## Sources

External guidance this file's rules were checked against:

- [How to write code review comments (Google eng-practices)](https://google.github.io/eng-practices/review/reviewer/comments.html):
  courtesy targeting the code, explain your reasoning, `Nit:`/`Optional:`/`FYI:`
  prefixes, and the balance between giving directions and pointing out
  problems.
- [Kubernetes contributor guide: review guidelines](https://github.com/kubernetes/community/blob/master/contributors/guide/review-guidelines.md):
  nit versus required change must be explicit, it is okay to say no, and
  question phrasing should be empathetic.
- [CPython devguide: pull request lifecycle](https://devguide.python.org/getting-started/pull-request-lifecycle/):
  comment on what is good, and suggest how when requesting changes.
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing):
  community-maintained tell catalog backing the em-dash, bold-label, and
  "Additionally" bans.
- [Daniel Stenberg: Death by a thousand slops](https://daniel.haxx.se/blog/2025/07/14/death-by-a-thousand-slops/):
  a maintainer's account of AI-slop submissions and their formatting tells.
- [conventionalcomments.org](https://conventionalcomments.org/) and one
  [critique thread](https://news.ycombinator.com/item?id=23009467): label
  prefixes as a deliberate team convention, and why they read robotic where
  unadopted.
