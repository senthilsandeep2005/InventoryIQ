import streamlit as st
from utils.style_loader import load_css


st.set_page_config(
    page_title="InventoryIQ",
    page_icon="📦",
    layout="wide"
)

load_css()

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

st.title("📦 InventoryIQ")
st.subheader("Enterprise Inventory Optimization Platform")
st.markdown("**Developed by Sandeep Senthil**")

st.markdown(
    """
InventoryIQ is a cloud-native inventory analytics platform that demonstrates how organizations can centralize warehouse data, analyze operational performance, and generate business insights using AWS cloud services and interactive dashboards.

The platform uses **Amazon S3**, **Amazon Athena**, **SQL**, **Python**, **Pandas**, **Plotly**, and **Streamlit** to transform raw warehouse data into executive-ready analytics.
"""
)

st.markdown("### Platform Overview")

st.markdown(
    """
**Cloud Architecture**
- Amazon S3 Data Lake
- Amazon Athena Serverless SQL
- Python Data Processing
- Streamlit Interactive Dashboard
- Plotly Visual Analytics

**Dataset**
- Adapted from the Kaggle [Logistics Warehouse Dataset](https://www.kaggle.com/datasets/ziya07/logistics-warehouse-dataset)
- Modeled as a single-distribution-center inventory optimization platform
"""
)

st.markdown("### Dashboard Modules")

st.markdown(
    """
**📊 Executive Dashboard**  
Executive KPIs for inventory value, inventory health, high-risk SKUs, reorder recommendations, sales performance, and warehouse activity.

**📦 Inventory Analytics**  
Analyze inventory value, ABC classification, stock levels, inventory health, reorder points, and SKU-level trends.

**💰 Sales Analytics**  
Explore revenue trends, category performance, monthly sales, supplier sales, and top-performing SKUs.

**🚚 Supplier Analytics**  
Evaluate supplier reliability, on-time delivery, supplier risk, inventory exposure, and regional supplier performance.

**⚠️ Risk Center**  
Monitor stockout risk, slow-moving inventory, excess inventory, urgent reorder needs, and high-priority inventory risks.
"""
)

st.markdown("### How to Use InventoryIQ")

st.markdown(
    """
1. Use the sidebar navigation to open each dashboard module.
2. Apply page-specific filters to drill into categories, suppliers, months, and risk levels.
3. Hover over charts for detailed values.
4. Use the data tables to inspect SKU, supplier, sales, and risk records.
5. Analytics are powered by AWS S3 and Amazon Athena queries.
"""
)

st.markdown("### Technology Stack")

st.markdown(
    """
- Python
- AWS S3
- Amazon Athena
- SQL
- Pandas
- Plotly
- Streamlit
"""
)

st.info(
    "This project demonstrates cloud analytics, business intelligence, inventory optimization, and data visualization skills for Product Management, Solutions Engineering, Technical Sales, Business Analytics, and Cloud Architecture roles."
)