---
name: x-post
description: >
  Draft X (Twitter) posts to promote blog posts in dry developer voice.
  Use when asked to write an X post, tweet, Twitter post, or promote a blog post on X.
  Also triggers on: "X에 올려줘", "트윗 써줘", "tweet this", "X post for this blog".
  Do NOT trigger for LinkedIn posts (use linkedin-post instead).
---

# X Post

Draft short X posts in dev Twitter voice to promote blog posts.

## When to Use

- Blog post URL or content provided, user wants to share on X
- "X에 올려줘", "트윗 써줘", "tweet this blog post"

## Workflow

1. Get the blog post URL or content
2. Fetch and read the full post (WebFetch or local file read)
3. Identify the core insight — what would make a developer stop scrolling
4. Draft 2-3 options following the voice rules below
5. Show character count for each option
6. User picks or asks for revision

## Character Counting

X counts every URL as exactly 23 characters (t.co shortener), regardless of actual length.

**Budget: 280 characters total** (X's current limit). But shorter is better — aim for under 200.

Count like this:
- Text characters: count normally
- Each URL: 23 characters
- Space before URL: 1 character

Show the count next to each draft: `(147 chars)`

## Voice Rules

The goal is to sound like a developer posting on their own timeline, not a brand account or a content marketer. Think: someone who just finished debugging something and is telling their coworkers about it.

### Do

- all lowercase (except proper nouns like "Unity", "Astro", "Claude Code")
- short declarative sentences. fragments are fine
- concrete technical details — function names, error messages, numbers
- matter-of-fact tone. state what happened
- end with the URL, no call to action around it

### Don't

- no dashes or em-dashes (—). use periods or commas to separate clauses
- no exclamation marks
- no emoji
- no hashtags
- no "check out", "read more", "link in bio", "thread below"
- no marketing adjectives ("amazing", "incredible", "game-changing")
- no first-person hype ("excited to share", "proud to announce")
- no rhetorical questions ("ever wondered why...?")

### Rhythm

Good dev tweets have a rhythm: setup → fact → punchline (or reversal).

```
[context in one sentence]. [what you tried or found]. [the result or surprise] [url]
```

The punchline often works by subverting expectation — something that should have worked didn't, or vice versa.

## Examples

These are real outputs the user approved. Study the rhythm, not the topic:

**Example 1 — debugging/failure story:**
> unity has an official mcp now so ai agents can actually control the editor. tried it. relay returns 0 tools. back to the community fork https://sunghogigio.com/blog/unity-official-mcp-broken-analysis

Why it works: setup (official mcp exists), attempt (tried it), reversal (0 tools), resolution (back to fork). All facts, no commentary.

**Example 2 — tool/workflow insight:**
> agents confidently write post.render() and Astro.glob() for astro 6. neither exists anymore. mcp helps if they ask but they never do. built a skill that checks before they write https://sunghogigio.com/blog/en/astro-agent-skill/

Why it works: concrete wrong code as hook, explains the gap (mcp vs skill), states the solution. The word "confidently" does heavy lifting — it implies the problem without editorializing.

## Extracting the Hook

When reading the blog post, look for:

1. **A surprising failure or reversal** — "X should work but doesn't" is always compelling
2. **A concrete detail** — function names, file sizes, error messages, tool names
3. **The "why should I care" angle** — what does this mean for someone else's workflow
4. **Tension between expectation and reality** — official vs community, documented vs actual

Skip: background/setup sections, step-by-step instructions, environment details. Go straight to the insight.

## Gotchas

### 1. Blog summary trap
The post is NOT a summary of the blog. It's a hook that makes someone want to click. Pick one angle, not three.

### 2. Too many clauses
If a draft has more than 4 periods, it's probably too complex. Split into a shorter version.

### 3. Overcapitalization
Only capitalize proper nouns. "MCP" is an acronym so it stays uppercase. "agent" and "skill" are lowercase.

### 4. Dash reflex
AI defaults to em-dashes for pauses. Use a period or comma instead. The user specifically dislikes dashes in this context.

### 5. "I wrote about" framing
Don't start with "wrote a post about X" or "new blog post on X". Jump straight into the content.

## Eval Criteria

1. Follows voice rules (lowercase, no dashes, no emoji, no hype)
2. Contains at least one concrete technical detail
3. Under 280 chars (with URL counted as 23)
4. Hook is from the blog's core insight, not a surface-level summary
5. URL placed at the end with no wrapper text
