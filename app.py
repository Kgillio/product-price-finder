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
        radial-gradient(circle at top left, rgba(0, 118, 210, 0.06), transparent 30%),
        radial-gradient(circle at top right, rgba(0, 77, 150, 0.06), transparent 35%),
        linear-gradient(180deg, #f7fbff 0%, #ffffff 42%, #f8fafc 100%);
    color: #172033;
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
        linear-gradient(135deg, rgba(0, 91, 165, 0.74), rgba(0, 153, 220, 0.58)),
        url("https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&fit=crop&w=1600&q=80");
    background-size: cover;
    background-position: center;
    border-radius: 0 0 34px 34px;
    padding: 4rem 2rem 4.8rem 2rem;
    margin: 0 -2rem 2rem -2rem;
    text-align: center;
    color: white;
    box-shadow: 0 28px 70px rgba(0, 55, 110, 0.16);
}

.hero-title {
    font-size: clamp(2.3rem, 5vw, 4rem);
    font-weight: 850;
    letter-spacing: -0.06em;
    margin: 0;
    line-height: 1.05;
    text-shadow: 0 3px 16px rgba(0,0,0,0.18);
}

.hero-subtitle {
    font-size: 1.12rem;
    margin-top: 1rem;
    opacity: 0.98;
    font-weight: 500;
    text-shadow: 0 2px 10px rgba(0,0,0,0.15);
}

.hero-pills {
    display: flex;
    justify-content: center;
    gap: 0.8rem;
    flex-wrap: wrap;
    margin-top: 1.6rem;
}

.hero-pill {
    background: rgba(255,255,255,0.22);
    border: 1px solid rgba(255,255,255,0.38);
    color: white;
    padding: 0.6rem 0.95rem;
    border-radius: 999px;
    font-size: 0.88rem;
    font-weight: 750;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
}

/* ==========================
   CARD HEADER STYLE
   ========================== */

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
    border-radius: 17px;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, #eef7ff, #ffffff);
    border: 1px solid #cfe4ff;
    color: #006fd6;
    font-size: 1.4rem;
    box-shadow: 0 8px 20px rgba(0, 111, 214, 0.08);
}

.card-title {
    font-size: 1.5rem;
    font-weight: 850;
    color: #172033;
    margin: 0;
    letter-spacing: -0.04em;
}

.card-subtitle {
    color: #657389;
    margin-top: 0.25rem;
    font-size: 0.96rem;
    line-height: 1.45;
}

.loaded-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: linear-gradient(90deg, #e7fff1, #f7fffa);
    border: 1px solid #bdeccb;
    color: #087b3b;
    padding: 0.42rem 0.72rem;
    border-radius: 999px;
    font-weight: 850;
    font-size: 0.82rem;
    white-space: nowrap;
    box-shadow: 0 6px 14px rgba(8, 123, 59, 0.08);
}

/* ==========================
   STREAMLIT CONTAINERS
   ========================== */

[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 24px !important;
    border: 1px solid rgba(196, 219, 244, 0.95) !important;
    box-shadow: 0 18px 48px rgba(15, 33, 58, 0.06) !important;
    background:
        linear-gradient(135deg, rgba(255,255,255,0.98), rgba(247,251,255,0.95)) !important;
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
    border: 1px solid #cfdbea !important;
    background: #ffffff !important;
    min-height: 48px !important;
    box-shadow:
        0 1px 0 rgba(255,255,255,0.95) inset,
        0 8px 20px rgba(16,24,40,0.035) !important;
}

div[data-baseweb="select"] > div {
    border-radius: 14px !important;
    border-color: #cfdbea !important;
    background: #ffffff !important;
    min-height: 48px !important;
    box-shadow:
        0 1px 0 rgba(255,255,255,0.95) inset,
        0 8px 20px rgba(16,24,40,0.035) !important;
}

div[data-baseweb="input"]:focus-within,
div[data-baseweb="select"] > div:focus-within {
    border-color: #75b7ff !important;
    box-shadow:
        0 0 0 3px rgba(0, 119, 223, 0.10),
        0 10px 24px rgba(16,24,40,0.05) !important;
}

