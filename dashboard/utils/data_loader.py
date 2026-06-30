import pandas as pd
import streamlit as st
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

USE_ATHENA = True


def clean_numeric_columns(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def load_local_data():
    inventory = pd.read_csv(DATA_DIR / "inventory_data_cleaning.csv")
    suppliers = pd.read_csv(DATA_DIR / "suppliers_data.csv")
    sales = pd.read_csv(DATA_DIR / "sales_orders.csv")
    transactions = pd.read_csv(DATA_DIR / "inventory_transactions.csv")
    purchase_orders = pd.read_csv(DATA_DIR / "purchase_orders.csv")

    return inventory, suppliers, sales, transactions, purchase_orders


@st.cache_data(ttl=3600)
def load_athena_data():
    from utils.athena_client import run_query
    status = st.status(
        "Loading InventoryIQ cloud data from Amazon Athena...",
        expanded=True
    )

    status.write("Connecting to AWS S3 data lake...")
    status.write("Running Athena queries...")
    status.write("Processing inventory, sales, supplier, and risk analytics...")

    inventory = run_query("SELECT * FROM inventory_data_cleaning")
    suppliers = run_query("SELECT * FROM suppliers_data")
    sales = run_query("SELECT * FROM sales_orders")
    transactions = run_query("SELECT * FROM inventory_transactions")
    purchase_orders = run_query("SELECT * FROM purchase_orders")

    status.update(
        label="InventoryIQ cloud data loaded successfully.",
        state="complete",
        expanded=False
    )
   
    # Make Athena transaction columns compatible with dashboard code
    if "event_type" in transactions.columns:
        transactions["transaction_type"] = transactions["event_type"]

    if "transaction_type" in transactions.columns:
        transactions["event_type"] = transactions["transaction_type"]

    if "transaction_timestamp" in transactions.columns:
        transactions["transaction_date"] = transactions["transaction_timestamp"]

    if "quantity_change" in transactions.columns:
        transactions["quantity"] = transactions["quantity_change"]

    inventory = clean_numeric_columns(
        inventory,
        [
            "stock_level",
            "reorder_point",
            "reorder_frequency_days",
            "lead_time_days",
            "daily_demand",
            "demand_std_dev",
            "item_popularity_score",
            "unit_price",
            "holding_cost_per_unit_day",
            "stockout_count_last_month",
            "order_fulfillment_rate",
            "total_orders_last_month",
            "turnover_ratio",
            "layout_efficiency_score",
            "forecasted_demand_next_7d",
            "kpi_score",
            "inventory_value",
            "days_of_inventory",
            "inventory_coverage_days",
            "holding_cost_exposure",
            "safety_stock",
            "reorder_quantity",
            "demand_growth_pct",
        ],
    )

    suppliers = clean_numeric_columns(
        suppliers,
        ["reliability_score", "on_time_delivery_rate"],
    )

    sales = clean_numeric_columns(
        sales,
        ["quantity_ordered", "unit_price"],
    )

    transactions = clean_numeric_columns(
        transactions,
        ["quantity", "quantity_change"],
    )

    purchase_orders = clean_numeric_columns(
        purchase_orders,
        ["quantity_ordered", "unit_cost"],
    )

    return inventory, suppliers, sales, transactions, purchase_orders


def load_data():
    if USE_ATHENA:
        return load_athena_data()

    return load_local_data()