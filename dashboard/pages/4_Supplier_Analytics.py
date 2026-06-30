import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
import plotly.express as px

from utils.style_loader import load_css
from utils.data_loader import load_data

PROJECT_ROOT = Path(__file__).resolve().parents[2]
IMAGE_DIR = PROJECT_ROOT / "images"
st.set_page_config(
    page_title="Supplier Analytics",
    page_icon="🚚",
    layout="wide"
)

load_css()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
IMAGE_DIR = PROJECT_ROOT / "images"

st.sidebar.image(str(IMAGE_DIR / "inventoryiq_logo_final.png"), use_container_width=True)
st.sidebar.markdown("---")
st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)


inventory, suppliers, sales, transactions, purchase_orders = load_data()
numeric_inventory_columns = [
    "inventory_value",
    "days_of_inventory",
]

for col in numeric_inventory_columns:
    if col in inventory.columns:
        inventory[col] = inventory[col].astype(float)

numeric_supplier_columns = [
    "reliability_score",
    "on_time_delivery_rate",
]

for col in numeric_supplier_columns:
    if col in suppliers.columns:
        suppliers[col] = suppliers[col].astype(float)

supplier_inventory = inventory.merge(
    suppliers,
    on="supplier_id",
    how="left"
)
col_icon, col_title = st.columns([0.08, 0.92])
with col_icon:
    st.image(str(IMAGE_DIR / "supplier_icon.png"), width=54)
with col_title:
    st.title("Supplier Analytics")
st.caption("Evaluate supplier reliability, inventory exposure, delivery performance, and supplier risk.")

st.sidebar.header("Supplier Filters")

supplier_options = ["All"] + sorted(supplier_inventory["supplier_id"].dropna().unique().tolist())
selected_supplier = st.sidebar.selectbox("Supplier", supplier_options)

region_options = ["All"] + sorted(supplier_inventory["supplier_region"].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Supplier Region", region_options)

risk_options = ["All"] + sorted(supplier_inventory["supplier_risk_level"].dropna().unique().tolist())
selected_risk = st.sidebar.selectbox("Supplier Risk", risk_options)

filtered_suppliers = supplier_inventory.copy()

if selected_supplier != "All":
    filtered_suppliers = filtered_suppliers[filtered_suppliers["supplier_id"] == selected_supplier]

if selected_region != "All":
    filtered_suppliers = filtered_suppliers[filtered_suppliers["supplier_region"] == selected_region]

if selected_risk != "All":
    filtered_suppliers = filtered_suppliers[filtered_suppliers["supplier_risk_level"] == selected_risk]


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


st.subheader("Supplier Performance Overview")

total_suppliers = filtered_suppliers["supplier_id"].nunique()
avg_reliability = filtered_suppliers["reliability_score"].mean()
avg_delivery_rate = filtered_suppliers["on_time_delivery_rate"].mean()
inventory_value = filtered_suppliers["inventory_value"].sum()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    metric_card("Suppliers", f"{total_suppliers:,}", "")

with kpi2:
    metric_card("Avg Reliability", f"{avg_reliability:.3f}", "")

with kpi3:
    metric_card("On-Time Delivery", f"{avg_delivery_rate:.3f}", "⏱")

with kpi4:
    metric_card("Inventory Value", f"${inventory_value:,.0f}", "")

st.divider()

left, right = st.columns(2)

with left:
    supplier_value = (
        filtered_suppliers.groupby(["supplier_id", "supplier_name"], as_index=False)
        .agg(total_inventory_value=("inventory_value", "sum"))
        .sort_values("total_inventory_value", ascending=False)
    )

    fig_value = px.bar(
        supplier_value,
        x="supplier_id",
        y="total_inventory_value",
        title="Inventory Value by Supplier"
    )

    st.plotly_chart(fig_value, use_container_width=True)

with right:
    reliability_chart = (
        filtered_suppliers.groupby(["supplier_id", "supplier_name"], as_index=False)
        .agg(avg_reliability=("reliability_score", "mean"))
        .sort_values("avg_reliability", ascending=False)
    )

    fig_reliability = px.bar(
        reliability_chart,
        x="supplier_id",
        y="avg_reliability",
        title="Supplier Reliability Score"
    )

    st.plotly_chart(fig_reliability, use_container_width=True)

st.divider()

left, right = st.columns(2)

with left:
    risk_summary = (
        filtered_suppliers.groupby("supplier_risk_level", as_index=False)
        .agg(sku_count=("item_id", "count"))
        .sort_values("sku_count", ascending=False)
    )

    fig_risk = px.pie(
        risk_summary,
        names="supplier_risk_level",
        values="sku_count",
        title="Supplier Risk Breakdown"
    )

    st.plotly_chart(fig_risk, use_container_width=True)

with right:
    region_summary = (
        filtered_suppliers.groupby("supplier_region", as_index=False)
        .agg(total_inventory_value=("inventory_value", "sum"))
        .sort_values("total_inventory_value", ascending=False)
    )

    fig_region = px.bar(
        region_summary,
        x="supplier_region",
        y="total_inventory_value",
        title="Inventory Value by Supplier Region"
    )

    st.plotly_chart(fig_region, use_container_width=True)

st.subheader("Supplier Performance Table")

supplier_table = (
    filtered_suppliers.groupby(
        [
            "supplier_id",
            "supplier_name",
            "supplier_region",
            "supplier_risk_level",
            "reliability_score",
            "on_time_delivery_rate",
        ],
        as_index=False
    )
    .agg(
        sku_count=("item_id", "count"),
        total_inventory_value=("inventory_value", "sum"),
        avg_days_inventory=("days_of_inventory", "mean"),
        high_risk_skus=("stockout_risk", lambda x: (x == "High").sum())
    )
    .sort_values("total_inventory_value", ascending=False)
)

st.dataframe(
    supplier_table.reset_index(drop=True),
    use_container_width=True,
    hide_index=True
)