# Worked Pages

Read this when building a design doc page, an open-questions page, or correcting an existing page. Every example is synthetic: the service, numbers, URLs, and IDs are invented, and `<user-id>` and `<upload-id>` stand for values returned by the Notion tools. Copy the judgment, not the wording; a team's own template still wins. Indentation in the Notion Markdown blocks is tab characters.

## Contents

- Design doc page
- Open-questions page
- Correcting an existing page

## Design Doc Page

The page title, set through `properties.title`, is "Rate limiter for the public API gateway". The content:

```markdown
<callout icon="icons/document_gray" color="gray_bg">
	**Status**: In Review
	**Owner**: <mention-user url="user://<owner-user-id>"/>
	**Reviewer**: api-gateway CODEOWNERS
	**Target**: per-tenant quotas enforced for all external tenants
	**Updated**: <mention-date start="2026-10-07"/>
	**Links**: [api-gateway repository](https://git.example.com/platform/api-gateway), [tracker project](https://tracker.example.com/projects/rate-limits)
</callout>
## Summary
- **What**: a shared rate limiter that enforces each tenant's request quota across all gateway instances.
	- Each of the 12 instances counts requests on its own today, so a tenant can exceed its quota up to twelvefold during a burst.
- **How**: one token bucket per tenant in the existing Redis cluster, checked by the gateway before routing.
	- The check adds 0.8 ms at p99 in the internal load test on <mention-date start="2026-09-30"/>.
- **Scope**: external tenants on the REST API by <mention-date start="2026-11-30"/>. Streaming endpoints follow in a later design.
- **Undecided**: behavior when Redis is unreachable. See Open questions.
## Context and scope
Quotas are configured per tenant per minute, and each gateway instance enforces the full quota with an in-memory counter. Over-quota traffic comes mostly from batch clients that start at the top of the hour.
![Most over-quota traffic arrives in the first two minutes of each hour. Read: x is the minute of the hour, y is requests per second for the 20 busiest tenants, and the dashed line is their summed quota.](file-upload://<upload-id-arrivals>)
This design covers admission at the gateway. Billing, quota configuration, and the edge network's volumetric protection are outside it.
## Goals and Non-goals
- **Goals**
	- No tenant exceeds its quota by more than 5% in any one-minute window.
	- Added gateway latency stays under 2 ms at p99.
- **Non-goals**
	- Per-endpoint quotas. Tenants ask for them, but billing has no per-endpoint price yet.
## Design
![A request is admitted only after one atomic token check in Redis; rejected requests never reach the upstream service. Read left to right: client, gateway, limiter check, upstream; the dashed path is a rejection with status 429.](file-upload://<upload-id-flow>)
- The gateway calls the limiter after authentication, so the tenant ID comes from the verified API key.
- One server-side script refills and takes a token atomically, so concurrent instances cannot both spend the last token.
- A rejected request gets status 429 with a `Retry-After` header computed from the refill rate.
### Interfaces and storage {toggle="true"}
	- Key per tenant: `rl:<tenant-id>`, holding the token count and the last refill time, with a TTL of two refill periods.
	- The quota source stays the existing tenant configuration service; the gateway caches it for 60 seconds.
### Option measurements (comparison evidence) {toggle="true"}
	<table header-row="true">
		<colgroup>
			<col width="190">
			<col width="90">
			<col width="110">
			<col width="250">
		</colgroup>
		<tr>
			<td>Algorithm</td>
			<td>p99 added</td>
			<td>Over-admission</td>
			<td>Main cost</td>
		</tr>
		<tr>
			<td>Token bucket</td>
			<td>0.8 ms</td>
			<td>1.9%</td>
			<td>One script call per check</td>
		</tr>
		<tr>
			<td>Sliding window log</td>
			<td>1.6 ms</td>
			<td>0.2%</td>
			<td>Memory grows with request rate</td>
		</tr>
		<tr>
			<td>Fixed window counter</td>
			<td>0.5 ms</td>
			<td>38%</td>
			<td>Double burst at window edges</td>
		</tr>
	</table>
	- Internal load test on <mention-date start="2026-09-30"/>: 12 gateway instances, 400 synthetic tenants, 20k requests per second, 30 minutes per algorithm.
	- Over-admission is the requests admitted above quota divided by the quota, in the worst one-minute window.
	- The design proposes the token bucket. Both it and the sliding window log meet the goals, and the token bucket's memory per tenant stays constant as traffic grows.
## Threat model and limits {toggle="true"}
	- **In scope**: a tenant spreading requests across instances to exceed its quota. Mitigated by the shared bucket.
	- **Out of scope**: volumetric floods below the gateway. Transferred to the edge network's protection, which absorbs them before authentication.
	- **Assumptions**: the tenant ID is taken only from an authenticated API key; an unauthenticated request never reaches the limiter.
	- **Residual risk**: during a Redis outage the limiter either stops enforcing or rejects all traffic, depending on the open question below.
## Alternatives considered {toggle="true"}
	- **Sliding window log**: the most accurate option. Rejected for this design because its memory per tenant grows with request rate, and the busiest tenants would need a larger Redis cluster.
	- **Per-instance counters with the quota divided by instance count**: no new dependency. Rejected because autoscaling changes the instance count every few minutes, so the divided quota is wrong whenever traffic changes.
## Test plan {toggle="true"}
	- Shadow mode first: the limiter records decisions without enforcing them, and over-admission is computed from the access logs.
	- Failure injection: a Redis failover, which takes 3\~5 s in staging, must not raise p99 above 2 ms after recovery.
	- Launch criterion: two weeks of shadow mode with over-admission under 5% and no tenant rejected below its quota.
## Milestones {toggle="true"}
	<table header-row="true">
		<colgroup>
			<col width="200">
			<col width="160">
			<col width="280">
		</colgroup>
		<tr>
			<td>Milestone</td>
			<td>Target</td>
			<td>Exit condition</td>
		</tr>
		<tr>
			<td>Shadow mode</td>
			<td><mention-date start="2026-11-02" end="2026-11-13"/></td>
			<td>Launch criterion met</td>
		</tr>
		<tr>
			<td>Internal tenants enforced</td>
			<td><mention-date start="2026-11-16"/></td>
			<td>No false rejections for 3 days</td>
		</tr>
		<tr>
			<td>External tenants enforced</td>
			<td><mention-date start="2026-11-30"/></td>
			<td>Rollout complete</td>
		</tr>
	</table>
	- Day-to-day tasks live in the tracker project linked in the header.
## Open questions
- **Before review**
	- Should the limiter fail open or fail closed when Redis is unreachable?
		- Blocks the failure behavior and the residual risk. Settled by the API platform owners against the availability target.
	- Is 5% over-admission in a one-minute window acceptable for billing?
		- Settled by the billing team.
- **During implementation**
	- Does the script stay under 1 ms at p99 at the 40k requests per second peak?
		- Settled by the peak-traffic load test.
## References {toggle="true"}
	- [Load test results, 2026-09-30](https://dashboards.example.com/gateway/rate-limit-load-test): the source of every number in the comparison table.
	- [Redis cluster capacity runbook](https://docs.example.com/runbooks/redis-capacity): the memory headroom behind the sliding window rejection.
```

