"""
Sinyal Teknikal — Swing Trading Scanner IDX
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
from plotly.subplots import make_subplots

# ════════════════════════════════════════════════════
# PAGE CONFIG
# ════════════════════════════════════════════════════

st.set_page_config(
    page_title="Sinyal Teknikal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ════════════════════════════════════════════════════
# CSS
# ════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  --bg:   #080d1a;
  --c1:   #0f1629;
  --c2:   #141d36;
  --c3:   #1b2847;
  --ln:   rgba(255,255,255,0.07);
  --acc:  #6c63ff;
  --bull: #3ad6a6;
  --bear: #ff6b6b;
  --warn: #f4b740;
  --purp: #b47ef4;
  --t1:   #e8eaf6;
  --t2:   #8892b0;
  --t3:   #3d4f6b;
}

/* ── Streamlit chrome ── */
#MainMenu, footer, .stDeployButton,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stHeader"] { display:none !important }

/* ── Page ── */
.stApp, .stAppHeader { background: var(--bg) !important }
.main .block-container {
  padding: 1rem 1rem 3rem !important;
  max-width: 1440px !important;
  font-family: 'Inter', system-ui, sans-serif;
}

/* ── App header ── */
.app-hdr {
  background: linear-gradient(135deg, #0f1629 0%, #1a1040 55%, #0d1a2e 100%);
  border: 1px solid rgba(108,99,255,.25);
  border-radius: 20px;
  padding: 22px 28px;
  margin-bottom: 18px;
  position: relative;
  overflow: hidden;
}
.app-hdr::before {
  content:''; position:absolute; top:-60%; left:-10%;
  width:50%; height:220%;
  background: radial-gradient(circle, rgba(108,99,255,.12) 0%, transparent 65%);
  pointer-events:none;
}
.app-hdr h1 {
  font-size: clamp(1.4rem, 5vw, 2rem);
  font-weight: 800;
  background: linear-gradient(135deg, #fff 30%, #6c63ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 6px;
  line-height: 1.2;
}
.app-hdr p { color: var(--t2); font-size: .82rem; margin: 0; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--c1) !important;
  border-right: 1px solid var(--ln) !important;
}
[data-testid="stSidebar"] .block-container { padding: 1.5rem 1rem !important; }
.sidebar-hdr {
  font-size: .65rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: .1em; color: var(--acc); margin-bottom: 14px; padding-bottom: 10px;
  border-bottom: 1px solid var(--ln);
}
.param-box {
  background: var(--c2); border: 1px solid var(--ln); border-radius: 12px;
  padding: 12px 14px; margin-top: 10px; font-size: .78rem;
}
.param-box .row { display:flex; justify-content:space-between; padding: 4px 0; border-bottom: 1px solid rgba(255,255,255,.04); }
.param-box .row:last-child { border-bottom: none; }
.param-box .lbl { color: var(--t2); }
.param-box .val { color: var(--t1); font-weight: 600; font-family: monospace; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--c1);
  border-radius: 14px;
  padding: 5px;
  gap: 2px;
  border: 1px solid var(--ln);
}
.stTabs [data-baseweb="tab"] {
  border-radius: 10px !important;
  color: var(--t2) !important;
  font-weight: 500 !important;
  padding: 8px 20px !important;
  font-size: .88rem !important;
  transition: all .15s !important;
}
.stTabs [aria-selected="true"] {
  background: var(--acc) !important;
  color: #fff !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 18px !important; }

/* ── Buttons ── */
.stButton > button {
  background: linear-gradient(135deg, #6c63ff, #4834d4) !important;
  color: #fff !important; border: none !important;
  border-radius: 12px !important; padding: .65rem 1.5rem !important;
  font-weight: 600 !important; font-size: .92rem !important;
  width: 100% !important; transition: all .2s !important;
  box-shadow: 0 4px 15px rgba(108,99,255,.3) !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 28px rgba(108,99,255,.45) !important;
}
.stButton > button:active { transform: translateY(0) !important; }
[data-testid="stDownloadButton"] > button {
  background: transparent !important;
  border: 1px solid var(--ln) !important;
  color: var(--t2) !important;
  font-size: .82rem !important;
  padding: .4rem 1rem !important;
  box-shadow: none !important;
}
[data-testid="stDownloadButton"] > button:hover { border-color: rgba(108,99,255,.4) !important; color: var(--t1) !important; }

/* ── Metrics ── */
[data-testid="metric-container"] {
  background: var(--c1); border: 1px solid var(--ln);
  border-radius: 14px; padding: 14px 16px !important;
  transition: border-color .2s;
}
[data-testid="metric-container"]:hover { border-color: rgba(108,99,255,.3); }
[data-testid="stMetricLabel"] > div {
  font-size: .66rem !important; color: var(--t2) !important;
  text-transform: uppercase; letter-spacing: .07em; font-weight: 600;
}
[data-testid="stMetricValue"] > div { font-size: 1.15rem !important; font-weight: 700 !important; color: var(--t1) !important; }
[data-testid="stMetricDelta"] > div { font-size: .77rem !important; }

/* ── Inputs ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stTextInput"] > div > div {
  background: var(--c2) !important; border: 1px solid var(--ln) !important; border-radius: 10px !important;
}
.stSelectbox label, .stTextInput label, .stSlider label, .stRadio label { color: var(--t2) !important; font-size: .8rem !important; }
[data-testid="stSlider"] [role="slider"] { background: var(--acc) !important; border-color: var(--acc) !important; }
.stRadio div[role="radiogroup"] label { color: var(--t1) !important; font-size: .88rem !important; }

/* ── Alerts ── */
[data-testid="stNotification"], .stInfo  { background: rgba(108,99,255,.08) !important; border: 1px solid rgba(108,99,255,.2) !important; border-radius: 12px !important; }
.stSuccess { background: rgba(58,214,166,.08) !important; border: 1px solid rgba(58,214,166,.2) !important; border-radius: 12px !important; }
.stWarning { background: rgba(244,183,64,.08) !important; border: 1px solid rgba(244,183,64,.2) !important; border-radius: 12px !important; }
.stError   { background: rgba(255,107,107,.08) !important; border: 1px solid rgba(255,107,107,.2) !important; border-radius: 12px !important; }

/* ── Progress ── */
[data-testid="stProgressBar"] > div { background: rgba(255,255,255,.05) !important; border-radius: 10px !important; }
[data-testid="stProgressBar"] > div > div { background: linear-gradient(90deg, var(--acc), var(--bull)) !important; border-radius: 10px !important; }

/* ── Divider ── */
hr { border-color: var(--ln) !important; margin: .75rem 0 !important; }

/* ══════════════════════════════
   STOCK CARDS
══════════════════════════════ */
.stats-bar { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 16px; }
.chip {
  background: var(--c1); border: 1px solid var(--ln);
  border-radius: 10px; padding: 6px 14px;
  font-size: .76rem; color: var(--t2);
  display: flex; align-items: center; gap: 6px;
}
.chip b { color: var(--t1); }

.stock-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 12px;
}

.sc {
  background: var(--c1); border: 1px solid var(--ln);
  border-radius: 16px; padding: 16px;
  transition: all .2s ease;
}
.sc:hover {
  border-color: rgba(108,99,255,.4);
  background: var(--c2);
  box-shadow: 0 6px 28px rgba(0,0,0,.45);
  transform: translateY(-2px);
}

.sc-top {
  display: flex; justify-content: space-between;
  align-items: flex-start; margin-bottom: 14px;
}
.sc-ticker { font-size: 1.05rem; font-weight: 700; color: #fff; letter-spacing: -.01em; }
.sc-name   { font-size: .72rem; color: var(--t2); margin-top: 3px; }

/* badges */
.badge { font-size: .67rem; font-weight: 700; padding: 4px 10px; border-radius: 20px; white-space: nowrap; }
.b-fire  { background: rgba(255,107,107,.15); color: #ff9090; border: 1px solid rgba(255,107,107,.3); }
.b-kuat  { background: rgba(58,214,166,.15);  color: #3ad6a6; border: 1px solid rgba(58,214,166,.3); }
.b-mod   { background: rgba(244,183,64,.15);  color: #f4b740; border: 1px solid rgba(244,183,64,.3); }
.b-lemah { background: rgba(255,165,0,.1);    color: #ffa552; border: 1px solid rgba(255,165,0,.2); }
.b-skip  { background: rgba(255,107,107,.08); color: #ff6b6b; border: 1px solid rgba(255,107,107,.15); }

/* card level grid */
.lvg { display: grid; grid-template-columns: repeat(3,1fr); gap: 7px; }
.lv {
  background: rgba(255,255,255,.03); border-radius: 9px;
  padding: 8px 7px; text-align: center; border-left: 3px solid transparent;
}
.lv-e{border-left-color:#8892b0} .lv-sl{border-left-color:#ff6b6b}
.lv-1{border-left-color:#3ad6a6} .lv-2{border-left-color:#f4b740}
.lv-3{border-left-color:#b47ef4} .lv-rr{border-left-color:#6c63ff}

.ll { font-size: .58rem; text-transform: uppercase; letter-spacing: .06em; color: var(--t2); display: block; }
.lval { font-size: .82rem; font-weight: 700; color: var(--t1); display: block; margin-top: 2px; }
.lpct { font-size: .63rem; display: block; margin-top: 1px; }
.pos { color: var(--bull) } .neg { color: var(--bear) }

/* ══════════════════════════════
   DETAIL VIEW
══════════════════════════════ */
.lvl-strip { display: flex; gap: 8px; flex-wrap: wrap; margin: 12px 0 18px; }
.ls {
  flex: 1; min-width: 72px; background: var(--c1);
  border: 1px solid var(--ln); border-top: 3px solid transparent;
  border-radius: 12px; padding: 12px 10px; text-align: center;
}
.ls-e{border-top-color:#8892b0} .ls-sl{border-top-color:#ff6b6b}
.ls-1{border-top-color:#3ad6a6} .ls-2{border-top-color:#f4b740} .ls-3{border-top-color:#b47ef4}
.ls-lbl { font-size: .6rem; text-transform: uppercase; letter-spacing: .07em; color: var(--t2); }
.ls-val  { font-size: .92rem; font-weight: 700; color: var(--t1); margin: 4px 0 2px; display: block; }
.ls-pct  { font-size: .68rem; }

/* signal breakdown rows */
.sig {
  display: flex; align-items: center; gap: 10px;
  padding: 9px 14px; background: var(--c1);
  border: 1px solid var(--ln); border-radius: 10px; margin-bottom: 6px;
}
.sig-n { font-weight: 600; font-size: .83rem; color: var(--t1); white-space: nowrap; }
.sig-d { font-size: .77rem; color: var(--t2); }

/* section label */
.sec-lbl {
  font-size: .68rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: .09em; color: var(--t2); margin: 20px 0 10px;
}

/* ══════════════════════════════
   MOBILE
══════════════════════════════ */
@media (max-width: 640px) {
  .main .block-container { padding: .6rem .6rem 2rem !important; }
  .app-hdr { padding: 16px 18px; border-radius: 16px; }
  .stock-grid { grid-template-columns: 1fr; }
  .lvg { grid-template-columns: repeat(2,1fr); }
  .lvl-strip { gap: 5px; }
  .ls { padding: 10px 7px; min-width: 56px; }
  .ls-val { font-size: .82rem; }
  .stats-bar { gap: 6px; }
  .chip { font-size: .7rem; padding: 5px 10px; }
  [data-testid="stMetricValue"] > div { font-size: 1rem !important; }
}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════
# CONSTANTS
# ════════════════════════════════════════════════════

IDX_UNIVERSE = {
    "BBCA": "Bank BCA",          "BBRI": "Bank BRI",
    "BMRI": "Bank Mandiri",      "BBNI": "Bank BNI",
    "BBTN": "Bank BTN",          "BRIS": "Bank Syariah Indonesia",
    "TLKM": "Telkom",            "ASII": "Astra Intl",
    "UNVR": "Unilever",          "ICBP": "Indofood CBP",
    "INDF": "Indofood",          "KLBF": "Kalbe Farma",
    "MYOR": "Mayora Indah",      "GGRM": "Gudang Garam",
    "ANTM": "Aneka Tambang",     "PTBA": "Bukit Asam",
    "ADRO": "Adaro Energy",      "INCO": "Vale Indonesia",
    "ITMG": "Indo Tambangraya",  "HRUM": "Harum Energy",
    "MDKA": "Merdeka Copper",    "BRPT": "Barito Pacific",
    "MEDC": "Medco Energy",      "PGAS": "Perusahaan Gas",
    "SMGR": "Semen Indonesia",   "INTP": "Indocement",
    "CTRA": "Ciputra Dev",       "BSDE": "BSD City",
    "PWON": "Pakuwon",           "WIKA": "Wijaya Karya",
    "PTPP": "PP Persero",        "GOTO": "GoTo",
    "EMTK": "Elang Mahkota",     "MNCN": "Media Nusantara",
    "TBIG": "Tower Bersama",     "TOWR": "Sarana Menara",
    "EXCL": "XL Axiata",         "ISAT": "Indosat",
    "ERAA": "Erajaya",           "MAPI": "Map Aktif",
    "JPFA": "Japfa Comfeed",     "CPIN": "Charoen Pokphand",
    "AALI": "Astra Agro",        "AKRA": "AKR Corporindo",
    "MIKA": "Mitra Keluarga",    "TKIM": "Tjiwi Kimia",
    "INKP": "Indah Kiat",        "SIDO": "Sido Muncul",
    "ESSA": "Emas Mineral",      "ENRG": "Energi Mega",
}

HORIZONS = {
    "Overnight (1 Hari)": dict(atr_tp=[0.8, 1.5, 2.2], atr_sl=0.6, period="3mo"),
    "2–3 Hari":           dict(atr_tp=[1.2, 2.2, 3.2], atr_sl=0.9, period="6mo"),
    "1 Minggu":           dict(atr_tp=[1.8, 3.0, 4.5], atr_sl=1.2, period="6mo"),
    "2 Minggu":           dict(atr_tp=[2.5, 4.0, 6.0], atr_sl=1.8, period="1y"),
    "1 Bulan":            dict(atr_tp=[3.0, 5.5, 8.0], atr_sl=2.5, period="1y"),
}

LEVEL_STYLE = {
    "entry": ("#8892b0", "dot",  "Entry"),
    "sl":    ("#ff6b6b", "dash", "SL"),
    "tp1":   ("#3ad6a6", "dash", "TP1"),
    "tp2":   ("#f4b740", "dash", "TP2"),
    "tp3":   ("#b47ef4", "dash", "TP3"),
}


# ════════════════════════════════════════════════════
# DATA & INDICATORS
# ════════════════════════════════════════════════════

@st.cache_data(ttl=600, show_spinner=False)
def load_data(ticker: str, period: str) -> pd.DataFrame:
    df = yf.download(ticker, period=period, interval="1d",
                     auto_adjust=True, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df.dropna(subset=["Close"])


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    c = df["Close"]
    df["SMA20"] = c.rolling(20).mean()
    df["SMA50"] = c.rolling(50).mean()
    df["EMA12"] = c.ewm(span=12, adjust=False).mean()
    df["EMA26"] = c.ewm(span=26, adjust=False).mean()

    delta    = c.diff()
    avg_gain = delta.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
    avg_loss = (-delta.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
    df["RSI"] = 100 - 100 / (1 + avg_gain / avg_loss.replace(0, pd.NA))

    df["MACD"]        = df["EMA12"] - df["EMA26"]
    df["MACD_SIGNAL"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_HIST"]   = df["MACD"] - df["MACD_SIGNAL"]

    h, l, pc   = df["High"], df["Low"], c.shift(1)
    tr         = pd.concat([(h-l), (h-pc).abs(), (l-pc).abs()], axis=1).max(axis=1)
    df["ATR"]      = tr.ewm(span=14, adjust=False).mean()
    df["VOL_MA20"] = df["Volume"].rolling(20).mean()
    return df


def score_and_check(df: pd.DataFrame):
    last  = df.iloc[-1]
    prev  = df.iloc[-2] if len(df) >= 2 else last
    score = 0
    checks = []

    if last["Close"] > last["SMA20"]:
        score += 1
        checks.append(("SMA-20", "bullish", "Harga di atas SMA-20"))
    else:
        checks.append(("SMA-20", "bearish", "Harga di bawah SMA-20"))

    if not pd.isna(last["SMA50"]):
        if last["Close"] > last["SMA50"]:
            score += 1
            checks.append(("SMA-50", "bullish", "Harga di atas SMA-50"))
        else:
            checks.append(("SMA-50", "bearish", "Harga di bawah SMA-50"))

    rsi = last["RSI"]
    if not pd.isna(rsi):
        if 45 <= rsi <= 65:
            score += 2
            checks.append((f"RSI {rsi:.0f}", "bullish", "Momentum optimal (45–65)"))
        elif rsi < 35:
            score += 1
            checks.append((f"RSI {rsi:.0f}", "bullish", "Oversold — potensi rebound"))
        elif rsi > 72:
            score -= 1
            checks.append((f"RSI {rsi:.0f}", "bearish", "Overbought — rawan koreksi"))
        else:
            checks.append((f"RSI {rsi:.0f}", "neutral", "Zona netral"))

    macd_bull  = last["MACD"] > last["MACD_SIGNAL"]
    fresh_bull = macd_bull and (prev["MACD"] <= prev["MACD_SIGNAL"])
    if fresh_bull:
        score += 2
        checks.append(("MACD", "bullish", "Golden cross baru ⚡"))
    elif macd_bull:
        score += 1
        checks.append(("MACD", "bullish", "Di atas signal line"))
    else:
        checks.append(("MACD", "bearish", "Di bawah signal line"))

    vol_r = last["Volume"] / last["VOL_MA20"] if last["VOL_MA20"] > 0 else 1.0
    if vol_r >= 1.5:
        score += 1
        checks.append((f"Volume {vol_r:.1f}×", "bullish", "Lonjakan volume"))
    elif vol_r >= 0.8:
        checks.append((f"Volume {vol_r:.1f}×", "neutral", "Volume normal"))
    else:
        score -= 1
        checks.append((f"Volume {vol_r:.1f}×", "bearish", "Volume sepi"))

    return score, checks


def calc_levels(entry: float, atr: float, h: dict):
    tp1 = entry + atr * h["atr_tp"][0]
    tp2 = entry + atr * h["atr_tp"][1]
    tp3 = entry + atr * h["atr_tp"][2]
    sl  = entry - atr * h["atr_sl"]
    rr  = (tp2 - entry) / (entry - sl) if entry > sl else 0
    return tp1, tp2, tp3, sl, rr


# ════════════════════════════════════════════════════
# FORMATTING HELPERS
# ════════════════════════════════════════════════════

def rp(n: float) -> str:
    return f"{int(round(n)):,}".replace(",", ".")

def pct(new: float, base: float) -> str:
    v = (new - base) / base * 100
    return f"{v:+.1f}%"

def pct_cls(new: float, base: float) -> str:
    return "pos" if new >= base else "neg"

def tier(score: int) -> tuple[str, str]:
    if score >= 6: return "🔥 Kuat Sekali", "b-fire"
    if score >= 4: return "🟢 Kuat",        "b-kuat"
    if score >= 2: return "🟡 Moderat",     "b-mod"
    if score >= 0: return "🟠 Lemah",       "b-lemah"
    return "🔴 Skip", "b-skip"

DOT = {"bullish": "🟢", "bearish": "🔴", "neutral": "🟡"}


# ════════════════════════════════════════════════════
# HTML COMPONENTS
# ════════════════════════════════════════════════════

def html_cards(rows: list) -> str:
    cards = ['<div class="stock-grid">']
    for r in rows:
        lbl, bcls = tier(r["_score"])
        e = r["_entry"]
        cards.append(f"""
