# Toss Portfolio Snapshot Contract

## Table of Contents

- Purpose
- Safety Boundary
- Credential Boundary
- Read-Only API Surface
- Snapshot Schema
- Freshness And Provenance
- Handoff Rules
- Blockers
- Negative Cases

## Purpose

This reference defines the normalized handoff object for read-only Toss Invest
OpenAPI account-state collection. Use it when a workflow needs current personal
portfolio state before investment analysis, cash planning, risk-budget checks, or
behavior-risk review. API surface classification lives in `api-coverage.md`.

The snapshot answers: "What does the broker account currently show?" It does not
answer: "What should the user do?"

## Safety Boundary

Allowed:

- Read account list.
- Read holdings.
- Read buying power by currency.
- Read USD/KRW exchange rate when available.
- Read open and closed orders over bounded windows.
- Read open and closed conditional orders.
- Read sellable quantity and commissions.
- Read market calendars, stock reference data, warnings, prices, and optional
  market context needed to interpret current holdings.
- Normalize and summarize the result.

Forbidden:

- Placing, canceling, or replacing orders.
- Transfers, withdrawals, deposits, or automatic rebalancing.
- Credential storage, token logging, or account-number storage.
- Tax/legal conclusions.
- Buy/sell/hold instructions.

## Credential Boundary

Use credentials from process environment or a user-specified env file only:

- `TOSS_INVEST_API_KEY`
- `TOSS_INVEST_SECRET_KEY`

Optional:

- `TOSS_INVEST_BASE_URL`
- `TOSS_INVEST_ACCOUNT_ALIAS`

Never commit env files, tokens, raw account numbers, raw responses, or broker
exports. The normalized output should mask account numbers and omit order IDs by
default.

Operational guidance:

- Pass an env-file path to the fetcher instead of copying values into the command
  line.
- Do not print, quote, summarize, or store the env file content.
- If setup needs checking, report only whether required keys are present or
  missing.
- Keep the access token in process memory for the current run only.

## Read-Only API Surface

