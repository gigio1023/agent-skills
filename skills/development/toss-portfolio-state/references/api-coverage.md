# Toss OpenAPI Coverage

## Table of Contents

- Source Of Truth
- Coverage Modes
- Default Read-Only Account State
- Basic Market Context
- Full Market Context
- Classified Read-Only Endpoints Not Called
- Mutating Endpoints Blocked
- Realtime WebSocket Channels Out Of Scope
- Known Documentation Edge Cases

## Source Of Truth

Use the official Toss Invest OpenAPI sources when checking endpoint coverage:

- `https://developers.tossinvest.com/llms.txt`
- `https://openapi.tossinvest.com/openapi-docs/latest/openapi.json`
- `https://openapi.tossinvest.com/openapi-docs/latest/asyncapi.json`

The OpenAPI JSON is the canonical source for REST endpoint paths, schemas, examples, rate-limit groups, and current version. The AsyncAPI 3.0 JSON is the canonical source for the realtime WebSocket API at `wss://openapi-ws.tossinvest.com/ws/v1`: channels, subscription declarations, message schemas, connection limits, keepalive, and reconnect semantics. Use this command to compare the bundled script against the current official endpoint and channel lists:

```bash
bun --no-env-file --no-install scripts/fetch_portfolio_snapshot.ts --print-api-coverage
```

Success requires `coverage_ok: true`, a nonzero `official_endpoint_count` and `official_channel_count`, and empty `missing_expected_endpoints`, `unclassified_official_endpoints`, `missing_expected_channels`, `unclassified_official_channels`, `missing_expected_realtime_operations`, and `unclassified_official_realtime_operations`. The command exits nonzero when either document cannot be fetched or parsed, when an expected endpoint, channel, or realtime operation disappears, or when a new official endpoint, channel, or realtime operation has not been classified. The reported `source` and `asyncapi_source` are the documents actually queried.

## Coverage Modes

- `--market-context none`: account-state only. Use for quick balance/holdings snapshots or when market data is handled by another source.
- `--market-context basic`: default. Adds stock metadata, warnings, current prices, price limits, and market-indicator prices for held and explicit symbols.
- `--market-context full`: adds heavier public market data: orderbook, trades, daily candles, rankings, market-indicator candles, and KOSPI/KOSDAQ investor trading.

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

## Classified Read-Only Endpoints Not Called

The official API also exposes these read-only endpoints. They are classified so new mutating surfaces cannot pass the coverage gate unnoticed, but the snapshot does not call them until its normalized contract has a decision-relevant field for their output.

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/v1/stocks/all` | Full tradable stock universe for one market. |
| `GET` | `/api/v1/stocks/{symbol}/credit-trades` | Korean stock margin-loan and stock-loan trends. |
| `GET` | `/api/v1/stocks/{symbol}/investor-trading` | Korean stock investor trading and holdings trends. |
| `GET` | `/api/v1/stocks/{symbol}/program-trades` | Korean stock program-trading trends. |
| `GET` | `/api/v1/stocks/{symbol}/securities-lending` | Korean stock securities-lending trends. |
| `GET` | `/api/v1/stocks/{symbol}/short-selling` | Korean stock short-selling trends. |

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

## Realtime WebSocket Channels Out Of Scope

The WebSocket API (AsyncAPI document version 1.2.2, checked 2026-09-23) exposes these channels. They are read-only: the market-data channels stream quotes, the order-event channel streams state changes of the user's own orders, and every send operation only declares subscriptions or keeps the connection alive. This snapshot skill never opens a WebSocket, so the channels are classified only to keep a new realtime surface from passing the coverage gate unnoticed. The script also classifies each channel's operations by action and operation ID.

| Channel | Purpose |
|---|---|
| `connection` | Handshake, subscription acknowledgements, error frames, and PING/PONG keepalive shared by all channels. |
| `realtime-trade` | Realtime trade ticks for declared `trade:kr` and `trade:us` symbols. |
| `realtime-orderbook` | Realtime orderbook updates for declared `orderbook:kr` and `orderbook:us` symbols. |
| `realtime-order` | Order events for the user's own account, declared as `personal:order` with `accountSeq`. |

## Known Documentation Edge Cases

- `GET /api/v1/orders` supports `status=OPEN|CLOSED`; the OpenAPI 1.2.17 schema (checked 2026-09-23) lists both values, although earlier schema descriptions said `CLOSED` was not supported. The fetcher still attempts `CLOSED` and records a warning if the upstream rejects it.
- Toss API responses include rate-limit headers. The fetcher runs sequentially, applies a small request delay, and retries `429` or transient server errors with `Retry-After` or exponential backoff.
