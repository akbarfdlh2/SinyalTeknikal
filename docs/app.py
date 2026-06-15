"""
Sinyal Teknikal — Crypto & Saham IDX
====================================
Web app lokal untuk analisa teknikal sederhana (SMA, EMA, RSI, MACD).
Data gratis dari Yahoo Finance via yfinance.

Cara pakai:
    pip install streamlit yfinance pandas plotly
    streamlit run app.py

CATATAN: Ini alat bantu baca tren, BUKAN rekomendasi beli/jual.
Indikator berbasis data masa lalu dan sering memberi sinyal palsu.
"""

import datetime as dt

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
from plotly.subplots import make_subplots

# ----------------------------------------------------------------------
# Indikator
# ----------------------------------------------------------------------
def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    c = df["Close"]
    df["SMA20"] = c.rolling(20).mean()
    df["SMA50"] = c.rolling(50).mean()
    df["EMA12"] = c.ewm(span=12, adjust=False).mean()
    df["EMA26"] = c.ewm(span=26, adjust=False).mean()

    # RSI-14 (Wilder)
    delta = c.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / 14, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / 14, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, pd.NA)
    df["RSI"] = 100 - 100 / (1 + rs)

    # MACD (12,26,9)
    df["MACD"] = df["EMA12"] - df["EMA26"]
    df["MACD_SIGNAL"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_HIST"] = df["MACD"] - df["MACD_SIGNAL"]
    return df


def build_signals(df: pd.DataFrame):
    """Kembalikan list cek + skor bias mekanis."""
    last = df.iloc[-1]
    checks = []

    above_sma20 = last["Close"] > last["SMA20"]
    checks.append(
        ("Harga vs SMA-20",
         "bullish" if above_sma20 else "bearish",
         "Harga di atas rata-rata 20 hari" if above_sma20 else "Harga di bawah rata-rata 20 hari")
    )

    if not pd.isna(last["SMA50"]):
        cross = last["SMA20"] > last["SMA50"]
        checks.append(
            ("SMA-20 vs SMA-50",
             "bullish" if cross else "bearish",
             "Rata-rata pendek di atas panjang" if cross else "Rata-rata pendek di bawah panjang")
        )

    rsi = last["RSI"]
    if not pd.isna(rsi):
        if rsi >= 70:
            checks.append((f"RSI-14 ({rsi:.0f})", "bearish", "Overbought (>70), rawan koreksi"))
        elif rsi <= 30:
            checks.append((f"RSI-14 ({rsi:.0f})", "bullish", "Oversold (<30), potensi rebound"))
        else:
            checks.append((f"RSI-14 ({rsi:.0f})", "neutral", "Zona netral"))

    macd_pos = last["MACD"] > last["MACD_SIGNAL"]
    checks.append(
        ("MACD",
         "bullish" if macd_pos else "bearish",
         "MACD di atas garis sinyal" if macd_pos else "MACD di bawah garis sinyal")
    )

    score = sum(1 if v == "bullish" else -1 if v == "bearish" else 0 for _, v, _ in checks)
    if score >= 2:
        bias = ("Cenderung Naik", "🟢")
    elif score <= -2:
        bias = ("Cenderung Turun", "🔴")
    else:
        bias = ("Netral", "🟡")
    return checks, bias, score


# ----------------------------------------------------------------------
# Data
# ----------------------------------------------------------------------
@st.cache_data(ttl=600, show_spinner=False)
def load_data(ticker: str, period: str) -> pd.DataFrame:
    df = yf.download(ticker, period=period, interval="1d",
                     auto_adjust=True, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df.dropna(subset=["Close"])


# ----------------------------------------------------------------------
# Chart
# ----------------------------------------------------------------------
DOT = {"bullish": "🟢", "bearish": "🔴", "neutral": "🟡"}


def make_chart(df: pd.DataFrame, label: str):
    fig = make_subplots(
        rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.04,
        row_heights=[0.55, 0.22, 0.23],
        subplot_titles=(f"{label} — Harga + SMA", "RSI-14", "MACD (12,26,9)"),
    )

    # harga + candle
    fig.add_trace(go.Candlestick(
        x=df.index, open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"],
        name="Harga", increasing_line_color="#3ad6a6", decreasing_line_color="#ff6b6b",
    ), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["SMA20"], name="SMA-20",
                             line=dict(color="#5b8def", width=1.3)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["SMA50"], name="SMA-50",
                             line=dict(color="#f4b740", width=1.3)), row=1, col=1)

    # RSI
    fig.add_trace(go.Scatter(x=df.index, y=df["RSI"], name="RSI",
                             line=dict(color="#5b8def", width=1.4)), row=2, col=1)
    fig.add_hline(y=70, line=dict(color="#ff6b6b", dash="dot"), row=2, col=1)
    fig.add_hline(y=30, line=dict(color="#3ad6a6", dash="dot"), row=2, col=1)

    # MACD
    colors = ["#3ad6a6" if v >= 0 else "#ff6b6b" for v in df["MACD_HIST"].fillna(0)]
    fig.add_trace(go.Bar(x=df.index, y=df["MACD_HIST"], name="Histogram",
                         marker_color=colors), row=3, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["MACD"], name="MACD",
                             line=dict(color="#5b8def", width=1.3)), row=3, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["MACD_SIGNAL"], name="Signal",
                             line=dict(color="#f4b740", width=1.3)), row=3, col=1)

    fig.update_layout(
        template="plotly_dark", height=720, margin=dict(l=10, r=10, t=40, b=10),
        xaxis_rangeslider_visible=False, legend=dict(orientation="h", y=1.06),
        paper_bgcolor="#0d1421", plot_bgcolor="#0d1421",
    )
    fig.update_yaxes(range=[0, 100], row=2, col=1)
    return fig