Why it is shaped this way:

- The callout and summary answer what, how, by when, and what is open before any scrolling. Only the owner is mentioned; the reviewer is a role, so nobody else receives a mention.
- Each figure answers one question: when over-quota traffic arrives, and how a request is admitted. Each caption states the claim before the reading key.
- The measurement table sits in a toggle under Design, is labeled comparison evidence, and the text says "proposes"; the header status is In Review because no selection has been approved.
- Cells hold values and short phrases; the measuring conditions and the metric definition are bullets under the table. Column widths follow content: about 90 to 110 for numbers, about 190 to 200 for names, and 250 to 280 for short descriptions. Each table totals 640, under the working total of about 700, because both sit inside toggles.
- The only undecided items are in Open questions. The threat model points to that question once instead of repeating a disclaimer.
- The test plan escapes `~` in a range (`3\~5 s`), and dates that readers act on, including the shadow-mode period, are date mentions.

## Open-Questions Page

When reviewers need the questions on their own, they get a separate page titled "Rate limiter: open questions" that links back to the design with a page mention:

```markdown
Design page: <mention-page url="https://www.notion.so/<design-page-id>"/>
## Before review
- Should the limiter fail open or fail closed when Redis is unreachable?
	- Blocks the failure behavior. Settled by the API platform owners against the availability target.
- Is 5% over-admission in a one-minute window acceptable for billing?
	- Settled by the billing team.
## During implementation
- Does the script stay under 1 ms at p99 at the 40k requests per second peak?
	- Settled by the peak-traffic load test.
## Out of scope for this design
- Should quotas apply per endpoint as well as per tenant?
	- Left to a later design, because billing has no per-endpoint price.
```

