import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
import streamlit as st
import plotly.express as px



from utils.athena_client import run_sql_file
from utils.style_loader import load_css
from utils.data_loader import load_data
PROJECT_ROOT = Path(__file__).resolve().parents[2]
IMAGE_DIR = PROJECT_ROOT / "images"

st.set_page_config(
    page_title="InventoryIQ Dashboard",
    page_icon="📦",
    layout="wide"
)

load_css()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
IMAGE_DIR = PROJECT_ROOT / "images"

st.sidebar.image(str(IMAGE_DIR / "inventoryiq_logo_final.png"), use_container_width=True)
st.sidebar.markdown("---")
st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

inventory, suppliers, sales, transactions, purchase_orders = load_data()

# Clean numeric fields used by local table logic
numeric_inventory_columns = [
    "stock_level",
    "reorder_point",
    "days_of_inventory",
    "reorder_quantity",
    "inventory_value",
    "kpi_score",
]

for col in numeric_inventory_columns:
    if col in inventory.columns:
        inventory[col] = pd.to_numeric(inventory[col], errors="coerce")

if "transaction_type" in transactions.columns:
    transactions["event_type"] = transactions["transaction_type"]

if "event_type" in transactions.columns:
    transactions["transaction_type"] = transactions["event_type"]


def metric_card(label, value, icon):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def format_number(value):
    return f"{float(value):,.0f}"


def format_currency(value):
    return f"${float(value):,.0f}"

header_col1, header_col2 = st.columns([0.055, 0.945], vertical_alignment="center")

with header_col1:
    st.image(str(IMAGE_DIR / "executive_dashboard_icon.png"), width=62)

with header_col2:
    st.markdown(
        "<h1 style='margin:0; padding:0;'>Executive Dashboard</h1>",
        unsafe_allow_html=True
    )
st.caption("Intelligent Inventory Optimization Platform | Python + AWS S3 + Athena + Streamlit")

# KPI cards powered directly by Athena SQL
kpi_df = run_sql_file("executive_kpis_athena.sql")

total_skus = int(float(kpi_df.loc[0, "total_skus"]))
total_inventory_value = float(kpi_df.loc[0, "total_inventory_value"])
avg_health_score = float(kpi_df.loc[0, "avg_inventory_health_score"])
high_risk_skus = int(float(kpi_df.loc[0, "high_risk_skus"]))
total_reorder_qty = float(kpi_df.loc[0, "total_reorder_quantity"])

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    metric_card("Total SKUs", f"{total_skus:,}", "")

with kpi2:
    metric_card("Inventory Value", format_currency(total_inventory_value), "")

with kpi3:
    metric_card("Avg Health Score", f"{avg_health_score:.3f}", "")

with kpi4:
    metric_card("High Risk SKUs", f"{high_risk_skus:,}", "")

with kpi5:
    metric_card("Reorder Qty", format_number(total_reorder_qty), "")

st.divider()

left, right = st.columns(2)

with left:
    inventory_by_category = run_sql_file("inventory_value_by_category_athena.sql")
    inventory_by_category["total_inventory_value"] = pd.to_numeric(
        inventory_by_category["total_inventory_value"], errors="coerce"
    )

    fig_inventory = px.bar(
        inventory_by_category,
        x="category",
        y="total_inventory_value",
        title="Inventory Value by Category"
    )

    st.plotly_chart(fig_inventory, use_container_width=True)

with right:
    sales_by_category = run_sql_file("sales_revenue_by_category_athena.sql")
    sales_by_category["total_revenue"] = pd.to_numeric(
        sales_by_category["total_revenue"], errors="coerce"
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
    monthly_sales = run_sql_file("monthly_sales_trend_athena.sql")

    if "sales_month" not in monthly_sales.columns and "order_month" in monthly_sales.columns:
        monthly_sales = monthly_sales.rename(columns={"order_month": "sales_month"})

    monthly_sales["total_revenue"] = pd.to_numeric(
        monthly_sales["total_revenue"], errors="coerce"
    )

    monthly_sales = monthly_sales.sort_values("sales_month")

    fig_monthly = px.line(
        monthly_sales,
        x="sales_month",
        y="total_revenue",
        title="Monthly Sales Trend",
        markers=True
    )

    st.plotly_chart(fig_monthly, use_container_width=True)

with right:
    transaction_summary = run_sql_file("transaction_activity_athena.sql")

    if "transaction_type" in transaction_summary.columns and "event_type" not in transaction_summary.columns:
        transaction_summary = transaction_summary.rename(columns={"transaction_type": "event_type"})

    if "transaction_count" not in transaction_summary.columns:
        count_column = [col for col in transaction_summary.columns if "count" in col.lower()]
        if count_column:
            transaction_summary = transaction_summary.rename(columns={count_column[0]: "transaction_count"})

    transaction_summary["transaction_count"] = pd.to_numeric(
        transaction_summary["transaction_count"], errors="coerce"
    )

    fig_transactions = px.pie(
        transaction_summary,
        names="event_type",
        values="transaction_count",
        title="Warehouse Transaction Activity"
    )

    st.plotly_chart(fig_transactions, use_container_width=True)

st.divider()

st.subheader("High Risk SKUs")

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

st.subheader("Reorder Priority Recommendations")

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