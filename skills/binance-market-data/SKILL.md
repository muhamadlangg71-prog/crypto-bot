---
name: binance-market-data
description: Use when the user wants crypto market data from Binance's official public API — prices, 24h stats, klines/OHLC history, order book, symbol info, or buy/sell indicators (RSI, EMA, MACD, Bollinger) computed from candles. Covers REST and WebSocket endpoints, rate limits, indicator formulas, and output rules. No API key needed.
---

# Binance Market Data (Official API)

Use this skill when the user wants crypto prices, OHLC/candles, order book, 24h stats, or computed technical indicators (RSI, EMA, MACD) from Binance's official API — no TradingView, no API key needed for market data.

## Key facts

- Binance's REST market-data endpoints are **official, public, and free**. No API key, no signature for market data.
- Public data endpoints: `https://api.binance.com/api/v3/...` or the data-only mirror `https://data-api.binance.vision/api/v3/...` (use the mirror for pure market data to avoid rate limits on the main host).
- Rate limit: generous weight-based system (1200 weight/min per IP by default). Respect HTTP 429 and 418 responses: back off and slow down.
- API keys are **only** needed for account, trade, and wallet endpoints — never ask for them for market data.

## Endpoints (all GET)

### Current price / 24h stats
- `GET /api/v3/ticker/price?symbol=BTCUSDT` — latest price only.
- `GET /api/v3/ticker/24hr?symbol=BTCUSDT` — price, priceChange, priceChangePercent, highPrice, lowPrice, volume, quoteVolume, weightedAvgPrice, open/close/openTime. Omit `symbol` to get all tickers (heavy; use `?symbols=["BTCUSDT","ETHUSDT"]` for a few).

### Candles / OHLC history
- `GET /api/v3/klines?symbol=BTCUSDT&interval=1h&limit=500` — returns arrays: `[openTime, open, high, low, close, volume, closeTime, quoteVolume, trades, ...]`.
- `interval` values: `1m`, `3m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `6h`, `8h`, `12h`, `1d`, `3d`, `1w`, `1M`. Max `limit` 1000; paginate with `endTime` for older data.

### Order book / trades / averages
- `GET /api/v3/depth?symbol=BTCUSDT&limit=20` — bids/asks. Valid limits: 5, 10, 20, 50, 100, 500, 1000, 5000.
- `GET /api/v3/trades?symbol=BTCUSDT&limit=50` — recent trades.
- `GET /api/v3/avgPrice?symbol=BTCUSDT` — average price over a window.

### Symbol discovery
- `GET /api/v3/exchangeInfo` — all symbols, status (TRADING), base/quote assets, filters (tick size, min notional). Use `?symbol=` to check one pair.
- `GET /api/v3/ticker/bookTicker?symbol=BTCUSDT` — best bid/ask.

### WebSocket (live, optional)
- `wss://stream.binance.com:9443/ws/btcusdt@kline_1m` for live candle updates, `@trade`, `@ticker`, `@depth20` streams; combined streams via `?streams=`. Only for runtimes with websocket support; REST polling is fine for periodic checks.

## Computing indicators from klines

Compute buy/sell signals yourself from `klines` closes (standard formulas):
- **RSI(14)**: average gain/loss over 14 closes; RSI < 30 oversold (buy note), > 70 overbought (sell note).
- **EMA(9/12/26)** and **MACD(12,26,9)**: MACD = EMA12 − EMA26; signal = EMA9 of MACD; bullish cross when MACD crosses above signal.
- **SMA(20/50/200)**: uptrend bias when price > SMA50 > SMA200 (golden-cross context).
- **Bollinger(20,2)**: SMA20 ± 2 stddev; price near lower band + RSI < 30 = oversold bounce candidate.
- **ATR(14)** for volatility-based position sizing/stops.

Pair with the alert-rule templates from the `market-push-notifications` skill when the user wants recurring signal checks.

## Execution notes

- Run requests from an HTTP-capable runtime (code interpreter, workflow HTTP step). Sandbox `curl` may be unavailable — don't rely on it.
- Keep requests minimal: batch with `symbols=[...]`, choose sensible `limit` (100 candles is usually enough for indicator warm-up; RSI/MACD need ~50+).
- On HTTP 429/418: stop, wait, retry slower; disclose to the user.

## Output rules

- Always show: symbol, price, 24h change, and the computed indicators with their timeframe (`interval`).
- State the endpoint used (`api.binance.com` or `data-api.binance.vision`) and that data is from Binance's official public API and may be a few seconds delayed.
- Buy/sell reads from computed indicators are technical opinions, **not financial advice** — include the disclaimer.
- For symbol questions (which pairs exist, min order size), check `exchangeInfo` before answering.