# ----------------------------------------------------------------------
# UI
# ----------------------------------------------------------------------
st.set_page_config(page_title="Sinyal Teknikal", page_icon="📈", layout="wide")

st.title("📈 Sinyal Teknikal — Crypto & Saham IDX")
st.caption("Alat bantu baca tren, bukan mesin profit. Indikator berbasis data masa lalu "
           "dan sering keliru. Keputusan & risikonya tetap di kamu.")

with st.sidebar:
    st.header("Pengaturan")
    mode = st.radio("Aset", ["Crypto", "Saham IDX", "Ticker manual"])

    if mode == "Crypto":
        pick = st.selectbox("Koin", ["BTC", "ETH", "SOL", "BNB", "XRP", "DOGE"])
        ticker = f"{pick}-USD"
    elif mode == "Saham IDX":
        pick = st.selectbox("Saham", ["BBCA", "BBRI", "BMRI", "TLKM", "ASII",
                                      "GOTO", "ANTM", "UNVR"])
        ticker = f"{pick}.JK"
    else:
        raw = st.text_input("Kode ticker Yahoo", "AAPL",
                            help="Contoh: AAPL, BTC-USD, BBCA.JK")
        ticker = raw.strip().upper()

    period = st.selectbox("Rentang", ["3mo", "6mo", "1y", "2y"], index=2)

# load + render
try:
    df = load_data(ticker, period)
except Exception as e:
    st.error(f"Gagal mengambil data: {e}")
    st.stop()

if df.empty or len(df) < 50:
    st.warning(f"Data untuk `{ticker}` tidak cukup (butuh ≥50 hari). "
               "Cek kode ticker atau perpanjang rentang.")
    st.stop()

df = add_indicators(df)
checks, (bias_label, bias_emoji), score = build_signals(df)

last_close = float(df["Close"].iloc[-1])
prev_close = float(df["Close"].iloc[-2])
chg = (last_close - prev_close) / prev_close * 100

c1, c2, c3 = st.columns(3)
c1.metric("Harga terakhir", f"{last_close:,.2f}", f"{chg:+.2f}%")
c2.metric("Bias indikator", f"{bias_emoji} {bias_label}", f"skor {score:+d}")
c3.metric("RSI-14", f"{df['RSI'].iloc[-1]:.0f}", help="30 oversold · 70 overbought")

st.plotly_chart(make_chart(df, ticker), use_container_width=True)

st.subheader("Ringkasan sinyal")
for name, verdict, note in checks:
    st.markdown(f"{DOT[verdict]} **{name}** — {note}")

st.info("Skor bias hanya menjumlahkan 4 indikator secara mekanis — bukan rekomendasi "
        "beli/jual. Di pasar sideways, indikator sering memberi sinyal palsu. "
        "Saham IDX dari Yahoo Finance biasanya delay ±15 menit.", icon="⚠️")
