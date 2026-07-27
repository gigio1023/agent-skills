# Voice and Tone — Sound Like a Human Reviewer

## Contents

- Hard Bans
- Voice: What Humans Actually Sound Like
- Inline Comment Shape
- Slop vs Human
- When to Allow Voice Markers
- Review Body
- Body Anti-patterns
- Self-Check Before Posting

This file exists because a typical AI-drafted PR review reads as obviously AI-generated even after the structural anti-patterns (severity tags, internal IDs, methodology headers) are stripped. The remaining "tells" live in voice and register. Apply this guide on the **first** draft, not after the user complains.

Case study: on one production-service PR, it took four rounds of "make it less AI-sloppy" before the comments stopped reading as AI. The lessons below are what made the final round land.

## Hard Bans

These are AI tells. Zero tolerance, applies even when one of them feels natural.

- **Tables inside inline comments.** Humans write prose in line comments. Tables show up only in the review body for cross-cutting summaries, and rarely even there.
- **`**Bold headers**` inside short comments.** No `**Severity: HIGH**`, no `**Issue:**`, no `**Fix:**`, no `**Why it matters:**`. A 3-sentence comment with bold section headers is the strongest AI tell after em-dash.
- **Conventional-comments labels.** No `issue (blocking):`, `nitpick:`, `praise:`, `suggestion (non-blocking):`. Real reviewers don't label their own comments.
- **Em-dash `—` and middle-dot `·`.** The strongest punctuation-level AI tells. Use `:` for definitions, `,` for clauses, period for sentence breaks.
- **`~해요 / ~에요` endings in Korean.** Child-like register. Use `~합니다 / ~입니다` or plain `~다` form.
- **Mechanical fragment chains.** `X → Y. Z 라 W 아님.` Real reviewers write sentences, not arrow-glued tokens. If you're using `→` more than once per comment, you're being a robot.
- **Filler lead-ins.** "지금", "한 가지 더", "추가로", "참고로", "여담이지만" at the start of a comment. Cut them. Start with the fact.
- **Softening before refusing.** "좋은 시도이지만…", "이해는 가지만…", "방향성은 맞는데…" If the answer is no, say no. Reviewers in tokio/rust/cpython refuse flat.

## Voice — What Humans Actually Sound Like

Verbatim examples collected from real reviewers in `rust-lang/rust`, `tokio-rs/tokio`, `python/cpython`, `pytorch/pytorch`. Read these before drafting.

> **Darksonn**, tokio-rs/tokio PR #8120
> "I think this behavior is wrong. It should only take from the LIFO slot if it has already checked all worker threads. The caller of this method probably has to loop twice."

> **Darksonn**, tokio-rs/tokio PR #8141
> "We are not adding this dependency. You can use `libc::memchr` similar to `tokio/src/util/memchr.rs` if you want to do this."

> **petrochenkov**, rust-lang/rust PR #156452
> "What breaks if we don't change the ident during AST lowering? In theory, all the resolution should be done in `rustc_resolve`..."

> **RalfJung**, rust-lang/rust PR #112464
> "This is a strange test. It says to only timeout after billions of years, yet apparently it expects the OS to timeout immediately. What is going on here?"

> **zware**, python/cpython PR #133964
> "As far as I can tell, these tests are not run by regrtest and are mostly relevant to libmpdec rather than _decimal. I mostly just don't see why they're here."

> **lolbinarycat**, rust-lang/rust PR #152449
> "Hey I think this code is dead. The search index is built using `type_`, which never returns either of the new types. Also, since `macro1` in the js test works correctly with filtering, I think that means these two workaround types aren't needed?"

> **malfet**, pytorch/pytorch PR #183065
> "Nit (to error out rather than silently fail on large tensors
> ```suggestion
> const auto output_W = c10::checked_convert<int32_t>(output_c.size(2));
> ```"

Patterns visible in those quotes:

