#!/usr/bin/env python3
"""Bot sinyal indikator untuk crypto futures (data publik Binance Futures API).

Strategi: kombinasi EMA crossover + RSI + MACD + ATR (volatility filter).
Output: BUY / SELL / NEUTRAL per simbol, plus rekomendasi.stop-loss berbasis ATR.

Pakai hanya API publik (read-only). Tidak melakukan order/trade.
"""

import json
import math
import sys
import time
import urllib.request

BASE_URL = "https://fapi.binance.com"
TIMEOUT = 10

DEFAULT_SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]
INTERVAL = "15m"
LIMIT = 200


def fetch_klines(symbol, interval=INTERVAL, limit=LIMIT):
    url = f"{BASE_URL}/fapi/v1/klines?symbol={symbol}&interval={interval}&limit={limit}"
    with urllib.request.urlopen(url, timeout=TIMEOUT) as resp:
        data = json.loads(resp.read().decode())
    return [
        {
            "time": k[0],
            "open": float(k[1]),
            "high": float(k[2]),
            "low": float(k[3]),
            "close": float(k[4]),
            "volume": float(k[5]),
        }
        for k in data
    ]


def ema(values, period):
    k = 2 / (period + 1)
    out = [values[0]]
    for v in values[1:]:
        out.append(v * k + out[-1] * (1 - k))
    return out


def rsi(closes, period=14):
    gains, losses = [], []
    for i in range(1, len(closes)):
        d = closes[i] - closes[i - 1]
        gains.append(max(d, 0))
        losses.append(max(-d, 0))
    ag, al = sum(gains[:period]) / period, sum(losses[:period]) / period
    out = [None] * period
    for i in range(period, len(gains) + 1):
        if i > period:
            ag = (ag * (period - 1) + gains[i - 1]) / period
            al = (al * (period - 1) + losses[i - 1]) / period
        rs = ag / al if al else float("inf")
        out.append(100 - 100 / (1 + rs))
    return out


def macd(closes, fast=12, slow=26, signal=9):
    ef, es = ema(closes, fast), ema(closes, slow)
    macd_line = [f - s for f, s in zip(ef, es)]
    signal_line = ema(macd_line, signal)
    hist = [m - s for m, s in zip(macd_line, signal_line)]
    return macd_line, signal_line, hist


def atr(candles, period=14):
    trs = []
    for i in range(1, len(candles)):
        h, l = candles[i]["high"], candles[i]["low"]
        pc = candles[i - 1]["close"]
        trs.append(max(h - l, abs(h - pc), abs(l - pc)))
    out = [None] * period
    val = sum(trs[:period]) / period
    out.append(val)
    for i in range(period, len(trs)):
        val = (val * (period - 1) + trs[i]) / period
        out.append(val)
    return out


def analyze(symbol):
    candles = fetch_klines(symbol)
    closes = [c["close"] for c in candles]
    last = closes[-1]

    ema9, ema21 = ema(closes, 9)[-1], ema(closes, 21)[-1]
    r = rsi(closes)[-1]
    _, _, hist = macd(closes)
    a = atr(candles)[-1]

    score = 0
    if ema9 > ema21:
        score += 1
    else:
        score -= 1
    if r > 55:
        score += 1
    elif r < 45:
        score -= 1
    if hist[-1] > 0:
        score += 1
    elif hist[-1] < 0:
        score -= 1
    if hist[-1] > hist[-2] > 0 or (hist[-1] > 0 > hist[-2]):
        score += 1
    elif hist[-1] < hist[-2] < 0 or (hist[-1] < 0 < hist[-2]):
        score -= 1

    if score >= 2:
        signal = "BUY"
    elif score <= -2:
        signal = "SELL"
    else:
        signal = "NEUTRAL"

    atr_pct = a / last * 100
    sl = (last - 1.5 * a) if signal == "BUY" else (last + 1.5 * a)
    tp = (last + 3.0 * a) if signal == "BUY" else (last - 3.0 * a)

    return {
        "symbol": symbol,
        "price": last,
        "signal": signal,
        "score": score,
        "rsi": round(r, 1),
        "atr_pct": round(atr_pct, 2),
        "stop_loss": round(sl, 6),
        "take_profit": round(tp, 6),
    }


def run(symbols):
    print(f"{'SYMBOL':<12}{'PRICE':>12}{'SIGNAL':>10}{'SCORE':>7}{'RSI':>7}{'ATR%':>7}{'SL':>13}{'TP':>13}")
    print("-" * 82)
    for sym in symbols:
        try:
            d = analyze(sym)
        except Exception as e:
            print(f"{sym:<12} ERROR: {e}")
            continue
        print(
            f"{d['symbol']:<12}{d['price']:>12.4g}{d['signal']:>10}{d['score']:>7}"
            f"{d['rsi']:>7}{d['atr_pct']:>7}{d['stop_loss']:>13.6g}{d['take_profit']:>13.6g}"
        )


if __name__ == "__main__":
    symbols = sys.argv[1:] or DEFAULT_SYMBOLS
    run(symbols)
