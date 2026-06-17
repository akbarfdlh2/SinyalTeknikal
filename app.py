"""
Sinyal Teknikal — Swing Trading Scanner IDX
"""

import datetime as dt
import html
import math
import time

import pandas as pd
import plotly.graph_objects as go
import requests
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
    initial_sidebar_state="collapsed",
)

# ════════════════════════════════════════════════════
# CSS
# ════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  --bg:  #080d1a;
  --c1:  #0f1629;
  --c2:  #141d36;
  --ln:  rgba(255,255,255,0.07);
  --acc: #6c63ff;
  --bull:#3ad6a6;
  --bear:#ff6b6b;
  --t1:  #e8eaf6;
  --t2:  #8892b0;
  --t3:  #3d4f6b;
}

/* ── Streamlit chrome ── */
#MainMenu, footer, .stDeployButton,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stHeader"], [data-testid="stAppHeader"],
[data-testid="manage-app-button"], .stAppHeader,
.viewerBadge_container__r5tak, .viewerBadge_link__qRIco { display:none !important }

/* ── Page ── */
.stApp { background: var(--bg) !important }
section[data-testid="stMain"] { padding-top: 0 !important; }
.main { padding-top: 0 !important; }
.main .block-container {
  padding: 0 1rem 3rem !important;
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

/* ── Icons ── */
.ic { display:inline-block; vertical-align:middle; flex-shrink:0; }

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
.sc-code-row { display: flex; align-items: center; gap: 5px; }
.sc-ticker { font-size: 1.05rem; font-weight: 700; color: #fff; letter-spacing: -.01em; }
.sc-name   { font-size: .72rem; color: var(--t2); margin-top: 3px; }
.copy-code {
  appearance: none; background: transparent; border: none;
  color: #9aa5c4; border-radius: 6px; width: 27px; height: 27px; padding: 0;
  display: inline-flex; align-items: center; justify-content: center;
  cursor: pointer; transition: all .15s; position: relative;
}
.copy-code::before, .copy-code::after {
  content: ""; position: absolute; width: 10px; height: 12px;
  border: 1.8px solid currentColor; border-radius: 2px;
  box-sizing: border-box; transition: all .15s;
}
.copy-code::before { transform: translate(-2px, -2px); }
.copy-code::after { transform: translate(3px, 3px); background: var(--c1); }
.copy-code:hover { color: #fff; background: rgba(108,99,255,.16); }
.copy-code.copied { color: var(--bull); background: rgba(58,214,166,.1); }
.copy-code.copied::before {
  width: 11px; height: 6px; border-width: 0 0 2px 2px;
  border-radius: 0; transform: translate(0, -1px) rotate(-45deg);
}
.copy-code.copied::after { display: none; }
.copy-info {
  appearance: none; width: 100%; margin-top: 9px; padding: 7px 10px;
  background: rgba(108,99,255,.08); color: var(--t2);
  border: 1px solid rgba(108,99,255,.2); border-radius: 8px;
  display: flex; align-items: center; justify-content: center; gap: 7px;
  font-size: .68rem; font-weight: 600; cursor: pointer; transition: all .15s;
}
.copy-info:hover { color: #fff; background: rgba(108,99,255,.18); border-color: rgba(108,99,255,.4); }
.copy-info.copied { color: var(--bull); background: rgba(58,214,166,.08); border-color: rgba(58,214,166,.3); }
.copy-info-icon {
  position: relative; display: inline-block; width: 13px; height: 14px;
}
.copy-info-icon::before, .copy-info-icon::after {
  content: ""; position: absolute; width: 8px; height: 10px;
  border: 1.5px solid currentColor; border-radius: 2px; box-sizing: border-box;
}
.copy-info-icon::before { left: 0; top: 0; }
.copy-info-icon::after { left: 4px; top: 4px; background: var(--c1); }
.copy-info.copied .copy-info-icon::before {
  width: 10px; height: 5px; left: 1px; top: 3px;
  border-width: 0 0 2px 2px; border-radius: 0; transform: rotate(-45deg);
}
.copy-info.copied .copy-info-icon::after { display: none; }

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

.ll { font-size: .58rem; text-transform: uppercase; letter-spacing: .06em; color: var(--t2); display: flex; align-items: center; justify-content: center; gap: 3px; }
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
.ls-lbl { font-size: .6rem; text-transform: uppercase; letter-spacing: .07em; color: var(--t2); display: flex; align-items: center; justify-content: center; gap: 3px; }
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
   SETTINGS STRIP
══════════════════════════════ */
.settings-strip {
  background: var(--c1); border: 1px solid var(--ln);
  border-radius: 16px; padding: 16px 20px; margin-bottom: 16px;
}
.dur-badge {
  background: rgba(108,99,255,.12); border: 1px solid rgba(108,99,255,.25);
  border-radius: 12px; padding: 10px 16px; text-align: center;
  min-height: 58px; display: flex; flex-direction: column; justify-content: center;
}
.dur-days { font-size: 1.1rem; font-weight: 800; color: #fff; }
.dur-hor  { font-size: .72rem; color: var(--t2); margin-top: 3px; }
.dur-warn { font-size: .7rem; color: var(--bear); margin-top: 3px; }

/* ══════════════════════════════
   FOOTER
══════════════════════════════ */
.app-footer {
  margin-top: 40px;
  padding: 20px 0 10px;
  border-top: 1px solid var(--ln);
  text-align: center;
  color: var(--t2);
  font-size: .78rem;
}
.app-footer a {
  color: var(--acc);
  text-decoration: none;
  font-weight: 500;
}
.app-footer a:hover { color: #8b85ff; text-decoration: underline; }
.app-footer .creator { font-weight: 600; color: var(--t1); }

/* ══════════════════════════════
   PORTFOLIO
══════════════════════════════ */
.port-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
  gap: 12px;
  margin-top: 12px;
}
.pc {
  background: var(--c1); border: 1px solid var(--ln);
  border-radius: 16px; padding: 16px;
  transition: all .2s ease;
}
.pc:hover {
  border-color: rgba(108,99,255,.4);
  background: var(--c2);
  box-shadow: 0 6px 28px rgba(0,0,0,.45);
}
.pc-top {
  display: flex; justify-content: space-between;
  align-items: flex-start; margin-bottom: 10px;
}
.pnl-pos { color: var(--bull); }
.pnl-neg { color: var(--bear); }
.pnl-big { font-size: 1.5rem; font-weight: 800; display: block; margin-top: 4px; }
.rec-badge {
  font-size: .68rem; font-weight: 700;
  padding: 4px 11px; border-radius: 20px; white-space: nowrap;
}
.rec-cut  { background: rgba(255,107,107,.15); color: #ff6b6b; border: 1px solid rgba(255,107,107,.3); }
.rec-warn { background: rgba(244,183,64,.15);  color: #f4b740; border: 1px solid rgba(244,183,64,.3); }
.rec-hold { background: rgba(136,146,176,.15); color: #8892b0; border: 1px solid rgba(136,146,176,.3); }
.rec-add  { background: rgba(58,214,166,.15);  color: #3ad6a6; border: 1px solid rgba(58,214,166,.3); }
.rec-tp   { background: rgba(108,99,255,.15);  color: #9b94ff; border: 1px solid rgba(108,99,255,.3); }
.pc-row {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 6px; margin-top: 8px;
}
.pc-cell {
  background: rgba(255,255,255,.03); border-radius: 9px;
  padding: 8px 10px; text-align: center;
}
.pc-lbl { font-size: .6rem; text-transform: uppercase; letter-spacing: .06em; color: var(--t2); }
.pc-val { font-size: .85rem; font-weight: 700; color: var(--t1); display: block; margin-top: 2px; }
.pc-err { font-size: .76rem; color: var(--bear); margin-top: 8px; }

/* ══════════════════════════════
   MOBILE
══════════════════════════════ */
@media (max-width: 640px) {
  .main .block-container { padding: .5rem .5rem 2.5rem !important; }
  .app-hdr { padding: 14px 16px; border-radius: 14px; }
  .app-hdr p { font-size: .74rem; }
  .stock-grid { grid-template-columns: 1fr; }
  .lvg { grid-template-columns: repeat(2,1fr); }
  .lvl-strip { gap: 5px; flex-wrap: wrap; }
  .ls { padding: 10px 7px; min-width: 62px; flex: 1 1 62px; }
  .ls-val { font-size: .82rem; }
  .stats-bar { gap: 6px; flex-wrap: wrap; }
  .chip { font-size: .7rem; padding: 5px 10px; }
  .settings-strip { padding: 12px 14px; }
  .dur-badge { padding: 8px 12px; min-height: unset; }

  /* Metric cards: smaller */
  [data-testid="stMetricValue"] > div { font-size: .92rem !important; }
  [data-testid="stMetricLabel"] > div { font-size: .58rem !important; }
  [data-testid="metric-container"] { padding: 10px 10px !important; }

  /* Force Streamlit columns to wrap 2-per-row */
  [data-testid="stHorizontalBlock"] {
    flex-wrap: wrap !important;
    gap: 0.4rem !important;
  }
  [data-testid="stColumn"] {
    min-width: calc(50% - 0.2rem) !important;
    flex: 1 1 calc(50% - 0.2rem) !important;
    box-sizing: border-box !important;
  }

  /* Tabs: scrollable, no wrap */
  .stTabs [data-baseweb="tab-list"] {
    overflow-x: auto !important;
    flex-wrap: nowrap !important;
    scrollbar-width: none;
    -webkit-overflow-scrolling: touch;
  }
  .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar { display: none; }
  .stTabs [data-baseweb="tab"] {
    padding: 7px 14px !important;
    font-size: .82rem !important;
    white-space: nowrap !important;
  }
}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════
# CONSTANTS
# ════════════════════════════════════════════════════

IDX_FALLBACK_UNIVERSE = {
    "BBCA": "Bank BCA",         "BBRI": "Bank BRI",
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

US_FALLBACK_UNIVERSE = {
    "AAPL": "Apple",             "MSFT": "Microsoft",
    "NVDA": "NVIDIA",            "AMZN": "Amazon",
    "GOOGL": "Alphabet",         "META": "Meta Platforms",
    "TSLA": "Tesla",             "AVGO": "Broadcom",
    "AMD": "Advanced Micro Devices",
    "NFLX": "Netflix",           "PLTR": "Palantir",
    "INTC": "Intel",             "QCOM": "Qualcomm",
    "MU": "Micron Technology",   "JPM": "JPMorgan Chase",
    "BAC": "Bank of America",    "V": "Visa",
    "MA": "Mastercard",          "WMT": "Walmart",
    "COST": "Costco",            "KO": "Coca-Cola",
    "DIS": "Walt Disney",        "UBER": "Uber",
    "CRM": "Salesforce",         "ORCL": "Oracle",
}

CRYPTO_UNIVERSE = {
    "BTC-USD":  "Bitcoin",          "ETH-USD":  "Ethereum",
    "BNB-USD":  "BNB",              "SOL-USD":  "Solana",
    "XRP-USD":  "XRP",              "ADA-USD":  "Cardano",
    "AVAX-USD": "Avalanche",        "DOGE-USD": "Dogecoin",
    "DOT-USD":  "Polkadot",         "LINK-USD": "Chainlink",
    "MATIC-USD":"Polygon",          "UNI-USD":  "Uniswap",
    "LTC-USD":  "Litecoin",         "BCH-USD":  "Bitcoin Cash",
    "ATOM-USD": "Cosmos",           "NEAR-USD": "NEAR Protocol",
    "APT-USD":  "Aptos",            "ARB-USD":  "Arbitrum",
    "OP-USD":   "Optimism",         "SUI-USD":  "Sui",
    "INJ-USD":  "Injective",        "FIL-USD":  "Filecoin",
    "ICP-USD":  "Internet Computer","PEPE-USD": "Pepe",
    "WIF-USD":  "dogwifhat",        "TON-USD":  "Toncoin",
}

INDODAX_FALLBACK_UNIVERSE = {
    "BTCIDR":  "Bitcoin",          "ETHIDR":  "Ethereum",
    "BNBIDR":  "BNB",              "SOLIDR":  "Solana",
    "XRPIDR":  "XRP",              "ADAIDR":  "Cardano",
    "AVAXIDR": "Avalanche",        "DOGEIDR": "Dogecoin",
    "DOTIDR":  "Polkadot",         "LINKIDR": "Chainlink",
    "POLIDR":  "Polygon",          "UNIIDR":  "Uniswap",
    "LTCIDR":  "Litecoin",         "BCHIDR":  "Bitcoin Cash",
    "ATOMIDR": "Cosmos",           "NEARIDR": "NEAR Protocol",
    "TRXIDR":  "TRON",             "ARBIDR":  "Arbitrum",
    "OPIDR":   "Optimism",         "SUIIDR":  "Sui",
    "INJIDR":  "Injective",        "FILIDR":  "Filecoin",
    "ICPIDR":  "Internet Computer","PEPEIDR": "Pepe",
    "WIFIDR":  "dogwifhat",        "TONIDR":  "Toncoin",
}

INDODAX_FALLBACK_PRICE_STEPS = {
    "BTCIDR": 1000.0,
    "ETHIDR": 1000.0,
    "LTCIDR": 1000.0,
    "BCHIDR": 1000.0,
    "PEPEIDR": 0.000001,
}

INDODAX_SCAN_DELAY_SECONDS = 0.4

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

@st.cache_data(ttl=3600, show_spinner=False)
def load_idx_markets() -> dict:
    try:
        query = yf.EquityQuery(
            "and",
            [
                yf.EquityQuery("eq", ["region", "id"]),
                yf.EquityQuery("gt", ["dayvolume", 0]),
            ],
        )
        markets = []
        offset = 0
        page_size = 250

        while True:
            result = yf.screen(
                query,
                offset=offset,
                size=page_size,
                sortField="dayvolume",
                sortAsc=False,
            )
            quotes = result.get("quotes", [])
            for quote in quotes:
                symbol = quote.get("symbol", "")
                if not symbol.endswith(".JK") or quote.get("quoteType") != "EQUITY":
                    continue
                code = symbol.removesuffix(".JK")
                name = quote.get("shortName") or quote.get("longName") or code
                markets.append((code, name))

            offset += len(quotes)
            if not quotes or offset >= result.get("total", 0):
                break

        return dict(markets) or IDX_FALLBACK_UNIVERSE
    except Exception:
        return IDX_FALLBACK_UNIVERSE


@st.cache_data(ttl=3600, show_spinner=False)
def load_us_markets() -> dict:
    try:
        query = yf.EquityQuery(
            "and",
            [
                yf.EquityQuery("eq", ["region", "us"]),
                yf.EquityQuery(
                    "is-in",
                    ["exchange", "NMS", "NGM", "NCM", "NYQ", "ASE"],
                ),
                yf.EquityQuery("gt", ["dayvolume", 0]),
                yf.EquityQuery("gte", ["intradaymarketcap", 1_000_000_000]),
            ],
        )
        markets = []
        page_size = 250
        max_results = 1000

        for offset in range(0, max_results, page_size):
            result = yf.screen(
                query,
                offset=offset,
                size=page_size,
                sortField="dayvolume",
                sortAsc=False,
            )
            quotes = result.get("quotes", [])
            for quote in quotes:
                symbol = quote.get("symbol", "")
                if not symbol or quote.get("quoteType") != "EQUITY":
                    continue
                name = quote.get("shortName") or quote.get("longName") or symbol
                markets.append((symbol, name))

            if not quotes or offset + len(quotes) >= result.get("total", 0):
                break

        return dict(markets) or US_FALLBACK_UNIVERSE
    except Exception:
        return US_FALLBACK_UNIVERSE


@st.cache_data(ttl=3600, show_spinner=False)
def load_indodax_markets() -> tuple[dict, dict]:
    try:
        pairs_response = requests.get("https://indodax.com/api/pairs", timeout=20)
        pairs_response.raise_for_status()
        pairs = pairs_response.json()

        summaries_response = requests.get("https://indodax.com/api/summaries", timeout=20)
        summaries_response.raise_for_status()
        summaries = summaries_response.json().get("tickers", {})

        markets = []
        price_steps = {}
        for pair in pairs:
            symbol = pair.get("symbol", "")
            if (
                pair.get("base_currency") != "idr"
                or pair.get("is_market_suspended")
                or not symbol
            ):
                continue

            ticker = summaries.get(pair.get("ticker_id", ""), {})
            name = ticker.get("name") or pair.get("description") or symbol
            if pair.get("is_maintenance"):
                name = f"{name} (Maintenance)"
            volume_idr = pd.to_numeric(ticker.get("vol_idr", 0), errors="coerce")
            volume_idr = 0.0 if pd.isna(volume_idr) else float(volume_idr)
            markets.append((symbol, name, volume_idr))

            price_step = pd.to_numeric(pair.get("price_precision", 1), errors="coerce")
            if not pd.isna(price_step) and float(price_step) > 0:
                price_steps[symbol] = float(price_step)

        markets.sort(key=lambda item: item[2], reverse=True)
        return (
            {symbol: name for symbol, name, _ in markets},
            price_steps,
        )
    except (requests.RequestException, AttributeError, TypeError, ValueError):
        return INDODAX_FALLBACK_UNIVERSE, INDODAX_FALLBACK_PRICE_STEPS


@st.cache_data(ttl=600, show_spinner=False)
def load_data(ticker: str, period: str, source: str = "yahoo") -> pd.DataFrame:
    if source == "indodax":
        period_days = {"3mo": 100, "6mo": 190, "1y": 370, "2y": 740}
        to_ts = int(time.time())
        response = requests.get(
            "https://indodax.com/tradingview/history_v2",
            params={
                "from": to_ts - period_days.get(period, 370) * 86400,
                "to": to_ts,
                "tf": "1D",
                "symbol": ticker,
            },
            timeout=20,
        )
        response.raise_for_status()
        records = response.json()
        if not isinstance(records, list):
            raise ValueError("Respons data Indodax tidak valid")

        columns = ["Open", "High", "Low", "Close", "Volume"]
        if not records:
            return pd.DataFrame(columns=columns)

        df = pd.DataFrame.from_records(records)
        if "Time" not in df or any(col not in df for col in columns):
            raise ValueError("Data OHLC Indodax tidak lengkap")

        df.index = pd.to_datetime(df.pop("Time"), unit="s", utc=True).dt.tz_convert(None)
        df.index.name = "Date"
        df[columns] = df[columns].apply(pd.to_numeric, errors="coerce")
        return (
            df[columns]
            .sort_index()
            .loc[lambda frame: ~frame.index.duplicated(keep="last")]
            .dropna(subset=["Close"])
        )

    df = yf.download(ticker, period=period, interval="1d",
                     auto_adjust=True, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df.dropna(subset=["Close"])


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    c = df["Close"]
    h, l = df["High"], df["Low"]

    df["SMA20"] = c.rolling(20).mean()
    df["SMA50"] = c.rolling(50).mean()
    df["EMA9"]  = c.ewm(span=9,  adjust=False).mean()
    df["EMA12"] = c.ewm(span=12, adjust=False).mean()
    df["EMA26"] = c.ewm(span=26, adjust=False).mean()

    # RSI-14
    delta    = c.diff()
    avg_gain = delta.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
    avg_loss = (-delta.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
    avg_loss = avg_loss.where(avg_loss != 0, float("nan"))
    df["RSI"] = 100 - 100 / (1 + avg_gain / avg_loss)

    # MACD
    df["MACD"]        = df["EMA12"] - df["EMA26"]
    df["MACD_SIGNAL"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_HIST"]   = df["MACD"] - df["MACD_SIGNAL"]

    # ATR & Volume MA
    pc = c.shift(1)
    tr = pd.concat([(h-l), (h-pc).abs(), (l-pc).abs()], axis=1).max(axis=1)
    df["ATR"]      = tr.ewm(span=14, adjust=False).mean()
    df["VOL_MA20"] = df["Volume"].rolling(20).mean()

    # Bollinger Bands (20, ±2σ)
    std20        = c.rolling(20).std()
    df["BB_UP"]  = df["SMA20"] + 2 * std20
    df["BB_LOW"] = df["SMA20"] - 2 * std20
    band_width   = df["BB_UP"] - df["BB_LOW"]
    band_width   = band_width.where(band_width != 0, float("nan"))
    df["BB_PCT"] = (c - df["BB_LOW"]) / band_width  # 0 = lower band, 1 = upper band

    # Stochastic %K/%D (14,3)
    low14  = l.rolling(14).min()
    high14 = h.rolling(14).max()
    stoch_range = high14 - low14
    stoch_range = stoch_range.where(stoch_range != 0, float("nan"))
    df["STOCH_K"] = 100 * (c - low14) / stoch_range
    df["STOCH_D"] = df["STOCH_K"].rolling(3).mean()

    # ADX (14) — kekuatan & arah tren
    up_move  = h.diff()
    dn_move  = -l.diff()
    plus_dm  = up_move.where((up_move > dn_move) & (up_move > 0), 0.0)
    minus_dm = dn_move.where((dn_move > up_move) & (dn_move > 0), 0.0)
    atr14    = tr.ewm(span=14, adjust=False).mean()
    atr14    = atr14.where(atr14 != 0, float("nan"))
    df["PLUS_DI"]  = 100 * plus_dm.ewm(span=14, adjust=False).mean() / atr14
    df["MINUS_DI"] = 100 * minus_dm.ewm(span=14, adjust=False).mean() / atr14
    di_sum = df["PLUS_DI"] + df["MINUS_DI"]
    di_sum = di_sum.where(di_sum != 0, float("nan"))
    dx     = 100 * (df["PLUS_DI"] - df["MINUS_DI"]).abs() / di_sum
    dx     = pd.to_numeric(dx, errors="coerce")
    df["ADX"] = dx.ewm(span=14, adjust=False).mean()

    return df


def score_and_check(df: pd.DataFrame):
    last  = df.iloc[-1]
    prev  = df.iloc[-2] if len(df) >= 2 else last
    score = 0
    checks = []

    # ── 1. Trend MA ────────────────────────────────
    above20 = last["Close"] > last["SMA20"]
    above50 = (not pd.isna(last["SMA50"])) and last["Close"] > last["SMA50"]
    if above20 and above50:
        score += 2
        checks.append(("Trend MA", "bullish", "Di atas SMA-20 & SMA-50 — uptrend"))
    elif above20:
        score += 1
        checks.append(("SMA-20", "bullish", "Di atas SMA-20 tapi masih di bawah SMA-50"))
    elif above50:
        checks.append(("SMA-50", "neutral", "Di atas SMA-50 tapi di bawah SMA-20"))
    else:
        score -= 1
        checks.append(("Trend MA", "bearish", "Di bawah SMA-20 & SMA-50 — downtrend ⚠️"))

    # ── 2. EMA-9 momentum pendek ───────────────────
    if not pd.isna(last["EMA9"]) and not pd.isna(prev["EMA9"]):
        if last["Close"] > last["EMA9"] and last["EMA9"] > prev["EMA9"]:
            score += 1
            checks.append(("EMA-9", "bullish", "Harga di atas EMA-9 & EMA naik"))
        elif last["Close"] < last["EMA9"]:
            checks.append(("EMA-9", "bearish", "Harga di bawah EMA-9"))
        else:
            checks.append(("EMA-9", "neutral", "EMA-9 mendatar"))

    # ── 3. RSI-14 ──────────────────────────────────
    rsi = last["RSI"]
    if not pd.isna(rsi):
        if 50 <= rsi <= 65:
            score += 2
            checks.append((f"RSI {rsi:.0f}", "bullish", "Momentum optimal (50–65)"))
        elif 40 <= rsi < 50:
            score += 1
            checks.append((f"RSI {rsi:.0f}", "bullish", "Momentum membaik"))
        elif rsi < 30:
            score += 1
            checks.append((f"RSI {rsi:.0f}", "bullish", "Oversold — potensi rebound kuat"))
        elif 30 <= rsi < 40:
            checks.append((f"RSI {rsi:.0f}", "neutral", "Zona lemah — waspada"))
        elif rsi > 72:
            score -= 1
            checks.append((f"RSI {rsi:.0f}", "bearish", "Overbought — rawan koreksi"))
        else:
            checks.append((f"RSI {rsi:.0f}", "neutral", "Zona netral"))

    # ── 4. MACD ────────────────────────────────────
    macd_bull  = last["MACD"] > last["MACD_SIGNAL"]
    fresh_bull = macd_bull and (prev["MACD"] <= prev["MACD_SIGNAL"])
    above_zero = last["MACD"] > 0
    if fresh_bull:
        score += 2
        checks.append(("MACD", "bullish", "Golden cross baru ⚡"))
    elif macd_bull and above_zero:
        score += 1
        checks.append(("MACD", "bullish", "Di atas signal & zero line"))
    elif macd_bull:
        score += 1
        checks.append(("MACD", "bullish", "Di atas signal line"))
    elif not above_zero:
        score -= 1
        checks.append(("MACD", "bearish", "Di bawah signal & zero line ⚠️"))
    else:
        checks.append(("MACD", "bearish", "Di bawah signal line"))

    # ── 5. Bollinger Bands ─────────────────────────
    bb_pct = last["BB_PCT"]
    if not pd.isna(bb_pct):
        if bb_pct <= 0.15:
            score += 2
            checks.append((f"BB {bb_pct:.0%}", "bullish", "Menyentuh lower band — setup beli potensial 🎯"))
        elif bb_pct <= 0.30:
            score += 1
            checks.append((f"BB {bb_pct:.0%}", "bullish", "Dekat lower band — harga murah relatif"))
        elif bb_pct >= 0.85:
            score -= 1
            checks.append((f"BB {bb_pct:.0%}", "bearish", "Menyentuh upper band — rawan koreksi"))
        else:
            checks.append((f"BB {bb_pct:.0%}", "neutral", "Posisi tengah Bollinger Band"))

    # ── 6. Stochastic (14,3) ───────────────────────
    sk = last["STOCH_K"]
    sd = last["STOCH_D"]
    pk = prev["STOCH_K"]
    pd_ = prev["STOCH_D"]
    if not pd.isna(sk) and not pd.isna(sd) and not pd.isna(pk) and not pd.isna(pd_):
        cross_up = (sk > sd) and (pk <= pd_)
        if sk < 20 and cross_up:
            score += 2
            checks.append((f"Stoch {sk:.0f}", "bullish", "Oversold + golden cross ⚡"))
        elif sk < 20:
            score += 1
            checks.append((f"Stoch {sk:.0f}", "bullish", "Oversold — tunggu konfirmasi crossover"))
        elif sk > 80:
            score -= 1
            checks.append((f"Stoch {sk:.0f}", "bearish", "Overbought — hati-hati"))
        elif sk > sd and pk <= pd_:
            score += 1
            checks.append((f"Stoch {sk:.0f}", "bullish", "Cross up di zona normal"))
        else:
            checks.append((f"Stoch {sk:.0f}", "neutral", "Zona normal"))

    # ── 7. ADX kekuatan tren ───────────────────────
    adx = last["ADX"]
    pdi = last["PLUS_DI"]
    mdi = last["MINUS_DI"]
    if not pd.isna(adx) and not pd.isna(pdi) and not pd.isna(mdi):
        if adx >= 25 and pdi > mdi:
            score += 1
            checks.append((f"ADX {adx:.0f}", "bullish", "Tren naik kuat (+DI > −DI)"))
        elif adx >= 25 and pdi < mdi:
            score -= 2
            checks.append((f"ADX {adx:.0f}", "bearish", "Tren TURUN kuat — sebaiknya hindari ⚠️"))
        elif adx < 20:
            checks.append((f"ADX {adx:.0f}", "neutral", "Sideways / lemah — selektif"))
        else:
            dir_lbl = "naik" if pdi > mdi else "turun"
            checks.append((f"ADX {adx:.0f}", "neutral", f"Tren sedang {dir_lbl}"))

    # ── 8. Volume ──────────────────────────────────
    vol_r = last["Volume"] / last["VOL_MA20"] if last["VOL_MA20"] > 0 else 1.0
    if vol_r >= 1.5:
        score += 1
        checks.append((f"Volume {vol_r:.1f}×", "bullish", "Lonjakan volume — konfirmasi kuat"))
    elif vol_r >= 0.8:
        checks.append((f"Volume {vol_r:.1f}×", "neutral", "Volume normal"))
    else:
        score -= 1
        checks.append((f"Volume {vol_r:.1f}×", "bearish", "Volume sepi — sinyal kurang valid"))

    return score, checks


def find_key_levels(
    df: pd.DataFrame,
    entry: float,
    atr: float,
    h: dict,
    cur: str = "IDR",
    price_step: float = None,
):
    def _rnd(n: float, direction: str) -> float:
        if price_step:
            units = (
                math.ceil(n / price_step)
                if direction == "up"
                else math.floor(n / price_step)
            )
            value = units * price_step
            decimals = (
                max(0, int(round(-math.log10(price_step))))
                if price_step < 1
                else 0
            )
            return float(round(value, decimals))
        if cur == "IDR":
            return float(math.ceil(n) if direction == "up" else math.floor(n))
        return n

    sw = 4
    n  = len(df)
    lookback = {"3mo": 50, "6mo": 80, "1y": 130, "2y": 200}.get(h["period"], 60)
    start = max(sw, n - lookback)

    tp_min = max(entry * 0.003, atr * 0.4)
    tp_max = atr * h["atr_tp"][2] * 1.4

    # ── Cari resistance (swing high di atas entry) ──
    raw_res = []
    h_arr = df["High"].values
    for i in range(start, n - sw):
        val = h_arr[i]
        if val == h_arr[max(0, i - sw):i + sw + 1].max():
            if entry + tp_min < val <= entry + tp_max:
                raw_res.append(float(val))

    tps = []
    if raw_res:
        raw_res.sort()
        i = 0
        while i < len(raw_res) and len(tps) < 3:
            grp = [raw_res[i]]
            j = i + 1
            while j < len(raw_res) and (raw_res[j] - grp[0]) / grp[0] < 0.01:
                grp.append(raw_res[j])
                j += 1
            lvl = _rnd(sum(grp) / len(grp), "up")
            if not tps or (lvl - tps[-1]) / tps[-1] > 0.006:
                tps.append(lvl)
            i = j

    if not tps:
        tps = [
            _rnd(entry + atr * h["atr_tp"][0], "up"),
            _rnd(entry + atr * h["atr_tp"][1], "up"),
            _rnd(entry + atr * h["atr_tp"][2], "up"),
        ]

    # ── Cari support (swing low di bawah entry) ──
    sl_default = _rnd(entry - atr * h["atr_sl"], "down")
    l_arr = df["Low"].values
    sl_min_dist = max(entry * 0.005, atr * 0.3)
    sl_max_dist = atr * h["atr_sl"] * 2.2

    raw_sup = []
    for i in range(start, n - sw):
        val = l_arr[i]
        if val == l_arr[max(0, i - sw):i + sw + 1].min():
            dist = entry - val
            if sl_min_dist <= dist <= sl_max_dist:
                raw_sup.append(float(val))

    sl = _rnd(max(raw_sup), "down") if raw_sup else sl_default

    rr_tp = tps[1] if len(tps) >= 2 else tps[0]
    rr = (rr_tp - entry) / (entry - sl) if entry > sl else 0

    return tps, sl, rr


# ════════════════════════════════════════════════════
# FORMATTING HELPERS
# ════════════════════════════════════════════════════

def rp(n: float, cur: str = "IDR") -> str:
    if cur == "USD":
        if n >= 10000: return f"${n:,.0f}"
        if n >= 100:   return f"${n:,.1f}"
        if n >= 1:     return f"${n:,.3f}"
        if n >= 0.01:  return f"${n:.5f}"
        return f"${n:.7f}"
    if cur == "IDR_INDODAX" and abs(n) < 1:
        return f"{n:.8f}".rstrip("0").rstrip(".").replace(".", ",")
    return f"{int(round(n)):,}".replace(",", ".")

def display_ticker(ticker: str, source: str = "yahoo") -> str:
    if source == "indodax" and ticker.endswith("IDR"):
        return f"{ticker[:-3]}/IDR"
    return ticker.replace("-USD", "")

def pct(new: float, base: float) -> str:
    v = (new - base) / base * 100
    return f"{v:+.1f}%"

def tier(score: int) -> tuple[str, str]:
    if score >= 9: return "🔥 Kuat Sekali", "b-fire"
    if score >= 6: return "🟢 Kuat",        "b-kuat"
    if score >= 3: return "🟡 Moderat",     "b-mod"
    if score >= 1: return "🟠 Lemah",       "b-lemah"
    return "🔴 Skip", "b-skip"

def portfolio_recommendation(score: int, pnl_pct: float) -> tuple[str, str]:
    if pnl_pct >= 20:
        return "💰 Take Profit", "rec-tp"
    if score >= 4 and pnl_pct <= -10:
        return "💪 Average Down", "rec-add"
    if score >= 2 and pnl_pct >= 5:
        return "✅ Hold / TP", "rec-tp"
    if score <= 0 and pnl_pct <= -20:
        return "✂️ Cut Loss", "rec-cut"
    if score <= 1 and pnl_pct <= -10:
        return "⚠️ Waspada", "rec-warn"
    return "⏳ Hold", "rec-hold"

def _svg(d: str, color: str = "currentColor", size: int = 9) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.2" '
        f'stroke-linecap="round" stroke-linejoin="round" class="ic">{d}</svg>'
    )

def _dot_svg(fill: str, stroke: str, inner: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" '
        f'viewBox="0 0 24 24" fill="none" class="ic">'
        f'<circle cx="12" cy="12" r="10" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
        f'{inner}</svg>'
    )

_I_ENTRY = _svg('<polyline points="22 7 13.5 15.5 8.5 10.5 1 18"/><polyline points="16 7 22 7 22 13"/>', "#8892b0")
_I_SL    = _svg('<circle cx="12" cy="12" r="10"/><path d="M15 9 9 15"/><path d="M9 9 15 15"/>', "#ff6b6b")
_I_RR    = _svg('<path d="m16 3 4 4-4 4"/><path d="M20 7H4"/><path d="m8 21-4-4 4-4"/><path d="M4 17h16"/>', "#6c63ff")
_I_TP    = [
    _svg('<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>', "#3ad6a6"),
    _svg('<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" y1="22" x2="4" y2="15"/>', "#f4b740"),
    _svg('<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>', "#b47ef4"),
]
_I_TOTAL = _svg('<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M3 9h18M9 21V9"/>', "#8892b0", 12)
_I_KUAT  = _svg('<polyline points="22 7 13.5 15.5 8.5 10.5 1 18"/><polyline points="16 7 22 7 22 13"/>', "#ff9090", 12)
_I_MOD   = _svg('<path d="M8 6h12M6 12h12M4 18h12"/>', "#f4b740", 12)
_I_LEMAH = _svg('<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>', "#ffa552", 12)

DOT = {
    "bullish": _dot_svg("rgba(58,214,166,.2)", "#3ad6a6",
        '<path d="M9 12 11 14 15 10" fill="none" stroke="#3ad6a6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'),
    "bearish": _dot_svg("rgba(255,107,107,.2)", "#ff6b6b",
        '<path d="M15 9 9 15M9 9 15 15" fill="none" stroke="#ff6b6b" stroke-width="2.5" stroke-linecap="round"/>'),
    "neutral": _dot_svg("rgba(244,183,64,.2)", "#f4b740",
        '<path d="M8 12h8" fill="none" stroke="#f4b740" stroke-width="2.5" stroke-linecap="round"/>'),
}


# ════════════════════════════════════════════════════
# HTML COMPONENTS
# ════════════════════════════════════════════════════

_TP_CLS   = ["lv-1", "lv-2", "lv-3"]
_RR_LABEL = {1: "TP1/SL", 2: "TP2/SL", 3: "TP2/SL"}

def _tp_cells(tps: list, entry: float, cur: str = "IDR") -> str:
    n = len(tps)
    cells = ""
    for i, tp in enumerate(tps):
        cells += f"""
    <div class="lv {_TP_CLS[i]}">
      <span class="ll">{_I_TP[i]}TP {i + 1}</span>
      <span class="lval">{rp(tp, cur)}</span>
      <span class="lpct pos">{pct(tp, entry)}</span>
    </div>"""
    return f'<div style="display:grid;grid-template-columns:repeat({n},1fr);gap:7px;margin-top:7px;">{cells}</div>'


def html_cards(rows: list) -> str:
    cards = ['<div class="stock-grid" data-copy-cards>']
    for r in rows:
        lbl, bcls = tier(r["_score"])
        e      = r["_entry"]
        tps    = r["_tps"]
        cur    = r.get("_cur", "IDR")
        rr_lbl = _RR_LABEL.get(len(tps), "TP2/SL")
        code = html.escape(str(r["Kode"]))
        name = html.escape(str(r["Nama"]))
        info_lines = [
            f"Kode: {r['Kode']}",
            f"Nama: {r['Nama']}",
            f"Sinyal: {lbl} (Skor {r['_score']})",
            "",
            f"Entry: {rp(e, cur)}",
            f"Stop Loss: {rp(r['_sl'], cur)} ({pct(r['_sl'], e)})",
            f"R:R: {r['_rr']:.1f}× ({rr_lbl})",
            "",
            "Target Profit:",
        ]
        info_lines.extend(
            f"- TP {i + 1}: {rp(tp, cur)} ({pct(tp, e)})"
            for i, tp in enumerate(tps)
        )
        full_info = html.escape("\n".join(info_lines), quote=True)
        cards.append(f"""
<div class="sc">
  <div class="sc-top">
    <div>
      <div class="sc-code-row">
        <div class="sc-ticker">{code}</div>
        <button class="copy-code" type="button" data-copy="{code}" title="Salin kode {code}" aria-label="Salin kode {code}"></button>
      </div>
      <div class="sc-name">{name}</div>
    </div>
    <span class="badge {bcls}">{lbl}</span>
  </div>
  <div class="lvg">
    <div class="lv lv-e">
      <span class="ll">{_I_ENTRY}Entry</span>
      <span class="lval">{rp(e, cur)}</span>
      <span class="lpct" style="color:var(--t3)">±0%</span>
    </div>
    <div class="lv lv-sl">
      <span class="ll">{_I_SL}Stop Loss</span>
      <span class="lval">{rp(r["_sl"], cur)}</span>
      <span class="lpct neg">{pct(r["_sl"], e)}</span>
    </div>
    <div class="lv lv-rr">
      <span class="ll">{_I_RR}R:R</span>
      <span class="lval">{r["_rr"]:.1f}×</span>
      <span class="lpct" style="color:var(--t3)">{rr_lbl}</span>
    </div>
  </div>
  {_tp_cells(tps, e, cur)}
  <button class="copy-info" type="button" data-copy="{full_info}" title="Salin informasi lengkap {code}" aria-label="Salin informasi lengkap {code}">
    <span class="copy-info-icon"></span>
    <span class="copy-info-label">Salin info lengkap</span>
  </button>
</div>""")
    cards.append("</div>")
    cards.append("""
<script>
(() => {
  const root = document.currentScript.previousElementSibling;
  if (!root || root.dataset.copyReady) return;
  root.dataset.copyReady = "true";

  const fallbackCopy = text => {
    const area = document.createElement("textarea");
    area.value = text;
    area.style.position = "fixed";
    area.style.opacity = "0";
    document.body.appendChild(area);
    area.select();
    document.execCommand("copy");
    area.remove();
  };

  root.addEventListener("click", async event => {
    const button = event.target.closest("[data-copy]");
    if (!button) return;
    const text = button.dataset.copy;
    try {
      if (navigator.clipboard?.writeText) await navigator.clipboard.writeText(text);
      else fallbackCopy(text);
    } catch (_) {
      fallbackCopy(text);
    }
    button.classList.add("copied");
    button.title = button.classList.contains("copy-code")
      ? `${text} tersalin`
      : "Informasi lengkap tersalin";
    const label = button.querySelector(".copy-info-label");
    if (label) label.textContent = "Informasi tersalin";
    setTimeout(() => {
      button.classList.remove("copied");
      button.title = button.classList.contains("copy-code")
        ? `Salin kode ${text}`
        : "Salin informasi lengkap";
      if (label) label.textContent = "Salin info lengkap";
    }, 1400);
  });
})();
</script>
""")
    return "\n".join(cards)


def html_stats(rows: list) -> str:
    total  = len(rows)
    kuat   = sum(1 for r in rows if r["_score"] >= 4)
    mod    = sum(1 for r in rows if 2 <= r["_score"] < 4)
    lemah  = sum(1 for r in rows if r["_score"] < 2)
    return f"""
<div class="stats-bar">
  <div class="chip">{_I_TOTAL} Total <b>{total}</b></div>
  <div class="chip">{_I_KUAT} Kuat <b>{kuat}</b></div>
  <div class="chip">{_I_MOD} Moderat <b>{mod}</b></div>
  <div class="chip">{_I_LEMAH} Lemah <b>{lemah}</b></div>
</div>"""


_LS_CLS = ["ls-1", "ls-2", "ls-3"]

def html_level_strip(entry: float, sl: float, tps: list, cur: str = "IDR") -> str:
    tp_items = ""
    for i, tp in enumerate(tps):
        tp_items += f"""
  <div class="ls {_LS_CLS[i]}">
    <div class="ls-lbl">{_I_TP[i]}TP {i + 1}</div>
    <span class="ls-val">{rp(tp, cur)}</span>
    <span class="ls-pct pos">{pct(tp, entry)}</span>
  </div>"""
    return f"""
<div class="lvl-strip">
  <div class="ls ls-e">
    <div class="ls-lbl">{_I_ENTRY}Entry</div>
    <span class="ls-val">{rp(entry, cur)}</span>
    <span class="ls-pct" style="color:var(--t3)">±0%</span>
  </div>
  <div class="ls ls-sl">
    <div class="ls-lbl">{_I_SL}Stop Loss</div>
    <span class="ls-val">{rp(sl, cur)}</span>
    <span class="ls-pct neg">{pct(sl, entry)}</span>
  </div>
  {tp_items}
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


def _fmt_idr_compact(val: float) -> str:
    a = abs(val)
    sign = "+" if val >= 0 else "-"
    if a >= 1_000_000_000:
        return f"{sign}{a/1_000_000_000:.2f}B"
    if a >= 1_000_000:
        return f"{sign}{a/1_000_000:.2f}jt"
    if a >= 1_000:
        return f"{sign}{a/1_000:.1f}rb"
    return f"{sign}{a:.0f}"


def html_portfolio_cards(items: list) -> str:
    cards = ['<div class="port-grid">']
    for item in items:
        code = html.escape(str(item["display"]))
        name = html.escape(str(item["name"]))
        cur  = item["cur"]

        if item.get("error"):
            cards.append(f"""
<div class="pc">
  <div class="pc-top">
    <div>
      <div class="sc-ticker">{code}</div>
      <div class="sc-name">{name}</div>
    </div>
  </div>
  <div class="pc-err">⚠ Gagal memuat: {html.escape(str(item['error']))}</div>
</div>""")
            continue

        buy   = item["buy_price"]
        qty   = item["qty"]
        curr  = item.get("current_price", buy)
        pnl_p = item.get("pnl_pct", 0.0)
        slbl  = item.get("signal_lbl", "—")
        rec   = item.get("rec", "—")
        rcls  = item.get("rec_cls", "rec-hold")

        pnl_cls  = "pnl-pos" if pnl_p >= 0 else "pnl-neg"
        pnl_sign = "+" if pnl_p >= 0 else ""
        pnl_idr  = (curr - buy) * qty
        pnl_str  = _fmt_idr_compact(pnl_idr)
        pnl_idr_cls = "pnl-pos" if pnl_idr >= 0 else "pnl-neg"

        cards.append(f"""
<div class="pc">
  <div class="pc-top">
    <div>
      <div class="sc-ticker">{code}</div>
      <div class="sc-name">{name}</div>
      <span class="pnl-big {pnl_cls}">{pnl_sign}{pnl_p:.1f}%</span>
    </div>
    <span class="rec-badge {rcls}">{rec}</span>
  </div>
  <div class="pc-row">
    <div class="pc-cell">
      <div class="pc-lbl">Harga Beli</div>
      <span class="pc-val">{rp(buy, cur)}</span>
    </div>
    <div class="pc-cell">
      <div class="pc-lbl">Harga Kini</div>
      <span class="pc-val">{rp(curr, cur)}</span>
    </div>
    <div class="pc-cell">
      <div class="pc-lbl">Signal</div>
      <span class="pc-val" style="font-size:.76rem">{slbl}</span>
    </div>
    <div class="pc-cell">
      <div class="pc-lbl">P&amp;L</div>
      <span class="pc-val {pnl_idr_cls}">{pnl_str}</span>
    </div>
  </div>
</div>""")

    cards.append("</div>")
    return "\n".join(cards)


# ════════════════════════════════════════════════════
# CHART
# ════════════════════════════════════════════════════

def make_chart(df: pd.DataFrame, label: str, levels: dict = None, cur: str = "IDR"):
    fig = make_subplots(
        rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.03,
        row_heights=[0.48, 0.18, 0.17, 0.17],
        subplot_titles=(
            f"{label} — Candlestick + MA + Bollinger Bands",
            "RSI-14",
            "MACD (12,26,9)",
            "Stochastic (14,3)",
        ),
    )

    # ── Panel 1: Harga ──────────────────────────────
    # Bollinger Bands (dibuat dulu agar berada di belakang candle)
    fig.add_trace(go.Scatter(
        x=df.index, y=df["BB_UP"], name="BB Atas",
        line=dict(color="rgba(108,99,255,0.35)", width=1),
        showlegend=False,
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=df.index, y=df["BB_LOW"], name="BB Bawah",
        line=dict(color="rgba(108,99,255,0.35)", width=1),
        fill="tonexty", fillcolor="rgba(108,99,255,0.06)",
        showlegend=False,
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=df.index, y=df["SMA20"], name="SMA-20/BB Mid",
        line=dict(color="rgba(108,99,255,0.5)", width=1, dash="dot"),
        showlegend=False,
    ), row=1, col=1)

    fig.add_trace(go.Candlestick(
        x=df.index, open=df["Open"], high=df["High"],
        low=df["Low"], close=df["Close"], name="Harga",
        increasing_line_color="#3ad6a6", decreasing_line_color="#ff6b6b",
        increasing_fillcolor="#3ad6a6", decreasing_fillcolor="#ff6b6b",
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=df.index, y=df["EMA9"], name="EMA-9",
        line=dict(color="#e879f9", width=1.2),
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
                annotation_text=f" {lbl}  {rp(val, cur)}",
                annotation_position="top left",
                annotation_font_color=color,
                annotation_font_size=11,
                row=1, col=1,
            )

    # ── Panel 2: RSI ────────────────────────────────
    fig.add_trace(go.Scatter(
        x=df.index, y=df["RSI"], name="RSI",
        line=dict(color="#5b8def", width=1.4),
    ), row=2, col=1)
    fig.add_hline(y=70, line_color="#ff6b6b", line_dash="dot", line_width=1, row=2, col=1)
    fig.add_hline(y=50, line_color="#3d4f6b", line_dash="dot", line_width=1, row=2, col=1)
    fig.add_hline(y=30, line_color="#3ad6a6", line_dash="dot", line_width=1, row=2, col=1)

    # ── Panel 3: MACD ───────────────────────────────
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

    # ── Panel 4: Stochastic ─────────────────────────
    fig.add_trace(go.Scatter(
        x=df.index, y=df["STOCH_K"], name="Stoch %K",
        line=dict(color="#5b8def", width=1.4),
    ), row=4, col=1)
    fig.add_trace(go.Scatter(
        x=df.index, y=df["STOCH_D"], name="Stoch %D",
        line=dict(color="#f4b740", width=1.4),
    ), row=4, col=1)
    fig.add_hline(y=80, line_color="#ff6b6b", line_dash="dot", line_width=1, row=4, col=1)
    fig.add_hline(y=50, line_color="#3d4f6b", line_dash="dot", line_width=1, row=4, col=1)
    fig.add_hline(y=20, line_color="#3ad6a6", line_dash="dot", line_width=1, row=4, col=1)

    fig.update_layout(
        template="plotly_dark",
        height=820,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_rangeslider_visible=False,
        legend=dict(orientation="h", y=1.05, font_size=11),
        paper_bgcolor="#0a0f1e",
        plot_bgcolor="#0a0f1e",
        font=dict(family="Inter, system-ui, sans-serif"),
    )
    for i in range(1, 5):
        fig.update_xaxes(gridcolor="#1b2847", showgrid=True, row=i, col=1)
        fig.update_yaxes(gridcolor="#1b2847", showgrid=True, row=i, col=1)
    fig.update_yaxes(range=[0, 100], row=2, col=1)
    fig.update_yaxes(range=[0, 100], row=4, col=1)
    return fig


# ════════════════════════════════════════════════════
# APP LAYOUT
# ════════════════════════════════════════════════════

# Header
st.markdown("""
<div class="app-hdr">
  <h1>📈 Sinyal Teknikal</h1>
  <p>Scanner swing trading · Saham IDX, US & Crypto · Entry / TP1 / TP2 / TP3 / SL dari level nyata ·
     Overnight hingga 1 bulan · ⚠️ Bukan rekomendasi investasi</p>
</div>
""", unsafe_allow_html=True)

# ── Helper tanggal ─────────────────────────────────
_HARI  = ["Sen","Sel","Rab","Kam","Jum","Sab","Min"]
_BULAN = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"]

def fmt_tgl(d: dt.date) -> str:
    return f"{_HARI[d.weekday()]}, {d.day} {_BULAN[d.month-1]} {d.year}"

def days_to_horizon(days: int) -> str:
    if days <= 1:   return "Overnight (1 Hari)"
    if days <= 4:   return "2–3 Hari"
    if days <= 9:   return "1 Minggu"
    if days <= 20:  return "2 Minggu"
    return "1 Bulan"


# ── Settings (main area) ────────────────────────────
today     = dt.date.today()
tomorrow  = today + dt.timedelta(days=1)

with st.container():
    st.markdown('<div class="settings-strip">', unsafe_allow_html=True)
    # Baris 1: tanggal beli & jual
    c1, c2 = st.columns(2)
    with c1:
        buy_date  = st.date_input("🛒 Beli sore",  value=today,    format="DD/MM/YYYY")
    with c2:
        sell_date = st.date_input("💰 Jual pagi",  value=tomorrow, format="DD/MM/YYYY")
    # Baris 2: durasi & skor minimum
    c3, c4 = st.columns([1, 2])
    with c3:
        days_diff = (sell_date - buy_date).days
        if days_diff <= 0:
            days_diff = 1
            warn_html = '<div class="dur-warn">⚠ Jual harus setelah beli</div>'
        else:
            warn_html = ""
        horizon_name = days_to_horizon(days_diff)
        st.markdown(
            f'<div class="dur-badge"><div class="dur-days">{days_diff} hari</div>'
            f'<div class="dur-hor">{horizon_name}</div>{warn_html}</div>',
            unsafe_allow_html=True,
        )
    with c4:
        min_score = st.slider(
            "Skor sinyal minimum", 0, 10, 3,
            help="0 = semua · 3 = moderat ke atas · 6 = kuat saja · 9 = kuat sekali",
        )
    st.markdown("</div>", unsafe_allow_html=True)

h_params = HORIZONS[horizon_name]
idx_universe = load_idx_markets()
us_universe = load_us_markets()
indodax_universe, indodax_price_steps = load_indodax_markets()


# ── Tabs ────────────────────────────────────────────
tab_scan, tab_portfolio, tab_detail = st.tabs(["🔍  Scanner", "💼  Portofolio", "📊  Analisa Detail"])


# ════════════════════════════════════════════════════
# TAB 1: SCANNER
# ════════════════════════════════════════════════════
with tab_scan:
    # ── Pilih aset ──────────────────────────────────
    asset_type = st.radio(
        "Aset",
        ["📊 Saham IDX", "Saham US", "₿ Crypto USD", "Crypto Indodax (IDR)"],
        horizontal=True,
        label_visibility="collapsed",
    )
    if asset_type.startswith("📊"):
        scan_limit = st.select_slider(
            "Jumlah saham IDX",
            options=[25, 50, 100, 150],
            value=50,
            help="Saham dipilih berdasarkan volume transaksi harian terbesar di Yahoo Finance.",
        )
        universe = dict(list(idx_universe.items())[:scan_limit])
        scan_source = "yahoo"
        scan_cur = "IDR"
        scan_label = f"saham IDX teraktif dari {len(idx_universe)} saham tersedia"
    elif asset_type == "Saham US":
        scan_limit = st.select_slider(
            "Jumlah saham US",
            options=[25, 50, 100, 150],
            value=50,
            help="Saham berkapitalisasi minimal USD 1 miliar, diurutkan berdasarkan volume harian.",
        )
        universe = dict(list(us_universe.items())[:scan_limit])
        scan_source = "yahoo"
        scan_cur = "USD"
        scan_label = f"saham US teraktif dari {len(us_universe)} saham tersedia"
    elif asset_type.startswith("₿"):
        universe = CRYPTO_UNIVERSE
        scan_source = "yahoo"
        scan_cur = "USD"
        scan_label = "koin crypto USD"
    else:
        scan_limit = st.select_slider(
            "Jumlah pair Indodax",
            options=[25, 50, 100, 150],
            value=50,
            help="Pair dipilih berdasarkan volume transaksi IDR 24 jam terbesar.",
        )
        universe = dict(list(indodax_universe.items())[:scan_limit])
        scan_source = "indodax"
        scan_cur = "IDR_INDODAX"
        scan_label = f"pair Indodax teraktif dari {len(indodax_universe)} pair tersedia"
    scan_market_key = f"{asset_type}:{len(universe)}"
    entry_lbl = "Entry" if scan_cur == "USD" else "Entry (Rp)"

    col_btn, col_txt = st.columns([1, 3])
    with col_btn:
        do_scan = st.button("🔄  Scan Sekarang", type="primary")
    with col_txt:
        st.caption(
            f"Memindai **{len(universe)} {scan_label}**. "
            "Pertama kali ±1–2 menit. Berikutnya dari cache 10 menit. "
            + (
                "Request Indodax diberi jeda agar aman terhadap rate limit."
                if scan_source == "indodax"
                else (
                    "Data Yahoo Finance dapat mengalami delay saat jam bursa."
                    if asset_type.startswith("📊") or asset_type == "Saham US"
                    else ""
                )
            )
        )

    if do_scan:
        st.session_state.pop("scan_rows", None)  # clear agar IDX & crypto tidak tercampur

        rows = []
        bar  = st.progress(0, text="Memulai scan…")
        codes = list(universe.keys())

        for i, code in enumerate(codes):
            if scan_source == "indodax" and i > 0:
                time.sleep(INDODAX_SCAN_DELAY_SECONDS)
            bar.progress(
                (i + 1) / len(codes),
                text=f"Menganalisa {code}… ({i+1}/{len(codes)})",
            )
            try:
                ticker = f"{code}.JK" if asset_type.startswith("📊") else code
                df = load_data(ticker, h_params["period"], scan_source)
                if len(df) < 55:
                    continue
                df = add_indicators(df)
                score, checks = score_and_check(df)
                if score < min_score:
                    continue

                last  = df.iloc[-1]
                entry = float(last["Close"])
                atr   = float(last["ATR"])
                if pd.isna(atr) or atr <= 0:
                    continue
                price_step = (
                    indodax_price_steps.get(ticker, 1.0)
                    if scan_source == "indodax"
                    else None
                )
                tps, sl, rr = find_key_levels(
                    df, entry, atr, h_params, scan_cur, price_step
                )

                tp_export = {
                    f"TP{j+1}": f"{rp(tp, scan_cur)} ({pct(tp, entry)})"
                    for j, tp in enumerate(tps)
                }

                rows.append(dict(
                    Kode=display_ticker(code, scan_source), Nama=universe[code],
                    _score=score, _entry=entry,
                    _sl=sl, _tps=tps, _rr=rr,
                    _checks=checks, _cur=scan_cur,
                    _ticker=ticker, _source=scan_source,
                    Signal=tier(score)[0],
                    Skor=score,
                    **{
                        entry_lbl: rp(entry, scan_cur),
                        "SL": f"{rp(sl, scan_cur)} ({pct(sl, entry)})",
                        **tp_export,
                        "R:R": f"{rr:.1f}×",
                    },
                ))
            except Exception:
                continue

        bar.empty()

        if not rows:
            st.warning("Tidak ada yang memenuhi filter. Coba turunkan skor minimum.")
        else:
            st.session_state["scan_rows"] = sorted(
                rows, key=lambda r: r["_score"], reverse=True
            )
            st.session_state["scan_market"] = scan_market_key
            st.success(f"✅ Ditemukan **{len(rows)}** aset, diurutkan dari sinyal terkuat.")

    if (
        st.session_state.get("scan_rows")
        and st.session_state.get("scan_market") == scan_market_key
    ):
        rows = st.session_state["scan_rows"]

        st.markdown(html_stats(rows), unsafe_allow_html=True)
        st.html(html_cards(rows), unsafe_allow_javascript=True)
        st.markdown("<br>", unsafe_allow_html=True)

        all_keys    = set().union(*(r.keys() for r in rows))
        cur_rows    = rows[0].get("_cur", "IDR")
        e_lbl       = "Entry" if cur_rows == "USD" else "Entry (Rp)"
        export_tp   = [f"TP{i+1}" for i in range(3) if f"TP{i+1}" in all_keys]
        export_cols = [c for c in ["Signal", "Skor", "Kode", "Nama", e_lbl, "SL"] + export_tp + ["R:R"] if c in all_keys]
        csv   = pd.DataFrame(rows)[export_cols].to_csv(index=False)
        fname = horizon_name.split("(")[0].strip().replace(" ", "_").replace("–", "-")
        st.download_button("⬇️  Download CSV", csv, file_name=f"scan_{fname}.csv", mime="text/csv")

        st.markdown('<div class="sec-lbl">Detail Aset</div>', unsafe_allow_html=True)

        all_names = {r["Kode"]: r["Nama"] for r in rows}
        sel_code  = st.selectbox(
            "Pilih untuk lihat chart & breakdown sinyal",
            [r["Kode"] for r in rows],
            format_func=lambda c: f"{c}  —  {all_names.get(c, c)}",
        )
        sel     = next(r for r in rows if r["Kode"] == sel_code)
        sel_cur = sel.get("_cur", "IDR")
        tps_sel = sel["_tps"]
        rr_tp_idx = min(1, len(tps_sel) - 1)

        # Metrics
        lbl, _ = tier(sel["_score"])
        mcols  = st.columns(3 + len(tps_sel) + 1)
        mcols[0].metric("Signal", lbl, f"Skor {sel['_score']}")
        mcols[1].metric("Entry",  rp(sel["_entry"], sel_cur))
        mcols[2].metric("SL",     rp(sel["_sl"], sel_cur), pct(sel["_sl"], sel["_entry"]))
        for i, tp in enumerate(tps_sel):
            mcols[3 + i].metric(f"TP {i+1}", rp(tp, sel_cur), pct(tp, sel["_entry"]))
        mcols[-1].metric("R:R", f"{sel['_rr']:.1f}×", f"TP{rr_tp_idx+1}/SL")

        st.markdown(
            html_level_strip(sel["_entry"], sel["_sl"], tps_sel, sel_cur),
            unsafe_allow_html=True,
        )

        st.markdown('<div class="sec-lbl">Breakdown Sinyal</div>', unsafe_allow_html=True)
        st.markdown(html_signals(sel["_checks"]), unsafe_allow_html=True)

        st.markdown('<div class="sec-lbl">Chart</div>', unsafe_allow_html=True)
        try:
            df_sel = load_data(
                sel.get("_ticker", sel.get("_yf_ticker")),
                h_params["period"],
                sel.get("_source", "yahoo"),
            )
            df_sel = add_indicators(df_sel)
            levels_sel = {"entry": sel["_entry"], "sl": sel["_sl"]}
            for i, tp in enumerate(sel["_tps"], 1):
                levels_sel[f"tp{i}"] = tp
            st.plotly_chart(
                make_chart(df_sel, sel_code, levels_sel, sel_cur),
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"Gagal memuat chart: {e}")


# ════════════════════════════════════════════════════
# TAB 2: PORTFOLIO MONITOR
# ════════════════════════════════════════════════════
with tab_portfolio:
    st.markdown(
        '<p style="color:var(--t2);font-size:.82rem;margin-bottom:14px">'
        "Monitor posisi trading Anda. Masukkan aset &amp; harga beli untuk melihat P&amp;L terkini "
        "beserta sinyal teknikal — apakah perlu <b style='color:#ff6b6b'>Cut Loss</b>, "
        "<b style='color:#8892b0'>Hold</b>, atau "
        "<b style='color:#3ad6a6'>Average Down</b>.</p>",
        unsafe_allow_html=True,
    )

    if "portfolio" not in st.session_state:
        st.session_state["portfolio"] = []

    # ── Form tambah aset ────────────────────────────
    with st.expander("➕ Tambah Aset ke Portofolio", expanded=not st.session_state["portfolio"]):
        p_market = st.selectbox(
            "Pasar",
            ["Crypto Indodax (IDR)", "Saham IDX", "Saham US", "Crypto USD"],
            key="p_market",
        )

        if p_market == "Crypto Indodax (IDR)":
            p_options = list(indodax_universe.keys())
            p_fmt     = lambda k: f"{display_ticker(k, 'indodax')}  —  {indodax_universe[k]}"
            p_source  = "indodax"
            p_cur     = "IDR_INDODAX"
            p_plbl    = "Harga Beli (IDR)"
        elif p_market == "Saham IDX":
            p_options = list(idx_universe.keys())
            p_fmt     = lambda k: f"{k}  —  {idx_universe[k]}"
            p_source  = "yahoo"
            p_cur     = "IDR"
            p_plbl    = "Harga Beli (Rp)"
        elif p_market == "Saham US":
            p_options = list(us_universe.keys())
            p_fmt     = lambda k: f"{k}  —  {us_universe[k]}"
            p_source  = "yahoo"
            p_cur     = "USD"
            p_plbl    = "Harga Beli ($)"
        else:
            p_options = list(CRYPTO_UNIVERSE.keys())
            p_fmt     = lambda k: f"{k.replace('-USD','')}  —  {CRYPTO_UNIVERSE[k]}"
            p_source  = "yahoo"
            p_cur     = "USD"
            p_plbl    = "Harga Beli ($)"

        p_asset = st.selectbox("Aset", p_options, format_func=p_fmt, key="p_asset")

        pfc1, pfc2 = st.columns(2)
        with pfc1:
            p_buy = st.number_input(p_plbl, min_value=0.0, value=0.0, format="%f", key="p_buy")
        with pfc2:
            p_qty = st.number_input("Jumlah (qty)", min_value=0.0, value=0.0, format="%f", key="p_qty")

        if st.button("Tambah ke Portofolio", key="p_add_btn"):
            if p_buy <= 0 or p_qty <= 0:
                st.error("Harga beli dan jumlah harus lebih dari 0.")
            else:
                if p_market == "Crypto Indodax (IDR)":
                    tk = p_asset
                    pdisplay = display_ticker(p_asset, "indodax")
                    pname = indodax_universe.get(p_asset, p_asset)
                elif p_market == "Saham IDX":
                    tk = f"{p_asset}.JK"
                    pdisplay = p_asset
                    pname = idx_universe.get(p_asset, p_asset)
                elif p_market == "Saham US":
                    tk = p_asset
                    pdisplay = p_asset
                    pname = us_universe.get(p_asset, p_asset)
                else:
                    tk = p_asset
                    pdisplay = p_asset.replace("-USD", "")
                    pname = CRYPTO_UNIVERSE.get(p_asset, p_asset)

                if any(x["ticker"] == tk for x in st.session_state["portfolio"]):
                    st.warning(f"{pdisplay} sudah ada di portofolio.")
                else:
                    st.session_state["portfolio"].append({
                        "source": p_source, "ticker": tk,
                        "display": pdisplay, "name": pname,
                        "buy_price": float(p_buy), "qty": float(p_qty),
                        "cur": p_cur,
                    })
                    st.success(f"✅ {pdisplay} ditambahkan.")
                    st.rerun()

    # ── Tampilan portofolio ─────────────────────────
    portfolio = st.session_state["portfolio"]

    if not portfolio:
        st.info("Portofolio kosong. Tambahkan aset di atas untuk mulai monitor.")
    else:
        pb1, pb2 = st.columns([1, 1])
        with pb1:
            do_refresh_port = st.button("🔄 Refresh Sinyal", key="p_refresh")
        with pb2:
            if st.button("🗑 Hapus Semua", key="p_clear"):
                st.session_state["portfolio"] = []
                st.session_state.pop("portfolio_results", None)
                st.rerun()

        if do_refresh_port:
            pbar = st.progress(0, text="Memuat sinyal portofolio…")
            results = []
            for pi, pitem in enumerate(portfolio):
                if pitem["source"] == "indodax" and pi > 0:
                    time.sleep(INDODAX_SCAN_DELAY_SECONDS)
                pbar.progress(
                    (pi + 1) / len(portfolio),
                    text=f"Menganalisa {pitem['display']}… ({pi+1}/{len(portfolio)})",
                )
                res = dict(pitem)
                try:
                    df_p = load_data(pitem["ticker"], h_params["period"], pitem["source"])
                    if len(df_p) < 30:
                        res["error"] = "Data terlalu sedikit"
                        results.append(res)
                        continue
                    df_p    = add_indicators(df_p)
                    last_p  = df_p.iloc[-1]
                    curr_p  = float(last_p["Close"])
                    pnl_pct = (curr_p - pitem["buy_price"]) / pitem["buy_price"] * 100
                    sc_p, _ = score_and_check(df_p)
                    lbl_p, _    = tier(sc_p)
                    rec_p, rcls = portfolio_recommendation(sc_p, pnl_pct)
                    res.update({
                        "current_price": curr_p,
                        "pnl_pct": pnl_pct,
                        "score": sc_p,
                        "signal_lbl": lbl_p,
                        "rec": rec_p,
                        "rec_cls": rcls,
                        "error": None,
                    })
                except Exception as ex:
                    res["error"] = str(ex)
                results.append(res)
            pbar.empty()
            st.session_state["portfolio_results"] = results

        results_display = st.session_state.get("portfolio_results", portfolio)

        # Ringkasan total P&L
        refreshed = [r for r in results_display if r.get("current_price") and not r.get("error")]
        if refreshed:
            total_modal = sum(r["buy_price"] * r["qty"] for r in refreshed)
            total_now   = sum(r["current_price"] * r["qty"] for r in refreshed)
            total_pnl   = total_now - total_modal
            total_pct   = total_pnl / total_modal * 100 if total_modal else 0
            cut_count   = sum(1 for r in refreshed if r.get("rec_cls") == "rec-cut")
            add_count   = sum(1 for r in refreshed if r.get("rec_cls") == "rec-add")
            mc1, mc2, mc3, mc4 = st.columns(4)
            mc1.metric("Modal", f"Rp {total_modal:,.0f}".replace(",", ".") if total_modal >= 1 else f"{total_modal:.4f}")
            mc2.metric("Nilai Kini", f"Rp {total_now:,.0f}".replace(",", ".") if total_now >= 1 else f"{total_now:.4f}")
            mc3.metric("P&L Total", _fmt_idr_compact(total_pnl), f"{'+' if total_pct >= 0 else ''}{total_pct:.1f}%")
            mc4.metric("Sinyal", f"✂️ {cut_count} Cut · 💪 {add_count} Add")

        st.markdown(html_portfolio_cards(results_display), unsafe_allow_html=True)

        # Tombol hapus per aset
        st.markdown('<div class="sec-lbl" style="margin-top:18px">Kelola Aset</div>', unsafe_allow_html=True)
        for pi, pitem in enumerate(portfolio):
            dc1, dc2 = st.columns([5, 1])
            with dc1:
                st.caption(f"{pitem['display']} — {pitem['name']} · Beli: {rp(pitem['buy_price'], pitem['cur'])} × {pitem['qty']}")
            with dc2:
                if st.button("Hapus", key=f"del_port_{pi}"):
                    st.session_state["portfolio"].pop(pi)
                    pr = st.session_state.get("portfolio_results", [])
                    if pi < len(pr):
                        pr.pop(pi)
                    st.session_state["portfolio_results"] = pr
                    st.rerun()


# ════════════════════════════════════════════════════
# TAB 3: ANALISA DETAIL
# ════════════════════════════════════════════════════
with tab_detail:
    col_m, col_t, col_p = st.columns([1, 1, 1])

    with col_m:
        mode = st.radio(
            "Aset",
            ["Saham IDX", "Saham US", "Crypto USD", "Crypto Indodax", "Manual"],
        )

    with col_t:
        data_source = "yahoo"
        if mode == "Saham IDX":
            pick   = st.selectbox(
                "Saham",
                list(idx_universe.keys()),
                format_func=lambda k: f"{k}  —  {idx_universe[k]}",
            )
            ticker = f"{pick}.JK"
            chart_label = pick
            det_cur = "IDR"
        elif mode == "Saham US":
            pick = st.selectbox(
                "Saham US",
                list(us_universe.keys()),
                format_func=lambda k: f"{k}  —  {us_universe[k]}",
            )
            ticker = pick
            chart_label = pick
            det_cur = "USD"
        elif mode == "Crypto USD":
            pick   = st.selectbox(
                "Koin",
                list(CRYPTO_UNIVERSE.keys()),
                format_func=lambda k: f"{k.replace('-USD','')}  —  {CRYPTO_UNIVERSE[k]}",
            )
            ticker = pick
            chart_label = display_ticker(ticker)
            det_cur = "USD"
        elif mode == "Crypto Indodax":
            pick = st.selectbox(
                "Koin Indodax",
                list(indodax_universe.keys()),
                format_func=lambda k: f"{display_ticker(k, 'indodax')}  —  {indodax_universe[k]}",
            )
            ticker = pick
            chart_label = f"{display_ticker(ticker, 'indodax')} · Indodax"
            data_source = "indodax"
            det_cur = "IDR_INDODAX"
        else:
            ticker = st.text_input("Ticker Yahoo Finance", "BBCA.JK").strip().upper()
            chart_label = ticker
            det_cur = "USD" if ticker.endswith("-USD") else "IDR"

    with col_p:
        period = st.selectbox("Rentang Data", ["3mo", "6mo", "1y", "2y"], index=2)

    try:
        df = load_data(ticker, period, data_source)
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
    if pd.isna(atr) or atr <= 0:
        st.warning(f"Data `{chart_label}` tidak memiliki volatilitas yang cukup untuk dianalisa.")
        st.stop()
    price_step = (
        indodax_price_steps.get(ticker, 1.0)
        if data_source == "indodax"
        else None
    )
    tps, sl, rr = find_key_levels(df, entry, atr, h_params, det_cur, price_step)
    lbl, _ = tier(score)

    rr_tp_idx = min(1, len(tps) - 1)
    dcols = st.columns(3 + len(tps) + 1)
    dcols[0].metric("Harga Terakhir", rp(entry, det_cur), f"{chg:+.2f}%")
    dcols[1].metric("Signal",         lbl,                 f"Skor {score}")
    dcols[2].metric("RSI-14",         f"{last['RSI']:.0f}")
    for i, tp in enumerate(tps):
        dcols[3 + i].metric(f"TP {i+1}", rp(tp, det_cur), pct(tp, entry))
    dcols[-1].metric("R:R", f"{rr:.1f}×", f"TP{rr_tp_idx+1}/SL")

    st.caption(
        f"**Beli:** {fmt_tgl(buy_date)}  →  **Jual:** {fmt_tgl(sell_date)}  "
        f"·  {days_diff} hari  ·  Horizon: **{horizon_name}**"
    )

    st.markdown(html_level_strip(entry, sl, tps, det_cur), unsafe_allow_html=True)

    levels_detail = {"entry": entry, "sl": sl}
    for i, tp in enumerate(tps, 1):
        levels_detail[f"tp{i}"] = tp
    st.plotly_chart(
        make_chart(df, chart_label, levels_detail, det_cur),
        use_container_width=True,
    )

    st.markdown('<div class="sec-lbl">Breakdown Sinyal</div>', unsafe_allow_html=True)
    st.markdown(html_signals(checks), unsafe_allow_html=True)

    st.info(
        f"**Entry** = harga penutupan terakhir (aproksimasi harga beli sore). "
        f"**TP** diambil dari swing high nyata (resistance sebelumnya di chart). "
        f"**SL** dari swing low terdekat di bawah entry. "
        f"Jika tidak ada swing yang cocok dalam range, fallback ke ATR-14 × faktor horizon. "
        f"Jumlah TP bisa 1–3 tergantung berapa level resistance yang ditemukan.",
        icon="ℹ️",
    )

# ════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════
st.markdown("""
<div class="app-footer">
  Created by <span class="creator"><a href="https://muhamadakbarfadilah.my.id/" target="_blank">Akbar Fadilah</a></span>
  &nbsp;·&nbsp; Founder &amp; Co-Founder at <a href="https://afdatech.com/" target="_blank">Afda Technology Solutions</a>
</div>
""", unsafe_allow_html=True)
