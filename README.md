# 📈 Sinyal Teknikal

Scanner swing trading **Saham IDX & Crypto** berbasis analisis teknikal — dibangun dengan Streamlit.

**Live demo:** [sinyalteknikal-afk8jj3pczxfsvrf8whvxy.streamlit.app](https://sinyalteknikal-afk8jj3pczxfsvrf8whvxy.streamlit.app)

> ⚠️ **Disclaimer:** Aplikasi ini hanya untuk tujuan edukasi dan riset. Bukan rekomendasi investasi. Selalu lakukan riset mandiri sebelum mengambil keputusan trading.

---

## Fitur

- **Scanner 50 Saham IDX + 26 Koin Crypto** — memindai aset dari berbagai sektor secara otomatis
- **Indikator Teknikal** — SMA-20, SMA-50, RSI-14, MACD (12,26,9), ATR-14, dan Volume
- **Sistem Scoring Sinyal** — skor 0–7 berdasarkan kekuatan konfluensi sinyal
- **5 Horizon Trading** — dari Overnight (1 hari) hingga 1 Bulan
- **Level dari Swing Nyata** — TP dari resistance sebelumnya, SL dari support terdekat di chart; ATR sebagai fallback
- **Risk:Reward Ratio** — kalkulasi R:R otomatis (TP2 vs SL)
- **Chart Interaktif** — candlestick + MA, RSI, dan MACD dalam satu tampilan
- **Analisa Detail** — dukung saham IDX, kripto, maupun ticker Yahoo Finance kustom
- **Export CSV** — unduh hasil scan sebagai file CSV

---

## Tingkatan Sinyal

| Badge | Skor | Keterangan |
|---|---|---|
| 🔥 Kuat Sekali | ≥ 6 | Konfluensi sinyal sangat kuat |
| 🟢 Kuat | ≥ 4 | Sinyal bullish solid |
| 🟡 Moderat | ≥ 2 | Sinyal cukup, perlu konfirmasi |
| 🟠 Lemah | ≥ 0 | Sinyal lemah, hindari entry |
| 🔴 Skip | < 0 | Kondisi bearish / tidak ideal |

---

## Metodologi Scoring

Setiap aset dievaluasi dari 5 faktor:

| Faktor | Kondisi | Poin |
|---|---|---|
| SMA-20 | Harga > SMA-20 | +1 |
| SMA-50 | Harga > SMA-50 | +1 |
| RSI-14 | 45–65 (momentum optimal) | +2 |
| RSI-14 | < 35 (oversold/rebound) | +1 |
| RSI-14 | > 72 (overbought) | −1 |
| MACD | Golden cross baru | +2 |
| MACD | Di atas signal line | +1 |
| Volume | ≥ 1.5× rata-rata 20 hari | +1 |
| Volume | < 0.8× rata-rata 20 hari | −1 |

---

## Horizon Trading

| Horizon | Period Data | SL × ATR | TP1 × ATR | TP2 × ATR | TP3 × ATR |
|---|---|---|---|---|---|
| Overnight (1 Hari) | 3 bulan | 0.6× | 0.8× | 1.5× | 2.2× |
| 2–3 Hari | 6 bulan | 0.9× | 1.2× | 2.2× | 3.2× |
| 1 Minggu | 6 bulan | 1.2× | 1.8× | 3.0× | 4.5× |
| 2 Minggu | 1 tahun | 1.8× | 2.5× | 4.0× | 6.0× |
| 1 Bulan | 1 tahun | 2.5× | 3.0× | 5.5× | 8.0× |

Faktor ATR digunakan sebagai fallback jika tidak ditemukan swing high/low yang memadai dalam rentang lookback.

---

## Cara Penggunaan

### Tab Scanner

1. Pilih **tanggal beli** dan **tanggal jual** untuk menentukan horizon otomatis
2. Atur **Skor Minimum** (default: 2 = Moderat ke atas)
3. Pilih aset: **Saham IDX** atau **Crypto**
4. Klik **Scan Sekarang**
5. Hasil tampil sebagai kartu diurutkan dari sinyal terkuat
6. Pilih aset dari dropdown untuk melihat chart dan breakdown sinyal
7. Unduh hasil via **Download CSV**

### Tab Analisa Detail

- Pilih mode: **Saham IDX**, **Crypto**, atau **Manual** (ticker Yahoo Finance kustom)
- Pilih rentang data (3 bulan – 2 tahun)
- Lihat chart lengkap dengan level Entry/TP/SL dan breakdown sinyal individual

---

## Instalasi

```bash
git clone https://github.com/akbarfdlh2/SinyalTeknikal.git
cd SinyalTeknikal
pip install -r requirements.txt
streamlit run app.py
```

Buka `http://localhost:8501` di browser.

---

## Dependensi

| Package | Kegunaan |
|---|---|
| `streamlit` | Framework UI web |
| `yfinance` | Data harga dari Yahoo Finance |
| `pandas` | Manipulasi data |
| `plotly` | Chart interaktif |

---

## Struktur Proyek

```
SinyalTeknikal/
├── app.py              # Aplikasi utama (UI + logika)
├── requirements.txt    # Dependensi Python
└── README.md
```

---

## Lisensi

MIT License — bebas digunakan untuk keperluan pribadi dan edukasi.

---

Dibuat oleh [Akbar Fadilah](https://muhamadakbarfadilah.my.id/) · Founder & Co-Founder di [Afda Technology Solutions](https://afdatech.com/)