<div class="sc">
  <div class="sc-top">
    <div>
      <div class="sc-ticker">{r["Kode"]}</div>
      <div class="sc-name">{r["Nama"]}</div>
    </div>
    <span class="badge {bcls}">{lbl}</span>
  </div>
  <div class="lvg">
    <div class="lv lv-e">
      <span class="ll">Entry</span>
      <span class="lval">{rp(e)}</span>
      <span class="lpct" style="color:var(--t3)">±0%</span>
    </div>
    <div class="lv lv-sl">
      <span class="ll">Stop Loss</span>
      <span class="lval">{rp(r["_sl"])}</span>
      <span class="lpct neg">{pct(r["_sl"], e)}</span>
    </div>
    <div class="lv lv-rr">
      <span class="ll">R:R</span>
      <span class="lval">{r["_rr"]:.1f}×</span>
      <span class="lpct" style="color:var(--t3)">TP2/SL</span>
    </div>
    <div class="lv lv-1">
      <span class="ll">TP 1</span>
      <span class="lval">{rp(r["_tp1"])}</span>
      <span class="lpct pos">{pct(r["_tp1"], e)}</span>
    </div>
    <div class="lv lv-2">
      <span class="ll">TP 2</span>
      <span class="lval">{rp(r["_tp2"])}</span>
      <span class="lpct pos">{pct(r["_tp2"], e)}</span>
    </div>
    <div class="lv lv-3">
      <span class="ll">TP 3</span>
      <span class="lval">{rp(r["_tp3"])}</span>
      <span class="lpct pos">{pct(r["_tp3"], e)}</span>
    </div>
  </div>