- **One claim, 1-3 sentences of prose.** Not a structured doc.
- **Lead with the fact or the verdict.** "I think this behavior is wrong." "We are not adding this dependency." "This is a strange test."
- **Backticks for code references inline.** `SCHEMA_URN`, `hmac.compare_digest`, `libc::memchr`. Not "the function on line 42", not "the variable defined above".
- **Assert when you observed it; hedge with evidence when you inferred it.** "is being sent back" vs "looks like it never ran, since I don't see a log entry".
- **Direct refusal is allowed.** "We are not adding this dependency" is a complete review comment.
- **Voice markers are allowed.** "Hey", "I think", "?!", "What is going on here?". Use sparingly. They signal a human.
- **Drop a ```suggestion block, or name the alternative concretely.** Don't end with "consider refactoring".

## Inline Comment Shape

The default shape, used 90% of the time:

```markdown
{The fact or the verdict, in one sentence.} {Optional second sentence with the consequence or the evidence.} {Optional third sentence with the fix or the alternative.}

```suggestion
{optional one-liner code fix}
```
```

That's the whole template. No title line. No labels. No bold. No bullets unless you are genuinely listing two parallel items.

If the fix needs more than one line of code, drop the ```suggestion block and write the alternative as prose: "Pull `compare_digest` from `hmac` and use that instead." Reviewers do this constantly when the fix isn't a single substitution.

## Slop vs Human — Side by Side

Same finding, drafted both ways.

### Slop

> ### Timing attack in token comparison
>
> **Severity: HIGH**
>
> **Issue:** The token comparison on line 87 uses `==`, which short-circuits on the first byte mismatch. This leaks information about the secret via response timing.
>
> **Why it matters:** An attacker can recover the token byte-by-byte by measuring response times across many requests.
>
> **Fix:** Use a constant-time comparison.
>
> ```suggestion
> if not hmac.compare_digest(provided, expected):
> ```

Tells: severity tag, bold section headers, three labeled paragraphs, methodology phrasing ("Why it matters"), reads like a textbook entry.

### Human

> `==` on the token leaks timing. Use `hmac.compare_digest` so the comparison is constant-time.
>
> ```suggestion
> if not hmac.compare_digest(provided, expected):
> ```

Two sentences, suggestion block, done. This is what `malfet`'s nit above looks like.

### Another pair

**Slop:**
> ### Missing null check on optional field
>
> **Issue:** `user.profile` is optional per the type definition, but the code accesses `user.profile.avatar` directly on line 134 without a null check.
>
> **Why it matters:** Will raise `AttributeError` when a user without a profile is passed in.
>
> **Fix:** Guard with `if user.profile is not None`.

**Human:**
> `user.profile` is `Optional` in the schema but we're reading `.avatar` off it directly. Will crash for users that haven't set up a profile yet.

The fix direction is obvious from the diagnosis, no need to spell it out. If it isn't obvious, add one sentence: "Easiest fix is an `if user.profile is not None` guard."

## When to Allow Voice Markers

"Hey", "I think", "Wait", "?!", a single question mark. These are allowed sparingly, one per review max. They signal you're reading the code and reacting, not running a checklist. Overuse turns into performance.

Don't use them to soften refusals. Use them when you're genuinely puzzled by something (`RalfJung`'s "What is going on here?") or genuinely surprised the code path is dead (`lolbinarycat`'s "Hey I think this code is dead").

## Review Body — Guide the Author, Don't Summarize the Review

The PR-level body has a different job from inline comments, and the rules above only cover inline. Inline comments answer "what's wrong with this line"; the body answers "what should the author do next". Drafts that summarize what you checked or what's wrong are reviewer-flexing — the author can see the inline comments on their own.

A body should be one of three things, or nothing:

1. **Triage**: which of the inline comments are blocking the merge, which are nice-to-have, which can be deferred. One sentence each.
2. **Items that can't be inline**: things that span the whole PR, or things outside the diff (post-merge checks, follow-up issues, deployment caveats). One short paragraph.
3. **A direct question or refusal at PR scope**: "I don't think this PR is ready, here's why" / "Why is this not split into two PRs?".

If you don't have any of those, leave the body empty. An empty body next to four sharp inline comments is fine and common.

### Case Study — Same Body, Two Drafts

This is the review body from the same case-study PR (identifiers anonymized).
The first version is what the AI drafted; the second is what the human reviewer
rewrote.

**Slop (652 chars, AI draft):**

