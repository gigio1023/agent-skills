---
name: toss-portfolio-state
description: >
  Use when the user wants a read-only Toss Invest OpenAPI portfolio snapshot,
  account balance/current holdings/order-history/market-context export, or
  normalized personal investment-state payload for another workflow. Triggers on
  "Toss API balance", "Toss OpenAPI holdings", "Toss portfolio snapshot", "Toss
  account-state export", "Toss market context", and "read my Toss investment
  status". NOT for investment advice, portfolio decisions, automatic trading,
  broker order creation/modification/cancelation, credential storage, or
  tax/legal conclusions; use investment-decision-support for judgment.
---

# Toss Portfolio State

Use this skill to collect a read-only Toss Invest OpenAPI snapshot and turn it
into a normalized `toss_portfolio_snapshot`. The output is personal account
state evidence plus optional market context: holdings, buying power, sellable
quantity, commissions, open and closed orders, conditional order history, FX,
market calendars, stock reference data, warnings, prices, and optional deeper
market data. It is not a trading engine and not an investment-decision system.

## Quick Start

1. Read `references/snapshot-contract.md` before mapping fields or changing the
   script.
2. Confirm the request is read-only. If the user asks for orders, transfers,
   automatic rebalancing, or live execution, stop this skill and route to the
   appropriate safety boundary.
3. Load credentials only from process environment or a user-specified env file.
   Never store secrets, tokens, raw account numbers, or raw broker responses in
   the skill directory.
4. Run the bundled fetcher with Bun. Use `--no-env-file` so Bun does not
   auto-load an ambient `.env`; pass the intended file explicitly:

```bash
bun --no-env-file --no-install scripts/fetch_portfolio_snapshot.ts --env-file .env --market-context basic --orders-days 30 --recent-orders-limit 40
```

5. Hand the normalized JSON to the requesting workflow. For
   `investment-decision-support`, treat it as a temporary personal-state input
   unless the user explicitly approves a durable state update.

## Workflow

### 1. Safety Gate

Accept only read-only collection. The allowed surface is token creation for API
access, account discovery, holdings, buying power, sellable quantity,
commissions, order history, conditional order history, exchange rate, market
calendar, stock reference data, stock warnings, prices, orderbook, trades,
candles, rankings, and market indicators. Anything that changes broker state is
out of scope because this skill exists to separate evidence from execution.

### 2. Collection

Use `bun --no-env-file --no-install scripts/fetch_portfolio_snapshot.ts` from
this skill directory when possible. If the harness cannot run Bun, manually
follow `references/snapshot-contract.md` and `references/api-coverage.md` while
preserving the same redaction and output fields.

Required credential names:

- `TOSS_INVEST_API_KEY`
- `TOSS_INVEST_SECRET_KEY`

Optional settings:

- `TOSS_INVEST_BASE_URL`
- `TOSS_INVEST_ACCOUNT_ALIAS`

Secret handling:

- Prefer inheriting process environment variables from the user's shell or pass
  an env-file path with `--env-file`.
- Do not paste secret values into commands, prompts, logs, or durable files.
- Do not print or summarize the env file content. If checking setup, report only
  whether required keys are present or missing.
- Do not use bare `bun` in instructions that touch credentials; Bun auto-loads
  ambient `.env` files by default, so use `bun --no-env-file --no-install ...`
  and let the script read only the explicit `--env-file`.

### 3. Normalization

Produce one JSON object with:

- `snapshot_type`
- `as_of_kst`
- `retrieved_at_utc`
- `account`
- `buying_power`
- `sellable_quantities`
- `commissions`
- `exchange_rate`
- `market_calendar`
- `holdings_overview`
- `holdings`
- `open_orders`
- `closed_orders_window`
- `recent_closed_orders`
- `conditional_orders`
- `market_context`
- `source_provenance`
- `warnings`

The closed set above lives in `references/snapshot-contract.md`; do not restate
the schema elsewhere.

### 4. Handoff

When another skill needs personal portfolio state, pass the normalized snapshot
or summarize only the fields needed for that decision. Keep these boundaries:

- Account state can block personal action readiness.
- Account state cannot prove a market thesis by itself.
- Recent order history can flag behavior risk, but it is not a complete tax-lot
  ledger.
- Toss quote or last-price fields are broker snapshot data; current market tape
  still needs independent source freshness checks.

## Reference Files

| File | When to read | Contains |
|---|---|---|
| `references/snapshot-contract.md` | Before fetching, mapping, validating, or handing off a snapshot | Credential boundary, output schema, freshness, redaction, and blocker rules. |
| `references/api-coverage.md` | When checking Toss OpenAPI coverage, deciding whether to call optional market APIs, or updating endpoint support | Official endpoint groups, read-only vs mutating classification, default/basic/full coverage, and known documentation edge cases. |

## Scripts

| Script | Use | Self-test |
|---|---|---|
| `scripts/fetch_portfolio_snapshot.ts` | Fetch and normalize a read-only Toss Invest OpenAPI portfolio snapshot. | `bun --no-env-file --no-install scripts/fetch_portfolio_snapshot.ts --self-test` |

## Validation

Before shipping changes:

- `SKILL.md` frontmatter has only `name` and `description`.
- The script self-test exits 0.
- `bun --no-env-file --no-install scripts/fetch_portfolio_snapshot.ts --print-api-coverage` reports no unexpected official endpoint outside the read-only or blocked mutating sets.
- The reference path exists and is one level deep.
- No credential, token, raw account number, or raw broker response is committed.
- Trigger examples include positive and near-miss negative cases.

## Trigger Tests

Positive prompts:

- "Use Toss API to summarize my current balance and holdings."
- "Fetch a Toss OpenAPI portfolio snapshot for investment-decision-support."
- "Read my Toss balance and recent orders without making trades."
- "Add Toss market context for my holdings, but do not place orders."

Near-miss negative prompts:

- "Should I buy more MU today?" Use `investment-decision-support`.
- "Connect Toss API and automatically rebalance my account." Reject execution
  setup; this skill stays read-only.

## Gotchas

- Do not let "API access" expand into order placement. This skill intentionally
  collects evidence only.
- Do not print or persist bearer tokens, raw account numbers, client secrets, or
  raw API envelopes. Mask account numbers and omit order IDs, conditional order
  IDs, client order IDs, and triggered order IDs.
- Do not "helpfully" open and quote `.env` contents. Use the file as an input
  source only, and keep values inside the script process.
- Do not use `bunx` for the bundled fetcher. `bunx` is for package executables;
  this skill ships a local Bun script.
- Do not treat the snapshot as current-market research. A broker snapshot may be
  stale, delayed, session-specific, or incomplete for market-tape purposes.
- Do not infer tax lots from recent closed orders alone. Treat tax-sensitive
  decisions as needing human or separate state confirmation.
- If Toss changes the response shape, surface the missing field as a blocker
  instead of guessing.