.stTextInput label,
.stSelectbox label,
.stMultiSelect label,
.stNumberInput label {
    font-weight: 800 !important;
    color: #26344c !important;
    font-size: 0.9rem !important;
}

.stTextInput input,
.stNumberInput input {
    min-height: 48px;
    background: #ffffff !important;
    color: #1f2937 !important;
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
    border: 1px solid #dfe8f2 !important;
    box-shadow: 0 14px 32px rgba(16,24,40,0.045);
    background: #ffffff !important;
}

/* ==========================
   METRICS
   ========================== */

[data-testid="stMetric"] {
    background: linear-gradient(180deg, #ffffff, #fbfdff);
    border: 1px solid #dfe8f3;
    padding: 1rem;
    border-radius: 17px;
    box-shadow: 0 10px 26px rgba(16,24,40,0.04);
}

[data-testid="stMetricLabel"] {
    color: #617086 !important;
    font-weight: 750 !important;
}

[data-testid="stMetricValue"] {
    color: #162033 !important;
    font-weight: 850 !important;
}

/* ==========================
   INFO / SUCCESS / WARNING BOXES
   ========================== */

[data-testid="stAlert"] {
    border-radius: 15px !important;
    border: 1px solid rgba(120, 170, 230, 0.22) !important;
}

/* ==========================
   FEATURE STRIP
   ========================== */

.feature-strip {
    background: rgba(255,255,255,0.95);
    border: 1px solid #d6eaff;
    border-radius: 24px;
    padding: 1.25rem;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    box-shadow: 0 14px 34px rgba(16,24,40,0.045);
    margin-top: 2rem;
}

.feature-item {
    display: flex;
    align-items: center;
    gap: 0.9rem;
    padding: 0.8rem;
}

.feature-icon {
    width: 46px;
    height: 46px;
    min-width: 46px;
    border-radius: 16px;
    display: grid;
    place-items: center;
    background: #eef7ff;
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
    .feature-strip {
        grid-template-columns: repeat(2, 1fr);
    }

    .hero-wrap {
        margin-left: -1rem;
        margin-right: -1rem;
        padding-bottom: 4rem;
    }
}

@media (max-width: 600px) {
    .feature-strip {
        grid-template-columns: 1fr;
    }

    .card-title-row {
        align-items: flex-start;
    }

    .hero-title {
        font-size: 2.2rem;
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

# Set defaults so later sections do not break
selected_class = ""
results = pd.DataFrame()
clicked_item_number = ""

# ==========================
# BEST MATCH SEARCH
# ==========================

with st.container(border=True):
    st.markdown(f"""
    <div class="card-title-row">
        <div class="icon-bubble">⭐</div>
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
    st.markdown("""
    <div class="card-title-row">
        <div class="icon-bubble">📁</div>
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

    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

    with filter_col1:
        product_class_search = st.text_input(
            "Filter Categories",
            placeholder="Type report, folder, binder..."
        )

        filtered_classes = [
            pc for pc in product_classes
            if product_class_search.lower() in pc.lower()
        ] if product_class_search else product_classes

    with filter_col2:
        selected_class = st.selectbox(
            "Select Category",
            options=[""] + filtered_classes,
            index=0
        )

    description_search = ""
    selected_brands = []
    selected_manufacturers = []

    if selected_class:
        results = df[df["Product Class"] == selected_class].copy()
        results = results.sort_values(direct_cost_col, ascending=True)

        with filter_col3:
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

        with filter_col4:
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
        st.markdown("""
        <div class="card-title-row">
            <div class="icon-bubble">🧮</div>
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

    # ==========================
    # COMPARE PRODUCT
    # ==========================

    st.write("")

    with st.container(border=True):
        st.markdown("""
        <div class="card-title-row">
            <div class="icon-bubble">⚖️</div>
            <div>
                <div class="card-title">Compare Product vs Best Deal</div>
                <div class="card-subtitle">Choose any product in the category and compare it against the lowest direct cost option.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

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