</div>""")
    cards.append("</div>")
    return "\n".join(cards)


def html_stats(rows: list) -> str:
    total  = len(rows)
    kuat   = sum(1 for r in rows if r["_score"] >= 4)
    mod    = sum(1 for r in rows if 2 <= r["_score"] < 4)
    lemah  = sum(1 for r in rows if r["_score"] < 2)
    return f"""
<div class="stats-bar">
  <div class="chip">Total <b>{total}</b></div>
  <div class="chip">🔥🟢 Kuat <b>{kuat}</b></div>
  <div class="chip">🟡 Moderat <b>{mod}</b></div>
  <div class="chip">🟠 Lemah <b>{lemah}</b></div>
</div>"""


def html_level_strip(entry, sl, tp1, tp2, tp3) -> str:
    return f"""
<div class="lvl-strip">
  <div class="ls ls-e">
    <div class="ls-lbl">Entry</div>
    <span class="ls-val">{rp(entry)}</span>
    <span class="ls-pct" style="color:var(--t3)">±0%</span>
  </div>
  <div class="ls ls-sl">
    <div class="ls-lbl">Stop Loss</div>
    <span class="ls-val">{rp(sl)}</span>
    <span class="ls-pct neg">{pct(sl, entry)}</span>
  </div>
  <div class="ls ls-1">
    <div class="ls-lbl">TP 1</div>
    <span class="ls-val">{rp(tp1)}</span>
    <span class="ls-pct pos">{pct(tp1, entry)}</span>
  </div>
  <div class="ls ls-2">
    <div class="ls-lbl">TP 2</div>
    <span class="ls-val">{rp(tp2)}</span>
    <span class="ls-pct pos">{pct(tp2, entry)}</span>
  </div>
  <div class="ls ls-3">
    <div class="ls-lbl">TP 3</div>
    <span class="ls-val">{rp(tp3)}</span>
    <span class="ls-pct pos">{pct(tp3, entry)}</span>
  </div>
