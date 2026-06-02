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

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

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
.viewerBadge_container__r5tak {
    display: none !important;
}

/* ==========================
   BASE
   ========================== */

* { font-family: 'Inter', sans-serif; box-sizing: border-box; }

.stApp {
    background: #f0f4f8;
    color: #1a2332;
}

.block-container {
    max-width: 100% !important;
    padding: 0 !important;
}

/* ==========================
   HERO BANNER
   ========================== */

.hero-wrap {
    background: linear-gradient(160deg, #0a2d5e 0%, #0d3d7a 40%, #1155a8 75%, #1a6bbf 100%);
    padding: 3.5rem 2rem 5rem 2rem;
    text-align: center;
    color: white;
    position: relative;
    overflow: hidden;
}

.hero-wrap::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
        radial-gradient(ellipse 60% 80% at 20% 50%, rgba(255,255,255,0.04) 0%, transparent 60%),
        radial-gradient(ellipse 50% 60% at 80% 30%, rgba(100,160,255,0.08) 0%, transparent 60%);
    pointer-events: none;
}

/* Decorative dots pattern */
.hero-wrap::after {
    content: '';
    position: absolute;
    inset: 0;
    background-image: radial-gradient(circle, rgba(255,255,255,0.06) 1px, transparent 1px);
    background-size: 28px 28px;
    pointer-events: none;
}

.hero-title {
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    margin: 0 0 0.7rem 0;
    line-height: 1.1;
    position: relative;
    z-index: 1;
}

.hero-subtitle {
    font-size: 1rem;
    margin: 0;
    opacity: 0.85;
    font-weight: 400;
    position: relative;
    z-index: 1;
}

/* ==========================
   PAGE CONTENT WRAPPER
   ========================== */

.page-content {
    max-width: 1120px;
    margin: 0 auto;
    padding: 0 1.5rem 4rem 1.5rem;
}

/* ==========================
   CARDS
   ========================== */

.card {
    background: #ffffff;
    border: 1px solid #e2eaf4;
    border-radius: 20px;
    padding: 1.5rem 1.6rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 2px 12px rgba(15, 30, 60, 0.06);
}

.float-card {
    margin-top: -2.8rem;
    position: relative;
    z-index: 5;
}

.card-header {
    display: flex;
    align-items: center;
    gap: 0.9rem;
    margin-bottom: 1rem;
}

.icon-circle {
    width: 44px;
    height: 44px;
    min-width: 44px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    background: linear-gradient(135deg, #e8f2ff, #dbeeff);
    border: 1.5px solid #c8deff;
    color: #2563eb;
}

.card-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #0f1e36;
    margin: 0 0 0.15rem 0;
    letter-spacing: -0.025em;
}

.card-desc {
    font-size: 0.875rem;
    color: #64748b;
    margin: 0;
    line-height: 1.4;
}

/* ==========================
   STATUS BAR (loaded products)
   ========================== */

.status-bar {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    background: #f0fdf6;
    border: 1px solid #bbf0d4;
    color: #16a34a;
    padding: 0.75rem 1rem;
    border-radius: 12px;
    font-weight: 600;
    font-size: 0.9rem;
}

.status-dot {
    width: 8px;
    height: 8px;
    background: #22c55e;
    border-radius: 50%;
    display: inline-block;
}

/* ==========================
   INPUTS - override streamlit
   ========================== */

div[data-baseweb="input"] input,
div[data-baseweb="input"] {
    border-radius: 10px !important;
    border: 1.5px solid #dde6f0 !important;
    background: #f8fafd !important;
    font-size: 0.9rem !important;
    color: #1a2332 !important;
}

div[data-baseweb="input"]:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
}

div[data-baseweb="select"] > div {
    border-radius: 10px !important;
    border: 1.5px solid #dde6f0 !important;
    background: #f8fafd !important;
    font-size: 0.9rem !important;
}

.stTextInput label,
.stSelectbox label,
.stMultiSelect label,
.stNumberInput label {
    font-weight: 600 !important;
    color: #334155 !important;
    font-size: 0.85rem !important;
    margin-bottom: 0.35rem !important;
}

/* Remove streamlit border from containers */
[data-testid="stVerticalBlockBorderWrapper"] {
    border: none !important;
    box-shadow: none !important;
    border-radius: 0 !important;
    padding: 0 !important;
    background: transparent !important;
}

/* ==========================
   DATAFRAME TABLE
   ========================== */

