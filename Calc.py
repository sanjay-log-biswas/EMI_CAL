import streamlit as st
import plotly.graph_objects as go
import math

st.set_page_config(
    page_title="LoanIQ — Smart EMI Calculator",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════════════════════════════
#  MASTER CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Root vars ── */
:root {
  --gold:    #FFD700;
  --gold2:   #FFA500;
  --accent:  #7C3AED;
  --accent2: #A78BFA;
  --bg:      #05050f;
  --surface: rgba(255,255,255,0.04);
  --border:  rgba(255,255,255,0.08);
  --text:    #E2E8F0;
  --muted:   #64748B;
  --success: #10B981;
  --danger:  #F43F5E;
}

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; }
html, body, .stApp {
  font-family: 'Outfit', sans-serif;
  background: var(--bg) !important;
  color: var(--text);
}

/* ── Animated mesh background ── */
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 20% 10%,  rgba(124,58,237,0.18) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 80%,  rgba(255,165,0,0.12)  0%, transparent 60%),
    radial-gradient(ellipse 70% 60% at 60% 30%,  rgba(16,185,129,0.06) 0%, transparent 60%);
  pointer-events: none;
  z-index: 0;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header, .stDeployButton { visibility: hidden !important; }
.block-container {
  padding: 0 !important;
  max-width: 100% !important;
}
section.main > div { padding: 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 99px; }

/* ══════════════════════════════
   LAYOUT WRAPPER
══════════════════════════════ */
.app-shell {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  padding: 0 0 4rem;
}

/* ══════════════════════════════
   TOP NAV BAR
══════════════════════════════ */
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.1rem 3rem;
  background: rgba(5,5,15,0.8);
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(20px);
  position: sticky;
  top: 0;
  z-index: 100;
}
.nav-brand {
  display: flex;
  align-items: center;
  gap: .7rem;
}
.nav-logo {
  width: 36px; height: 36px;
  background: linear-gradient(135deg, var(--accent), var(--gold2));
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem;
}
.nav-name {
  font-size: 1.25rem;
  font-weight: 800;
  background: linear-gradient(90deg, #fff 30%, var(--gold));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.5px;
}
.nav-pills { display: flex; gap: .5rem; }
.nav-pill {
  padding: .35rem .9rem;
  border-radius: 99px;
  font-size: .78rem;
  font-weight: 600;
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--muted);
  letter-spacing: .3px;
}
.nav-pill.active {
  background: linear-gradient(90deg, rgba(124,58,237,.25), rgba(255,165,0,.2));
  border-color: rgba(124,58,237,.5);
  color: var(--gold);
}

