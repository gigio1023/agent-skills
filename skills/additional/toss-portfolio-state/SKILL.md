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
  tax/legal conclusions; leave judgment to a decision-support skill when one
  is installed.
---

# Toss Portfolio State

Collect a read-only Toss Invest OpenAPI snapshot as a normalized `toss_portfolio_snapshot` for temporary account-state evidence.

## Quick Start

1. Read `references/snapshot-contract.md` before mapping fields or changing the script.
2. Confirm from the requested outcome that the task is read-only. If it includes orders, transfers, automatic rebalancing, or live execution, state the boundary and stop before loading credentials.
3. Check prerequisites. Both scripts need Bun on this device (verified with 1.4.2). The direct route needs Toss Invest OpenAPI credentials (`TOSS_INVEST_API_KEY` and `TOSS_INVEST_SECRET_KEY`) in an env file the user names or in the process environment. The remote route needs `ssh` on this device and the credentials on the remote host at the fixed paths in `references/remote-access.md`. If Bun is missing, return a blocker that points to the official Bun install instructions; installing it needs the user's approval. Never store secrets, tokens, raw account numbers, or raw broker responses in the skill directory.
4. Choose the route and run the transport bundled with the active skill directory:

   - If `~/.config/toss-portfolio-state/remote.json` exists (or the file named by `TOSS_PORTFOLIO_REMOTE_CONFIG`), a remote route is configured: a host the user controls, such as a home server, whose public IP Toss accepts. Read `references/remote-access.md` and run:

     ```bash
     bun --no-env-file --no-install scripts/remote_portfolio_snapshot.ts fetch --market-context basic --orders-days 30 --recent-orders-limit 40
     ```

   - If no remote route is configured and the user's Toss API key accepts requests only from a registered IP that this device does not have, offer the one-time remote setup in `references/remote-access.md`. Run it only after the user approves the local SSH key and config changes.
   - Otherwise, run the direct fetcher with an explicit env file that the user names. Load credentials only from that file or the process environment, and keep `--no-env-file` so Bun does not auto-load an ambient `.env`:

     ```bash
     bun --no-env-file --no-install scripts/fetch_portfolio_snapshot.ts --env-file <env-file> --market-context basic --orders-days 30 --recent-orders-limit 40
     ```

     CLI flags override the explicit env file, which overrides process environment. The default origin is the official HTTPS host.

   When a configured remote route fails, return its blocker. Never fall back silently to a local request, because this device's public IP may not be registered with Toss; run the direct fetcher instead only when the user explicitly chooses it.

5. Hand the normalized JSON to the requesting workflow. When a separately installed decision-support skill consumes it, treat the JSON as a temporary personal-state input unless the user explicitly approves a durable state update.

Keep the requested mode and window or documented defaults. Refetch only for needed freshness or an unresolved required field, not to enrich a summary.

## Workflow

### 1. Safety Gate

Accept only read-only collection. The allowed surface is token creation for API access, account discovery, holdings, buying power, sellable quantity, commissions, order history, conditional order history, exchange rate, market calendar, stock reference data, stock warnings, prices, orderbook, trades, candles, rankings, and market indicators. Anything that changes broker state is out of scope because this skill exists to separate evidence from execution.

### 2. Collection

The required names are `TOSS_INVEST_API_KEY` and `TOSS_INVEST_SECRET_KEY`; optional settings are `TOSS_INVEST_BASE_URL` and `TOSS_INVEST_ACCOUNT_ALIAS`. CLI flags override the explicit env file, which overrides process environment. A non-official base URL requires the explicit `--allow-custom-base-url` gate and must be a user-approved HTTPS endpoint or a loopback mock.

Secret handling:

- Do not paste secret values into commands, prompts, logs, or durable files.
- Report only whether required env keys are present; never print their values.
- Always use `bun --no-env-file --no-install` and pass the intended env file explicitly so Bun cannot auto-load an ambient `.env`.

### 3. Normalization

Produce one normalized object using the documented field set, redaction rules, and external-data trust boundary in `references/snapshot-contract.md`. Preserve timestamps, provenance, and warnings even when a downstream consumer asks for a shorter summary. Never guess after schema drift; return a blocker when missing meaning is decisive.

### 4. Handoff

