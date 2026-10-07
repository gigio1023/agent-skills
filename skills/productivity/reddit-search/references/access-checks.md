# Access Checks

Dated observations behind the access facts in [SKILL.md](../SKILL.md). Each check was one plain request with default client settings, from macOS. Add a dated entry when a route changes rather than editing an old one.

## Reddit

| Route | 2026-09-25 | 2026-10-07 |
| --- | --- | --- |
| `www.reddit.com/r/<sub>/` with curl | JavaScript challenge page | 200 with a JavaScript challenge page, no posts |
| `www.reddit.com/r/<sub>/.json` | 403 | 403 |
| `www.reddit.com/r/<sub>/.rss` | 429 after one call | 403 on the first call |
| `old.reddit.com/r/<sub>/` | Login redirect | 302 to `/login/?reason=lor2` |
| Anthropic WebFetch | Refused | "Claude Code is unable to fetch from www.reddit.com" |
| Anthropic WebSearch, `site:reddit.com` query | No reddit.com URLs | No reddit.com URLs; one third-party mirror URL |
| Claude desktop built-in browser | Refused to open reddit.com | Not rechecked |

Reddit announced the Responsible Builder Policy on 2025-11-11 in r/redditdev (post `1oug31u`, read through Arctic Shift on 2026-10-07): new OAuth tokens for the Data API require approval, existing access continues, and developers are pointed to Devvit or an approval request. Reddit sued Perplexity, SerpApi, Oxylabs, and AWMProxy on 2025-10-22 over scraping Reddit content, including through search-engine result pages.

## Arctic Shift API

Source: the [API README](https://github.com/ArthurHeitmann/arctic_shift/blob/master/api/README.md), read 2026-10-07, plus live calls the same day.

- Base URL `https://arctic-shift.photon-reddit.com`. Endpoints the helper uses: `/api/posts/search`, `/api/comments/search`, `/api/posts/ids`, `/api/comments/tree`, `/api/subreddits/search`. No account, key, or auth header; live calls returned 200 without one.
- Date parameters accept epoch seconds or milliseconds, partial ISO 8601, or an offset. The README lists `1year`, `3m`, `2d`, `1hour`, `5min`, and `10s`. Live: `6m` and `3m` resolved to months, `1y` and `2y` also parse though undocumented, and `2years` or `2foo` return `'before' must be a valid date (epoch, ISO, or relative)`. The skill uses only the documented forms.
- `r/` and `u/` prefixes on `subreddit` and `author` are ignored by the API.
- `limit` is 1 to 100 for search (or `auto`), 1 to 25000 for `comments/tree` (default 50; collapsed comments come back as `kind: more`), and up to 1000 for subreddit search. Search sorts only by `created_utc`.
- `title`, `selftext`, and `query` keyword search need `author` or `subreddit` and are "not supported with very active users or subreddits". Comment `body` search uses Postgres `websearch_to_tsquery` syntax (phrases, `OR`, `-exclude`); the README marks that section as possibly out of date.
- Rate limits are dynamic by server load and request complexity; a 429 carries `X-RateLimit-Reset` (seconds) and `X-RateLimit-Reset-At`. A couple of requests per second is described as fine; the helper stays below that at one request per 1.5 seconds. For bulk data the README points to the monthly dumps.
- Timeouts: the README's message is "Query timed out" and suggests retrying once for warm-up or narrowing the filter. On 2026-10-07 the server returned "Timeout. Maybe slow down a bit" for title searches over 10 days and 3 months of r/redditdev, and for some plain date queries, while a 2-day title search, a keyword-free 2-day listing, comment body search, and `comments/tree` answered.
- Score and comment counts are 0 or 1 until a refresh about 36 hours after posting. Post `1oug31u` showed score 0 and 115 reported comments while `comments/tree` returned 307, so later activity is not always reflected.