> 외부 호환성과 보안 관점 리뷰. 운영 서버에 띄워 두고 외부에서 찔러본 결과 기준입니다.
>
> `executor.py:86-94` 의 `_extract_token_usage` 가 어떤 경우든 0/0/0 짜리 `TokenUsage()` 를 돌려주고, 같은 파일 199-204 의 `ArtifactMetadata` 호출에서 `quality_score` 인자가 빠져 있어 항상 `None` 으로 응답에 들어갑니다. 스펙 상 둘 다 optional 이라 protocol 위반은 아닌데, 호출 측에서 비용이나 품질 추적용으로 이 값을 본다면 항상 같은 값을 받게 됩니다. 고치려면 `LLMClient.call_with_parse` 가 OpenAI `usage` 를 끝까지 들고 오게 손봐야 하고 `quality_score` 는 "1.0 이 무엇을 의미하는지" 부터 합의해야 해서, 이번 마이그레이션 범위와는 결이 좀 다릅니다. 본 PR 머지는 그대로 진행하고 두 가지를 분리한 이슈로 따로 다루는 게 깔끔하지 싶습니다.
>
> 머지 후 운영 `/.well-known/agent.json` 응답이 가이드와 일치하는지 한 번 확인. `scripts/post_deploy_smoke.py` 같은 형태로 자동화해 두면 다음 배포에서도 재사용할 수 있을 것 같습니다.

**Human (102 chars, after rewrite):**

> 필수적인 리뷰는 서비스 버전과 input, output schema이고 그 외는 옵셔널해서 천천히 봐주시면 될 것 같습니다. 머지 후 운영 `/.well-known/agent.json` 응답이 가이드와 일치하는지 확인만 하면 될 것 같습니다.

What the rewrite cut, and why:

- **The methodology lead-in.** "외부 호환성과 보안 관점 리뷰. 운영 서버에 띄워 두고 외부에서 찔러본 결과 기준" is reviewer-flexing. The author doesn't need to know how you reviewed; they need to know what to do.
- **The whole `_extract_token_usage` paragraph.** Long, technically detailed, ends with "이번 마이그레이션 범위와는 결이 좀 다릅니다. 본 PR 머지는 그대로 진행하고 두 가지를 분리한 이슈로 따로 다루는 게 깔끔하지 싶습니다." If the conclusion is "out of scope, split it out", then the whole paragraph belongs in a follow-up issue, not in the review body. The body shouldn't argue for an off-scope finding it's already deferring.
- **The `scripts/post_deploy_smoke.py` suggestion.** Speculation about future tooling. If you actually want the author to write this script, file an issue. Don't drop "you could also do X" in the body.
- **Hedge stacking.** "결이 좀 다릅니다", "깔끔하지 싶습니다", "재사용할 수 있을 것 같습니다" — multiple hedges in adjacent sentences turn into a fog. The rewrite kept one `~될 것 같습니다` because it's load-bearing (gives the author a real call), and dropped the rest.

The rewrite kept what was *actionable for the author*: which inlines are required, which are optional, what to check after deploy. Everything else got cut.

### Body Anti-patterns

- "PR #X 의 Y 관점 리뷰" / "운영 환경에서 확인한 결과 기준" — meta-description of the review process. Cut.
- A full paragraph describing a problem that you then say is "out of scope" — if it's out of scope, file an issue and stop writing about it here.
- "할 수 있을 것 같습니다", "정리해두면 좋을 것 같습니다", "검토해보시면 어떨까 싶습니다" stacked across multiple sentences. Pick one ask, state it once.
- Repeating an inline comment's content in the body for "summary purposes". The author will read both. Don't double-bill.
- Listing what files you looked at, what skills you ran, what your verification approach was. None of that helps the merge decision.

### Body Length Rule of Thumb

If the body is longer than the longest inline comment, it's almost certainly wrong. The bulk of a review's content lives in inlines anchored to specific lines; the body is a thin coordinating layer.

## Self-Check Before Posting

Run this checklist on every drafted comment. If any line answers "yes", redraft.

- Does it have a title or a header line?
- Does it have `**Bold**` labels like `**Issue**`, `**Fix**`, `**Why**`?
- Does it have a severity tag anywhere?
- Does it have an em-dash `—` or middle-dot `·`?
- Does it end with "고려해주세요", "검토 부탁드립니다", "확인 부탁드려도 될까요"?
- Does it start with "지금", "한 가지 더", "추가로"?
- Is there a table?
- Does the Korean use `~해요 / ~에요`?
- Are there more than 3 sentences without a code suggestion block?
- Does it use `→` more than once?

Zero "yes" answers, then post.
