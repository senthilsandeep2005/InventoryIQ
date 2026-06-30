import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
import streamlit as st
import plotly.express as px

from utils.style_loader import load_css
from utils.athena_client import run_query


st.set_page_config(
    page_title="Sales Analytics",
    page_icon="💰",
    layout="wide"
)

load_css()
st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)


@st.cache_data(ttl=3600)
def load_sales_data():
    return run_query("""
        SELECT
            s.sales_order_id,
            s.item_id,
            i.category AS category,
            i.supplier_id AS supplier_id,
            CAST(s.quantity_ordered AS DOUBLE) AS quantity_ordered,
            CAST(s.unit_price AS DOUBLE) AS unit_price,
            CAST(s.order_date AS VARCHAR) AS order_date,
            SUBSTR(CAST(s.order_date AS VARCHAR), 1, 7) AS order_month,
            ROUND(CAST(s.quantity_ordered AS DOUBLE) * CAST(s.unit_price AS DOUBLE), 2) AS calculated_revenue
        FROM sales_orders s
        LEFT JOIN inventory_data_cleaning i
            ON s.item_id = i.item_id
    """)


sales = load_sales_data()

sales["quantity_ordered"] = pd.to_numeric(sales["quantity_ordered"], errors="coerce")
sales["unit_price"] = pd.to_numeric(sales["unit_price"], errors="coerce")
sales["calculated_revenue"] = pd.to_numeric(sales["calculated_revenue"], errors="coerce")
sales["order_month"] = sales["order_month"].astype(str)


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


st.title("💰 Sales Analytics")
st.caption("Analyze revenue trends, category performance, top-selling SKUs, and customer demand.")

st.sidebar.header("Sales Filters")

category_options = ["All"] + sorted(sales["category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Category", category_options)

supplier_options = ["All"] + sorted(sales["supplier_id"].dropna().unique().tolist())
selected_supplier = st.sidebar.selectbox("Supplier", supplier_options)

month_options = ["All"] + sorted(sales["order_month"].dropna().unique().tolist())
selected_month = st.sidebar.selectbox("Order Month", month_options)

filtered_sales = sales.copy()

if selected_category != "All":
    filtered_sales = filtered_sales[filtered_sales["category"] == selected_category]

if selected_supplier != "All":
    filtered_sales = filtered_sales[filtered_sales["supplier_id"] == selected_supplier]

if selected_month != "All":
    filtered_sales = filtered_sales[filtered_sales["order_month"] == selected_month]

st.subheader("Filtered Sales Overview")

total_revenue = filtered_sales["calculated_revenue"].sum()
total_orders = filtered_sales["sales_order_id"].nunique()
units_sold = filtered_sales["quantity_ordered"].sum()
avg_order_value = total_revenue / total_orders if total_orders else 0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    metric_card("Revenue", f"${total_revenue:,.0f}", "💰")

with kpi2:
    metric_card("Orders", f"{total_orders:,}", "🧾")

with kpi3:
    metric_card("Units Sold", f"{units_sold:,.0f}", "📦")

with kpi4:
    metric_card("Avg Order Value", f"${avg_order_value:,.2f}", "📊")

st.divider()

left, right = st.columns(2)

with left:
    revenue_by_category = (
        filtered_sales.groupby("category", as_index=False)
        .agg(total_revenue=("calculated_revenue", "sum"))
        .sort_values("total_revenue", ascending=False)
    )

    fig_category = px.bar(
        revenue_by_category,
        x="category",
        y="total_revenue",
        title="Revenue by Category"
    )

    st.plotly_chart(fig_category, use_container_width=True)

with right:
    monthly_revenue = (
        filtered_sales.groupby("order_month", as_index=False)
        .agg(total_revenue=("calculated_revenue", "sum"))
        .sort_values("order_month")
    )

    fig_monthly = px.line(
        monthly_revenue,
        x="order_month",
        y="total_revenue",
        title="Monthly Revenue Trend",
        markers=True
    )

    st.plotly_chart(fig_monthly, use_container_width=True)

st.subheader("Top 10 Revenue SKUs")

top_skus = (
    filtered_sales.groupby(["item_id", "category", "supplier_id"], as_index=False)
    .agg(
        total_revenue=("calculated_revenue", "sum"),
        units_sold=("quantity_ordered", "sum"),
        order_count=("sales_order_id", "count")
    )
    .sort_values("total_revenue", ascending=False)
    .head(10)
)

st.dataframe(
    top_skus.reset_index(drop=True),
    use_container_width=True,
    hide_index=True
)

st.divider()

left, right = st.columns(2)

with left:
    supplier_summary = (
        filtered_sales.groupby("supplier_id", as_index=False)
        .agg(total_revenue=("calculated_revenue", "sum"))
        .sort_values("total_revenue", ascending=False)
    )

    fig_supplier = px.bar(
        supplier_summary,
        x="supplier_id",
        y="total_revenue",
        title="Revenue by Supplier"
    )

    st.plotly_chart(fig_supplier, use_container_width=True)

with right:
    fig_order_size = px.histogram(
        filtered_sales,
        x="quantity_ordered",
        nbins=25,
        title="Order Size Distribution"
    )

    st.plotly_chart(fig_order_size, use_container_width=True)

st.subheader("Sales Order Explorer")

st.dataframe(
    filtered_sales[
        [
            "sales_order_id",
            "item_id",
            "category",
            "supplier_id",
            "quantity_ordered",
            "unit_price",
            "calculated_revenue",
            "order_month"
        ]
    ]
    .sort_values("calculated_revenue", ascending=False)
    .reset_index(drop=True),
    use_container_width=True,
    hide_index=True
)