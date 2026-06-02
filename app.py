import streamlit as st
import pandas as pd
from rapidfuzz import fuzz

st.set_page_config(
    page_title="Direct Buy Search",
    layout="wide"
)

st.markdown("""
<style>

/* Hide Streamlit footer */
footer {
    visibility: hidden;
}

/* Hide hamburger menu */
#MainMenu {
    visibility: hidden;
}

/* Hide toolbar */
[data-testid="stToolbar"] {
    display: none !important;
}

/* Hide fullscreen button */
button[title="View fullscreen"] {
    display: none !important;
}

/* Hide deploy/status widgets */
[data-testid="stStatusWidget"] {
    display: none !important;
}

/* Hide built with Streamlit badge */
.stAppDeployButton {
    display: none !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

/* Hide bottom embedded app bar */
.viewerBadge_container__1QSob,
.viewerBadge_link__1S137,
.viewerBadge_text__1JaDK,
.viewerBadge_container__r5tak {
    display: none !important;
}

</style>
""", unsafe_allow_html=True)

st.title("Direct Buy Search")
st.write("Search by category, descriptions, brand, manufacturer, or item number.")

file_name = "cost list pricer.xlsx"

@st.cache_data
def load_data():
    df = pd.read_excel(file_name)
    df.columns = df.columns.astype(str).str.strip()
    return df

df = load_data()

st.success(f"Loaded {len(df):,} products")

direct_cost_col = next(col for col in df.columns if "JUN 2026" in col and "Direct Cost" in col)
list_price_col = next(col for col in df.columns if "MAY 2026 List Price" in col)

moq_col = "Min Ord Qty"
uom_col = "ISG UOM"

df[direct_cost_col] = pd.to_numeric(df[direct_cost_col], errors="coerce")
df[list_price_col] = pd.to_numeric(df[list_price_col], errors="coerce")

if moq_col in df.columns:
    df[moq_col] = pd.to_numeric(df[moq_col], errors="coerce")

# ==========================
# BEST MATCH SEARCH
# ==========================

st.write("## Best Match Search")

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

    st.write("### Best Matching Products")

    st.dataframe(
        best_results[
            [
                "Match Score",
                "Product Class",
                "Brand Name",
                "Manufacturer Name",
                "ISG Product Code",
                "Short Description",
                list_price_col,
                direct_cost_col
            ]
        ].head(100),
        use_container_width=True
    )

    st.info(f"Showing top {min(len(best_results), 100)} best matches.")

st.divider()

# ==========================
# CATEGORY SEARCH
# ==========================

st.write("## Category Search")

product_classes = sorted(
    df["Product Class"].dropna().astype(str).unique()
)

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

if selected_class:
    results = df[df["Product Class"] == selected_class].copy()

    results = results.sort_values(direct_cost_col, ascending=True)

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

    col1, col2 = st.columns(2)

    with col1:
        brand_options = sorted(results["Brand Name"].dropna().astype(str).unique())
        selected_brands = st.multiselect("Filter by Brand", brand_options)

    with col2:
        manufacturer_options = sorted(results["Manufacturer Name"].dropna().astype(str).unique())
        selected_manufacturers = st.multiselect("Filter by Manufacturer", manufacturer_options)

    if selected_brands:
        results = results[results["Brand Name"].astype(str).isin(selected_brands)]

    if selected_manufacturers:
        results = results[results["Manufacturer Name"].astype(str).isin(selected_manufacturers)]

    st.write(f"### Cheapest products in {selected_class}")
    st.caption("Click a row below to auto-fill the calculator.")

    display_columns = [
        "Brand Name",
        "Manufacturer Name",
        "ISG Product Code",
        "Short Description",
        "Long Description",
        list_price_col,
        direct_cost_col
    ]

    if moq_col in df.columns:
        display_columns.insert(5, moq_col)

    if uom_col in df.columns:
        display_columns.insert(6, uom_col)

    display_df = results[display_columns].copy()

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

    # ==========================
    # ITEM NUMBER COST CALCULATOR
    # ==========================

    st.write("### Item Number Cost Calculator")

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

            st.write("#### Item Details")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Direct Cost", f"${item_cost:,.2f}")
            c2.metric("List Price", f"${item_list_price:,.2f}")
            c3.metric("MOQ", f"{item_moq:,.0f}" if pd.notna(item_moq) else "N/A")
            c4.metric("ISG UOM", str(item_uom))

            st.write("##### Product")
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

            st.write("#### Cost Estimate")

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

    st.write("### Compare Product vs Cheapest Option")

    if not results.empty:
        cheapest_product = results.iloc[0]

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

        cheapest_cost = cheapest_product[direct_cost_col]
        selected_cost = selected_product[direct_cost_col]
        savings = selected_cost - cheapest_cost

        c1, c2, c3 = st.columns(3)

        c1.metric("Cheapest Cost", f"${cheapest_cost:,.2f}")
        c2.metric("Selected Product Cost", f"${selected_cost:,.2f}")
        c3.metric("Potential Savings", f"${savings:,.2f}")

        st.write("#### Cheapest Product")
        st.write(cheapest_product["Short Description"])

        st.write("#### Selected Product")
        st.write(selected_product["Short Description"])

    st.info(f"Showing {len(results):,} products sorted from cheapest to most expensive.")