/* ══════════════════════════════
   HERO SECTION
══════════════════════════════ */
.hero-section {
  text-align: center;
  padding: 4rem 2rem 2.5rem;
}
.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: .45rem;
  background: linear-gradient(90deg, rgba(124,58,237,.2), rgba(255,165,0,.15));
  border: 1px solid rgba(124,58,237,.4);
  border-radius: 99px;
  padding: .4rem 1.1rem;
  font-size: .78rem;
  font-weight: 600;
  color: var(--gold);
  letter-spacing: .8px;
  text-transform: uppercase;
  margin-bottom: 1.4rem;
}
.hero-badge-dot {
  width: 7px; height: 7px;
  background: var(--gold);
  border-radius: 50%;
  animation: pulse-dot 1.8s ease-in-out infinite;
}
@keyframes pulse-dot {
  0%,100% { opacity:1; transform:scale(1); }
  50%      { opacity:.4; transform:scale(.7); }
}
.hero-title {
  font-size: clamp(2.4rem, 5vw, 4rem);
  font-weight: 900;
  line-height: 1.1;
  letter-spacing: -2px;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, #fff 0%, #c4b5fd 40%, var(--gold) 80%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.hero-sub {
  font-size: 1.05rem;
  color: var(--muted);
  max-width: 480px;
  margin: 0 auto 2.5rem;
  line-height: 1.7;
  font-weight: 400;
}
.hero-stats {
  display: flex;
  justify-content: center;
  gap: 2.5rem;
  margin-bottom: 3rem;
}
.h-stat { text-align: center; }
.h-stat-value {
  font-size: 1.6rem;
  font-weight: 800;
  background: linear-gradient(90deg, var(--accent2), var(--gold));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.h-stat-label {
  font-size: .73rem;
  color: var(--muted);
  font-weight: 500;
  letter-spacing: .5px;
  text-transform: uppercase;
  margin-top: .1rem;
}

/* ══════════════════════════════
   MAIN GRID
══════════════════════════════ */
.main-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

/* ══════════════════════════════
   GLASS CARD
══════════════════════════════ */
.g-card {
  background: linear-gradient(145deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 2rem;
  backdrop-filter: blur(20px);
  box-shadow:
    0 1px 0 rgba(255,255,255,0.06) inset,
    0 20px 60px rgba(0,0,0,0.4);
  position: relative;
  overflow: hidden;
}
.g-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
}

.card-header {
  display: flex;
  align-items: center;
  gap: .75rem;
  margin-bottom: 1.8rem;
}
.card-icon {
  width: 40px; height: 40px;
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem;
  flex-shrink: 0;
}
.icon-purple { background: linear-gradient(135deg, #4C1D95, #7C3AED); }
.icon-gold   { background: linear-gradient(135deg, #92400E, #F59E0B); }
.icon-green  { background: linear-gradient(135deg, #064E3B, #10B981); }
.icon-pink   { background: linear-gradient(135deg, #881337, #F43F5E); }

.card-label {
  font-size: .7rem;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--muted);
}
.card-title-text {
  font-size: 1.1rem;
  font-weight: 700;
  color: #fff;
  margin-top: .1rem;
}

/* ══════════════════════════════
   STREAMLIT WIDGET OVERRIDES
══════════════════════════════ */
/* labels */
div[data-testid="stNumberInput"] label,
div[data-testid="stSlider"] label {
  color: #94A3B8 !important;
  font-size: .82rem !important;
  font-weight: 600 !important;
  letter-spacing: .5px !important;
  text-transform: uppercase !important;
  font-family: 'Outfit', sans-serif !important;
  margin-bottom: .3rem !important;
}

/* number inputs */
div[data-testid="stNumberInput"] input {
  background: rgba(255,255,255,0.05) !important;
  border: 1.5px solid rgba(255,255,255,0.1) !important;
  border-radius: 14px !important;
  color: #fff !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 1.05rem !important;
  font-weight: 600 !important;
  padding: .7rem 1rem !important;
  transition: all .2s !important;
}
div[data-testid="stNumberInput"] input:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(124,58,237,.2), 0 0 20px rgba(124,58,237,.1) !important;
  background: rgba(124,58,237,0.08) !important;
}

/* sliders */
div[data-testid="stSlider"] .rc-slider-rail {
  background: rgba(255,255,255,0.08) !important;
  height: 6px !important;
}
div[data-testid="stSlider"] .rc-slider-track {
  background: linear-gradient(90deg, var(--accent), var(--gold)) !important;
  height: 6px !important;
}
div[data-testid="stSlider"] .rc-slider-handle {
  border: 3px solid var(--gold) !important;
  background: #1a1a3e !important;
  width: 20px !important; height: 20px !important;
  margin-top: -7px !important;
  box-shadow: 0 0 12px rgba(255,165,0,.5) !important;
}
div[data-testid="stSlider"] .rc-slider-dot { display: none !important; }
div[data-testid="stSlider"] .rc-slider-mark-text {
  color: var(--muted) !important;
  font-size: .72rem !important;
  font-family: 'Outfit', sans-serif !important;
}

/* ── Calculate button ── */
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #4C1D95, #7C3AED, #A78BFA) !important;
  color: #fff !important;
  font-family: 'Outfit', sans-serif !important;
  font-size: 1rem !important;
  font-weight: 700 !important;
  border: none !important;
  border-radius: 16px !important;
  padding: .85rem 2rem !important;
  width: 100% !important;
  letter-spacing: .3px;
  box-shadow: 0 8px 32px rgba(124,58,237,.45), 0 1px 0 rgba(255,255,255,.15) inset !important;
  transition: all .25s ease !important;
  position: relative;
  overflow: hidden;
}
.stButton > button[kind="primary"]::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.1), transparent);
  border-radius: 16px;
}
.stButton > button[kind="primary"]:hover {
  transform: translateY(-3px) scale(1.01) !important;
  box-shadow: 0 16px 48px rgba(124,58,237,.6), 0 1px 0 rgba(255,255,255,.2) inset !important;
}
.stButton > button[kind="primary"]:active {
  transform: translateY(-1px) scale(.99) !important;
}

/* secondary (reset) button */
.stButton > button[kind="secondary"] {
  background: rgba(255,255,255,0.05) !important;
  color: var(--muted) !important;
  border: 1px solid var(--border) !important;
  border-radius: 16px !important;
  font-family: 'Outfit', sans-serif !important;
  font-size: .9rem !important;
  font-weight: 600 !important;
  padding: .8rem !important;
  width: 100% !important;
  transition: all .2s !important;
}
.stButton > button[kind="secondary"]:hover {
  background: rgba(255,255,255,0.09) !important;
  color: #fff !important;
  border-color: rgba(255,255,255,0.2) !important;
}

/* ── Error / warning msgs ── */
div[data-testid="stAlert"] {
  background: rgba(244,63,94,.1) !important;
  border: 1px solid rgba(244,63,94,.3) !important;
  border-radius: 14px !important;
  color: #FDA4AF !important;
}

/* ══════════════════════════════
   RESULT CARDS
══════════════════════════════ */
.emi-spotlight {
  background: linear-gradient(135deg, #1e0a3c, #3b0764);
  border: 1px solid rgba(124,58,237,.4);
  border-radius: 24px;
  padding: 2rem;
  text-align: center;
  position: relative;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(124,58,237,.3), 0 0 0 1px rgba(255,255,255,.05) inset;
  margin-bottom: 1.5rem;
}
.emi-spotlight::before {
  content: '';
  position: absolute;
  width: 200px; height: 200px;
  background: radial-gradient(circle, rgba(124,58,237,.4), transparent 70%);
  top: -60px; left: -60px;
  border-radius: 50%;
}
.emi-spotlight::after {
  content: '';
  position: absolute;
  width: 150px; height: 150px;
  background: radial-gradient(circle, rgba(255,165,0,.25), transparent 70%);
  bottom: -40px; right: -40px;
  border-radius: 50%;
}
.emi-tag {
  position: relative;
  z-index: 1;
  display: inline-block;
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 99px;
  padding: .3rem .9rem;
  font-size: .7rem;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--accent2);
  margin-bottom: 1rem;
}
.emi-amount {
  position: relative;
  z-index: 1;
  font-family: 'JetBrains Mono', monospace;
  font-size: clamp(2.2rem, 5vw, 3.4rem);
  font-weight: 600;
  background: linear-gradient(90deg, #C4B5FD, #fff 50%, #FCD34D);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -1px;
  line-height: 1;
  margin-bottom: .5rem;
}
.emi-sub {
  position: relative;
  z-index: 1;
  font-size: .82rem;
  color: var(--muted);
  font-weight: 500;
}

.metrics-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.metric-card {
  background: linear-gradient(145deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 1.4rem 1.2rem;
  position: relative;
  overflow: hidden;
  transition: transform .2s, box-shadow .2s;
}
.metric-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.3);
}
.metric-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
}
.mc-purple::before { background: linear-gradient(90deg, var(--accent), var(--accent2)); }
.mc-gold::before   { background: linear-gradient(90deg, var(--gold2), var(--gold)); }
.mc-green::before  { background: linear-gradient(90deg, #059669, var(--success)); }
.mc-pink::before   { background: linear-gradient(90deg, #BE185D, var(--danger)); }

.metric-icon { font-size: 1.4rem; margin-bottom: .6rem; }
.metric-label {
  font-size: .68rem;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: .4rem;
}
.metric-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.2rem;
  font-weight: 600;
  color: #fff;
}

/* ══════════════════════════════
   BREAKDOWN BAR
══════════════════════════════ */
.breakdown-section { margin: 1.5rem 0 .5rem; }
.breakdown-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: .8rem;
}
.breakdown-title {
  font-size: .75rem;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--muted);
}
.breakdown-bar-wrap {
  background: rgba(255,255,255,0.06);
  border-radius: 99px;
  height: 12px;
  overflow: hidden;
  margin-bottom: .7rem;
}
.breakdown-bar {
  height: 100%;
  border-radius: 99px;
  background: linear-gradient(90deg, var(--accent), var(--gold2));
  position: relative;
}
.breakdown-bar::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent 60%, rgba(255,255,255,.3));
  border-radius: 99px;
}
.breakdown-legend {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}
.legend-dot {
  display: inline-block;
  width: 8px; height: 8px;
  border-radius: 50%;
  margin-right: .4rem;
  vertical-align: middle;
}
.legend-item {
  font-size: .78rem;
  font-weight: 500;
  color: var(--muted);
}
.legend-item span { color: #fff; font-weight: 600; }

/* ══════════════════════════════
   SCHEDULE TABLE
══════════════════════════════ */
.schedule-wrap {
  margin-top: 1.2rem;
  overflow: hidden;
  border-radius: 16px;
  border: 1px solid var(--border);
}
.schedule-table {
  width: 100%;
  border-collapse: collapse;
  font-size: .82rem;
}
.schedule-table thead th {
  background: rgba(255,255,255,0.05);
  padding: .7rem 1rem;
  text-align: left;
  font-size: .68rem;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--muted);
  border-bottom: 1px solid var(--border);
}
.schedule-table tbody tr {
  border-bottom: 1px solid rgba(255,255,255,0.04);
  transition: background .15s;
}
.schedule-table tbody tr:hover { background: rgba(255,255,255,0.04); }
.schedule-table tbody tr:last-child { border-bottom: none; }
.schedule-table tbody td {
  padding: .65rem 1rem;
  color: var(--text);
  font-family: 'JetBrains Mono', monospace;
  font-size: .8rem;
}
.schedule-table tbody td:first-child {
  font-family: 'Outfit', sans-serif;
  color: var(--muted);
  font-weight: 600;
}
.badge-month {
  display: inline-block;
  background: rgba(124,58,237,.2);
  border: 1px solid rgba(124,58,237,.3);
  border-radius: 6px;
  padding: .15rem .5rem;
  font-size: .72rem;
  color: var(--accent2);
}

/* ══════════════════════════════
   SUMMARY CARD
══════════════════════════════ */
.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: .85rem 0;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}
.summary-row:last-child { border-bottom: none; }
.summary-key {
  font-size: .82rem;
  color: var(--muted);
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: .5rem;
}
.summary-val {
  font-family: 'JetBrains Mono', monospace;
  font-size: .9rem;
  font-weight: 600;
  color: #fff;
}
.summary-val.highlight { color: var(--gold); font-size: 1rem; }

