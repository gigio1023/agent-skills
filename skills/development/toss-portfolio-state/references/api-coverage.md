# Toss OpenAPI Coverage

## Table of Contents

- Source Of Truth
- Coverage Modes
- Default Read-Only Account State
- Basic Market Context
- Full Market Context
- Mutating Endpoints Blocked
- Known Documentation Edge Cases

## Source Of Truth

Use the official Toss Invest OpenAPI sources when checking endpoint coverage:

- `https://developers.tossinvest.com/llms.txt`
- `https://openapi.tossinvest.com/openapi-docs/latest/openapi.json`

The OpenAPI JSON is the canonical source for endpoint paths, schemas, examples,
rate-limit groups, and current version. Use this command to compare the bundled
script against the current official endpoint list:

```bash
bun --no-env-file --no-install scripts/fetch_portfolio_snapshot.ts --print-api-coverage
```

Success requires `coverage_ok: true`, a nonzero `official_endpoint_count`, an
empty `missing_expected_endpoints`, and an empty
`unclassified_official_endpoints`. The command exits nonzero when the document
cannot be fetched or parsed, when an expected endpoint disappears, or when a new
official endpoint has not been classified. The reported `source` is the origin
actually queried.

## Coverage Modes

- `--market-context none`: account-state only. Use for quick balance/holdings
  snapshots or when market data is handled by another source.
- `--market-context basic`: default. Adds stock metadata, warnings, current
  prices, price limits, and market-indicator prices for held and explicit
  symbols.
- `--market-context full`: adds heavier public market data: orderbook, trades,
  daily candles, rankings, market-indicator candles, and KOSPI/KOSDAQ investor
  trading.

## Default Read-Only Account State

The fetcher calls these endpoints by default:

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/oauth2/token` | Issue a bearer token for this run. |
| `GET` | `/api/v1/accounts` | Select the account and obtain `accountSeq`. |
| `GET` | `/api/v1/holdings` | Read current holdings and PnL. |
| `GET` | `/api/v1/buying-power` | Read KRW and USD buying power. |
| `GET` | `/api/v1/sellable-quantity` | Read sellable quantity for held symbols. |
| `GET` | `/api/v1/commissions` | Read market commission rates. |
| `GET` | `/api/v1/orders` | Read open and closed orders. |
| `GET` | `/api/v1/orders/{orderId}` | Read order details for open and recently closed orders. |
| `GET` | `/api/v1/conditional-orders` | Read open and closed conditional orders. |
| `GET` | `/api/v1/conditional-orders/{conditionalOrderId}` | Read conditional order details. |
| `GET` | `/api/v1/exchange-rate` | Read USD/KRW reference rate. |
| `GET` | `/api/v1/market-calendar/KR` | Read Korean market calendar. |
| `GET` | `/api/v1/market-calendar/US` | Read US market calendar. |

## Basic Market Context

Basic mode adds these read-only endpoints:

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/v1/stocks` | Stock master data for held and explicit symbols. |
| `GET` | `/api/v1/stocks/{symbol}/warnings` | Buy-warning and VI flags. |
| `GET` | `/api/v1/prices` | Current prices. |
| `GET` | `/api/v1/price-limits` | Daily upper/lower price limits. |
| `GET` | `/api/v1/market-indicators/prices` | KOSPI/KOSDAQ and Korean bond indicator prices. |

## Full Market Context

Full mode additionally calls:

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/v1/orderbook` | Orderbook by symbol. |
| `GET` | `/api/v1/trades` | Recent trades by symbol. |
| `GET` | `/api/v1/candles` | Daily candles by symbol. |
| `GET` | `/api/v1/rankings` | KR/US rankings. |
| `GET` | `/api/v1/market-indicators/{symbol}/candles` | Indicator candles. |
| `GET` | `/api/v1/market-indicators/{symbol}/investor-trading` | KOSPI/KOSDAQ investor trading. |

## Mutating Endpoints Blocked

These official endpoints exist but are not part of this skill:

| Method | Path | Reason |
|---|---|---|
| `POST` | `/api/v1/orders` | Creates real broker orders. |
| `POST` | `/api/v1/orders/{orderId}/modify` | Modifies real broker orders. |
| `POST` | `/api/v1/orders/{orderId}/cancel` | Cancels real broker orders. |
| `POST` | `/api/v1/conditional-orders` | Creates conditional orders that can trigger trades. |
| `POST` | `/api/v1/conditional-orders/{conditionalOrderId}/modify` | Modifies conditional orders. |
| `DELETE` | `/api/v1/conditional-orders/{conditionalOrderId}` | Cancels conditional orders. |

## Known Documentation Edge Cases

- `GET /api/v1/orders` operation text supports `status=OPEN|CLOSED`, while an
  older schema description may still say `CLOSED` is not supported. The fetcher
  attempts `CLOSED` and records a warning if the upstream rejects it.
- Toss API responses include rate-limit headers. The fetcher runs sequentially,
  applies a small request delay, and retries `429` or transient server errors
  with `Retry-After` or exponential backoff.
