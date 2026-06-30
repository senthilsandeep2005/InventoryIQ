import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
import streamlit as st
import plotly.express as px

from utils.style_loader import load_css
from utils.data_loader import load_data


st.set_page_config(
    page_title="Inventory Analytics",
    page_icon="📦",
    layout="wide"
)

load_css()
st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

inventory, suppliers, sales, transactions, purchase_orders = load_data()

numeric_columns = [
    "inventory_value",
    "stock_level",
    "reorder_point",
    "reorder_quantity",
    "days_of_inventory",
]

for col in numeric_columns:
    if col in inventory.columns:
        inventory[col] = pd.to_numeric(inventory[col], errors="coerce")

inventory["abc_class"] = inventory["inventory_value"].apply(
    lambda value: "A" if value >= 50000 else "B" if value >= 15000 else "C"
)


def metric_card(label, value, icon):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{icon} {label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.title("📦 Inventory Analytics")
st.caption("Explore inventory value, stock levels, reorder needs, and SKU health across the distribution center.")

st.sidebar.header("Inventory Filters")

category_options = ["All"] + sorted(inventory["category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Category", category_options)

risk_options = ["All"] + sorted(inventory["stockout_risk"].dropna().unique().tolist())
selected_risk = st.sidebar.selectbox("Stockout Risk", risk_options)

supplier_options = ["All"] + sorted(inventory["supplier_id"].dropna().unique().tolist())
selected_supplier = st.sidebar.selectbox("Supplier", supplier_options)

filtered_inventory = inventory.copy()

if selected_category != "All":
    filtered_inventory = filtered_inventory[filtered_inventory["category"] == selected_category]

if selected_risk != "All":
    filtered_inventory = filtered_inventory[filtered_inventory["stockout_risk"] == selected_risk]

if selected_supplier != "All":
    filtered_inventory = filtered_inventory[filtered_inventory["supplier_id"] == selected_supplier]

st.subheader("Filtered Inventory Overview")

total_skus = filtered_inventory["item_id"].nunique()
inventory_value = filtered_inventory["inventory_value"].sum()
avg_stock_level = filtered_inventory["stock_level"].mean()
avg_days_inventory = filtered_inventory["days_of_inventory"].mean()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    metric_card("Filtered SKUs", f"{total_skus:,}", "📦")

with kpi2:
    metric_card("Inventory Value", f"${inventory_value:,.0f}", "💰")

with kpi3:
    metric_card("Avg Stock Level", f"{avg_stock_level:.1f}", "📊")

with kpi4:
    metric_card("Avg Days Inventory", f"{avg_days_inventory:.1f}", "⏱️")

st.divider()

left, right = st.columns(2)

with left:
    category_value = (
        filtered_inventory.groupby("category", as_index=False)
        .agg(total_inventory_value=("inventory_value", "sum"))
        .sort_values("total_inventory_value", ascending=False)
    )

    fig_category = px.bar(
        category_value,
        x="category",
        y="total_inventory_value",
        title="Inventory Value by Category"
    )

    st.plotly_chart(fig_category, use_container_width=True)

with right:
    risk_summary = (
        filtered_inventory.groupby("stockout_risk", as_index=False)
        .agg(sku_count=("item_id", "count"))
        .sort_values("sku_count", ascending=False)
    )

    fig_risk = px.bar(
        risk_summary,
        x="stockout_risk",
        y="sku_count",
        title="SKU Count by Stockout Risk"
    )

    st.plotly_chart(fig_risk, use_container_width=True)

st.divider()

left, right = st.columns(2)

with left:
    abc_summary = (
        filtered_inventory.groupby("abc_class", as_index=False)
        .agg(
            inventory_value=("inventory_value", "sum"),
            sku_count=("item_id", "count")
        )
        .sort_values("abc_class")
    )

    fig_abc = px.bar(
        abc_summary,
        x="abc_class",
        y="inventory_value",
        color="abc_class",
        title="Inventory Value by ABC Classification"
    )

    st.plotly_chart(fig_abc, use_container_width=True)

with right:
    fig_stock = px.histogram(
        filtered_inventory,
        x="stock_level",
        nbins=30,
        title="Stock Level Distribution"
    )

    st.plotly_chart(fig_stock, use_container_width=True)

st.subheader("Top 10 Highest Value Inventory")

top_inventory = (
    filtered_inventory
    .sort_values("inventory_value", ascending=False)
    .head(10)
)

st.dataframe(
    top_inventory[
        [
            "item_id",
            "category",
            "supplier_id",
            "inventory_value",
            "stock_level",
            "days_of_inventory",
            "stockout_risk"
        ]
    ].reset_index(drop=True),
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("SKU Explorer")

st.dataframe(
    filtered_inventory[
        [
            "item_id",
            "category",
            "supplier_id",
            "stock_level",
            "reorder_point",
            "reorder_quantity",
            "days_of_inventory",
            "stockout_risk",
            "inventory_value",
        ]
    ].sort_values("inventory_value", ascending=False).reset_index(drop=True),
    use_container_width=True,
    hide_index=True
)