import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
import streamlit as st
import plotly.express as px
from utils.athena_client import run_sql_file

from utils.style_loader import load_css
from utils.data_loader import load_data


st.set_page_config(
    page_title="InventoryIQ Dashboard",
    page_icon="📦",
    layout="wide"
)

load_css()
st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

inventory, suppliers, sales, transactions, purchase_orders = load_data()

# Clean sales fields from Athena
sales["quantity_ordered"] = pd.to_numeric(sales["quantity_ordered"], errors="coerce")
sales["unit_price"] = pd.to_numeric(sales["unit_price"], errors="coerce")
sales["calculated_revenue"] = sales["quantity_ordered"] * sales["unit_price"]
sales["sales_revenue"] = sales["calculated_revenue"]

# Clean date/month field
if "order_date" in sales.columns:
    sales["order_date"] = sales["order_date"].astype(str)
    sales["sales_month"] = sales["order_date"].str.slice(0, 7)

if "sales_month" not in sales.columns and "order_month" in sales.columns:
    sales["sales_month"] = sales["order_month"]

# Clean transaction compatibility
if "transaction_type" in transactions.columns:
    transactions["event_type"] = transactions["transaction_type"]

if "event_type" in transactions.columns:
    transactions["transaction_type"] = transactions["event_type"]


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


st.title("📦 InventoryIQ")
st.caption("Intelligent Inventory Optimization Platform | Python + AWS S3 + Athena + Streamlit")

# KPI calculations
kpi_df = run_sql_file("executive_kpis_athena.sql")

total_skus = int(kpi_df.loc[0, "total_skus"])
total_inventory_value = float(kpi_df.loc[0, "total_inventory_value"])
avg_health_score = float(kpi_df.loc[0, "avg_inventory_health_score"])
high_risk_skus = int(kpi_df.loc[0, "high_risk_skus"])
total_reorder_qty = float(kpi_df.loc[0, "total_reorder_quantity"])

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
        .agg(total_revenue=("calculated_revenue", "sum"))
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
    monthly_sales = (
        sales.groupby("sales_month", as_index=False)
        .agg(total_revenue=("calculated_revenue", "sum"))
        .sort_values("sales_month")
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
    .head(10)
)

st.dataframe(
    high_risk_table[
        [
            "item_id",
            "category",
            "stock_level",
            "reorder_point",
            "days_of_inventory",
            "reorder_quantity",
            "supplier_id",
        ]
    ].reset_index(drop=True),
    use_container_width=True,
    hide_index=True
)

st.subheader("📋 Reorder Priority Recommendations")

reorder_table = inventory[inventory["reorder_quantity"] > 0].copy()

reorder_table["priority_score"] = (
    reorder_table["inventory_value"]
    * reorder_table["reorder_quantity"]
)

reorder_table = (
    reorder_table
    .sort_values("priority_score", ascending=False)
    .head(10)
)
st.dataframe(
    reorder_table[
        [
            "item_id",
            "category",
            "stock_level",
            "reorder_point",
            "reorder_quantity",
            "inventory_value",
            "priority_score",
            "stockout_risk",
            "supplier_id",
        ]
    ].reset_index(drop=True),
    use_container_width=True,
    hide_index=True
)