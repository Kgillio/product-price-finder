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
.viewerBadge_container__r5tak {
    display: none !important;
}

/* ==========================
   PAGE BACKGROUND
   ========================== */

.stApp {
    background:
        radial-gradient(circle at top left, rgba(0, 123, 255, 0.10), transparent 30%),
        radial-gradient(circle at top right, rgba(0, 82, 155, 0.10), transparent 35%),
        linear-gradient(180deg, #f5f8fc 0%, #ffffff 45%, #f7f9fc 100%);
    color: #162033;
}

.block-container {
    max-width: 1180px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}

/* ==========================
   HERO
   ========================== */

.hero-wrap {
    background:
        linear-gradient(135deg, rgba(0, 73, 135, 0.96), rgba(0, 122, 204, 0.86)),
        url("https://images.unsplash.com/photo-1586281380349-632531db7ed4?auto=format&fit=crop&w=1600&q=80");
    background-size: cover;
    background-position: center;
    border-radius: 0 0 28px 28px;
    padding: 3.5rem 2rem 5.5rem 2rem;
    margin: -1.5rem -2rem 0 -2rem;
    text-align: center;
    color: white;
    box-shadow: 0 24px 60px rgba(0, 55, 110, 0.18);
}

.hero-title {
    font-size: clamp(2.2rem, 5vw, 4.2rem);
    font-weight: 850;
    letter-spacing: -0.06em;
    margin: 0;
    line-height: 1.05;
}

.hero-subtitle {
    font-size: 1.15rem;
    margin-top: 1rem;
    opacity: 0.92;
    font-weight: 450;
}

.hero-pills {
    display: flex;
    justify-content: center;
    gap: 0.8rem;
    flex-wrap: wrap;
    margin-top: 1.5rem;
}

.hero-pill {
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.25);
    color: white;
    padding: 0.55rem 0.9rem;
    border-radius: 999px;
    font-size: 0.88rem;
    backdrop-filter: blur(10px);
}

/* ==========================
   CARDS
   ========================== */

.section-card {
    background: rgba(255,255,255,0.94);
    border: 1px solid rgba(214, 224, 238, 0.95);
    box-shadow: 0 18px 45px rgba(15, 33, 58, 0.08);
    border-radius: 22px;
    padding: 1.5rem;
    margin-bottom: 1.55rem;
}

.float-card {
    margin-top: -3.4rem;
    position: relative;
    z-index: 3;
}

.card-title-row {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    margin-bottom: 0.25rem;
}

.icon-bubble {
    width: 46px;
    height: 46px;
    border-radius: 16px;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, #e8f2ff, #f3f8ff);
    border: 1px solid #d8e8ff;
    color: #006fd6;
    font-size: 1.45rem;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.8);
}

.card-title {
    font-size: 1.45rem;
    font-weight: 800;
    color: #182235;
    margin: 0;
    letter-spacing: -0.03em;
}

.card-subtitle {
    color: #637083;
    margin-top: 0.15rem;
    font-size: 0.95rem;
}

/* ==========================
   STATUS BAR
   ========================== */

