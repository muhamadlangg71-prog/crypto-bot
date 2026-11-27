---
name: binance-news-scanner
description: Use when the user asks for the latest crypto/Binance news - official Binance announcements (new listings, delistings, events) via the public announcements endpoint, general crypto news via news search, and pairing each item with live prices from Binance's official API. Covers announcement filtering by impact, scheduled digests, and output rules.
---

# Binance News Scanner

Use this skill when the user wants the latest crypto news with a Binance focus: official Binance announcements (new listings, delistings, maintenance, events), or general crypto news paired with live prices from Binance's API.

## Important honesty note

Binance has **no official general-news API**. What exists publicly:
- Binance's own **announcement/CM** endpoints (used by binance.com/announcements) — public but unofficial, may change.
- Everything else (market news, regulation, hacks, macro) comes from news search, not Binance.

Always fetch live items and show timestamps — never answer "latest news" from memory.

## 1. Official Binance announcements

- `GET https://www.binance.com/bapi/apex/v1/public/apex/cms/article/list/query?type=1&pageNo=1&pageSize=20&catalogId=48` — English announcements (new listings, delistings, product updates). `catalogId=48` is the announcement catalog; other catalogs exist for events (e.g. `catalogId=54` activity/launchpool — verify against the live response).
- Response items carry `title`, `releaseDate` (ms epoch), and `code` (slug; the article URL is `https://www.binance.com/en/support/announcement/<code>`).
- For Indonesian: `https://www.binance.com/bapi/apex/v1/public/apex/cms/article/list/query?type=1&pageNo=1&pageSize=20&catalogId=49` may serve other locales — verify against the live response.
- **High-impact filters**: treat *"will list"* / *"adds"* (new listing) and *"delists"* / *"removes"* announcements as high priority — they cause sharp price moves for the affected pairs. Also watch *"renames"*, *MGIR/IEO/Launchpool* events, and maintenance notices.
- Do not poll aggressively: once per run is enough; cache within a run.

## 2. General crypto news

Use the `web_search` **news_search** tool:
- `Bitcoin BTC news today`, `Ethereum news`, `crypto market today`
- `Binance news` / `Binance hack` / `Binance regulation`
- Event queries: `Fed rate decision crypto`, `crypto ETF news`

Rank by recency; cite source + timestamp for every item.

## 3. Pair news with live prices (Binance official API)

For each symbol in the news, fetch `GET https://api.binance.com/api/v3/ticker/24hr?symbol=<SYM>USDT` (see the `binance-market-data` skill) and report: current price, 24h change, volume. This makes each item actionable: headline + price reaction.

## Scheduled digests

When the user wants a recurring round-up (e.g. daily 07:00): build a scheduled Mistral workflow combining announcements + news search + price check, delivered via Gmail (see `market-push-notifications`). For push on **high-impact announcements only** (listing/delisting), dedupe on announcement `code`.

## Output rules

- Format per item: headline (bold), 1–2 sentence summary, source + timestamp, affected symbol(s) with live price and 24h change.
- Clearly label the as-of time of the newest item.
- Mark which items are official Binance announcements vs third-party news.
- Separate facts from interpretation; news is **not financial advice**.
- If the announcements endpoint fails (403/404 — it is unofficial), fall back to news search and disclose the switch.
