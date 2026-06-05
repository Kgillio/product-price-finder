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
.viewerBadge_container__r5tak {
    display: none !important;
}

/* ==========================
   PAGE BACKGROUND
   Seamless Kentico white blend
   ========================== */

.stApp {
    background: #ffffff !important;
    color: #172033;
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
        radial-gradient(circle at 12% 18%, rgba(40, 132, 189, 0.14), transparent 28%),
        radial-gradient(circle at 90% 12%, rgba(0, 111, 214, 0.10), transparent 30%),
        linear-gradient(135deg, #ffffff 0%, #f7fbff 42%, #eef7ff 100%);
    border: 1px solid #dbeafe;
    border-radius: 28px;
    padding: 3.1rem 2.2rem 3.1rem 2.2rem;
    margin: 1.3rem auto 1.8rem auto;
    text-align: center;
    color: #172033;
    box-shadow: 0 20px 52px rgba(15, 55, 95, 0.08);
    position: relative;
    overflow: hidden;
    max-width: 1120px;
}

.hero-wrap::before {
    content: "";
    position: absolute;
    inset: 0;
    background:
        linear-gradient(160deg, transparent 48%, rgba(40,132,189,0.08) 49%, transparent 51%),
        linear-gradient(170deg, transparent 57%, rgba(0,111,214,0.06) 58%, transparent 60%);
    pointer-events: none;
}

.hero-wrap::after {
    content: "";
    position: absolute;
    left: 5%;
    right: 5%;
    bottom: 0;
    height: 5px;
    background: linear-gradient(90deg, transparent, rgba(40,132,189,0.55), transparent);
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
    background: linear-gradient(135deg, #ffffff, #eef7ff);
    border: 1px solid #cfe5ff;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow:
        0 16px 34px rgba(40,132,189,0.12),
        inset 0 1px 0 rgba(255,255,255,0.9);
}

.hero-icon-card svg {
    width: 60px;
    height: 60px;
    filter: drop-shadow(0 8px 14px rgba(40,132,189,0.12));
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
    color: #10233f;
    text-shadow: none;
}

.hero-subtitle {
    font-size: 1.08rem;
    margin-top: 0.9rem;
    color: #52647c;
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
    margin: 0 0 1.15rem 0;
    padding: 1.25rem 1.45rem;
    background: linear-gradient(180deg, #f6fbff 0%, #edf6fe 100%);
    border: 1px solid #dbeafe;
    border-bottom-color: #cfe3f8;
    border-radius: 18px 18px 0 0;
    position: relative;
    overflow: hidden;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.85);
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
    background: rgba(255,255,255,0.82);
    border: 1px solid #dbeafe;
    color: #2884bd;
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
    box-shadow: 0 6px 14px rgba(8, 123, 59, 0.06);
}

/* ==========================
   STREAMLIT CONTAINERS
   Softer white cards
   ========================== */

[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 22px !important;
    border: 1px solid rgba(220, 230, 242, 0.95) !important;
    box-shadow: 0 10px 28px rgba(15, 33, 58, 0.045) !important;
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
    box-shadow: 0 10px 24px rgba(16,24,40,0.04);
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
   PRODUCT IMAGE PREVIEW
   ========================== */

.product-image-card {
    border: 1px solid #dfe8f3;
    border-radius: 18px;
    padding: 1rem;
    background: linear-gradient(180deg, #ffffff, #fbfdff);
    box-shadow: 0 10px 26px rgba(16,24,40,0.04);
    text-align: center;
}

.product-image-title {
    font-weight: 850;
    color: #172033;
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

# Keep the selected calculator item available across reruns.
# This lets someone click a row in either Best Match Search or Category Search
# and have the calculator auto-fill with that item number.
if "calculator_item_number" not in st.session_state:
    st.session_state["calculator_item_number"] = ""

if "calculator_selected_source" not in st.session_state:
    st.session_state["calculator_selected_source"] = ""

# ==========================
# ITEM NUMBER COST CALCULATOR FUNCTION
# ==========================

def render_item_number_cost_calculator(calculator_location_key="main"):
    """Shows the item number calculator wherever this function is placed on the page."""
    st.write("")

    with st.container(border=True):
        st.markdown(f"""
        <div class="section-header">
            <div class="icon-bubble">{calculator_icon}</div>
            <div>
                <div class="card-title">Item Number Cost Calculator</div>
                <div class="card-subtitle">Click a product row above or enter an item number to estimate direct cost, list price, and total price.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        selected_source = st.session_state.get("calculator_selected_source", "")
        selected_calculator_item = st.session_state.get("calculator_item_number", "")

        if selected_calculator_item:
            if selected_source:
                st.success(f"Selected item from {selected_source}: {selected_calculator_item}")
            else:
                st.success(f"Selected item: {selected_calculator_item}")

        item_number_search = st.text_input(
            "Enter Item Number",
            placeholder="Example: ABFARB8012M",
            key="calculator_item_number"
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
        "Search anything — Example: clear report covers, blue folder, Avery binder",
        placeholder="...."
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
        st.caption("Click a row below to auto-fill the calculator.")

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

        best_match_selection = st.dataframe(
            best_display,
            use_container_width=True,
            height=420,
            on_select="rerun",
            selection_mode="single-row",
            key="best_match_products_table"
        )

        if best_match_selection.selection.rows:
            selected_row_position = best_match_selection.selection.rows[0]
            selected_best_item_number = best_display.iloc[selected_row_position]["ISG Product Code"]

            st.session_state["calculator_item_number"] = str(selected_best_item_number)
            st.session_state["calculator_selected_source"] = "Best Match Search"

            st.success(f"Selected item from Best Match Search: {selected_best_item_number}")

        st.info(f"Showing top {min(len(best_results), 100)} best matches.")

        # Calculator now appears directly under the Best Matching Products table,
        # so users do not have to scroll to the bottom for the estimate.
        render_item_number_cost_calculator("best_match")

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

            st.session_state["calculator_item_number"] = str(clicked_item_number)
            st.session_state["calculator_selected_source"] = "Category Search"

            st.success(f"Selected item from Category Search: {clicked_item_number}")

        st.info(f"Showing {len(results):,} products sorted from best deal to highest cost.")

        # When someone uses Category Search without Best Match Search,
        # keep the calculator directly under that selected table too.
        if not best_match_search:
            render_item_number_cost_calculator("category")

    else:
        results = pd.DataFrame()

        st.write("")
        st.markdown("## Best deals in")
        st.markdown("# Select a category")
        st.info("Choose a category from the dropdown to view matching products.")