When another skill needs personal portfolio state, pass the normalized snapshot or summarize only the fields needed for that decision. Keep these boundaries:

- Account state can block personal action readiness but cannot prove a market thesis.
- Recent orders can flag behavior risk but do not form a complete tax-lot ledger.
- Toss quote or last-price fields are broker snapshot data; current market tape still needs independent source freshness checks.

The snapshot is personal financial data. Keep it in the session or a private location the user approves. Never commit it to a repository, and do not paste it into shared channels or third-party services unless the user asks.

## Reference Files

| File | When to read | Contains |
|---|---|---|
| `references/snapshot-contract.md` | Before fetching, mapping, validating, or handing off a snapshot | Credential boundary, output schema, freshness, redaction, and blocker rules. |
| `references/api-coverage.md` | When checking Toss OpenAPI or AsyncAPI coverage, deciding whether to call optional market APIs, or updating endpoint support | Official endpoint groups, read-only vs mutating classification, realtime WebSocket channels, default/basic/full coverage, and known documentation edge cases. |
| `references/remote-access.md` | When the API must use a registered home public IP or a new client device needs SSH setup | Per-device setup, server prerequisites, remote execution, and fail-closed rules. |

## Scripts

| Script | Use | Self-test |
|---|---|---|
| `scripts/fetch_portfolio_snapshot.ts` | Fetch and normalize a read-only Toss Invest OpenAPI portfolio snapshot. | `bun --no-env-file --no-install scripts/fetch_portfolio_snapshot.ts --self-test` |
| `scripts/remote_portfolio_snapshot.ts` | Set up per-device Tailscale SSH access and run the fetcher on the registered home-server egress. | `bun --no-env-file --no-install scripts/remote_portfolio_snapshot.ts --self-test` |
| `scripts/request_confidentiality.test.ts` | Check redirect rejection and error redaction with loopback servers and synthetic credentials. | `bun --no-env-file --no-install test scripts/request_confidentiality.test.ts` |

## Output Contract

On success, return or hand off the normalized JSON and lead any human summary with its `as_of_kst`, account alias/masked identity, requested account facts, and warnings. State the selected market-context mode. Keep required facts, caveats, and downstream actions; omit endpoint-by-endpoint narration.

On failure, return a blocker with the failed capability, whether the failure is credentials, account discovery, API availability, or schema drift, and the smallest safe next action. Do not return a confident partial snapshot when the request depends on the missing field.

## Validation

Validate the package and inspect for secrets. For changed scripts, invocations, or API mappings, also run the applicable checks below. Prose edits need no live account collection or network coverage crawl:

- Both documented script self-tests exit 0. The remote test must reject credential/base-URL overrides and preserve encoded snapshot arguments.
- The request-confidentiality tests exit 0. They must prove token and account requests reject HTTP 307/308 before contacting the redirect destination, and HTTP errors or malformed JSON never expose upstream text. These tests use only local mock servers and synthetic credentials.
- `bun --no-env-file --no-install scripts/fetch_portfolio_snapshot.ts --print-api-coverage` exits 0 with `coverage_ok: true`, no missing expected endpoints or realtime channels, and no unclassified official endpoints, realtime channels, or realtime operations. The check reads both the OpenAPI and AsyncAPI documents; fetch, parse, missing-entry, and classification failures exit nonzero.

## Gotchas

- Do not print or persist bearer tokens, raw account numbers, client secrets, or raw API envelopes. Mask account numbers and omit order IDs, conditional order IDs, client order IDs, and triggered order IDs.
- API requests reject redirects, including redirects from the approved origin. HTTP errors report only the status; arbitrary upstream error messages, codes, request IDs, and JSON parser excerpts are intentionally omitted. Known credential, token, account-number, and order-ID values are also removed from error and warning strings.
- Do not use `bunx` for the bundled fetcher. `bunx` is for package executables; this skill ships a local Bun script.
- Do not install a separate wrapper command on the client; run the transport bundled with the active skill.
- Do not copy SSH private keys between devices. The setup route creates one key per device and only authorizes its public key on the home server.
- Do not treat the snapshot as current-market research. A broker snapshot may be stale, delayed, session-specific, or incomplete for market-tape purposes.
- Do not infer tax lots from recent closed orders alone. Treat tax-sensitive decisions as needing human or separate state confirmation.
