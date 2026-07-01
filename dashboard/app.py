from pathlib import Path
import streamlit as st
from utils.style_loader import load_css


st.set_page_config(
    page_title="Overview",
    page_icon="images/inventoryiq_logo_final.png",
    layout="wide",
)

load_css()
PROJECT_ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = PROJECT_ROOT / "images"


st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] ul li:first-child a span {
        display: none !important;
    }

    [data-testid="stSidebarNav"] ul li:first-child a::after {
        content: "Overview";
        font-size: 14px;
        font-weight: 600;
        color: #0f172a;
    }

    [data-testid="stSidebarNav"] ul li:first-child a {
        display: flex !important;
        align-items: center !important;
        padding: 0.45rem 0.75rem !important;
        border-radius: 10px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = PROJECT_ROOT / "images"

st.sidebar.image(str(IMAGE_DIR / "inventoryiq_logo_final.png"), use_container_width=True)

st.image(str(IMAGE_DIR / "inventoryiq_logo_final.png"), width=360)

st.subheader("Enterprise Inventory Optimization Platform")
st.markdown("**Developed by Sandeep Senthil**")

st.markdown(
    """
InventoryIQ is a cloud-based inventory analytics platform that helps users explore inventory performance, sales trends, supplier reliability, and operational risk through interactive dashboards.
"""
)

st.markdown("### Dashboard Modules")

st.markdown(
    """
**Executive Dashboard**  
High-level KPIs for inventory value, health score, high-risk SKUs, sales trends, and reorder priorities.

**Inventory Analytics**  
SKU-level analysis of stock levels, inventory value, ABC classification, reorder points, and stockout risk.

**Sales Analytics**  
Revenue, order volume, units sold, average order value, monthly trends, and top-performing SKUs.

**Supplier Analytics**  
Supplier reliability, on-time delivery, supplier risk, regional performance, and inventory exposure.

**Risk Center**  
High-risk inventory, reorder priority, stockout risk, excess inventory, and operational risk monitoring.
"""
)

st.markdown("### How to Use InventoryIQ")

st.markdown(
    """
1. Use the sidebar to open each dashboard module.
2. Apply filters to drill into categories, suppliers, months, and risk levels.
3. Hover over charts to view detailed values.
4. Review tables for SKU, supplier, sales, and risk records.
"""
)
st.info(
    "InventoryIQ converts warehouse, sales, supplier, and transaction data into interactive dashboards that help users explore inventory health, demand trends, supplier performance, and operational risk."
)