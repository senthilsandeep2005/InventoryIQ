import streamlit as st
from utils.style_loader import load_css


st.set_page_config(
    page_title="InventoryIQ",
    page_icon="📦",
    layout="wide"
)

load_css()

st.title("📦 InventoryIQ")

st.subheader("Enterprise Inventory Optimization Platform")

st.markdown("""
Welcome to InventoryIQ.

This application demonstrates an end-to-end inventory optimization platform built with:

- Python
- Amazon S3
- Amazon Athena
- SQL
- Streamlit
- Plotly

Use the navigation menu on the left to explore:

- Executive Dashboard
- Inventory Analytics
- Sales Analytics
- Supplier Analytics
- Risk Center
""")