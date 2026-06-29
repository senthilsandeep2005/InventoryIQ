import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

# Set random seed so results are reproducible
random.seed(42)

# Project paths based on your current folder/file names
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FOLDER = PROJECT_ROOT / "data"

INVENTORY_FILE = DATA_FOLDER / "inventory_data_cleaning.csv"
SUPPLIERS_FILE = DATA_FOLDER / "suppliers_data.csv"
OUTPUT_FILE = DATA_FOLDER / "purchase_orders.csv"

# Load cleaned inventory data and suppliers data
inventory = pd.read_csv(INVENTORY_FILE)
suppliers = pd.read_csv(SUPPLIERS_FILE)

# Basic validation to catch common file/data issues early
required_inventory_columns = [
    "item_id",
    "unit_price",
    "lead_time_days",
]

for column in required_inventory_columns:
    if column not in inventory.columns:
        raise ValueError(f"Missing required column in inventory file: {column}")

if "supplier_id" not in inventory.columns:
    raise ValueError(
        "Missing supplier_id in inventory_data_cleaning.csv. "
        "Add/populate supplier_id before generating purchase orders."
    )

if "supplier_id" not in suppliers.columns:
    raise ValueError("Missing supplier_id in suppliers data.csv")

# Remove rows without supplier_id because purchase orders must connect to suppliers
inventory = inventory.dropna(subset=["supplier_id"])

if inventory.empty:
    raise ValueError(
        "No inventory rows have supplier_id filled in. "
        "Populate supplier_id before running this script."
    )

# Number of purchase orders to generate
num_purchase_orders = 7500

# Possible purchase order statuses
po_statuses = ["Delivered", "Open", "Delayed", "Cancelled"]
status_weights = [0.75, 0.12, 0.10, 0.03]

purchase_orders = []

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

for i in range(1, num_purchase_orders + 1):
    item = inventory.sample(1).iloc[0]

    item_id = item["item_id"]
    supplier_id = item["supplier_id"]
    unit_price = float(item["unit_price"])
    lead_time_days = int(item["lead_time_days"])

    order_date = start_date + timedelta(
        days=random.randint(0, (end_date - start_date).days)
    )

    expected_delivery_date = order_date + timedelta(days=lead_time_days)

    po_status = random.choices(po_statuses, weights=status_weights, k=1)[0]

    if po_status == "Delivered":
        actual_delivery_date = expected_delivery_date + timedelta(days=random.randint(-2, 3))
    elif po_status == "Delayed":
        actual_delivery_date = expected_delivery_date + timedelta(days=random.randint(4, 14))
    else:
        actual_delivery_date = ""

    order_quantity = random.randint(50, 1000)

    # Assume supplier purchase cost is about 60% to 80% of selling price
    unit_cost = round(unit_price * random.uniform(0.60, 0.80), 2)
    total_purchase_cost = round(order_quantity * unit_cost, 2)

    purchase_orders.append(
        {
            "po_id": f"PO{i:05d}",
            "supplier_id": supplier_id,
            "item_id": item_id,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "expected_delivery_date": expected_delivery_date.strftime("%Y-%m-%d"),
            "actual_delivery_date": actual_delivery_date
            if actual_delivery_date == ""
            else actual_delivery_date.strftime("%Y-%m-%d"),
            "order_quantity": order_quantity,
            "unit_cost": unit_cost,
            "total_purchase_cost": total_purchase_cost,
            "po_status": po_status,
        }
    )

purchase_orders_df = pd.DataFrame(purchase_orders)

purchase_orders_df.to_csv(OUTPUT_FILE, index=False)

print("purchase_orders.csv created successfully.")
print(f"Rows created: {len(purchase_orders_df)}")
print(f"Saved to: {OUTPUT_FILE}")