[data-testid="stDataFrame"] {
    border-radius: 14px !important;
    overflow: hidden !important;
    border: 1px solid #e8eef6 !important;
    box-shadow: none !important;
}

/* ==========================
   METRICS
   ========================== */

[data-testid="stMetric"] {
    background: #f8fafd;
    border: 1px solid #e5edf7;
    padding: 0.9rem 1rem;
    border-radius: 14px;
    box-shadow: none;
}

[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
}

[data-testid="stMetricValue"] {
    color: #0f1e36 !important;
    font-weight: 800 !important;
    font-size: 1.4rem !important;
}

/* ==========================
   INFO / SUCCESS ALERTS
   ========================== */

[data-testid="stAlert"] {
    border-radius: 12px !important;
}

/* ==========================
   BUTTONS
   ========================== */

.stButton > button {
    border-radius: 10px !important;
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    color: white !important;
    border: none !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.5rem !important;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25) !important;
}

/* ==========================
   FILTER PANEL (left column)
   ========================== */

.filter-panel {
    background: #ffffff;
    border: 1px solid #e2eaf4;
    border-radius: 16px;
    padding: 1.25rem;
    box-shadow: 0 2px 12px rgba(15, 30, 60, 0.05);
}

.filter-label {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: #94a3b8;
    margin-bottom: 0.75rem;
}

.tip-box {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 12px;
    padding: 0.85rem;
    margin-top: 1rem;
    font-size: 0.85rem;
    color: #1d4ed8;
    line-height: 1.45;
}

.tip-box strong {
    display: block;
    margin-bottom: 0.25rem;
    font-weight: 700;
}

/* ==========================
   RESULTS PANEL (right column)
   ========================== */

.results-header {
    margin-bottom: 0.5rem;
}

.results-subtitle {
    font-size: 0.85rem;
    color: #64748b;
    margin-top: 0.2rem;
}

.empty-state {
    text-align: center;
    padding: 2.5rem 1rem;
    color: #94a3b8;
}

.empty-state-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #334155;
    margin-bottom: 0.4rem;
}

.empty-state-desc {
    font-size: 0.9rem;
    color: #64748b;
}

/* ==========================
   FEATURE STRIP (bottom)
   ========================== */

.feature-strip {
    background: #ffffff;
    border: 1px solid #e2eaf4;
    border-radius: 20px;
    padding: 1.35rem 1.5rem;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.5rem;
    box-shadow: 0 2px 12px rgba(15, 30, 60, 0.05);
    margin-top: 1.25rem;
}

.feature-item {
    display: flex;
    align-items: flex-start;
    gap: 0.9rem;
    padding: 0.65rem 0.5rem;
}

.feature-icon {
    width: 44px;
    height: 44px;
    min-width: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
}