</div>"""


def html_signals(checks: list) -> str:
    rows = []
    for name, verdict, note in checks:
        dot = DOT[verdict]
        rows.append(f"""
<div class="sig">
  <span>{dot}</span>
  <span class="sig-n">{name}</span>
  <span class="sig-d">— {note}</span>
</div>""")
    return "\n".join(rows)


# ════════════════════════════════════════════════════
# CHART
# ════════════════════════════════════════════════════

def make_chart(df: pd.DataFrame, label: str, levels: dict = None):
    fig = make_subplots(
        rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.04,
        row_heights=[0.55, 0.22, 0.23],
        subplot_titles=(f"{label} — Candlestick + MA", "RSI-14", "MACD (12,26,9)"),
    )

    fig.add_trace(go.Candlestick(
        x=df.index, open=df["Open"], high=df["High"],
        low=df["Low"], close=df["Close"], name="Harga",
        increasing_line_color="#3ad6a6", decreasing_line_color="#ff6b6b",
        increasing_fillcolor="#3ad6a6", decreasing_fillcolor="#ff6b6b",
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=df.index, y=df["SMA20"], name="SMA-20",
        line=dict(color="#5b8def", width=1.4),
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=df.index, y=df["SMA50"], name="SMA-50",
        line=dict(color="#f4b740", width=1.4),
    ), row=1, col=1)

    if levels:
        for key, val in levels.items():
            if key not in LEVEL_STYLE:
                continue
            color, dash, lbl = LEVEL_STYLE[key]
            fig.add_hline(
                y=val, line_color=color, line_dash=dash, line_width=1.2,
                annotation_text=f" {lbl}  {rp(val)}",
                annotation_position="top left",
                annotation_font_color=color,
                annotation_font_size=11,
                row=1, col=1,
            )

    fig.add_trace(go.Scatter(
        x=df.index, y=df["RSI"], name="RSI",
        line=dict(color="#5b8def", width=1.4),
    ), row=2, col=1)
    fig.add_hline(y=70, line_color="#ff6b6b", line_dash="dot", line_width=1, row=2, col=1)
    fig.add_hline(y=50, line_color="#3d4f6b", line_dash="dot", line_width=1, row=2, col=1)
    fig.add_hline(y=30, line_color="#3ad6a6", line_dash="dot", line_width=1, row=2, col=1)

    hist_colors = ["#3ad6a6" if v >= 0 else "#ff6b6b" for v in df["MACD_HIST"].fillna(0)]
    fig.add_trace(go.Bar(
        x=df.index, y=df["MACD_HIST"], name="Histogram",
        marker_color=hist_colors, opacity=0.8,
    ), row=3, col=1)
    fig.add_trace(go.Scatter(
        x=df.index, y=df["MACD"], name="MACD",
        line=dict(color="#5b8def", width=1.4),
    ), row=3, col=1)
    fig.add_trace(go.Scatter(
        x=df.index, y=df["MACD_SIGNAL"], name="Signal",
        line=dict(color="#f4b740", width=1.4),
    ), row=3, col=1)

    fig.update_layout(
        template="plotly_dark",
        height=680,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_rangeslider_visible=False,
        legend=dict(orientation="h", y=1.07, font_size=11),
        paper_bgcolor="#0a0f1e",
        plot_bgcolor="#0a0f1e",
        font=dict(family="Inter, system-ui, sans-serif"),
    )
    for i in range(1, 4):
        fig.update_xaxes(gridcolor="#1b2847", showgrid=True, row=i, col=1)
        fig.update_yaxes(gridcolor="#1b2847", showgrid=True, row=i, col=1)
    fig.update_yaxes(range=[0, 100], row=2, col=1)
    return fig


# ════════════════════════════════════════════════════
# APP LAYOUT
# ════════════════════════════════════════════════════

# Header
st.markdown("""
<div class="app-hdr">
  <h1>📈 Sinyal Teknikal</h1>
  <p>Scanner swing trading IDX · Entry / TP1 / TP2 / TP3 / SL berbasis ATR ·
     Beli sore jual pagi hingga 1 bulan · ⚠️ Bukan rekomendasi investasi</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-hdr">⚙️ Pengaturan</div>', unsafe_allow_html=True)

    horizon_name = st.selectbox(
        "Horizon Trading",
        list(HORIZONS.keys()),
        help="Pilih durasi hold. Overnight = beli sore jual pagi besok.",
    )
    h_params = HORIZONS[horizon_name]

    min_score = st.slider(
        "Skor sinyal minimum", 0, 6, 2,
        help="0 = semua · 2 = moderat ke atas · 4 = kuat saja",
    )

    st.markdown(f"""
<div class="param-box">
  <div class="row"><span class="lbl">Period data</span><span class="val">{h_params['period']}</span></div>
  <div class="row"><span class="lbl">SL × ATR</span><span class="val">×{h_params['atr_sl']}</span></div>
  <div class="row"><span class="lbl">TP1 × ATR</span><span class="val">×{h_params['atr_tp'][0]}</span></div>
  <div class="row"><span class="lbl">TP2 × ATR</span><span class="val">×{h_params['atr_tp'][1]}</span></div>
  <div class="row"><span class="lbl">TP3 × ATR</span><span class="val">×{h_params['atr_tp'][2]}</span></div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption(
        "Level dihitung dari ATR-14 (Average True Range). "
        "Makin panjang horizon → TP/SL makin lebar mengikuti volatilitas saham."
    )


# ── Tabs ────────────────────────────────────────────
tab_scan, tab_detail = st.tabs(["🔍  Scanner Saham IDX", "📊  Analisa Detail"])


# ════════════════════════════════════════════════════
# TAB 1: SCANNER
# ════════════════════════════════════════════════════
with tab_scan:
    col_btn, col_txt = st.columns([1, 3])
    with col_btn:
        do_scan = st.button("🔄  Scan Sekarang", type="primary")
    with col_txt:
        st.caption(
            f"Memindai **{len(IDX_UNIVERSE)} saham IDX**. "
            "Pertama kali ±1–2 menit (unduh data). Berikutnya dari cache 10 menit."
        )

    if do_scan:
        rows = []
        bar  = st.progress(0, text="Memulai scan…")
        tickers = list(IDX_UNIVERSE.keys())

        for i, code in enumerate(tickers):
            bar.progress(
                (i + 1) / len(tickers),
                text=f"Menganalisa {code}… ({i+1}/{len(tickers)})",
            )
            try:
                df = load_data(f"{code}.JK", h_params["period"])
                if len(df) < 55:
                    continue
                df = add_indicators(df)
                score, checks = score_and_check(df)
                if score < min_score:
                    continue

                last  = df.iloc[-1]
                entry = float(last["Close"])
                atr   = float(last["ATR"])
                tp1, tp2, tp3, sl, rr = calc_levels(entry, atr, h_params)

                rows.append(dict(
                    Kode=code, Nama=IDX_UNIVERSE[code],
                    _score=score, _entry=entry,
                    _sl=sl, _tp1=tp1, _tp2=tp2, _tp3=tp3, _rr=rr,
                    _checks=checks,
                    # flat export cols
                    Signal=tier(score)[0],
                    Skor=score,
                    **{
                        "Entry (Rp)": rp(entry),
                        "SL":  f"{rp(sl)} ({pct(sl, entry)})",
                        "TP1": f"{rp(tp1)} ({pct(tp1, entry)})",
                        "TP2": f"{rp(tp2)} ({pct(tp2, entry)})",
                        "TP3": f"{rp(tp3)} ({pct(tp3, entry)})",
                        "R:R": f"{rr:.1f}×",
                    },
                ))
            except Exception:
                continue

        bar.empty()

        if not rows:
            st.warning("Tidak ada saham memenuhi filter. Coba turunkan skor minimum.")
        else:
            st.session_state["scan_rows"] = sorted(
                rows, key=lambda r: r["_score"], reverse=True
            )
            st.success(f"✅ Ditemukan **{len(rows)}** saham, diurutkan dari sinyal terkuat.")

    # ── Hasil scan ──────────────────────────────────
    if st.session_state.get("scan_rows"):
        rows = st.session_state["scan_rows"]

        st.markdown(html_stats(rows), unsafe_allow_html=True)
        st.markdown(html_cards(rows), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Download
        export_cols = ["Signal", "Skor", "Kode", "Nama",
                       "Entry (Rp)", "SL", "TP1", "TP2", "TP3", "R:R"]
        csv = pd.DataFrame(rows)[export_cols].to_csv(index=False)
        fname = horizon_name.split("(")[0].strip().replace(" ", "_").replace("–", "-")
        st.download_button("⬇️  Download hasil sebagai CSV", csv,
                           file_name=f"scan_{fname}.csv", mime="text/csv")

        # ── Detail per saham ────────────────────────
        st.markdown('<div class="sec-lbl">Detail Saham</div>', unsafe_allow_html=True)

        sel_code = st.selectbox(
            "Pilih saham untuk chart & breakdown sinyal",
            [r["Kode"] for r in rows],
            format_func=lambda c: f"{c}  —  {IDX_UNIVERSE.get(c, c)}",
        )
        sel = next(r for r in rows if r["Kode"] == sel_code)

        # Metrics row
        m1, m2, m3, m4, m5 = st.columns(5)
        lbl, _  = tier(sel["_score"])
        m1.metric("Signal",  lbl,                    f"Skor {sel['_score']}")
        m2.metric("Entry",   f"Rp {rp(sel['_entry'])}")
        m3.metric("SL",      f"Rp {rp(sel['_sl'])}",  pct(sel["_sl"],  sel["_entry"]))
        m4.metric("TP2",     f"Rp {rp(sel['_tp2'])}", pct(sel["_tp2"], sel["_entry"]))
        m5.metric("R:R",     f"{sel['_rr']:.1f}×",    "TP2 / SL")

        # Level strip
        st.markdown(
            html_level_strip(
                sel["_entry"], sel["_sl"],
                sel["_tp1"], sel["_tp2"], sel["_tp3"]
            ),
            unsafe_allow_html=True,
        )

        # Signal breakdown
        st.markdown('<div class="sec-lbl">Breakdown Sinyal</div>', unsafe_allow_html=True)
        st.markdown(html_signals(sel["_checks"]), unsafe_allow_html=True)

        # Chart
        st.markdown('<div class="sec-lbl">Chart</div>', unsafe_allow_html=True)
        try:
            df_sel = load_data(f"{sel_code}.JK", h_params["period"])
            df_sel = add_indicators(df_sel)
            st.plotly_chart(
                make_chart(df_sel, sel_code, dict(
                    entry=sel["_entry"], sl=sel["_sl"],
                    tp1=sel["_tp1"], tp2=sel["_tp2"], tp3=sel["_tp3"],
                )),
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"Gagal memuat chart: {e}")


# ════════════════════════════════════════════════════
# TAB 2: ANALISA DETAIL
# ════════════════════════════════════════════════════
with tab_detail:
    col_m, col_t, col_p = st.columns([1, 1, 1])

    with col_m:
        mode = st.radio("Aset", ["Saham IDX", "Crypto", "Manual"])

    with col_t:
        if mode == "Saham IDX":
            pick   = st.selectbox(
                "Saham",
                list(IDX_UNIVERSE.keys()),
                format_func=lambda k: f"{k}  —  {IDX_UNIVERSE[k]}",
            )
            ticker = f"{pick}.JK"
        elif mode == "Crypto":
            pick   = st.selectbox("Koin", ["BTC", "ETH", "SOL", "BNB", "XRP", "DOGE"])
            ticker = f"{pick}-USD"
        else:
            ticker = st.text_input("Ticker Yahoo Finance", "BBCA.JK").strip().upper()

    with col_p:
        period = st.selectbox("Rentang Data", ["3mo", "6mo", "1y", "2y"], index=2)

    try:
        df = load_data(ticker, period)
    except Exception as e:
        st.error(f"Gagal ambil data: {e}")
        st.stop()

    if df.empty or len(df) < 50:
        st.warning(f"Data `{ticker}` tidak cukup (butuh ≥50 hari).")
        st.stop()

    df    = add_indicators(df)
    score, checks = score_and_check(df)
    last  = df.iloc[-1]
    prev  = df.iloc[-2]
    entry = float(last["Close"])
    chg   = (entry - float(prev["Close"])) / float(prev["Close"]) * 100
    atr   = float(last["ATR"])
    tp1, tp2, tp3, sl, rr = calc_levels(entry, atr, h_params)
    lbl, _ = tier(score)

    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Harga Terakhir", f"Rp {rp(entry)}", f"{chg:+.2f}%")
    c2.metric("Signal",         lbl,                 f"Skor {score}")
    c3.metric("RSI-14",         f"{last['RSI']:.0f}")
    c4.metric("R:R (TP2/SL)",   f"{rr:.1f}×")

    # Horizon label
    st.caption(f"**Horizon aktif:** {horizon_name}")

    # Level strip
    st.markdown(html_level_strip(entry, sl, tp1, tp2, tp3), unsafe_allow_html=True)

    # Chart
    st.plotly_chart(
        make_chart(df, ticker, dict(entry=entry, sl=sl, tp1=tp1, tp2=tp2, tp3=tp3)),
        use_container_width=True,
    )

    # Signal breakdown
    st.markdown('<div class="sec-lbl">Breakdown Sinyal</div>', unsafe_allow_html=True)
    st.markdown(html_signals(checks), unsafe_allow_html=True)

    # Info
    st.info(
        f"**Entry** = harga penutupan terakhir (aproksimasi harga beli sore hari). "
        f"**Level** dihitung dari ATR-14 × faktor horizon: "
        f"SL ×{h_params['atr_sl']} · TP1 ×{h_params['atr_tp'][0]} · "
        f"TP2 ×{h_params['atr_tp'][1]} · TP3 ×{h_params['atr_tp'][2]}. "
        f"ATR adaptif — masing-masing saham punya lebar TP/SL berbeda sesuai volatilitas.",
        icon="ℹ️",
    )
