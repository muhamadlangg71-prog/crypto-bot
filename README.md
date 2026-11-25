# Crypto Signal Bot

Bot sinyal indikator untuk **crypto futures** (data publik Binance Futures API). Menghitung EMA 9/21, RSI 14, MACD, dan ATR untuk menghasilkan sinyal BUY / SELL / NEUTRAL beserta rekomendasi stop-loss & take-profit.

Hanya pakai Python standard library — **tidak perlu `pip install` apa pun**. Cocok dijalankan di PC, VPS, maupun Termux (Android).

## Cara pakai

```bash
# default: BTC, ETH, SOL, BNB, XRP — candle 15 menit
python3 bot.py

# pilih token futures sendiri (nama pasangan Binance):
python3 bot.py DOGEUSDT ADAUSDT LINKUSDT 1000PEPEUSDT
```

Windows: ganti `python3` menjadi `python`.

## Contoh output

```
SYMBOL          PRICE    SIGNAL  SCORE   RSI  ATR%     SL        TP
------------------------------------------------------------------
BTCUSDT        58510     SELL      -4   35.2  0.43  58891.8  57755.6
ETHUSDT          1639  NEUTRAL     -1   38.2  0.48   1650.4  1615.2
```

## Logika sinyal

Skor dihitung dari kombinasi indikator (rentang -5 s.d. +5):

| Komponen | Kontribusi |
|---|---|
| EMA 9 vs EMA 21 | momentum tren |
| RSI 14 | >55 bullish, <45 bearish |
| MACD histogram | arah momentum |
| Slope MACD | konfirmasi |

| Skor | Sinyal |
|---|---|
| >= +2 | BUY |
| <= -2 | SELL |
| lainnya | NEUTRAL |

SL/TP dihitung dari 1.5x / 3x ATR.

## Konfigurasi

Edit konstanta di bagian atas `bot.py`:

- `DEFAULT_SYMBOLS` — daftar token default
- `INTERVAL` — timeframe candle: `1m`, `5m`, `15m`, `1h`, `4h`, `1d`
- `LIMIT` — jumlah candle yang diambil

Jalankan otomatis tiap 15 menit (Termux/bash):

```bash
while true; do clear; python3 bot.py; sleep 900; done
```

## Catatan

- Bot ini hanya **alat bantu analisis**, bukan jaminan profit. Selalu pakai manajemen risiko, terutama di futures.
- API Binance Futures kadang diblokir ISP tertentu; kalau muncul error timeout, penyebabnya akses jaringan, bukan bot-nya.