.fi-blue   { background: #eff6ff; color: #2563eb; }
.fi-green  { background: #f0fdf4; color: #16a34a; }
.fi-purple { background: #f5f3ff; color: #7c3aed; }
.fi-orange { background: #fff7ed; color: #ea580c; }

.feature-title {
    font-weight: 700;
    font-size: 0.9rem;
    color: #1e293b;
    margin-bottom: 0.2rem;
}

.feature-text {
    color: #64748b;
    font-size: 0.82rem;
    line-height: 1.4;
}

/* ==========================
   SECTION DIVIDER
   ========================== */

.section-gap { margin-top: 1.25rem; }

/* ==========================
   RESPONSIVE
   ========================== */

@media (max-width: 900px) {
    .feature-strip { grid-template-columns: repeat(2, 1fr); }
    .hero-title { font-size: 2rem; }
}

@media (max-width: 600px) {
    .feature-strip { grid-template-columns: 1fr; }
    .hero-title { font-size: 1.7rem; }
}

</style>
""", unsafe_allow_html=True)

# ==========================
# HERO
# ==========================

st.markdown("""
<div class="hero-wrap">
    <h1 class="hero-title">Explore Brands &amp; Categories</h1>
    <p class="hero-subtitle">Find the best products at the best prices.</p>
</div>
""", unsafe_allow_html=True)

# ==========================
# LOAD DATA
# ==========================

file_name = "cost list pricer.xlsx"

@st.cache_data
def load_data():
    df = pd.read_excel(file_name)
    df.columns = df.columns.astype(str).str.strip()
    return df

df = load_data()

direct_cost_col = next(col for col in df.columns if "JUN 2026" in col and "Direct Cost" in col)
list_price_col  = next(col for col in df.columns if "MAY 2026 List Price" in col)

moq_col = "Min Ord Qty"
uom_col = "ISG UOM"

df[direct_cost_col] = pd.to_numeric(df[direct_cost_col], errors="coerce")
df[list_price_col]  = pd.to_numeric(df[list_price_col],  errors="coerce")

if moq_col in df.columns:
    df[moq_col] = pd.to_numeric(df[moq_col], errors="coerce")

# ==========================
# DIRECT BUY SEARCH CARD (float)
# ==========================

st.markdown(f"""
<div style="max-width:1120px;margin:0 auto;padding:0 1.5rem;">
<div class="card float-card">
    <div class="card-header">
        <div class="icon-circle">🔎</div>
        <div>
            <div class="card-title">Direct Buy Search</div>
            <div class="card-desc">Search by category, descriptions, brand, manufacturer, or item number.</div>
        </div>
    </div>
    <div class="status-bar">
        <span class="status-dot"></span>
        Loaded {len(df):,} products
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================
# BEST MATCH SEARCH CARD
# ==========================

st.markdown("""
<div class="card">
    <div class="card-header">
        <div class="icon-circle">⭐</div>
        <div>
            <div class="card-title">Best Match Search</div>
            <div class="card-desc">Search anything to find the most relevant products.</div>
        </div>
    </div>
""", unsafe_allow_html=True)

best_match_col, illus_col = st.columns([0.65, 0.35])

search_columns = [
    "Product Class", "Brand Name", "Manufacturer Name",
    "ISG Product Code", "Short Description", "Long Description"
]
available_search_columns = [c for c in search_columns if c in df.columns]

with best_match_col:
    best_match_search = st.text_input(
        "Search anything",
        placeholder="Example: clear report covers, blue folder, Avery binder",
        label_visibility="collapsed"
    )
    st.caption("Example: clear report covers, blue folder, Avery binder")

with illus_col:
    st.markdown("""
    <div style="display:flex;justify-content:center;align-items:center;height:100%;padding:0.5rem;">
        <svg width="120" height="100" viewBox="0 0 120 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <!-- Box body -->
          <rect x="25" y="45" width="70" height="45" rx="5" fill="#e8f2ff" stroke="#bbd6ff" stroke-width="1.5"/>
          <!-- Box flap left -->
          <path d="M25 45 L35 25 L60 35 L60 45Z" fill="#dbeeff" stroke="#bbd6ff" stroke-width="1.5"/>
          <!-- Box flap right -->
          <path d="M95 45 L85 25 L60 35 L60 45Z" fill="#c7e0ff" stroke="#bbd6ff" stroke-width="1.5"/>
          <!-- Magnifier circle -->
          <circle cx="82" cy="30" r="16" fill="white" stroke="#93c5fd" stroke-width="2"/>
          <circle cx="82" cy="30" r="10" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5"/>
          <!-- Magnifier handle -->
          <line x1="93" y1="41" x2="103" y2="51" stroke="#93c5fd" stroke-width="3" stroke-linecap="round"/>
          <!-- Sparkles -->
          <circle cx="30" cy="22" r="3" fill="#bfdbfe" opacity="0.7"/>
          <circle cx="45" cy="12" r="2" fill="#93c5fd" opacity="0.5"/>
          <circle cx="16" cy="35" r="2" fill="#bfdbfe" opacity="0.6"/>
          <!-- Shine lines -->
          <line x1="60" y1="8" x2="60" y2="14" stroke="#93c5fd" stroke-width="1.5" stroke-linecap="round" opacity="0.5"/>
          <line x1="57" y1="11" x2="63" y2="11" stroke="#93c5fd" stroke-width="1.5" stroke-linecap="round" opacity="0.5"/>
        </svg>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # close .card

if best_match_search:
    search_df = df.copy()
    search_df["Search Text"] = (
        search_df[available_search_columns].fillna("").astype(str).agg(" ".join, axis=1)
    )
    search_df["Match Score"] = search_df["Search Text"].apply(
        lambda text: fuzz.token_set_ratio(best_match_search.lower(), text.lower())
    )
    best_results = search_df[search_df["Match Score"] >= 40].copy()
    best_results = best_results.sort_values(["Match Score", direct_cost_col], ascending=[False, True])

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"### Best Matching Products")

    best_display = best_results[[
        "Match Score", "Product Class", "Manufacturer Name",
        "ISG Product Code", "Short Description", list_price_col, direct_cost_col
    ]].head(100).copy()

    best_display[list_price_col]  = best_display[list_price_col].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "")
    best_display[direct_cost_col] = best_display[direct_cost_col].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "")

    st.dataframe(best_display, use_container_width=True)
    st.info(f"Showing top {min(len(best_results), 100)} best matches.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================
# CATEGORY SEARCH CARD
# ==========================

st.markdown("""
<div class="card">
    <div class="card-header">
        <div class="icon-circle">📁</div>
        <div>
            <div class="card-title">Category Search</div>
            <div class="card-desc">Browse and filter products by category, brand, and more.</div>
        </div>
    </div>
""", unsafe_allow_html=True)

product_classes = sorted(df["Product Class"].dropna().astype(str).unique())

filter_col, result_col = st.columns([0.30, 0.70], gap="large")

with filter_col:
    st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
    st.markdown('<div class="filter-label">Filter Categories</div>', unsafe_allow_html=True)

    product_class_search = st.text_input(
        "Filter Categories",
        placeholder="Type report, folder, binder...",
        label_visibility="collapsed",
        key="cat_filter_input"
    )

    filtered_classes = [
        pc for pc in product_classes
        if product_class_search.lower() in pc.lower()
    ] if product_class_search else product_classes

    st.markdown('<div class="filter-label" style="margin-top:0.85rem;">Select Category</div>', unsafe_allow_html=True)
    selected_class = st.selectbox(
        "Select Category",
        options=["Choose a category"] + filtered_classes,
        index=0,
        label_visibility="collapsed"
    )
    if selected_class == "Choose a category":
        selected_class = ""

    st.markdown('<div class="filter-label" style="margin-top:0.85rem;">Search within these products</div>', unsafe_allow_html=True)
    description_search = st.text_input(
        "Search within these products",
        placeholder="Example: clear, blue, letter, pressboard",
        label_visibility="collapsed",
        key="desc_search"
    )

    st.markdown('<div class="filter-label" style="margin-top:0.85rem;">Filter by Brand</div>', unsafe_allow_html=True)

    # Compute brand/mfr options based on category
    if selected_class:
        cat_results = df[df["Product Class"] == selected_class].copy()
        if description_search:
            cat_results = cat_results[
                cat_results["Short Description"].astype(str).str.contains(description_search, case=False, na=False)
                | cat_results["Long Description"].astype(str).str.contains(description_search, case=False, na=False)
            ]
        brand_options    = ["All Brands"]    + sorted(cat_results["Brand Name"].dropna().astype(str).unique())
        mfr_options      = ["All Manufacturers"] + sorted(cat_results["Manufacturer Name"].dropna().astype(str).unique())
    else:
        brand_options = ["All Brands"]
        mfr_options   = ["All Manufacturers"]

    selected_brand_dd = st.selectbox(
        "Filter by Brand",
        options=brand_options,
        label_visibility="collapsed",
        key="brand_dd"
    )

    st.markdown('<div class="filter-label" style="margin-top:0.85rem;">Filter by Manufacturer</div>', unsafe_allow_html=True)
    selected_mfr_dd = st.selectbox(
        "Filter by Manufacturer",
        options=mfr_options,
        label_visibility="collapsed",
        key="mfr_dd"
    )

    st.markdown("""
    <div class="tip-box">
        <strong>💡 Tip</strong>
        Use filters to narrow down results and find the best deals.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)  # close filter-panel

with result_col:
    if not selected_class:
        st.markdown("""
        <div style="padding:1rem 0;">
            <div style="font-size:0.85rem;color:#94a3b8;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;display:flex;align-items:center;gap:0.4rem;">
                🏷️ Best deals in
            </div>
            <div style="font-size:2rem;font-weight:800;color:#1e293b;margin:0.3rem 0 0.5rem 0;letter-spacing:-0.04em;">
                Select a category
            </div>
            <div style="font-size:0.88rem;color:#64748b;margin-bottom:1.5rem;">
                Click a row below to auto-fill the calculator.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Empty table placeholder with column headers
        empty_df = pd.DataFrame(columns=["Manufacturer Name", "Product Code", "Description", "MOQ", "UOM", "List Price", "Direct Cost"])
        st.dataframe(empty_df, use_container_width=True, height=200)

        st.markdown("""
        <div style="text-align:center;padding:2rem 1rem;">
            <svg width="70" height="70" viewBox="0 0 70 70" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="10" y="28" width="50" height="35" rx="4" fill="#e8f2ff" stroke="#bbd6ff" stroke-width="1.5"/>
              <path d="M10 28 L18 14 L35 21 L35 28Z" fill="#dbeeff" stroke="#bbd6ff" stroke-width="1.5"/>
              <path d="M60 28 L52 14 L35 21 L35 28Z" fill="#c7e0ff" stroke="#bbd6ff" stroke-width="1.5"/>
              <circle cx="35" cy="47" r="6" fill="#93c5fd" opacity="0.4"/>
            </svg>
            <div style="font-weight:700;color:#475569;margin-top:0.75rem;">Select a category to view products</div>
            <div style="font-size:0.85rem;color:#94a3b8;margin-top:0.25rem;">Start by choosing a category from the dropdown.</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================
# RESULTS (when category selected)
# ==========================

clicked_item_number = ""

if selected_class:
    results = df[df["Product Class"] == selected_class].copy()
    results = results.sort_values(direct_cost_col, ascending=True)

    if description_search:
        results = results[
            results["Short Description"].astype(str).str.contains(description_search, case=False, na=False)
            | results["Long Description"].astype(str).str.contains(description_search, case=False, na=False)
        ]

    if selected_brand_dd != "All Brands":
        results = results[results["Brand Name"].astype(str) == selected_brand_dd]

    if selected_mfr_dd != "All Manufacturers":
        results = results[results["Manufacturer Name"].astype(str) == selected_mfr_dd]

    with result_col:
        st.markdown(f"""
        <div class="results-header">
            <div style="font-size:0.85rem;color:#94a3b8;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;display:flex;align-items:center;gap:0.4rem;">
                🏷️ Best deals in
            </div>
            <div style="font-size:1.7rem;font-weight:800;color:#1e293b;margin:0.3rem 0 0.25rem 0;letter-spacing:-0.04em;">
                {selected_class}
            </div>
            <div class="results-subtitle">Click a row below to auto-fill the calculator.</div>
        </div>
        """, unsafe_allow_html=True)

        display_columns = ["Manufacturer Name", "ISG Product Code", "Short Description"]
        if moq_col in df.columns:
            display_columns.append(moq_col)
        if uom_col in df.columns:
            display_columns.append(uom_col)
        display_columns += [list_price_col, direct_cost_col]

        display_df = results[display_columns].copy()
        display_df[list_price_col]  = display_df[list_price_col].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "")
        display_df[direct_cost_col] = display_df[direct_cost_col].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "")

        table_selection = st.dataframe(
            display_df,
            use_container_width=True,
            on_select="rerun",
            selection_mode="single-row",
            key="cat_products_table"
        )

        if table_selection.selection.rows:
            row_pos = table_selection.selection.rows[0]
            clicked_item_number = display_df.iloc[row_pos]["ISG Product Code"]

        st.info(f"Showing {len(results):,} products sorted from best deal to highest cost.")

st.markdown("</div>", unsafe_allow_html=True)  # close .card (category search)

# ==========================
# ITEM NUMBER COST CALCULATOR
# ==========================

if selected_class:
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <div class="icon-circle">🧮</div>
            <div>
                <div class="card-title">Item Number Cost Calculator</div>
                <div class="card-desc">Click a product row above or enter an item number to estimate direct cost, list price, and savings.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if clicked_item_number:
        st.success(f"Selected item from table: {clicked_item_number}")

    item_number_search = st.text_input(
        "Enter Item Number",
        value=str(clicked_item_number) if clicked_item_number else "",
        placeholder="Example: ABFARB8012M"
    )

    if item_number_search:
        item_matches = results[
            results["ISG Product Code"].astype(str).str.contains(item_number_search, case=False, na=False)
        ].copy()

        if not item_matches.empty:
            item_matches = item_matches.sort_values(direct_cost_col, ascending=True)

            item_choices = (
                item_matches["Manufacturer Name"].astype(str) + " | "
                + item_matches["ISG Product Code"].astype(str) + " | "
                + item_matches["Short Description"].astype(str) + " | $"
                + item_matches[direct_cost_col].round(2).astype(str)
            )

            selected_item_label = st.selectbox("Select matching item", item_choices)
            selected_item_index = item_choices[item_choices == selected_item_label].index[0]
            selected_item = item_matches.loc[selected_item_index]

            item_cost       = selected_item[direct_cost_col]
            item_list_price = selected_item[list_price_col]
            item_moq        = selected_item[moq_col] if moq_col in df.columns else 1
            item_uom        = selected_item[uom_col] if uom_col in df.columns else "N/A"

            st.markdown("### Item Details")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Direct Cost",  f"${item_cost:,.2f}")
            c2.metric("List Price",   f"${item_list_price:,.2f}")
            c3.metric("MOQ",          f"{item_moq:,.0f}" if pd.notna(item_moq) else "N/A")
            c4.metric("ISG UOM",      str(item_uom))

            st.markdown("#### Product")
            st.write(selected_item["Short Description"])

            quantity = st.number_input(
                "Enter quantity you want to buy",
                min_value=1,
                value=int(item_moq) if pd.notna(item_moq) and item_moq > 0 else 1,
                step=1
            )

            if pd.notna(item_moq) and quantity < item_moq:
                st.warning(f"This item has an MOQ of {item_moq:,.0f}. You entered {quantity:,}, so the estimate uses the MOQ.")
                billable_quantity = item_moq
            else:
                billable_quantity = quantity

            total_direct_cost = billable_quantity * item_cost
            total_list_price  = billable_quantity * item_list_price
            savings_vs_list   = total_list_price - total_direct_cost

            st.markdown("### Cost Estimate")
            e1, e2, e3, e4 = st.columns(4)
            e1.metric("Billable Qty",       f"{billable_quantity:,.0f}")
            e2.metric("Total Direct Cost",  f"${total_direct_cost:,.2f}")
            e3.metric("Total List Price",   f"${total_list_price:,.2f}")
            e4.metric("Savings vs List",    f"${savings_vs_list:,.2f}")

        else:
            st.warning("No item number matches found in this category.")

    # ==========================
    # COMPARE PRODUCT
    # ==========================

    st.markdown("""
    <div class="card">
        <div class="card-header">
            <div class="icon-circle">⚖️</div>
            <div>
                <div class="card-title">Compare Product vs Best Deal</div>
                <div class="card-desc">Choose any product in the category and compare it against the lowest direct cost option.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not results.empty:
        best_deal_product = results.iloc[0]

        product_choices = (
            results["Manufacturer Name"].astype(str) + " | "
            + results["ISG Product Code"].astype(str) + " | "
            + results["Short Description"].astype(str) + " | $"
            + results[direct_cost_col].round(2).astype(str)
        )

        selected_product_label = st.selectbox("Choose a product to compare", product_choices)
        selected_index   = product_choices[product_choices == selected_product_label].index[0]
        selected_product = results.loc[selected_index]

        best_deal_cost = best_deal_product[direct_cost_col]
        selected_cost  = selected_product[direct_cost_col]
        savings        = selected_cost - best_deal_cost

        c1, c2, c3 = st.columns(3)
        c1.metric("Best Deal Cost",       f"${best_deal_cost:,.2f}")
        c2.metric("Selected Product Cost",f"${selected_cost:,.2f}")
        c3.metric("Potential Savings",    f"${savings:,.2f}")

        cc1, cc2 = st.columns(2)
        with cc1:
            st.markdown("#### Best Deal Product")
            st.write(best_deal_product["Short Description"])
        with cc2:
            st.markdown("#### Selected Product")
            st.write(selected_product["Short Description"])

# ==========================
# BOTTOM FEATURE STRIP
# ==========================

st.markdown("""
<div class="feature-strip">
    <div class="feature-item">
        <div class="feature-icon fi-blue">🏷️</div>
        <div>
            <div class="feature-title">Best Prices</div>
            <div class="feature-text">Find the lowest direct costs</div>
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-icon fi-green">🛡️</div>
        <div>
            <div class="feature-title">Trusted Brands</div>
            <div class="feature-text">Top manufacturers you know</div>
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-icon fi-purple">📦</div>
        <div>
            <div class="feature-title">Wide Selection</div>
            <div class="feature-text">Tens of thousands of products</div>
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-icon fi-orange">⚡</div>
        <div>
            <div class="feature-title">Fast &amp; Easy</div>
            <div class="feature-text">Quick search and smart filters</div>
        </div>
    </div>
</div>
</div>
""", unsafe_allow_html=True)
