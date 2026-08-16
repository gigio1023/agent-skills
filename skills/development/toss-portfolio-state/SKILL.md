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

Collect a read-only Toss Invest OpenAPI snapshot as a normalized
`toss_portfolio_snapshot`. It is temporary account-state evidence, not a trading
engine or investment recommendation.

## Quick Start

1. Read `references/snapshot-contract.md` before mapping fields or changing the
   script.
2. Confirm from the requested outcome that the task is read-only. If it includes
   orders, transfers, automatic rebalancing, or live execution, state the
   boundary and stop before loading credentials.
3. Prefer the configured home-server route when Toss restricts API access to
   that public IP. Read `references/remote-access.md`, then run the bundled Bun
   transport from the active skill directory:

```bash
bun --no-env-file --no-install scripts/remote_portfolio_snapshot.ts fetch --market-context basic --orders-days 30 --recent-orders-limit 40
```

   If the device is not configured, run the reference's one-time setup only
   after the user approves local SSH key and config changes. Do not create a
   per-device wrapper binary or fall back to a local Toss request.

4. Use the direct fetcher only when the user explicitly chooses a local route
   whose egress IP is authorized. Load credentials only from process environment
   or a user-specified env file. Never store secrets, tokens, raw account
   numbers, or raw broker responses in the skill directory. Use `--no-env-file`
   so Bun does not auto-load an ambient `.env`; pass the intended file explicitly:

```bash
bun --no-env-file --no-install scripts/fetch_portfolio_snapshot.ts --env-file .env --market-context basic --orders-days 30 --recent-orders-limit 40
```

   CLI flags override the explicit env file, which overrides process
   environment. The default origin is the official HTTPS host.

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

The required names are `TOSS_INVEST_API_KEY` and
`TOSS_INVEST_SECRET_KEY`; optional settings are `TOSS_INVEST_BASE_URL` and
`TOSS_INVEST_ACCOUNT_ALIAS`. CLI flags override the explicit env file, which
overrides process environment. A non-official base URL requires the explicit
`--allow-custom-base-url` gate and must be a user-approved HTTPS endpoint or a
loopback mock.

Secret handling:

- Do not paste secret values into commands, prompts, logs, or durable files.
- Report only whether required env keys are present; never print their values.
- Always use `bun --no-env-file --no-install` and pass the intended env file
  explicitly so Bun cannot auto-load an ambient `.env`.

### 3. Normalization

Produce one normalized object using the closed field set, redaction rules, and
external-data trust boundary in `references/snapshot-contract.md`. Preserve
timestamps, provenance, and warnings even when a downstream consumer asks for a
shorter summary. Never guess after schema drift; return a blocker when missing
meaning is decisive.

### 4. Handoff

When another skill needs personal portfolio state, pass the normalized snapshot
or summarize only the fields needed for that decision. Keep these boundaries:

- Account state can block personal action readiness but cannot prove a market
  thesis.
- Recent orders can flag behavior risk but do not form a complete tax-lot ledger.
- Toss quote or last-price fields are broker snapshot data; current market tape
  still needs independent source freshness checks.

## Reference Files

| File | When to read | Contains |
|---|---|---|
| `references/snapshot-contract.md` | Before fetching, mapping, validating, or handing off a snapshot | Credential boundary, output schema, freshness, redaction, and blocker rules. |
| `references/api-coverage.md` | When checking Toss OpenAPI coverage, deciding whether to call optional market APIs, or updating endpoint support | Official endpoint groups, read-only vs mutating classification, default/basic/full coverage, and known documentation edge cases. |
| `references/remote-access.md` | When the API must use a registered home public IP or a new client device needs SSH setup | Per-device setup, server prerequisites, remote execution, and fail-closed rules. |

## Scripts

| Script | Use | Self-test |
|---|---|---|
| `scripts/fetch_portfolio_snapshot.ts` | Fetch and normalize a read-only Toss Invest OpenAPI portfolio snapshot. | `bun --no-env-file --no-install scripts/fetch_portfolio_snapshot.ts --self-test` |
| `scripts/remote_portfolio_snapshot.ts` | Set up per-device Tailscale SSH access and run the fetcher on the registered home-server egress. | `bun --no-env-file --no-install scripts/remote_portfolio_snapshot.ts --self-test` |

## Output Contract

On success, return or hand off the normalized JSON and lead any human summary
with its `as_of_kst`, account alias/masked identity, requested account facts,
and warnings. State the selected market-context mode. Keep required facts,
caveats, and downstream actions; omit endpoint-by-endpoint narration.

On failure, return a blocker with the failed capability, whether the failure is
credentials, account discovery, API availability, or schema drift, and the
smallest safe next action. Do not return a confident partial snapshot when the
request depends on the missing field.

## Validation

Before shipping changes:

- Both documented script self-tests exit 0. The remote test must reject
  credential/base-URL overrides and preserve encoded snapshot arguments.
- `bun --no-env-file --no-install scripts/fetch_portfolio_snapshot.ts --print-api-coverage` exits 0 with `coverage_ok: true`, no missing expected endpoints, and no unclassified official endpoints. Fetch, parse, missing-endpoint, and classification failures exit nonzero.
- Run the package validator and confirm no credential, token, raw account
  number, private hostname, or raw broker response was committed.

## Gotchas

- Do not print or persist bearer tokens, raw account numbers, client secrets, or
  raw API envelopes. Mask account numbers and omit order IDs, conditional order
  IDs, client order IDs, and triggered order IDs.
- Do not use `bunx` for the bundled fetcher. `bunx` is for package executables;
  this skill ships a local Bun script.
- Do not install a client-wide `toss-home-snapshot` wrapper. Resolve and run the
  transport bundled with the active skill so updates move with the package.
- Do not copy SSH private keys between devices. The setup route creates one key
  per device and only authorizes its public key on the home server.
- Do not treat the snapshot as current-market research. A broker snapshot may be
  stale, delayed, session-specific, or incomplete for market-tape purposes.
- Do not infer tax lots from recent closed orders alone. Treat tax-sensitive
  decisions as needing human or separate state confirmation.
- If Toss changes the response shape, surface the missing field as a blocker
  instead of guessing.
