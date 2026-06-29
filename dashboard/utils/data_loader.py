import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"


def load_data():
    inventory = pd.read_csv(DATA_DIR / "inventory_data_cleaning.csv")
    suppliers = pd.read_csv(DATA_DIR / "suppliers_data.csv")
    sales = pd.read_csv(DATA_DIR / "sales_orders.csv")
    transactions = pd.read_csv(DATA_DIR / "inventory_transactions.csv")
    purchase_orders = pd.read_csv(DATA_DIR / "purchase_orders.csv")

    return (
        inventory,
        suppliers,
        sales,
        transactions,
        purchase_orders,
    )