import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
import plotly.express as px

from utils.style_loader import load_css
from utils.data_loader import load_data


st.set_page_config(
    page_title="Risk Center",
    page_icon="⚠️",
    layout="wide"
)

load_css()
st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)


inventory, suppliers, sales, transactions, purchase_orders = load_data()

risk_data = inventory.merge(
    suppliers,
    on="supplier_id",
    how="left"
)

st.title("⚠️ Risk Center")
st.caption("Identify stockout risk, supplier risk, slow-moving inventory, and urgent replenishment needs.")

st.sidebar.header("Risk Filters")

category_options = ["All"] + sorted(risk_data["category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Category", category_options)

stockout_options = ["All"] + sorted(risk_data["stockout_risk"].dropna().unique().tolist())
selected_stockout = st.sidebar.selectbox("Stockout Risk", stockout_options)

supplier_risk_options = ["All"] + sorted(risk_data["supplier_risk_level"].dropna().unique().tolist())
selected_supplier_risk = st.sidebar.selectbox("Supplier Risk", supplier_risk_options)

filtered_risk = risk_data.copy()

if selected_category != "All":
    filtered_risk = filtered_risk[filtered_risk["category"] == selected_category]

if selected_stockout != "All":
    filtered_risk = filtered_risk[filtered_risk["stockout_risk"] == selected_stockout]

if selected_supplier_risk != "All":
    filtered_risk = filtered_risk[filtered_risk["supplier_risk_level"] == selected_supplier_risk]


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


st.subheader("Risk Overview")

high_risk_skus = (filtered_risk["stockout_risk"] == "High").sum()
reorder_qty = filtered_risk["reorder_quantity"].sum()
slow_moving_skus = (filtered_risk["slow_moving_flag"] == 1).sum()
excess_inventory_skus = (filtered_risk["excess_inventory_flag"] == 1).sum()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    metric_card("High Risk SKUs", f"{high_risk_skus:,}", "⚠️")

with kpi2:
    metric_card("Reorder Quantity", f"{reorder_qty:,}", "📋")

with kpi3:
    metric_card("Slow Moving SKUs", f"{slow_moving_skus:,}", "🐢")

with kpi4:
    metric_card("Excess Inventory SKUs", f"{excess_inventory_skus:,}", "📦")

st.divider()

left, right = st.columns(2)

with left:
    risk_by_category = (
        filtered_risk.groupby(["category", "stockout_risk"], as_index=False)
        .agg(sku_count=("item_id", "count"))
    )

    fig_category_risk = px.bar(
        risk_by_category,
        x="category",
        y="sku_count",
        color="stockout_risk",
        title="Stockout Risk by Category",
        barmode="group"
    )

    st.plotly_chart(fig_category_risk, use_container_width=True)

with right:
    supplier_risk_summary = (
        filtered_risk.groupby("supplier_risk_level", as_index=False)
        .agg(sku_count=("item_id", "count"))
        .sort_values("sku_count", ascending=False)
    )

    fig_supplier_risk = px.pie(
        supplier_risk_summary,
        names="supplier_risk_level",
        values="sku_count",
        title="SKU Exposure by Supplier Risk"
    )

    st.plotly_chart(fig_supplier_risk, use_container_width=True)

st.divider()

left, right = st.columns(2)

with left:
    reorder_by_category = (
        filtered_risk.groupby("category", as_index=False)
        .agg(total_reorder_quantity=("reorder_quantity", "sum"))
        .sort_values("total_reorder_quantity", ascending=False)
    )

    fig_reorder = px.bar(
        reorder_by_category,
        x="category",
        y="total_reorder_quantity",
        title="Reorder Quantity by Category"
    )

    st.plotly_chart(fig_reorder, use_container_width=True)

with right:
    slow_moving = filtered_risk[filtered_risk["slow_moving_flag"] == 1]

    slow_by_category = (
        slow_moving.groupby("category", as_index=False)
        .agg(sku_count=("item_id", "count"))
        .sort_values("sku_count", ascending=False)
    )

    fig_slow = px.bar(
        slow_by_category,
        x="category",
        y="sku_count",
        title="Slow Moving SKUs by Category"
    )

    st.plotly_chart(fig_slow, use_container_width=True)

st.subheader("Urgent Reorder Watchlist")

urgent_reorders = (
    filtered_risk[filtered_risk["reorder_quantity"] > 0]
    .sort_values("reorder_quantity", ascending=False)
    .head(25)
)

st.dataframe(
    urgent_reorders[
        [
            "item_id",
            "category",
            "supplier_id",
            "supplier_name",
            "stock_level",
            "reorder_point",
            "reorder_quantity",
            "stockout_risk",
            "supplier_risk_level",
        ]
    ].reset_index(drop=True),
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("Risk Detail Explorer")

st.dataframe(
    filtered_risk[
        [
            "item_id",
            "category",
            "supplier_id",
            "supplier_name",
            "stock_level",
            "reorder_point",
            "reorder_quantity",
            "days_of_inventory",
            "stockout_risk",
            "slow_moving_flag",
            "excess_inventory_flag",
            "supplier_risk_level",
        ]
    ].sort_values("reorder_quantity", ascending=False).reset_index(drop=True),
    use_container_width=True,
    hide_index=True
)