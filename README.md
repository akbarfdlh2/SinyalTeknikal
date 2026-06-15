# 📈 Sinyal Teknikal

Scanner swing trading saham IDX berbasis analisis teknikal — dibangun dengan Streamlit.

> ⚠️ **Disclaimer:** Aplikasi ini hanya untuk tujuan edukasi dan riset. Bukan rekomendasi investasi. Selalu lakukan riset mandiri sebelum mengambil keputusan trading.

---

## Fitur

- **Scanner 50 Saham IDX** — memindai saham-saham likuid dari berbagai sektor secara otomatis
- **Indikator Teknikal** — SMA-20, SMA-50, RSI-14, MACD (12,26,9), ATR-14, dan Volume
- **Sistem Scoring Sinyal** — setiap saham diberi skor berdasarkan kekuatan konfluensi sinyal
- **5 Horizon Trading** — dari Overnight (1 hari) hingga 1 Bulan
- **Level ATR Otomatis** — Entry, TP1, TP2, TP3, dan Stop Loss dihitung dari ATR-14 menyesuaikan volatilitas tiap saham
- **Risk:Reward Ratio** — kalkulasi R:R otomatis (TP2 vs SL)
- **Chart Interaktif** — candlestick + MA, RSI, dan MACD dalam satu tampilan
- **Analisa Detail** — mendukung saham IDX, kripto, maupun ticker Yahoo Finance kustom
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

## Horizon Trading & Parameter ATR

| Horizon | Period Data | SL × ATR | TP1 × ATR | TP2 × ATR | TP3 × ATR |
|---|---|---|---|---|---|
| Overnight (1 Hari) | 3 bulan | 0.6× | 0.8× | 1.5× | 2.2× |
| 2–3 Hari | 6 bulan | 0.9× | 1.2× | 2.2× | 3.2× |
| 1 Minggu | 6 bulan | 1.2× | 1.8× | 3.0× | 4.5× |
| 2 Minggu | 1 tahun | 1.8× | 2.5× | 4.0× | 6.0× |
| 1 Bulan | 1 tahun | 2.5× | 3.0× | 5.5× | 8.0× |

---

## Instalasi & Menjalankan

### Prasyarat

- Python 3.9+
- pip

### Langkah-langkah

```bash
# 1. Clone repositori
git clone https://github.com/<username>/SinyalTeknikal.git
cd SinyalTeknikal

# 2. (Opsional) Buat virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# 3. Install dependensi
pip install -r requirements.txt

# 4. Jalankan aplikasi
streamlit run app.py
```

Aplikasi akan terbuka otomatis di browser pada `http://localhost:8501`.

---

## Dependensi

| Package | Kegunaan |
|---|---|
| `streamlit` | Framework UI web |
| `yfinance` | Pengambilan data harga saham dari Yahoo Finance |
| `pandas` | Manipulasi dan analisis data |
| `plotly` | Visualisasi chart interaktif |

---

## Struktur Proyek

```
SinyalTeknikal/
├── app.py              # Aplikasi utama (UI + logika)
├── requirements.txt    # Dependensi Python
├── .streamlit/
│   └── config.toml     # Konfigurasi tema Streamlit (dark mode)
└── README.md
```

---

## Cara Penggunaan

### Tab Scanner Saham IDX

1. Pilih **Horizon Trading** di sidebar sesuai durasi hold yang diinginkan
2. Atur **Skor Minimum** (default: 2 = Moderat ke atas)
3. Klik tombol **Scan Sekarang**
4. Hasil muncul sebagai kartu saham diurutkan dari sinyal terkuat
5. Pilih saham dari dropdown untuk melihat chart dan breakdown sinyal detail
6. Unduh hasil scan via tombol **Download CSV**

### Tab Analisa Detail

- Pilih mode aset: **Saham IDX**, **Crypto**, atau **Manual** (ticker kustom)
- Pilih rentang data (3 bulan – 2 tahun)
- Melihat chart lengkap, level TP/SL, dan breakdown sinyal secara individual

---

## Metodologi Scoring

Setiap saham dievaluasi berdasarkan 5 faktor:

| Faktor | Kondisi Bullish | Poin |
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

## Lisensi

MIT License — bebas digunakan untuk keperluan pribadi dan edukasi.
