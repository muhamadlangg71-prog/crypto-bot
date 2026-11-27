---
name: x-news-scanner
description: Use when the user wants crypto/market news from X (Twitter) - specific accounts' posts, hashtags, viral takes, or to monitor X as a news source. Covers free news-search fallbacks targeting X content, curated high-signal crypto accounts, official X API v2 (paid) and custom connector setup, and pairing with live Binance prices. No X connector exists in the workspace - the skill is honest about that.
---

# X (Twitter) News Scanner

Use this skill when the user wants breaking crypto/market news **from X (Twitter)** — accounts, hashtags, or viral takes — or wants the agent to monitor X as a news source.

## Honest limitations first

- There is **no X connector** in this workspace's connector store, and no authenticated X tool in the session.
- X's official **API v2** requires an API key; meaningful **read access (search/timeline) is a paid tier**. Only suggest it if the user already has or agrees to get a paid X developer account. With a key, a custom MCP connector can be added via the Studio connector store (`create_connector` flow).
- X blocks unauthenticated scraping; do not attempt logins, and treat third-party mirrors (Nitter etc.) as unreliable and often dead.

## How to get X news without API access

### 1. News search targeting X content (primary, free)
Use the `web_search` **news_search** / **web_search** tools — most breaking crypto news originates on X and gets reported within minutes:
- `Bitcoin news X twitter today`
- `site:x.com <symbol>` or `site:twitter.com <topic>` queries
- `"CZ" OR "Binance" announcement tweet`
- Account-driven queries: `Elon Musk tweet crypto`, `Whale Alert bitcoin`, `Wu Blockchain`

Rank by recency; cite the outlet reporting the tweet, the account, and the timestamp.

### 2. Curated high-signal crypto X accounts (search for their latest posts by name)
- Official: `@binance`, `@BinanceResearch`, `@cz_binance`
- Breaking/on-chain: `@WuBlockchain`, `@lookonchain`, `@whale_alert`, `@EmberCN`
- Market commentary: `@CoinDesk`, `@TheBlock__`, `@WatcherGuru`

When the user names an account, query news search with the account handle + topic rather than trying to open x.com directly (login walls block direct reads).

### 3. If the user has a paid X API key
- Search: `GET https://api.x.com/2/tweets/search/recent?query=<q>&max_results=25` with `Authorization: Bearer <token>`.
- Suggest adding it as a **custom MCP connector** in the Mistral Studio store so workflows/agents can call it; credentials are added on the Studio page, never pasted into chat.
- Rate limits are tier-dependent: schedule checks at minutes-level, not seconds.

## Pairing with prices and signals

Combine X-sourced items with live data from the `binance-market-data` skill: for each symbol mentioned, fetch `/api/v3/ticker/24hr` and report price + 24h change. Mark items that are **rumors/unverified** ("according to a post on X") vs confirmed news.

## Output rules

- Per item: what was posted, by whom (account), when (timestamp), source used (X directly vs outlet reporting the post), affected symbol + live price.
- Always state that X posts are unverified and frequently wrong; treat them as leads, not facts — **not financial advice**.
- Never claim live access to X when using search fallbacks; disclose which path was used.