.status-bar {
    background: linear-gradient(90deg, #e8fff1, #f0fff7);
    border: 1px solid #c9f0d9;
    color: #09803d;
    padding: 0.85rem 1rem;
    border-radius: 14px;
    margin-top: 1.2rem;
    font-weight: 700;
    font-size: 0.95rem;
}

/* ==========================
   STREAMLIT INPUTS
   ========================== */

div[data-baseweb="input"] {
    border-radius: 13px !important;
    border: 1px solid #d9e2ef !important;
    background: #ffffff !important;
    box-shadow: 0 1px 0 rgba(16,24,40,0.02);
}

div[data-baseweb="select"] > div {
    border-radius: 13px !important;
    border-color: #d9e2ef !important;
    background: #ffffff !important;
}

.stTextInput label,
.stSelectbox label,
.stMultiSelect label,
.stNumberInput label {
    font-weight: 750 !important;
    color: #25324a !important;
    font-size: 0.9rem !important;
}

.stTextInput input,
.stNumberInput input {
    min-height: 44px;
}

/* ==========================
   BUTTONS
   ========================== */

.stButton > button {
    border-radius: 13px !important;
    border: 1px solid #006fd6 !important;
    background: linear-gradient(135deg, #0077df, #005ea8) !important;
    color: white !important;
    font-weight: 750 !important;
    box-shadow: 0 10px 24px rgba(0, 111, 214, 0.18);
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 14px 30px rgba(0, 111, 214, 0.25);
}

/* ==========================
   DATAFRAMES
   ========================== */

[data-testid="stDataFrame"] {
    border-radius: 16px !important;
    overflow: hidden !important;
    border: 1px solid #dfe7f1 !important;
    box-shadow: 0 12px 28px rgba(16,24,40,0.05);
}

/* ==========================
   METRICS
   ========================== */

[data-testid="stMetric"] {
    background: linear-gradient(180deg, #ffffff, #f8fbff);
    border: 1px solid #dfe8f3;
    padding: 1rem;
    border-radius: 16px;
    box-shadow: 0 10px 26px rgba(16,24,40,0.04);
}

[data-testid="stMetricLabel"] {
    color: #617086 !important;
    font-weight: 700 !important;
}

[data-testid="stMetricValue"] {
    color: #162033 !important;
    font-weight: 850 !important;
}

/* ==========================
   SMALL HELPER CARDS
   ========================== */

.feature-strip {
    background: rgba(255,255,255,0.88);
    border: 1px solid #cfe4ff;
    border-radius: 22px;
    padding: 1.2rem;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    box-shadow: 0 14px 34px rgba(16,24,40,0.06);
    margin-top: 1rem;
}

.feature-item {
    display: flex;
    align-items: center;
    gap: 0.9rem;
    padding: 0.8rem;
}

.feature-icon {
    width: 44px;
    height: 44px;
    border-radius: 16px;
    display: grid;
    place-items: center;
    background: #eaf4ff;
    color: #006fd6;
    font-size: 1.25rem;
}

.feature-title {
    font-weight: 850;
    color: #182235;
    margin-bottom: 0.15rem;
}

.feature-text {
    color: #627084;
    font-size: 0.88rem;
    line-height: 1.35;
}

.tip-box {
    background: linear-gradient(135deg, #eef7ff, #f8fbff);
    border: 1px solid #cfe4ff;
    border-radius: 16px;
    padding: 1rem;
    color: #294362;
    font-size: 0.92rem;
    margin-top: 1rem;
}

/* ==========================
   HEADINGS
   ========================== */

h1, h2, h3 {
    letter-spacing: -0.035em;
}

hr {
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
}

/* ==========================
   RESPONSIVE
   ========================== */

@media (max-width: 900px) {
    .feature-strip {
        grid-template-columns: repeat(2, 1fr);
    }

    .hero-wrap {
        margin-left: -1rem;
        margin-right: -1rem;
        padding-bottom: 4.5rem;
    }
}

@media (max-width: 600px) {
    .feature-strip {
        grid-template-columns: 1fr;
    }

    .section-card {
        padding: 1.1rem;
        border-radius: 18px;
    }
}

</style>
""", unsafe_allow_html=True)

# ==========================
# HERO
# ==========================

st.markdown("""
<div class="hero-wrap">
    <h1 class="hero-title">Explore Brands & Categories</h1>
    <div class="hero-subtitle">Find the best Direct Buy products, compare costs, and search smarter.</div>
    <div class="hero-pills">
        <div class="hero-pill">Best Match Search</div>
        <div class="hero-pill">Category Filters</div>
        <div class="hero-pill">Cost Calculator</div>
        <div class="hero-pill">Best Deal Comparison</div>
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

# ==========================
# TOP SEARCH CARD
# ==========================

st.markdown(f"""
<div class="section-card float-card">
    <div class="card-title-row">
        <div class="icon-bubble">🔎</div>
        <div>
            <div class="card-title">Direct Buy Search</div>
            <div class="card-subtitle">Search by category, descriptions, brand, manufacturer, or item number.</div>
        </div>
    </div>
    <div class="status-bar">✅ Loaded {len(df):,} products</div>
</div>
""", unsafe_allow_html=True)

# ==========================
# BEST MATCH SEARCH
# ==========================

st.markdown("""
<div class="section-card">
    <div class="card-title-row">
        <div class="icon-bubble">⭐</div>
        <div>
            <div class="card-title">Best Match Search</div>
            <div class="card-subtitle">Search anything to find the most relevant products across categories, brands, descriptions, and item numbers.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

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

    st.dataframe(best_display, use_container_width=True)

    st.info(f"Showing top {min(len(best_results), 100)} best matches.")

# ==========================
# CATEGORY SEARCH
# ==========================

st.markdown("""
<div class="section-card">
    <div class="card-title-row">
        <div class="icon-bubble">📁</div>
        <div>
            <div class="card-title">Category Search</div>
            <div class="card-subtitle">Browse by category, then narrow results by description, brand, and manufacturer.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

product_classes = sorted(
    df["Product Class"].dropna().astype(str).unique()
)

left_filter_col, right_results_col = st.columns([0.34, 0.66], gap="large")

with left_filter_col:
    st.markdown("### Filters")

    product_class_search = st.text_input(
        "Filter Categories",
        placeholder="Type report, folder, binder..."
    )

    filtered_classes = [
        pc for pc in product_classes
        if product_class_search.lower() in pc.lower()
    ] if product_class_search else product_classes

    selected_class = st.selectbox(
        "Select Category",
        options=[""] + filtered_classes,
        index=0
    )

    st.markdown("""
    <div class="tip-box">
        <strong>💡 Tip</strong><br>
        Start with a category, then use description, brand, and manufacturer filters to narrow the product list.
    </div>
    """, unsafe_allow_html=True)

with right_results_col:
    if not selected_class:
        st.markdown("### Best deals in")
        st.markdown("## Select a category")
        st.info("Choose a category from the dropdown to view matching products.")

if selected_class:
    results = df[df["Product Class"] == selected_class].copy()

    results = results.sort_values(direct_cost_col, ascending=True)

    with left_filter_col:
        description_search = st.text_input(
            "Search within these products",
            placeholder="Example: clear, blue, letter, pressboard"
        )

    if description_search:
        results = results[
            results["Short Description"].astype(str).str.contains(description_search, case=False, na=False)
            |
            results["Long Description"].astype(str).str.contains(description_search, case=False, na=False)
        ]

    with left_filter_col:
        brand_options = sorted(results["Brand Name"].dropna().astype(str).unique())
        selected_brands = st.multiselect("Filter by Brand", brand_options)

        manufacturer_options = sorted(results["Manufacturer Name"].dropna().astype(str).unique())
        selected_manufacturers = st.multiselect("Filter by Manufacturer", manufacturer_options)

    if selected_brands:
        results = results[results["Brand Name"].astype(str).isin(selected_brands)]

    if selected_manufacturers:
        results = results[results["Manufacturer Name"].astype(str).isin(selected_manufacturers)]

    with right_results_col:
        st.markdown(f"### Best deals in {selected_class}")
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

        display_df[list_price_col] = display_df[list_price_col].apply(
            lambda x: f"${x:,.2f}" if pd.notna(x) else ""
        )

        display_df[direct_cost_col] = display_df[direct_cost_col].apply(
            lambda x: f"${x:,.2f}" if pd.notna(x) else ""
        )

        table_selection = st.dataframe(
            display_df,
            use_container_width=True,
            on_select="rerun",
            selection_mode="single-row",
            key="cheapest_products_table"
        )

        clicked_item_number = ""

        if table_selection.selection.rows:
            selected_row_position = table_selection.selection.rows[0]
            clicked_item_number = display_df.iloc[selected_row_position]["ISG Product Code"]

        st.info(f"Showing {len(results):,} products sorted from best deal to highest cost.")

    # ==========================
    # ITEM NUMBER COST CALCULATOR
    # ==========================

    st.markdown("""
    <div class="section-card">
        <div class="card-title-row">
            <div class="icon-bubble">🧮</div>
            <div>
                <div class="card-title">Item Number Cost Calculator</div>
                <div class="card-subtitle">Click a product row above or enter an item number to estimate direct cost, list price, and savings.</div>
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

    # ==========================
    # COMPARE PRODUCT
    # ==========================

    st.markdown("""
    <div class="section-card">
        <div class="card-title-row">
            <div class="icon-bubble">⚖️</div>
            <div>
                <div class="card-title">Compare Product vs Best Deal</div>
                <div class="card-subtitle">Choose any product in the category and compare it against the lowest direct cost option.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not results.empty:
        best_deal_product = results.iloc[0]

        product_choices = (
            results["Manufacturer Name"].astype(str)
            + " | "
            + results["ISG Product Code"].astype(str)
            + " | "
            + results["Short Description"].astype(str)
            + " | $"
            + results[direct_cost_col].round(2).astype(str)
        )

        selected_product_label = st.selectbox(
            "Choose a product to compare",
            product_choices
        )

        selected_index = product_choices[product_choices == selected_product_label].index[0]
        selected_product = results.loc[selected_index]

        best_deal_cost = best_deal_product[direct_cost_col]
        selected_cost = selected_product[direct_cost_col]
        savings = selected_cost - best_deal_cost

        c1, c2, c3 = st.columns(3)

        c1.metric("Best Deal Cost", f"${best_deal_cost:,.2f}")
        c2.metric("Selected Product Cost", f"${selected_cost:,.2f}")
        c3.metric("Potential Savings", f"${savings:,.2f}")

        compare_col1, compare_col2 = st.columns(2)

        with compare_col1:
            st.markdown("#### Best Deal Product")
            st.write(best_deal_product["Short Description"])

        with compare_col2:
            st.markdown("#### Selected Product")
            st.write(selected_product["Short Description"])

# ==========================
# BOTTOM FEATURE STRIP
# ==========================

st.markdown("""
<div class="feature-strip">
    <div class="feature-item">
        <div class="feature-icon">🏷️</div>
        <div>
            <div class="feature-title">Best Prices</div>
            <div class="feature-text">Find the lowest direct costs fast.</div>
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-icon">🛡️</div>
        <div>
            <div class="feature-title">Trusted Brands</div>
            <div class="feature-text">Search top manufacturers and brands.</div>
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-icon">📦</div>
        <div>
            <div class="feature-title">Wide Selection</div>
            <div class="feature-text">Browse thousands of products.</div>
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-icon">⚡</div>
        <div>
            <div class="feature-title">Fast & Easy</div>
            <div class="feature-text">Quick search with smart filters.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
