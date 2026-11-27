# Skills

Agent skills for market data, signals, news, and push notifications. Each skill is a folder with a `SKILL.md` (YAML frontmatter + Markdown instructions) and can be loaded by any agent that supports file-based skills (e.g. Mistral Studio skills).

| Skill | Purpose | Source |
|---|---|---|
| `binance-market-data` | Crypto prices, klines/OHLC, order book, and computed buy/sell indicators (RSI, EMA, MACD, Bollinger, ATR) | Binance official public API (free, no API key) |
| `binance-news-scanner` | Official Binance announcements (listings, delistings, events) + general crypto news, paired with live prices | Binance announcements endpoint + news search |
| `x-news-scanner` | Crypto news from X (Twitter): accounts, hashtags, viral posts, paired with live prices | News search targeting X content; optional paid X API v2 |
| `market-push-notifications` | Push-notification pipeline for signals, price alerts, and news digests | Binance API + Gmail delivery, scheduled workflows |

## Design notes

- No TradingView dependency anywhere: all market data comes from Binance's official public API; news comes from search-based retrieval.
- Every skill includes honest limitation notes, rate-limit handling, output formatting rules, and a "not financial advice" disclaimer.
- The three signal/news skills cross-reference each other: data → signals → news → notifications.
