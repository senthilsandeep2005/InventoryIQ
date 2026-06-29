import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.style_loader import load_css
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="InventoryIQ Dashboard",
    page_icon="📦",
    layout="wide"
)

load_css()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

from utils.data_loader import load_data

inventory, suppliers, sales, transactions, purchase_orders = load_data()

st.title("📦 InventoryIQ")
st.caption("Intelligent Inventory Optimization Platform | Python + AWS S3 + Athena + Streamlit")

# KPI calculations
total_skus = inventory["item_id"].nunique()
total_inventory_value = inventory["inventory_value"].sum()
avg_health_score = inventory["kpi_score"].mean()
high_risk_skus = (inventory["stockout_risk"] == "High").sum()
total_reorder_qty = inventory["reorder_quantity"].sum()

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


kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    metric_card("Total SKUs", f"{total_skus:,}", "📦")

with kpi2:
    metric_card("Inventory Value", f"${total_inventory_value:,.0f}", "💰")

with kpi3:
    metric_card("Avg Health Score", f"{avg_health_score:.3f}", "📊")

with kpi4:
    metric_card("High Risk SKUs", f"{high_risk_skus:,}", "⚠️")

with kpi5:
    metric_card("Reorder Qty", f"{total_reorder_qty:,}", "📋")

st.divider()

# Charts
left, right = st.columns(2)

with left:
    inventory_by_category = (
        inventory.groupby("category", as_index=False)
        .agg(total_inventory_value=("inventory_value", "sum"))
        .sort_values("total_inventory_value", ascending=False)
    )

    fig_inventory = px.bar(
        inventory_by_category,
        x="category",
        y="total_inventory_value",
        title="Inventory Value by Category"
    )
    st.plotly_chart(fig_inventory, use_container_width=True)

with right:
    sales_with_category = sales.merge(
        inventory[["item_id", "category"]],
        on="item_id",
        how="left"
    )

    sales_by_category = (
        sales_with_category.groupby("category", as_index=False)
        .agg(total_revenue=("sales_revenue", "sum"))
        .sort_values("total_revenue", ascending=False)
    )

    fig_sales = px.bar(
        sales_by_category,
        x="category",
        y="total_revenue",
        title="Sales Revenue by Category"
    )
    st.plotly_chart(fig_sales, use_container_width=True)

left, right = st.columns(2)

with left:
    sales["order_date"] = pd.to_datetime(sales["order_date"])
    sales["sales_month"] = sales["order_date"].dt.to_period("M").astype(str)

    monthly_sales = (
        sales.groupby("sales_month", as_index=False)
        .agg(total_revenue=("sales_revenue", "sum"))
    )

    fig_monthly = px.line(
        monthly_sales,
        x="sales_month",
        y="total_revenue",
        title="Monthly Sales Trend",
        markers=True
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

with right:
    transaction_summary = (
    transactions.groupby("event_type", as_index=False)
    .agg(transaction_count=("item_id", "count"))
    .sort_values("transaction_count", ascending=False)
    )

    fig_transactions = px.pie(
    transaction_summary,
    names="event_type",
    values="transaction_count",
    title="Warehouse Transaction Activity"
    )
    st.plotly_chart(fig_transactions, use_container_width=True)

st.divider()

st.subheader("⚠️ High Risk SKUs")
high_risk_table = (
    inventory[inventory["stockout_risk"] == "High"]
    .sort_values("reorder_quantity", ascending=False)
    [
        [
            "item_id",
            "category",
            "stock_level",
            "reorder_point",
            "days_of_inventory",
            "reorder_quantity",
            "supplier_id",
        ]
    ]
)

st.dataframe(high_risk_table, use_container_width=True, hide_index=True)

st.subheader("📋 Reorder Recommendations")
reorder_table = (
    inventory[inventory["reorder_quantity"] > 0]
    .sort_values("reorder_quantity", ascending=False)
    [
        [
            "item_id",
            "category",
            "stock_level",
            "reorder_point",
            "reorder_quantity",
            "stockout_risk",
            "supplier_id",
        ]
    ]
)

st.dataframe(reorder_table, use_container_width=True, hide_index=True)