The groups follow when an answer is needed, so a reviewer sees what must be settled before approving. No question is assigned to a named person; the deciding role is enough.

## Correcting An Existing Page

The user asks to clean up the Design section of an earlier draft of the same page. The fetched section reads:

```markdown
## Design
We decided to use the quota guard with sliding windows (Alex's benchmark showed it is the most accurate). Note: this might still change and the numbers are preliminary, so please double-check before relying on them.
<table>
	<tr>
		<td>Quota guard (token)</td>
		<td>Fast enough in our tests but we are not fully sure how it behaves when Redis restarts, needs more checking</td>
	</tr>
	<tr>
		<td>Quota guard (sliding)</td>
		<td>Most accurate, Alex recommends it</td>
	</tr>
</table>
Reviewers: Alex, Sam, Robin, Kai
```

Problems: "quota guard" is a coined name for a rate limiter; "decided" is unsupported because the owner has not decided; names sit on evidence and in a reviewer list; the table has no header row, no widths, and sentences in its cells, and it sits in the visible body; a blanket disclaimer stands where the condition that limits the numbers belongs; and an unresolved question is buried in a cell.

After the edit:

```markdown
## Design
- The design proposes a token-bucket rate limiter. The option measurements are comparison evidence against the main alternative, the sliding window log.
### Option measurements (comparison evidence) {toggle="true"}
	<table header-row="true">
		<colgroup>
			<col width="200">
			<col width="100">
			<col width="120">
		</colgroup>
		<tr>
			<td>Algorithm</td>
			<td>p99 added</td>
			<td>Over-admission</td>
		</tr>
		<tr>
			<td>Token bucket</td>
			<td>0.8 ms</td>
			<td>1.9%</td>
		</tr>
		<tr>
			<td>Sliding window log</td>
			<td>1.6 ms</td>
			<td>0.2%</td>
		</tr>
	</table>
	- Internal load test on <mention-date start="2026-09-30"/>: 20k requests per second, one 30-minute run per algorithm.
```

And in Open questions, under Before review:

```markdown
	- How does the token bucket behave when Redis restarts mid-burst?
		- Settled by the failure-injection run in the test plan.
```

"The numbers are preliminary" did not disappear: what made them preliminary, one 30-minute run per algorithm, now sits beside the measurements as the condition a reader needs to weigh them, and the Redis-restart doubt became an open question. The reviewer list moved to the header callout as "api-gateway CODEOWNERS". Because "quota guard" also labeled the mechanism figure, the figure was re-rendered with "rate limiter", uploaded, and swapped in with `replace_content`, keeping every other image source and child page tag. The verification fetch confirmed no names remain outside mentions, the table has its header row and widths, and the image count is unchanged.
