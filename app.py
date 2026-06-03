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

:root {
    --isg-navy: #0B5E8E;
    --isg-blue: #0A84C6;
    --isg-aqua: #6ECFE3;
    --isg-green: #78BE5A;
    --isg-slate: #55707D;
    --isg-ink: #173447;
    --isg-soft-blue: #EEF9FC;
    --isg-soft-green: #F3FAEF;
}

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
   PAGE BACKGROUND
   Seamless Kentico white blend
   ========================== */

.stApp {
    background: linear-gradient(180deg, #ffffff 0%, #f8fcfd 100%) !important;
    color: var(--isg-ink);
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
    max-width: 1220px;
    padding-top: 0rem;
    padding-bottom: 5rem;
}

/* ==========================
   HERO
   ========================== */

.hero-wrap {
    background:
        radial-gradient(circle at 10% 18%, rgba(120, 190, 90, 0.16), transparent 28%),
        radial-gradient(circle at 88% 12%, rgba(110, 207, 227, 0.22), transparent 31%),
        linear-gradient(135deg, #ffffff 0%, #f4fbfd 45%, #eaf8fb 100%);
    border: 1px solid #cdeef5;
    border-radius: 28px;
    padding: 3.1rem 2.2rem 3.1rem 2.2rem;
    margin: 1.3rem auto 1.8rem auto;
    text-align: center;
    color: var(--isg-ink);
    box-shadow: 0 20px 52px rgba(11, 94, 142, 0.09);
    position: relative;
    overflow: hidden;
    max-width: 1120px;
}

.hero-wrap::before {
    content: "";
    position: absolute;
    inset: 0;
    background:
        linear-gradient(160deg, transparent 48%, rgba(110,207,227,0.14) 49%, transparent 51%),
        linear-gradient(170deg, transparent 57%, rgba(120,190,90,0.10) 58%, transparent 60%);
    pointer-events: none;
}

.hero-wrap::after {
    content: "";
    position: absolute;
    left: 5%;
    right: 5%;
    bottom: 0;
    height: 5px;
    background: linear-gradient(90deg, transparent, rgba(110,207,227,0.70), rgba(120,190,90,0.45), transparent);
    border-radius: 999px 999px 0 0;
}

.hero-content {
    position: relative;
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.45rem;
    flex-wrap: wrap;
}

.hero-icon-card {
    width: 104px;
    height: 104px;
    min-width: 104px;
    border-radius: 28px;
    background: linear-gradient(135deg, #ffffff, #eef9fc);
    border: 1px solid #c8edf5;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow:
        0 16px 34px rgba(10,132,198,0.12),
        inset 0 1px 0 rgba(255,255,255,0.9);
}

.hero-icon-card svg {
    width: 60px;
    height: 60px;
    filter: drop-shadow(0 8px 14px rgba(10,132,198,0.14));
}

.hero-copy {
    text-align: left;
    max-width: 820px;
}

.hero-title {
    font-size: clamp(2.25rem, 5vw, 4rem);
    font-weight: 900;
    letter-spacing: -0.065em;
    margin: 0;
    line-height: 1.05;
    color: var(--isg-ink);
    text-shadow: none;
}

.hero-subtitle {
    font-size: 1.08rem;
    margin-top: 0.9rem;
    color: var(--isg-slate);
    opacity: 1;
    font-weight: 600;
    text-shadow: none;
}

/* ==========================
   CARD HEADER STYLE
   ========================== */

.section-header {
    display: flex;
    align-items: center;
    gap: 0.95rem;
    margin: 0.15rem 0.15rem 1.2rem 0.15rem;
    padding: 1.25rem 1.45rem;
    background:
        linear-gradient(90deg, rgba(120,190,90,0.11) 0%, rgba(110,207,227,0.16) 38%, rgba(255,255,255,0.88) 100%),
        linear-gradient(180deg, #f6fcfd 0%, #eef9fc 100%);
    border: 1px solid #d2edf4;
    border-bottom-color: #c0e6f0;
    border-radius: 17px 17px 0 0;
    position: relative;
    overflow: hidden;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.88);
}

.section-header::before,
.section-header::after {
    display: none;
    content: none;
}

.section-header > * {
    position: relative;
    z-index: 2;
}

.card-title-row {
    display: flex;
    align-items: center;
    gap: 0.95rem;
    margin-bottom: 0.55rem;
}

.card-title-wrap {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
}

.icon-bubble {
    width: 50px;
    height: 50px;
    min-width: 50px;
    border-radius: 16px;
    display: grid;
    place-items: center;
    background: rgba(255,255,255,0.86);
    border: 1px solid #cdeef5;
    color: var(--isg-blue);
    font-size: 1.4rem;
    box-shadow: none;
}

.icon-bubble svg {
    width: 24px;
    height: 24px;
    display: block;
}

.card-title {
    font-size: 1.5rem;
    font-weight: 850;
    color: var(--isg-ink);
    margin: 0;
    letter-spacing: -0.04em;
}

.card-subtitle {
    color: var(--isg-slate);
    margin-top: 0.25rem;
    font-size: 0.96rem;
    line-height: 1.45;
}

.loaded-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: linear-gradient(90deg, #edf9e9, #f7fcf5);
    border: 1px solid #c9eec0;
    color: #3f8f2f;
    padding: 0.42rem 0.72rem;
    border-radius: 999px;
    font-weight: 850;
    font-size: 0.82rem;
    white-space: nowrap;
    box-shadow: 0 6px 14px rgba(120, 190, 90, 0.10);
}

/* ==========================
   STREAMLIT CONTAINERS
   Softer white cards
   ========================== */

[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 22px !important;
    border: 1px solid rgba(199, 225, 232, 0.95) !important;
    box-shadow: 0 10px 28px rgba(11, 94, 142, 0.045) !important;
    background: #ffffff !important;
    padding: 1.35rem !important;
}

/* More breathing room */
[data-testid="column"] {
    padding: 0.15rem 0.35rem;
}

div[data-testid="stVerticalBlock"] > div {
    gap: 0.85rem;
}

/* ==========================
   BRIGHTER INPUTS
   ========================== */

div[data-baseweb="input"] {
    border-radius: 14px !important;
    border: 1px solid #c8dfe8 !important;
    background: #ffffff !important;
    min-height: 48px !important;
    box-shadow:
        0 1px 0 rgba(255,255,255,0.95) inset,
        0 8px 20px rgba(16,24,40,0.035) !important;
}

div[data-baseweb="select"] > div {
    border-radius: 14px !important;
    border-color: #c8dfe8 !important;
    background: #ffffff !important;
    min-height: 48px !important;
    box-shadow:
        0 1px 0 rgba(255,255,255,0.95) inset,
        0 8px 20px rgba(16,24,40,0.035) !important;
}

div[data-baseweb="input"]:focus-within,
div[data-baseweb="select"] > div:focus-within {
    border-color: var(--isg-aqua) !important;
    box-shadow:
        0 0 0 3px rgba(110, 207, 227, 0.20),
        0 10px 24px rgba(16,24,40,0.05) !important;
}

.stTextInput label,
.stSelectbox label,
.stMultiSelect label,
.stNumberInput label {
    font-weight: 800 !important;
    color: var(--isg-ink) !important;
    font-size: 0.9rem !important;
}

.stTextInput input,
.stNumberInput input {
    min-height: 48px;
    background: #ffffff !important;
    color: var(--isg-ink) !important;
}

.stTextInput input::placeholder {
    color: #8a97a8 !important;
    opacity: 1 !important;
}

/* Multiselect selected/input area */
[data-baseweb="select"] input {
    background: #ffffff !important;
}

/* ==========================
   DATA TABLES
   ========================== */

[data-testid="stDataFrame"] {
    border-radius: 17px !important;
    overflow: hidden !important;
    border: 1px solid #d4e9ef !important;
    box-shadow: 0 10px 24px rgba(16,24,40,0.04);
    background: #ffffff !important;
}

/* ==========================
   METRICS
   ========================== */

[data-testid="stMetric"] {
    background: linear-gradient(180deg, #ffffff, #f7fcfd);
    border: 1px solid #d4e9ef;
    padding: 1rem;
    border-radius: 17px;
    box-shadow: 0 10px 26px rgba(16,24,40,0.04);
}

[data-testid="stMetricLabel"] {
    color: var(--isg-slate) !important;
    font-weight: 750 !important;
}

[data-testid="stMetricValue"] {
    color: var(--isg-ink) !important;
    font-weight: 850 !important;
}

/* ==========================
   INFO / SUCCESS / WARNING BOXES
   ========================== */

[data-testid="stAlert"] {
    border-radius: 15px !important;
    border: 1px solid rgba(110, 207, 227, 0.28) !important;
}

/* ==========================
   TEXT CLEANUP
   ========================== */

h1, h2, h3 {
    letter-spacing: -0.035em;
}

h2 {
    margin-top: 0.8rem !important;
}

h3 {
    margin-top: 0.7rem !important;
}

hr {
    margin-top: 2rem;
    margin-bottom: 2rem;
}

/* ==========================
   RESPONSIVE
   ========================== */

@media (max-width: 900px) {
    .hero-wrap {
        margin-left: -1rem;
        margin-right: -1rem;
        padding-bottom: 4rem;
    }
}

@media (max-width: 600px) {
    .card-title-row,
    .section-header {
        align-items: flex-start;
    }

    .hero-title {
        font-size: 2.2rem;
    }
}

</style>
""", unsafe_allow_html=True)

# ==========================
# SVG ICONS
# ==========================

best_match_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" 
viewBox="0 0 24 24" fill="none" stroke="#0A84C6" stroke-width="2" 
stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-search-icon lucide-search">
<path d="m21 21-4.34-4.34"/>
<circle cx="11" cy="11" r="8"/>
</svg>
"""

category_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" 
viewBox="0 0 24 24" fill="none" stroke="#0A84C6" stroke-width="2" 
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
viewBox="0 0 24 24" fill="none" stroke="#0A84C6" stroke-width="2" 
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
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0A84C6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-package-search-icon lucide-package-search">
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
list_price_col = next(col for col in df.columns if "MAY 2026 List Price" in col)

moq_col = "Min Ord Qty"
uom_col = "ISG UOM"

df[direct_cost_col] = pd.to_numeric(df[direct_cost_col], errors="coerce")
df[list_price_col] = pd.to_numeric(df[list_price_col], errors="coerce")

if moq_col in df.columns:
    df[moq_col] = pd.to_numeric(df[moq_col], errors="coerce")

# Set defaults so later sections do not break
selected_class = ""
results = pd.DataFrame()
clicked_item_number = ""

# ==========================
# BEST MATCH SEARCH
# ==========================

with st.container(border=True):
    st.markdown(f"""
    <div class="section-header">
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
        "Search anything",
        placeholder="Example: clear report covers, blue folder, Avery binder"
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
        search_df = df.copy()

        search_df["Search Text"] = (
            search_df[available_search_columns]
            .fillna("")
            .astype(str)
            .agg(" ".join, axis=1)
        )

        search_df["Match Score"] = search_df["Search Text"].apply(
            lambda text: fuzz.token_set_ratio(best_match_search.lower(), text.lower())
        )

        best_results = search_df[search_df["Match Score"] >= 40].copy()

        best_results = best_results.sort_values(
            ["Match Score", direct_cost_col],
            ascending=[False, True]
        )

        st.markdown("### Best Matching Products")

        best_display = best_results[
            [
                "Match Score",
                "Product Class",
                "Manufacturer Name",
                "ISG Product Code",
                "Short Description",
                list_price_col,
                direct_cost_col
            ]
        ].head(100).copy()

        best_display[list_price_col] = best_display[list_price_col].apply(
            lambda x: f"${x:,.2f}" if pd.notna(x) else ""
        )

        best_display[direct_cost_col] = best_display[direct_cost_col].apply(
            lambda x: f"${x:,.2f}" if pd.notna(x) else ""
        )

        st.dataframe(best_display, use_container_width=True, height=420)

        st.info(f"Showing top {min(len(best_results), 100)} best matches.")

st.write("")

# ==========================
# CATEGORY SEARCH
# ==========================

with st.container(border=True):
    st.markdown(f"""
    <div class="section-header">
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
        st.caption("Click a row below to auto-fill the calculator.")

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

        if "List Price" in display_df.columns:
            display_df["List Price"] = display_df["List Price"].apply(
                lambda x: f"${x:,.2f}" if pd.notna(x) else ""
            )

        if "Direct Cost" in display_df.columns:
            display_df["Direct Cost"] = display_df["Direct Cost"].apply(
                lambda x: f"${x:,.2f}" if pd.notna(x) else ""
            )

        table_selection = st.dataframe(
            display_df,
            use_container_width=True,
            on_select="rerun",
            selection_mode="single-row",
            key="cheapest_products_table",
            height=440
        )

        if table_selection.selection.rows:
            selected_row_position = table_selection.selection.rows[0]
            clicked_item_number = display_df.iloc[selected_row_position]["Product Code"]

        st.info(f"Showing {len(results):,} products sorted from best deal to highest cost.")

    else:
        clicked_item_number = ""
        results = pd.DataFrame()

        st.write("")
        st.markdown("## Best deals in")
        st.markdown("# Select a category")
        st.info("Choose a category from the dropdown to view matching products.")

# ==========================
# ITEM NUMBER COST CALCULATOR
# ==========================

if selected_class:
    st.write("")

    with st.container(border=True):
        st.markdown(f"""
        <div class="section-header">
            <div class="icon-bubble">{calculator_icon}</div>
            <div>
                <div class="card-title">Item Number Cost Calculator</div>
                <div class="card-subtitle">Click a product row above or enter an item number to estimate direct cost, list price, and savings.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        if clicked_item_number:
            st.success(f"Selected item from table: {clicked_item_number}")

        item_number_search = st.text_input(
            "Enter Item Number",
            value=str(clicked_item_number) if clicked_item_number else "",
            placeholder="Example: ABFARB8012M"
        )

        if item_number_search:
            item_matches = results[
                results["ISG Product Code"]
                .astype(str)
                .str.contains(item_number_search, case=False, na=False)
            ].copy()

            if not item_matches.empty:
                item_matches = item_matches.sort_values(direct_cost_col, ascending=True)

                item_choices = (
                    item_matches["Manufacturer Name"].astype(str)
                    + " | "
                    + item_matches["ISG Product Code"].astype(str)
                    + " | "
                    + item_matches["Short Description"].astype(str)
                    + " | $"
                    + item_matches[direct_cost_col].round(2).astype(str)
                )

                selected_item_label = st.selectbox("Select matching item", item_choices)

                selected_item_index = item_choices[item_choices == selected_item_label].index[0]
                selected_item = item_matches.loc[selected_item_index]

                item_cost = selected_item[direct_cost_col]
                item_list_price = selected_item[list_price_col]
                item_moq = selected_item[moq_col] if moq_col in df.columns else 1
                item_uom = selected_item[uom_col] if uom_col in df.columns else "N/A"

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
                    step=1
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
                savings_vs_list = total_list_price - total_direct_cost

                st.markdown("### Cost Estimate")

                e1, e2, e3, e4 = st.columns(4)
                e1.metric("Billable Qty", f"{billable_quantity:,.0f}")
                e2.metric("Total Direct Cost", f"${total_direct_cost:,.2f}")
                e3.metric("Total List Price", f"${total_list_price:,.2f}")
                e4.metric("Savings vs List", f"${savings_vs_list:,.2f}")

            else:
                st.warning("No item number matches found in this category.")
