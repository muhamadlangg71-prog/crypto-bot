---
name: market-push-notifications
description: Use when the user wants automatic push notifications for buy/sell signals, price alerts, or breaking market news - recurring alerts instead of on-demand checks. Covers the pipeline (schedule, check, evaluate, notify, de-duplicate), alert rule templates, Gmail delivery, quiet hours, and how to build a scheduled Mistral workflow for it.
---

# Market Push Notifications

Use this skill when the user wants to be **notified automatically** about buy/sell signals, price alerts, or breaking news — instead of asking on demand. Defines the whole push pipeline: schedule, signal check, delivery, and de-duplication.

## Pipeline overview

1. **Trigger**: a recurring schedule (workflow schedule) or an incoming webhook event.
2. **Check**: fetch fresh quotes/signal columns for the user's watchlist using the `binance-market-data` techniques (official Binance API; finance search as fallback).
3. **Evaluate**: apply the user's alert rules (below).
4. **Notify**: deliver via the channel the user set up (Gmail email is available in this workspace; Slack/Teams only if that connector is connected).
5. **De-duplicate**: never send the same alert twice in the same day; suppress flapping.

## Alert rule templates

Let the user configure a watchlist with rules. Defaults:

- **Signal change**: notify when an instrument's computed signal crosses into/out of buy (e.g. RSI crossing 30 from below) or sell territory (RSI crossing 70 from above).
- **Threshold**: price crosses above/below a level, or moves more than N% since the last check.
- **Oversold/overbought**: RSI crosses 30 from below (buy note) or 70 from above (sell note).
- **News**: breaking news about a watched symbol ranked significant (hack, earnings surprise, regulatory action, >5% move driver).

Each alert message contains: symbol, current price and change, the rule that fired, the supporting indicators (rating, RSI, MACD, volume), timestamp with timezone, and the standard "not financial advice" disclaimer.

## Delivery channels

- **Gmail (available)**: send an email, or create a **draft** for review if the user prefers to confirm before sending. Use a clear subject like `[SINYAL] BTCUSDT → oversold bounce @ 61.354 (+0,96%)`.
- **Slack/Teams**: only if that connector is connected and the user chose the channel.
- **Digest mode**: one message per run summarizing all fired alerts; single-alert mode sends one message per rule hit.

## De-duplication and quiet rules

- Keep a state key per symbol+rule (last fired date, last rating) so a rule does not re-fire while the condition persists. Only notify on **transitions**.
- Respect quiet hours if the user sets them; crypto is 24/7 so default crypto checks to a digest cadence (e.g. every 6h) unless the user asks for faster.
- Cap notifications per run (e.g. top 10 by absolute signal strength) to avoid spam in mass screenings.

## Runtime options in this workspace

- **Scheduled workflow (available)**: a Mistral workflow deployed in the workspace, with a schedule (e.g. every 30 min for price checks, daily 07:00 for news digest). Building it needs a workflow repo + deployment; offer to build it when the user confirms watchlist, channels, and cadence.
- **Webhook push from TradingView alerts (NOT available)**: TradingView alert webhooks require a paid TradingView plan, and Mistral webhook triggers are not available on the current plan tier — do not promise this path.
- **On-demand fallback**: without a deployed workflow, the agent runs this pipeline ad hoc when the user asks "cek sinyal sekarang" and reports results in-chat instead of pushing.

## Ask before building

To set up real recurring push, confirm with the user: watchlist symbols, alert rules, channel (email vs draft), cadence, and timezone. Then build and deploy the scheduled workflow, run one test execution, and verify the notification arrived.