The bundled script uses this default read-only surface:

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/oauth2/token` | Obtain a bearer token for this run. |
| `GET` | `/api/v1/accounts` | Discover available accounts and select the brokerage account. |
| `GET` | `/api/v1/holdings` | Read current holdings and overview PnL fields. |
| `GET` | `/api/v1/buying-power?currency=KRW` | Read KRW buying power. |
| `GET` | `/api/v1/buying-power?currency=USD` | Read USD buying power. |
| `GET` | `/api/v1/sellable-quantity?symbol=...` | Read sellable quantity for held symbols. |
| `GET` | `/api/v1/commissions` | Read account commission rates by market. |
| `GET` | `/api/v1/exchange-rate?baseCurrency=USD&quoteCurrency=KRW` | Read the broker-provided USD/KRW rate. |
| `GET` | `/api/v1/market-calendar/KR` | Read Korean market session calendar. |
| `GET` | `/api/v1/market-calendar/US` | Read US market session calendar. |
| `GET` | `/api/v1/orders?status=OPEN` | Read open orders. |
| `GET` | `/api/v1/orders?status=CLOSED` | Read recent closed orders for behavior and liquidity context. |
| `GET` | `/api/v1/orders/{orderId}` | Read order details for open and recently closed orders, then omit order IDs from output. |
| `GET` | `/api/v1/conditional-orders?status=OPEN` | Read open conditional orders. |
| `GET` | `/api/v1/conditional-orders?status=CLOSED` | Read recent closed conditional orders. |
| `GET` | `/api/v1/conditional-orders/{conditionalOrderId}` | Read conditional order details, then omit conditional order IDs from output. |
| `GET` | `/api/v1/stocks?symbols=...` | Read stock reference data for holdings and explicit symbols in basic/full market context. |
| `GET` | `/api/v1/stocks/{symbol}/warnings` | Read stock warning flags in basic/full market context. |
| `GET` | `/api/v1/prices?symbols=...` | Read current prices in basic/full market context. |
| `GET` | `/api/v1/price-limits?symbol=...` | Read price limits in basic/full market context. |
| `GET` | `/api/v1/market-indicators/prices?symbols=...` | Read market indicator prices in basic/full market context. |

Full market context additionally calls orderbook, trades, candles, rankings,
market-indicator candles, and KOSPI/KOSDAQ investor trading. Mutating order and
conditional-order endpoints are deliberately blocked. If the API documentation
changes, update this table, `api-coverage.md`, and the script together.

## Snapshot Schema

The output object is named `toss_portfolio_snapshot` and uses this top-level
field set:

```json
{
  "snapshot_type": "toss_portfolio_snapshot",
  "as_of_kst": "YYYY-MM-DDTHH:mm:ss+09:00",
  "retrieved_at_utc": "YYYY-MM-DDTHH:mm:ss.sssZ",
  "api": {},
  "account": {},
  "read_only_endpoints_called": [],
  "buying_power": {},
  "sellable_quantities": [],
  "commissions": [],
  "exchange_rate": {},
  "market_calendar": {},
  "holdings_overview": {},
  "holdings": [],
  "open_orders": {},
  "closed_orders_window": {},
  "recent_closed_orders": [],
  "conditional_orders": {},
  "market_context": {},
  "source_provenance": [],
  "warnings": []
}
```

Field rules:

- `account.account_no_masked` may show a short masked prefix/suffix but never the
  raw account number.
- Money and quantity values remain strings to avoid decimal precision loss.
- `holdings[].symbol`, `name`, `market_country`, `currency`, `quantity`,
  `average_purchase_price`, `last_price`, `market_value`,
  `market_value_after_cost`, `profit_loss_after_cost`, and
  `profit_loss_rate_pct` are the portable holding fields.
- `recent_closed_orders[]` omits broker order IDs and keeps only timestamp,
  symbol, side, status, currency, quantity, filled quantity, average filled
  price, filled amount, commission, tax, and settlement date.
- `open_orders.orders[]` follows the same redaction rule and is included because
  open orders can block personal action readiness.
- `conditional_orders.open[]` and `conditional_orders.recent_closed[]` omit
  conditional order IDs, client order IDs, triggered order IDs, and raw API
  envelopes. They may include normalized trigger prices, target rates, status,
  quantity, and expiry because those are personal state.
- `market_context` may be `none`, `basic`, or `full`; full mode can be larger
  and should not be written durably without user approval.
- `warnings[]` records missing optional endpoints, schema drift, empty accounts,
  stale windows, or fields that should block downstream judgment.

## Freshness And Provenance

Every snapshot should include:

- `as_of_kst`: user-facing account-state timestamp.
- `retrieved_at_utc`: machine timestamp for this run.
- `api.openapi_version`: version string when available, otherwise `unknown`.
- `source_provenance[]`: source name, endpoint family, freshness note, and
  redaction note.

For action-sensitive investment decisions, a snapshot older than the same local
trading day should usually block personal action readiness. A workflow may still
perform market-only analysis if it labels the personal state stale.

## Handoff Rules

When handing the snapshot to another skill:

- Pass the JSON object directly when possible.
- If summarizing, preserve timestamp, account alias, buying power, holdings,
  recent-order count, and warnings.
- Do not write durable repo state unless the user explicitly asks.
- If durable state is approved, write derived state only into that workflow's
  designated state files, not into this skill directory.

## Blockers

Return a blocker report instead of a partial confident snapshot when:

- Credentials are missing.
- Account discovery returns no usable account.
- Holdings response is missing required fields.
- Buying power is unavailable for a currency needed by the request.
- Open-order, conditional-order, or closed-order access fails and the downstream
  request depends on behavior, execution state, settlement, or recent trade
  history.
- API response shape changed enough that field meaning is unclear.

## Negative Cases

Route away from this skill when the user wants:

- Investment judgment, enter-now-vs-wait, trim/rebalance posture, or risk-budget
  synthesis.
- Broker order placement or auto-trading.
- Tax reporting or legal conclusions.
- A general market-data API for prices, options, futures, macro, or news.
