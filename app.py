import os
import streamlit as st
import pandas as pd
from rapidfuzz import fuzz

# ==========================
# PAGE SETUP
# ==========================

st.set_page_config(
    page_title="Direct Buy Search",
    layout="wide"
)

# ==========================
# CUSTOM CSS
# ==========================

st.markdown("""
<style>

/* ==========================
   HIDE STREAMLIT DEFAULT UI
   ========================== */

footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
[data-testid="stToolbar"] { display: none !important; }
button[title="View fullscreen"] { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }
.stAppDeployButton { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
.viewerBadge_container__1QSob,
.viewerBadge_link__1S137,
.viewerBadge_text__1JaDK,
.viewerBadge_container__r5tak { display: none !important; }

/* ==========================
   PREMIUM APP COLORWAY
   ========================== */

:root {
    --navy: #071a33;
    --navy-2: #0a2a52;
    --ink: #10213b;
    --muted: #60718a;
    --line: #dbe7f3;
    --soft: #f7fbff;
    --teal: #00a6b4;
    --cyan: #38d5ee;
    --blue: #1577d2;
    --green: #0f9f65;
}

.stApp {
    background: #ffffff !important;
    color: var(--ink);
    font-family: Inter, "Segoe UI", Arial, sans-serif;
}

html,
body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main,
.main,
.block-container {
    background: #ffffff !important;
}

[data-testid="stAppViewContainer"] {
    background: #ffffff !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stSidebar"] {
    background: #ffffff !important;
}

.block-container {
    max-width: 1180px;
    padding-top: 0.75rem;
    padding-bottom: 5rem;
}

/* ==========================
   HERO - MATCHES THE MOCKUP
   ========================== */

.hero-wrap {
    max-width: 1120px;
    margin: 0.65rem auto 1.25rem auto;
    padding: 3.6rem 3.35rem;
    border-radius: 0 0 0 0;
    position: relative;
    overflow: hidden;
    color: #ffffff;
    background:
        radial-gradient(circle at 92% 58%, rgba(0,255,225,0.42), transparent 7rem),
        radial-gradient(circle at 10% 18%, rgba(0,191,255,0.25), transparent 10rem),
        linear-gradient(135deg, #07172e 0%, #092448 44%, #07345a 100%);
    box-shadow: 0 24px 55px rgba(7, 26, 51, 0.20);
    border: 1px solid rgba(151, 205, 255, 0.18);
}

.hero-wrap::before {
    content: "";
    position: absolute;
    inset: 0;
    background:
        linear-gradient(115deg, transparent 0 58%, rgba(56,213,238,0.07) 58% 59%, transparent 59% 100%),
        linear-gradient(155deg, transparent 0 64%, rgba(56,213,238,0.10) 64% 65%, transparent 65% 100%);
    pointer-events: none;
}

.hero-wrap::after {
    content: "";
    position: absolute;
    top: -6rem;
    right: -3rem;
    width: 38rem;
    height: 19rem;
    opacity: 0.42;
    background-image:
        linear-gradient(rgba(56,213,238,0.42) 1px, transparent 1px),
        linear-gradient(90deg, rgba(56,213,238,0.42) 1px, transparent 1px);
    background-size: 38px 38px;
    transform: perspective(460px) rotateX(60deg) rotateZ(-12deg);
    filter: drop-shadow(0 0 16px rgba(56,213,238,0.35));
    pointer-events: none;
}

.hero-content {
    position: relative;
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 1.75rem;
    flex-wrap: nowrap;
}

.hero-icon-card {
    width: 104px;
    height: 104px;
    min-width: 104px;
    border-radius: 24px;
    background:
        linear-gradient(145deg, rgba(56,213,238,0.28), rgba(0,166,180,0.16)),
        rgba(255,255,255,0.06);
    border: 1px solid rgba(86, 237, 255, 0.58);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow:
        0 0 0 1px rgba(255,255,255,0.08) inset,
        0 0 26px rgba(0, 222, 255, 0.25),
        0 20px 42px rgba(0,0,0,0.28);
}

.hero-icon-card svg {
    width: 58px;
    height: 58px;
    stroke: #dbfbff !important;
    filter: drop-shadow(0 0 12px rgba(56,213,238,0.65));
}

.hero-copy {
    text-align: left;
    max-width: 780px;
}

.hero-title {
    font-size: clamp(2.3rem, 4.2vw, 3.35rem);
    font-weight: 900;
    letter-spacing: -0.055em;
    margin: 0;
    line-height: 1.03;
    color: #ffffff;
    text-shadow: 0 12px 32px rgba(0,0,0,0.28);
}

.hero-subtitle {
    max-width: 680px;
    font-size: 1.05rem;
    margin-top: 0.9rem;
    color: #d8efff;
    font-weight: 650;
    line-height: 1.5;
}

/* ==========================
   NOTICE
   ========================== */

.directory-notice {
    max-width: 1120px;
    margin: 0 auto 1.1rem auto;
    padding: 1rem 1.25rem;
    border: 1px solid #c93b3b;
    border-radius: 12px;
    background: linear-gradient(180deg, #e24b4b 0%, #c92f2f 100%);
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 0.95rem;
    box-shadow: 0 12px 28px rgba(160, 24, 24, 0.18);
    font-size: 0.95rem;
    line-height: 1.45;
}

.directory-notice-icon {
    width: 30px;
    height: 30px;
    min-width: 30px;
    border-radius: 999px;
    background: rgba(255,255,255,0.18);
    color: #ffffff;
    display: grid;
    place-items: center;
    font-weight: 900;
    font-size: 0.95rem;
    box-shadow: 0 8px 18px rgba(120, 16, 16, 0.22);
    border: 1px solid rgba(255,255,255,0.28);
}

.directory-notice-text { font-weight: 700; color: #ffffff; }
.directory-notice a {
    color: #ffffff;
    font-weight: 900;
    text-decoration: underline;
}
.directory-notice a:hover { color: #ffe6e6; }

/* ==========================
   STREAMLIT CARDS
   ========================== */

[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 18px !important;
    border: 1px solid rgba(201, 219, 236, 0.96) !important;
    box-shadow:
        0 20px 50px rgba(7, 26, 51, 0.08),
        0 1px 0 rgba(255,255,255,0.92) inset !important;
    background:
        linear-gradient(180deg, rgba(255,255,255,0.98), rgba(250,253,255,0.98)) !important;
    padding: 1.2rem !important;
    overflow: hidden !important;
}

[data-testid="column"] { padding: 0.12rem 0.35rem; }
div[data-testid="stVerticalBlock"] > div { gap: 0.82rem; }

/* ==========================
   SECTION HEADERS
   ========================== */

.section-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: -0.25rem -0.25rem 1.15rem -0.25rem;
    padding: 1.25rem 1.35rem;
    border: 1px solid #cfe3f6;
    border-radius: 16px 16px 0 0;
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(circle at 2% 28%, rgba(56,213,238,0.16), transparent 10rem),
        linear-gradient(180deg, #f7fcff 0%, #eef7ff 100%);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.88);
}

.section-header::after {
    content: "";
    position: absolute;
    left: 0;
    bottom: 0;
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, rgba(0,166,180,0.35), rgba(21,119,210,0.12), transparent);
}

.card-title-wrap {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
}

.icon-bubble {
    width: 56px;
    height: 56px;
    min-width: 56px;
    border-radius: 15px;
    display: grid;
    place-items: center;
    background: linear-gradient(145deg, #057c8f, #0ab7c5);
    border: 1px solid rgba(255,255,255,0.58);
    color: #ffffff;
    box-shadow: 0 14px 28px rgba(0, 143, 165, 0.25);
}

.icon-bubble svg {
    width: 27px;
    height: 27px;
    stroke: #ffffff !important;
    display: block;
}

.card-title {
    font-size: 1.35rem;
    font-weight: 900;
    color: #10213b;
    margin: 0;
    letter-spacing: -0.04em;
}

.card-subtitle {
    color: #60718a;
    margin-top: 0.25rem;
    font-size: 0.93rem;
    line-height: 1.45;
    font-weight: 650;
}

.loaded-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: linear-gradient(90deg, #ddfff0, #f3fff9);
    border: 1px solid #a6ecc8;
    color: #057648;
    padding: 0.42rem 0.72rem;
    border-radius: 999px;
    font-weight: 900;
    font-size: 0.78rem;
    white-space: nowrap;
    box-shadow: 0 8px 16px rgba(15, 159, 101, 0.10);
}

.section-header.best-match-header { border-left: 4px solid #0aa6b7; }
.section-header.category-header { border-left: 4px solid #0aa6b7; }
.section-header.calculator-header { border-left: 4px solid #0aa6b7; }

.table-action-tip {
    display: flex;
    align-items: center;
    gap: 0.68rem;
    margin: 0.1rem 0 0.85rem 0;
    padding: 0.78rem 1rem;
    border: 1px solid #cfe3f6;
    border-radius: 13px;
    background: linear-gradient(180deg, #f9fcff 0%, #eef7ff 100%);
    color: #2c4565;
    font-size: 0.9rem;
    font-weight: 800;
    box-shadow: 0 10px 20px rgba(16, 64, 104, 0.045);
}

.table-action-tip span {
    width: 24px;
    height: 24px;
    min-width: 24px;
    border-radius: 999px;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, #0076d6, #12c6d1);
    color: #ffffff;
    font-weight: 900;
    font-size: 0.78rem;
}

.calculator-mini-note {
    margin: -0.25rem 0 1rem 0;
    padding: 0.75rem 0.95rem;
    border: 1px solid #dfeaf5;
    border-radius: 13px;
    background: #fbfdff;
    color: #5f7188;
    font-size: 0.88rem;
    font-weight: 700;
}

/* ==========================
   INPUTS / FILTERS
   ========================== */

div[data-baseweb="input"],
div[data-baseweb="select"] > div {
    border-radius: 13px !important;
    border: 1px solid #cfddeb !important;
    background: #ffffff !important;
    min-height: 48px !important;
    box-shadow:
        0 1px 0 rgba(255,255,255,0.95) inset,
        0 10px 24px rgba(7,26,51,0.045) !important;
}

div[data-baseweb="input"]:focus-within,
div[data-baseweb="select"] > div:focus-within {
    border-color: #33c9da !important;
    box-shadow:
        0 0 0 3px rgba(18, 198, 209, 0.12),
        0 12px 26px rgba(7,26,51,0.06) !important;
}

.stTextInput label,
.stSelectbox label,
.stMultiSelect label,
.stNumberInput label {
    font-weight: 850 !important;
    color: #273852 !important;
    font-size: 0.86rem !important;
}

.stTextInput input,
.stNumberInput input {
    min-height: 48px;
    background: #ffffff !important;
    color: #10213b !important;
}

.stTextInput input::placeholder { color: #96a5b6 !important; opacity: 1 !important; }
[data-baseweb="select"] input { background: #ffffff !important; }

/* ==========================
   DATA TABLES
   ========================== */

[data-testid="stDataFrame"] {
    border-radius: 15px !important;
    overflow: hidden !important;
    border: 1px solid #dce7f1 !important;
    box-shadow: 0 14px 28px rgba(7,26,51,0.055);
    background: #ffffff !important;
}

[data-testid="stDataFrame"] div[role="columnheader"] {
    font-weight: 900 !important;
    color: #253650 !important;
    background: #f4f9fd !important;
}

[data-testid="stDataFrame"] div[role="gridcell"] { color: #263a55 !important; }

/* ==========================
   METRIC CARDS
   ========================== */

[data-testid="stMetric"] {
    background:
        radial-gradient(circle at 15% 20%, rgba(56,213,238,0.09), transparent 4.5rem),
        linear-gradient(180deg, #ffffff, #fbfdff);
    border: 1px solid #dfe8f3;
    padding: 1.05rem;
    border-radius: 16px;
    box-shadow: 0 14px 28px rgba(7,26,51,0.055);
}

[data-testid="stMetricLabel"] {
    color: #617189 !important;
    font-weight: 800 !important;
}

[data-testid="stMetricValue"] {
    color: #10213b !important;
    font-weight: 900 !important;
    letter-spacing: -0.035em;
}

/* ==========================
   ALERTS / TEXT
   ========================== */

[data-testid="stAlert"] {
    border-radius: 13px !important;
    border: 1px solid rgba(120, 170, 230, 0.26) !important;
    box-shadow: 0 8px 20px rgba(7,26,51,0.035) !important;
}

h1, h2, h3 { letter-spacing: -0.04em; color: #10213b; }
h2 { margin-top: 0.75rem !important; font-weight: 900 !important; }
h3 { margin-top: 0.65rem !important; font-weight: 900 !important; }
hr { margin-top: 2rem; margin-bottom: 2rem; }

.product-image-card {
    border: 1px solid #dfe8f3;
    border-radius: 18px;
    padding: 1rem;
    background: linear-gradient(180deg, #ffffff, #fbfdff);
    box-shadow: 0 14px 28px rgba(7,26,51,0.055);
    text-align: center;
}
.product-image-title {
    font-weight: 900;
    color: #10213b;
    font-size: 1.05rem;
    margin-bottom: 0.55rem;
    letter-spacing: -0.03em;
}
.product-image-help {
    color: #657389;
    font-size: 0.84rem;
    margin-top: 0.55rem;
    line-height: 1.35;
}


/* ==========================
   STRONG SECTION DIVIDER
   Separates Best Match from Category Search
   ========================== */

.category-transition {
    max-width: 1120px;
    margin: 2.15rem auto 1.35rem auto;
    padding: 1.45rem 1.5rem 1.3rem 1.5rem;
    position: relative;
    text-align: center;
    overflow: hidden;
    border-radius: 18px;
    background:
        radial-gradient(circle at 50% -18%, rgba(52, 181, 255, 0.30), transparent 22%),
        radial-gradient(circle at 8% 105%, rgba(0, 170, 255, 0.30), transparent 22%),
        radial-gradient(circle at 92% 105%, rgba(0, 170, 255, 0.30), transparent 22%),
        linear-gradient(135deg, #082e67 0%, #062556 42%, #031c45 100%);
    border: 1px solid rgba(56, 177, 255, 0.28);
    box-shadow:
        0 18px 42px rgba(7,26,51,0.16),
        inset 0 1px 0 rgba(255,255,255,0.10),
        inset 0 -18px 40px rgba(0, 10, 28, 0.20);
}

.category-transition::before,
.category-transition::after {
    content: "";
    position: absolute;
    top: 50%;
    width: 26%;
    height: 3px;
    border-radius: 999px;
    background: linear-gradient(90deg, transparent, rgba(81, 210, 255, 0.95), rgba(81, 210, 255, 0.25));
    box-shadow: 0 0 12px rgba(81, 210, 255, 0.35);
}

.category-transition::before {
    left: 2.15rem;
}

.category-transition::after {
    right: 2.15rem;
    transform: rotate(180deg);
}

.category-transition-dots-left,
.category-transition-dots-right {
    position: absolute;
    top: 1rem;
    width: 9rem;
    height: 5.8rem;
    opacity: 0.55;
    background-image: radial-gradient(rgba(70, 206, 255, 0.70) 1.2px, transparent 1.2px);
    background-size: 10px 10px;
    pointer-events: none;
}

.category-transition-dots-left { left: 1.3rem; }
.category-transition-dots-right { right: 1.3rem; }

.category-transition-icon {
    width: 64px;
    height: 64px;
    border-radius: 999px;
    margin: -0.15rem auto 0.6rem auto;
    display: grid;
    place-items: center;
    color: #ffffff;
    background: radial-gradient(circle at 35% 30%, #1eb6ff 0%, #0b4aa0 55%, #062b67 100%);
    border: 1px solid rgba(255,255,255,0.42);
    box-shadow:
        0 18px 34px rgba(0, 45, 111, 0.38),
        0 0 0 10px rgba(43, 154, 255, 0.10),
        inset 0 1px 6px rgba(255,255,255,0.18);
    position: relative;
    z-index: 2;
}

.category-transition-icon svg {
    width: 27px;
    height: 27px;
    stroke: #ffffff !important;
}

.category-transition-title {
    position: relative;
    z-index: 2;
    color: #ffffff;
    font-size: 1.18rem;
    font-weight: 950;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 0;
    text-shadow: 0 2px 10px rgba(0,0,0,0.22);
}

.category-transition-subtitle {
    position: relative;
    z-index: 2;
    color: #e8f4ff;
    font-size: 0.98rem;
    font-weight: 750;
    margin-top: 0.35rem;
}

.category-zone-start {
    margin-top: 0.4rem;
}

.category-header {
    background:
        radial-gradient(circle at 2% 28%, rgba(0,166,180,0.22), transparent 10rem),
        linear-gradient(180deg, #f2fbfd 0%, #eaf8fb 100%) !important;
    border-color: rgba(0, 166, 180, 0.35) !important;
    border-left: 5px solid #0aa6b7 !important;
}


/* ==========================
   RESPONSIVE
   ========================== */

@media (max-width: 900px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; }
    .hero-wrap { padding: 2.2rem 1.3rem; }
    .hero-content { flex-wrap: wrap; }
    .hero-copy { text-align: left; }
}

@media (max-width: 600px) {
    .section-header { align-items: flex-start; }
    .hero-icon-card { width: 82px; height: 82px; min-width: 82px; }
    .hero-title { font-size: 2.05rem; }
}


/* ==========================
   HIDE STREAMLIT HEADING LINK ICONS
   Removes the small chain/link icons that appear beside headings
   ========================== */

a.anchor-link,
[data-testid="stMarkdownContainer"] a.anchor-link,
h1 a.anchor-link,
h2 a.anchor-link,
h3 a.anchor-link,
h4 a.anchor-link,
h5 a.anchor-link,
h6 a.anchor-link {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

[data-testid="stMarkdownContainer"] h1:hover a,
[data-testid="stMarkdownContainer"] h2:hover a,
[data-testid="stMarkdownContainer"] h3:hover a,
[data-testid="stMarkdownContainer"] h4:hover a,
[data-testid="stMarkdownContainer"] h5:hover a,
[data-testid="stMarkdownContainer"] h6:hover a {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# SVG ICONS
# ==========================

best_match_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" 
viewBox="0 0 24 24" fill="none" stroke="#2884bd" stroke-width="2" 
stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-search-icon lucide-search">
<path d="m21 21-4.34-4.34"/>
<circle cx="11" cy="11" r="8"/>
</svg>
"""

category_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" 
viewBox="0 0 24 24" fill="none" stroke="#2884bd" stroke-width="2" 
stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chart-bar-stacked-icon lucide-chart-bar-stacked">
<path d="M11 13v4"/>
<path d="M15 5v4"/>
<path d="M3 3v16a2 2 0 0 0 2 2h16"/>
<rect x="7" y="13" width="9" height="4" rx="1"/>
<rect x="7" y="5" width="12" height="4" rx="1"/>
</svg>
"""

calculator_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" 
viewBox="0 0 24 24" fill="none" stroke="#2884bd" stroke-width="2" 
stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-calculator-icon lucide-calculator">
<rect width="16" height="20" x="4" y="2" rx="2"/>
<line x1="8" x2="16" y1="6" y2="6"/>
<line x1="16" x2="16" y1="14" y2="18"/>
<path d="M16 10h.01"/>
<path d="M12 10h.01"/>
<path d="M8 10h.01"/>
<path d="M12 14h.01"/>
<path d="M8 14h.01"/>
<path d="M12 18h.01"/>
<path d="M8 18h.01"/>
</svg>
"""

# ==========================
# HERO
# ==========================

st.markdown("""
<div class="hero-wrap">
<div class="hero-content">
<div class="hero-icon-card">
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2884bd" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-package-search-icon lucide-package-search">
<path d="M12 22V12"/>
<path d="M20.27 18.27 22 20"/>
<path d="M21 10.498V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.729l7 4a2 2 0 0 0 2 .001l.98-.559"/>
<path d="M3.29 7 12 12l8.71-5"/>
<path d="m7.5 4.27 8.997 5.148"/>
<circle cx="18.5" cy="16.5" r="2.5"/>
</svg>
</div>
<div class="hero-copy">
<h1 class="hero-title">Direct Buy File Search</h1>
<div class="hero-subtitle">Search thousands of supplier products instantly by item number, manufacturer, brand, description, or category.</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# ==========================
# DIRECT BUY FILE DISCLAIMER
# ==========================

st.markdown("""
<div class="directory-notice">
    <div class="directory-notice-icon">i</div>
    <div class="directory-notice-text">
        Search thousands of supplier products currently available in the Direct Buy file.
        If an item is not found, visit the supplier's page in the
        <a href="/Members/Supplier-Directory" target="_blank">Supplier Directory</a>.
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================
# LOAD DATA
# ==========================

file_name = "cost list pricer V2.xlsx"
fallback_file_name = "cost list pricer.xlsx"

@st.cache_data
def load_data():
    # Use the new V2 file with images. If it is not found, fall back to the old file
    # so the app does not break while you are updating files in GitHub/Streamlit.
    selected_file = file_name if os.path.exists(file_name) else fallback_file_name
    df = pd.read_excel(selected_file)
    df.columns = df.columns.astype(str).str.strip()
    return df

df = load_data()

# Column A from the spreadsheet. This is shown to users as Vend Code
# instead of showing the internal Match Score.
vend_code_col = df.columns[0]

direct_cost_col = next(col for col in df.columns if "JUN 2026" in col and "Direct Cost" in col)
list_price_col = next(col for col in df.columns if "MAY 2026 List Price" in col)

# Image column support.
# Your V2 file has the product picture links in the "Images" column.
# This also handles common alternate column names in case the header changes later.
image_col = next(
    (
        col for col in df.columns
        if str(col).strip().lower() in [
            "images",
            "image",
            "picture",
            "pictures",
            "photo",
            "photos",
            "image url",
            "image_url",
            "product image",
            "product images"
        ]
    ),
    None
)

# Backup: Excel column AC is the 29th column, which is index 28 in Python.
# This makes the app still work if the column header is changed or blank.
if image_col is None and len(df.columns) >= 29:
    image_col = df.columns[28]


def get_product_image_urls(value):
    """Return one or more usable image URLs from an Excel cell."""
    if pd.isna(value):
        return []

    text_value = str(value).strip()
    if not text_value or text_value.lower() in ["nan", "none"]:
        return []

    # Handles one URL, multiple URLs separated by commas, semicolons, pipes, or line breaks.
    separators = ["\n", "\r", ";", "|", ","]
    parts = [text_value]

    for separator in separators:
        new_parts = []
        for part in parts:
            new_parts.extend(part.split(separator))
        parts = new_parts

    urls = []
    for part in parts:
        clean_url = part.strip().strip('"').strip("'")
        if clean_url.lower().startswith(("http://", "https://")):
            urls.append(clean_url)

    return urls

moq_col = "Min Ord Qty"
uom_col = "ISG UOM"

df[direct_cost_col] = pd.to_numeric(df[direct_cost_col], errors="coerce")
df[list_price_col] = pd.to_numeric(df[list_price_col], errors="coerce")

if moq_col in df.columns:
    df[moq_col] = pd.to_numeric(df[moq_col], errors="coerce")

# Speed helper: create a lowercase item number column once.
# This makes calculator lookups faster, especially when a row click sends an exact item number.
if "ISG Product Code" in df.columns:
    df["_item_code_search"] = df["ISG Product Code"].astype(str).str.strip().str.lower()

# ==========================
# SPEED HELPERS
# ==========================

def run_best_match_search(search_text, available_search_columns, direct_cost_column):
    """Run fuzzy Best Match Search only when the actual search text changes."""
    search_df = df.copy()

    search_df["Search Text"] = (
        search_df[available_search_columns]
        .fillna("")
        .astype(str)
        .agg(" ".join, axis=1)
    )

    search_df["Match Score"] = search_df["Search Text"].apply(
        lambda text: fuzz.token_set_ratio(search_text.lower(), text.lower())
    )

    best_results = search_df[search_df["Match Score"] >= 40].copy()

    best_results = best_results.sort_values(
        ["Match Score", direct_cost_column],
        ascending=[False, True]
    )

    return best_results

def get_item_matches(item_number_search):
    """Fast calculator lookup. Exact item-code matches are used first, then contains search."""
    clean_search = str(item_number_search).strip().lower()

    if not clean_search or "_item_code_search" not in df.columns:
        return pd.DataFrame()

    exact_matches = df[df["_item_code_search"] == clean_search].copy()

    if not exact_matches.empty:
        return exact_matches.sort_values(direct_cost_col, ascending=True)

    contains_matches = df[
        df["_item_code_search"].str.contains(clean_search, case=False, na=False, regex=False)
    ].copy()

    if not contains_matches.empty:
        contains_matches = contains_matches.sort_values(direct_cost_col, ascending=True)

    return contains_matches

# Set defaults so later sections do not break
selected_class = ""
results = pd.DataFrame()

# Keep each calculator independent across reruns.
# Important: Streamlit does not let us change a widget-backed session_state key
# after that widget has already been created in the same run.
# So Best Match and Category Search each get their own calculator item key.
for calculator_key in ["best_match", "category", "main"]:
    item_key = f"{calculator_key}_calculator_item_number"
    source_key = f"{calculator_key}_calculator_selected_source"
    pending_item_key = f"{calculator_key}_pending_calculator_item_number"
    pending_source_key = f"{calculator_key}_pending_calculator_selected_source"

    if item_key not in st.session_state:
        st.session_state[item_key] = ""

    if source_key not in st.session_state:
        st.session_state[source_key] = ""

    if pending_item_key not in st.session_state:
        st.session_state[pending_item_key] = ""

    if pending_source_key not in st.session_state:
        st.session_state[pending_source_key] = ""

# ==========================
# ITEM NUMBER COST CALCULATOR FUNCTION
# ==========================

def render_item_number_cost_calculator(calculator_location_key="main"):
    """Shows the item number calculator wherever this function is placed on the page."""
    st.write("")

    calculator_titles = {
        "best_match": "Item Number Cost Calculator",
        "category": "Item Number Cost Calculator",
        "main": "Item Number Cost Calculator"
    }

    calculator_title = calculator_titles.get(
        calculator_location_key,
        "Item Number Cost Calculator"
    )

    with st.container(border=True):
        st.markdown(f"""
        <div class="section-header calculator-header">
            <div class="icon-bubble">{calculator_icon}</div>
            <div>
                <div class="card-title">{calculator_title}</div>
                <div class="card-subtitle">Click a product row above or enter an item number to estimate direct cost, list price, and total price.</div>
            </div>
        </div>
        <div class="calculator-mini-note">This calculator is tied to this section, so Best Match Search and Category Search can each be used separately.</div>
        """, unsafe_allow_html=True)

        st.write("")

        item_state_key = f"{calculator_location_key}_calculator_item_number"
        source_state_key = f"{calculator_location_key}_calculator_selected_source"
        pending_item_key = f"{calculator_location_key}_pending_calculator_item_number"
        pending_source_key = f"{calculator_location_key}_pending_calculator_selected_source"

        # Apply clicked-row selections before the text input widget is created.
        # This keeps row-click auto-fill fast and prevents the calculator from going blank.
        if st.session_state.get(pending_item_key):
            st.session_state[item_state_key] = st.session_state[pending_item_key]
            st.session_state[source_state_key] = st.session_state.get(pending_source_key, "")
            st.session_state[pending_item_key] = ""
            st.session_state[pending_source_key] = ""

        selected_source = st.session_state.get(source_state_key, "")
        selected_calculator_item = st.session_state.get(item_state_key, "")

        if selected_calculator_item:
            if selected_source:
                st.success(f"Selected item from {selected_source}: {selected_calculator_item}")
            else:
                st.success(f"Selected item: {selected_calculator_item}")

        item_number_search = st.text_input(
            "Enter Item Number",
            placeholder="Example: ABFARB8012M",
            key=item_state_key
        )

        if item_number_search:
            # Search the full file, not just the selected category.
            # This allows Best Match Search clicks to work even when no category is selected.
            item_matches = get_item_matches(item_number_search)

            if not item_matches.empty:

                item_choices = (
                    item_matches["Manufacturer Name"].astype(str)
                    + " | "
                    + item_matches["ISG Product Code"].astype(str)
                    + " | "
                    + item_matches["Short Description"].astype(str)
                    + " | $"
                    + item_matches[direct_cost_col].round(2).astype(str)
                )

                selected_item_label = st.selectbox(
                    "Select matching item",
                    item_choices,
                    key=f"selected_item_label_{calculator_location_key}"
                )

                selected_item_index = item_choices[item_choices == selected_item_label].index[0]
                selected_item = item_matches.loc[selected_item_index]

                item_cost = selected_item[direct_cost_col]
                item_list_price = selected_item[list_price_col]
                item_moq = selected_item[moq_col] if moq_col in df.columns else 1
                item_uom = selected_item[uom_col] if uom_col in df.columns else "N/A"

                calculator_left, image_right = st.columns([3, 1], gap="large")

                with calculator_left:
                    st.markdown("### Item Details")

                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Direct Cost", f"${item_cost:,.2f}")
                    c2.metric("List Price", f"${item_list_price:,.2f}")
                    c3.metric("MOQ", f"{item_moq:,.0f}" if pd.notna(item_moq) else "N/A")
                    c4.metric("ISG UOM", str(item_uom))

                    st.markdown("#### Product")
                    st.write(selected_item["Short Description"])

                    quantity = st.number_input(
                        "Enter quantity you want to buy",
                        min_value=1,
                        value=int(item_moq) if pd.notna(item_moq) and item_moq > 0 else 1,
                        step=1,
                        key=f"quantity_{calculator_location_key}"
                    )

                    if pd.notna(item_moq) and quantity < item_moq:
                        st.warning(
                            f"This item has an MOQ of {item_moq:,.0f}. "
                            f"You entered {quantity:,}, so the estimate uses the MOQ."
                        )
                        billable_quantity = item_moq
                    else:
                        billable_quantity = quantity

                    total_direct_cost = billable_quantity * item_cost
                    total_list_price = billable_quantity * item_list_price
                    st.markdown("### Cost Estimate")

                    e1, e2, e3 = st.columns(3)
                    e1.metric("Billable Qty", f"{billable_quantity:,.0f}")
                    e2.metric("Total Direct Cost", f"${total_direct_cost:,.2f}")
                    e3.metric("Total List Price", f"${total_list_price:,.2f}")

                with image_right:
                    image_urls = get_product_image_urls(selected_item.get(image_col, "")) if image_col else []

                    if image_urls:
                        st.image(image_urls[0], use_container_width=True)

                        if len(image_urls) > 1:
                            image_choice = st.selectbox(
                                "More images",
                                options=list(range(1, len(image_urls) + 1)),
                                format_func=lambda image_number: f"Image {image_number}",
                                key=f"image_choice_{calculator_location_key}_{selected_item['ISG Product Code']}"
                            )
                            st.image(image_urls[image_choice - 1], use_container_width=True)

            else:
                st.warning("No item number matches found in the Direct Buy file.")

# ==========================
# BEST MATCH SEARCH
# ==========================

with st.container(border=True):
    st.markdown(f"""
    <div class="section-header best-match-header">
        <div class="icon-bubble">{best_match_icon}</div>
        <div>
            <div class="card-title-wrap">
                <div class="card-title">Best Match Search</div>
                <div class="loaded-pill">✅ Loaded {len(df):,} products</div>
            </div>
            <div class="card-subtitle">Search anything to find the most relevant products across categories, brands, descriptions, and item numbers.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    best_match_search = st.text_input(
        "Search anything — Example: clear report covers, blue folder, Avery binder",
        placeholder="Search anything — Example: clear report covers, blue folder, Avery binder"
    )

    search_columns = [
        "Product Class",
        "Brand Name",
        "Manufacturer Name",
        "ISG Product Code",
        "Short Description",
        "Long Description"
    ]

    available_search_columns = [col for col in search_columns if col in df.columns]

    if best_match_search:
        # Important speed fix:
        # Streamlit reruns the whole page after row clicks and quantity changes.
        # This stores the fuzzy Best Match results so the expensive fuzzy search
        # only reruns when the search box text changes.
        best_match_cache_key = f"{best_match_search}|{'|'.join(available_search_columns)}"

        if st.session_state.get("best_match_cache_key") != best_match_cache_key:
            st.session_state["best_match_cache_key"] = best_match_cache_key
            st.session_state["best_match_results"] = run_best_match_search(
                best_match_search,
                available_search_columns,
                direct_cost_col
            )

        best_results = st.session_state.get("best_match_results", pd.DataFrame())

        st.markdown("### Best Matching Products")
        st.markdown(
            """
            <div class="table-action-tip">
                <span>✓</span>
                Click any product row to auto-fill the Best Match Cost Calculator below.
            </div>
            """,
            unsafe_allow_html=True
        )

        best_display = best_results[
            [
                vend_code_col,
                "Product Class",
                "Manufacturer Name",
                "ISG Product Code",
                "Short Description",
                list_price_col,
                direct_cost_col
            ]
        ].head(100).copy()

        best_display = best_display.rename(columns={
            vend_code_col: "Vend Code",
            "Manufacturer Name": "Manufacturer",
            "ISG Product Code": "Product Code",
            "Short Description": "Description",
            list_price_col: "List Price",
            direct_cost_col: "Direct Cost"
        })

        if st.session_state.get("best_match_calculator_item_number"):
            st.success(
                f"Selected item from Best Match Search: "
                f"{st.session_state['best_match_calculator_item_number']}"
            )

        st.info(f"Showing top {min(len(best_results), 100)} best matches.")

        best_match_selection = st.dataframe(
            best_display,
            use_container_width=True,
            height=420,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
            key="best_match_products_table",
            column_config={
                "Vend Code": st.column_config.TextColumn("Vend Code"),
                "List Price": st.column_config.NumberColumn("List Price", format="$%.2f"),
                "Direct Cost": st.column_config.NumberColumn("Direct Cost", format="$%.2f"),
            }
        )

        if best_match_selection.selection.rows:
            selected_row_position = best_match_selection.selection.rows[0]
            selected_best_item_number = str(best_display.iloc[selected_row_position]["Product Code"])

            st.session_state["best_match_pending_calculator_item_number"] = selected_best_item_number
            st.session_state["best_match_pending_calculator_selected_source"] = "Best Match Search"

        # Calculator appears directly under the Best Matching Products table.
        render_item_number_cost_calculator("best_match")

st.markdown("""
<div class="category-transition">
    <div class="category-transition-dots-left"></div>
    <div class="category-transition-dots-right"></div>
    <div class="category-transition-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
        viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
        stroke-linecap="round" stroke-linejoin="round">
            <path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/>
            <path d="M3 6h18"/>
            <path d="M16 10a4 4 0 0 1-8 0"/>
        </svg>
    </div>
    <div class="category-transition-title">Browse by Category</div>
    <div class="category-transition-subtitle">Can’t find what you need above? Explore the full Direct Buy product catalog below.</div>
</div>
""", unsafe_allow_html=True)

# ==========================
# CATEGORY SEARCH
# ==========================

with st.container(border=True):
    st.markdown(f"""
    <div class="section-header category-header">
        <div class="icon-bubble">{category_icon}</div>
        <div>
            <div class="card-title">Category Search</div>
            <div class="card-subtitle">Browse by category, then narrow results by description, brand, and manufacturer.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    product_classes = sorted(
        df["Product Class"].dropna().astype(str).unique()
    )

    st.markdown("## Filters")

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        selected_class = st.selectbox(
            "Select Category",
            options=[""] + product_classes,
            index=0
        )

    description_search = ""
    selected_brands = []
    selected_manufacturers = []

    if selected_class:
        results = df[df["Product Class"] == selected_class].copy()
        results = results.sort_values(direct_cost_col, ascending=True)

        with filter_col2:
            description_search = st.text_input(
                "Search within products",
                placeholder="Example: clear, blue, letter"
            )

        if description_search:
            results = results[
                results["Short Description"].astype(str).str.contains(description_search, case=False, na=False)
                |
                results["Long Description"].astype(str).str.contains(description_search, case=False, na=False)
            ]

        with filter_col3:
            brand_options = sorted(results["Brand Name"].dropna().astype(str).unique())
            selected_brands = st.multiselect("Filter by Brand", brand_options)

        manufacturer_options = sorted(results["Manufacturer Name"].dropna().astype(str).unique())
        selected_manufacturers = st.multiselect("Filter by Manufacturer", manufacturer_options)

        if selected_brands:
            results = results[results["Brand Name"].astype(str).isin(selected_brands)]

        if selected_manufacturers:
            results = results[results["Manufacturer Name"].astype(str).isin(selected_manufacturers)]

        st.write("")
        st.markdown(f"## Best deals in {selected_class}")
        st.markdown(
            """
            <div class="table-action-tip">
                <span>✓</span>
                Click any product row to auto-fill the Category Search Cost Calculator below.
            </div>
            """,
            unsafe_allow_html=True
        )

        display_columns = [
            "Manufacturer Name",
            "ISG Product Code",
            "Short Description",
            list_price_col,
            direct_cost_col
        ]

        if moq_col in df.columns:
            display_columns.insert(3, moq_col)

        if uom_col in df.columns:
            display_columns.insert(4, uom_col)

        display_df = results[display_columns].copy()

        rename_map = {
            list_price_col: "List Price",
            direct_cost_col: "Direct Cost",
            "Manufacturer Name": "Manufacturer",
            "ISG Product Code": "Product Code",
            "Short Description": "Description",
            "Min Ord Qty": "MOQ"
        }

        display_df = display_df.rename(columns=rename_map)

        if st.session_state.get("category_calculator_item_number"):
            st.success(
                f"Selected item from Category Search: "
                f"{st.session_state['category_calculator_item_number']}"
            )

        st.info(f"Showing {len(results):,} products sorted from best deal to highest cost.")

        table_selection = st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
            key="cheapest_products_table",
            height=440,
            column_config={
                "MOQ": st.column_config.NumberColumn("MOQ", format="%d"),
                "List Price": st.column_config.NumberColumn("List Price", format="$%.2f"),
                "Direct Cost": st.column_config.NumberColumn("Direct Cost", format="$%.2f"),
            }
        )

        if table_selection.selection.rows:
            selected_row_position = table_selection.selection.rows[0]
            clicked_item_number = str(display_df.iloc[selected_row_position]["Product Code"])

            st.session_state["category_pending_calculator_item_number"] = clicked_item_number
            st.session_state["category_pending_calculator_selected_source"] = "Category Search"

        # Category Search has its own independent calculator.
        # This can be used at the same time as the Best Match calculator.
        render_item_number_cost_calculator("category")

    else:
        results = pd.DataFrame()

        st.write("")
        st.markdown("## Best deals in")
        st.markdown("# Select a category")
        st.info("Choose a category from the dropdown to view matching products. You can then narrow the list by description, brand, or manufacturer.")