/* ══════════════════════════════
   FOOTER
══════════════════════════════ */
.app-footer {
  text-align: center;
  padding: 3rem 2rem 1rem;
  color: var(--muted);
  font-size: .78rem;
}
.app-footer strong { color: var(--accent2); }

/* plotly chart transparent */
.js-plotly-plot .plotly, .js-plotly-plot .plotly svg { background: transparent !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  NAVBAR
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="navbar">
  <div class="nav-brand">
    <div class="nav-logo">💎</div>
    <div class="nav-name">LoanIQ</div>
  </div>
  <div class="nav-pills">
    <div class="nav-pill active">EMI Calculator</div>
    <div class="nav-pill">Amortisation</div>
    <div class="nav-pill">Compare</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="app-shell">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-section">
  <div class="hero-badge">
    <div class="hero-badge-dot"></div>
    Smart Loan Intelligence
  </div>
  <h1 class="hero-title">Calculate Your<br>Perfect EMI</h1>
  <p class="hero-sub">Instant insights into your loan — interest, closing amount, and monthly repayments, all in one place.</p>
  <div class="hero-stats">
    <div class="h-stat">
      <div class="h-stat-value">100%</div>
      <div class="h-stat-label">Accurate</div>
    </div>
    <div class="h-stat">
      <div class="h-stat-value">0s</div>
      <div class="h-stat-label">Instant Result</div>
    </div>
    <div class="h-stat">
      <div class="h-stat-value">Free</div>
      <div class="h-stat-label">Always</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN GRID — LEFT (inputs) | RIGHT (live preview)
# ══════════════════════════════════════════════════════════════════════════════
left, right = st.columns([1, 1], gap="large")

with left:
    # ── Input card ──
    st.markdown("""
    <div class="g-card">
      <div class="card-header">
        <div class="card-icon icon-purple">📋</div>
        <div>
          <div class="card-label">Step 1</div>
          <div class="card-title-text">Loan Details</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    principle = st.number_input(
        "Principal Amount (₹)",
        min_value=0.0, max_value=100_000_000.0,
        value=500_000.0, step=10_000.0, format="%.0f",
        help="Total loan amount you borrowed"
    )
    st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)

    rate = st.number_input(
        "Monthly Interest Rate (%)",
        min_value=0.0, max_value=10.0,
        value=1.0, step=0.05, format="%.2f",
        help="Monthly rate (e.g. 1% per month = 12% per year)"
    )
    st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        time_years = st.number_input("Years", min_value=0, max_value=30, value=5, step=1)
    with c2:
        time_months = st.number_input("Months", min_value=0, max_value=11, value=0, step=1)

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
    calc   = st.button("⚡  Calculate EMI Now", use_container_width=True, type="primary")
    st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)
    reset  = st.button("↺  Reset", use_container_width=True, type="secondary")


# ══════════════════════════════════════════════════════════════════════════════
#  CALCULATION CORE
# ══════════════════════════════════════════════════════════════════════════════
def compute(p, r, ty, tm):
    rate_yearly   = r * 12
    time_total    = ty + (tm / 12)
    interest      = (p * rate_yearly * time_total) / 100
    final_closing = p + interest
    emi           = (final_closing / time_total) / 12 if time_total > 0 else 0
    return rate_yearly, time_total, interest, final_closing, emi

# Auto-compute for live preview in right panel
if principle > 0 and rate > 0 and (time_years > 0 or time_months > 0):
    rate_yearly, time_total, interest, final_closing, emi = compute(principle, rate, time_years, time_months)
    valid = True
else:
    valid = False

with right:
    if not valid:
        st.markdown("""
        <div class="g-card" style="min-height:340px; display:flex; align-items:center; justify-content:center; flex-direction:column; gap:1rem; text-align:center;">
          <div style="font-size:3rem">📊</div>
          <div style="color:#64748B; font-size:.95rem; line-height:1.6;">
            Fill in your loan details on the left<br>and your results will appear here.
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # EMI spotlight
        st.markdown(f"""
        <div class="emi-spotlight">
          <div class="emi-tag">Monthly EMI</div>
          <div class="emi-amount">₹ {emi:,.2f}</div>
          <div class="emi-sub">per month for {int(time_total*12)} months</div>
        </div>
        """, unsafe_allow_html=True)

        # 2×2 metric cards
        pct_p = (principle / final_closing) * 100
        pct_i = (interest  / final_closing) * 100
        st.markdown(f"""
        <div class="metrics-row">
          <div class="metric-card mc-purple">
            <div class="metric-icon">🏦</div>
            <div class="metric-label">Total Interest</div>
            <div class="metric-value">₹ {interest:,.0f}</div>
          </div>
          <div class="metric-card mc-gold">
            <div class="metric-icon">💰</div>
            <div class="metric-label">Final Payable</div>
            <div class="metric-value">₹ {final_closing:,.0f}</div>
          </div>
          <div class="metric-card mc-green">
            <div class="metric-icon">📅</div>
            <div class="metric-label">Total Months</div>
            <div class="metric-value">{int(time_total*12)} mo</div>
          </div>
          <div class="metric-card mc-pink">
            <div class="metric-icon">📈</div>
            <div class="metric-label">Annual Rate</div>
            <div class="metric-value">{rate_yearly:.1f}%</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Breakdown bar
        st.markdown(f"""
        <div class="g-card" style="padding:1.4rem 1.6rem;">
          <div class="breakdown-title" style="margin-bottom:.8rem;">Principal vs Interest</div>
          <div class="breakdown-bar-wrap">
            <div class="breakdown-bar" style="width:{pct_p:.1f}%"></div>
          </div>
          <div class="breakdown-legend">
            <div class="legend-item">
              <span class="legend-dot" style="background:linear-gradient(90deg,#7C3AED,#A78BFA)"></span>
              Principal &nbsp;<span>{pct_p:.1f}%</span>
            </div>
            <div class="legend-item">
              <span class="legend-dot" style="background:linear-gradient(90deg,#F59E0B,#FFD700)"></span>
              Interest &nbsp;<span>{pct_i:.1f}%</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  BELOW THE FOLD — shown only after Calculate is pressed
# ══════════════════════════════════════════════════════════════════════════════
if calc:
    if principle <= 0 or rate <= 0 or (time_years == 0 and time_months == 0):
        st.markdown("<div style='max-width:1200px;margin:1rem auto;padding:0 2rem'>", unsafe_allow_html=True)
        st.error("⚠️  Please fill in all fields with valid values before calculating.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        rate_yearly, time_total, interest, final_closing, emi = compute(principle, rate, time_years, time_months)
        total_months = int(time_total * 12)

        st.markdown("<div style='max-width:1200px;margin:2rem auto;padding:0 2rem'>", unsafe_allow_html=True)

        # ── Row: Donut chart + Summary ──────────────────────────────────────
        ch_col, sm_col = st.columns([1, 1], gap="large")

        with ch_col:
            st.markdown("""
            <div class="g-card">
              <div class="card-header">
                <div class="card-icon icon-gold">🥧</div>
                <div>
                  <div class="card-label">Visual</div>
                  <div class="card-title-text">Loan Composition</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            fig = go.Figure(go.Pie(
                labels=["Principal", "Interest"],
                values=[principle, interest],
                hole=.72,
                marker=dict(
                    colors=["#7C3AED", "#F59E0B"],
                    line=dict(color="#05050f", width=3)
                ),
                textinfo="none",
                hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<br>%{percent}<extra></extra>"
            ))
            fig.add_annotation(
                text=f"<b style='font-size:1.2em'>₹{final_closing/1e5:.1f}L</b><br><span style='color:#64748B;font-size:.7em'>TOTAL</span>",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="#ffffff", family="Outfit")
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=True,
                legend=dict(
                    orientation="h", x=0.5, y=-0.08, xanchor="center",
                    font=dict(color="#94A3B8", size=12, family="Outfit"),
                    bgcolor="rgba(0,0,0,0)"
                ),
                margin=dict(t=10, b=10, l=10, r=10),
                height=280
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with sm_col:
            rows_data = [
                ("💳", "Principal Borrowed",    f"₹ {principle:,.2f}", ""),
                ("📈", "Monthly Interest Rate", f"{rate:.2f}%",         ""),
                ("📅", "Annual Interest Rate",  f"{rate_yearly:.2f}%",  ""),
                ("🗓️", "Loan Tenure",           f"{time_years}y {time_months}m ({total_months} months)", ""),
                ("🏦", "Total Interest",        f"₹ {interest:,.2f}",  ""),
                ("💰", "Final Closing Amount",  f"₹ {final_closing:,.2f}", "highlight"),
                ("📆", "Monthly EMI",           f"₹ {emi:,.2f}",       "highlight"),
            ]
            rows_html = ""
            for icon, key, val, cls in rows_data:
                rows_html += f"""
                <div class="summary-row">
                  <div class="summary-key">{icon} {key}</div>
                  <div class="summary-val {cls}">{val}</div>
                </div>"""

            st.markdown(f"""
            <div class="g-card">
              <div class="card-header">
                <div class="card-icon icon-green">📋</div>
                <div>
                  <div class="card-label">Summary</div>
                  <div class="card-title-text">Full Breakdown</div>
                </div>
              </div>
              {rows_html}
            </div>
            """, unsafe_allow_html=True)

        # ── Amortisation schedule ─────────────────────────────────────────
        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="g-card">
          <div class="card-header">
            <div class="card-icon icon-pink">📆</div>
            <div>
              <div class="card-label">Amortisation</div>
              <div class="card-title-text">Monthly Payment Schedule</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Build schedule rows (cap at 24 for display)
        monthly_interest_rate = rate / 100
        balance = principle
        show_months = min(total_months, 24)
        rows_sched = ""
        for m in range(1, show_months + 1):
            m_interest  = balance * monthly_interest_rate
            m_principal = emi - m_interest
            balance     = max(balance - m_principal, 0)
            rows_sched += f"""
            <tr>
              <td><span class="badge-month">#{m:02d}</span></td>
              <td>₹ {emi:,.2f}</td>
              <td>₹ {m_principal:,.2f}</td>
              <td>₹ {m_interest:,.2f}</td>
              <td>₹ {balance:,.2f}</td>
            </tr>"""

        note = f"<div style='padding:.7rem 1rem;font-size:.75rem;color:#64748B;border-top:1px solid rgba(255,255,255,0.05)'>Showing first {show_months} of {total_months} months</div>" if total_months > 24 else ""
        st.markdown(f"""
        <div class="schedule-wrap">
          <table class="schedule-table">
            <thead>
              <tr>
                <th>Month</th>
                <th>EMI</th>
                <th>Principal</th>
                <th>Interest</th>
                <th>Balance</th>
              </tr>
            </thead>
            <tbody>{rows_sched}</tbody>
          </table>
          {note}
        </div>
        """, unsafe_allow_html=True)

        # ── Bar chart: principal vs interest paid each month ──────────────
        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
        months_list, p_paid, i_paid, balances = [], [], [], []
        bal = principle
        for m in range(1, show_months + 1):
            mi = bal * monthly_interest_rate
            mp = emi - mi
            bal = max(bal - mp, 0)
            months_list.append(f"M{m:02d}")
            p_paid.append(round(mp, 2))
            i_paid.append(round(mi, 2))
            balances.append(round(bal, 2))

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            name="Principal", x=months_list, y=p_paid,
            marker_color="#7C3AED", marker_line_width=0
        ))
        fig2.add_trace(go.Bar(
            name="Interest", x=months_list, y=i_paid,
            marker_color="#F59E0B", marker_line_width=0
        ))
        fig2.update_layout(
            barmode="stack",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Outfit", color="#64748B", size=11),
            legend=dict(
                orientation="h", x=1, xanchor="right", y=1.1,
                font=dict(color="#94A3B8"),
                bgcolor="rgba(0,0,0,0)"
            ),
            xaxis=dict(showgrid=False, tickfont=dict(size=10)),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)",
                       tickprefix="₹", tickfont=dict(size=10)),
            margin=dict(t=20, b=20, l=10, r=10),
            height=300,
            title=dict(
                text="Principal & Interest per Month",
                font=dict(color="#fff", size=14, family="Outfit"),
                x=0.01
            )
        )
        st.markdown('<div class="g-card" style="padding:1.5rem">', unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
  Built with <strong>LoanIQ</strong> · Results are indicative and for planning purposes only.
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)