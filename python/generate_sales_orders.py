import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FOLDER = PROJECT_ROOT / "data"

INVENTORY_FILE = DATA_FOLDER / "inventory_data_cleaning.csv"
OUTPUT_FILE = DATA_FOLDER / "sales_orders.csv"

inventory = pd.read_csv(INVENTORY_FILE)

required_columns = ["item_id", "unit_price"]

for_column_error = []
for column in required_columns:
    if column not in inventory.columns:
        for_column_error.append(column)

if for_column_error:
    raise ValueError(f"Missing required columns: {for_column_error}")

num_sales_orders = 25000

order_statuses = ["Fulfilled", "Backordered", "Cancelled"]
status_weights = [0.88, 0.09, 0.03]

sales_orders = []

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

for i in range(1, num_sales_orders + 1):
    item = inventory.sample(1).iloc[0]

    item_id = item["item_id"]
    unit_price = float(item["unit_price"])

    order_date = start_date + timedelta(
        days=random.randint(0, (end_date - start_date).days)
    )

    quantity_ordered = random.randint(1, 25)

    sales_revenue = round(quantity_ordered * unit_price, 2)

    order_status = random.choices(order_statuses, weights=status_weights, k=1)[0]

    sales_orders.append(
        {
            "sales_order_id": f"SO{i:05d}",
            "customer_id": f"CUST{random.randint(1, 500):04d}",
            "item_id": item_id,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "quantity_ordered": quantity_ordered,
            "unit_price": unit_price,
            "sales_revenue": sales_revenue,
            "order_status": order_status,
        }
    )

sales_orders_df = pd.DataFrame(sales_orders)

sales_orders_df.to_csv(OUTPUT_FILE, index=False)

print("sales_orders.csv created successfully.")
print(f"Rows created: {len(sales_orders_df)}")
print(f"Saved to: {OUTPUT_FILE}")