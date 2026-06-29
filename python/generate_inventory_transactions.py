import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FOLDER = PROJECT_ROOT / "data"

INVENTORY_FILE = DATA_FOLDER / "inventory_data_cleaning.csv"
OUTPUT_FILE = DATA_FOLDER / "inventory_transactions.csv"

inventory = pd.read_csv(INVENTORY_FILE)

required_columns = ["item_id"]

for column in required_columns:
    if column not in inventory.columns:
        raise ValueError(f"Missing required column: {column}")

num_transactions = 75000

event_types = [
    "customer_order",
    "restock",
    "inventory_adjustment",
    "damaged_inventory",
    "return"
]

event_weights = [0.55, 0.20, 0.10, 0.08, 0.07]

transaction_reasons = {
    "customer_order": "Customer sale fulfilled",
    "restock": "Supplier replenishment received",
    "inventory_adjustment": "Cycle count adjustment",
    "damaged_inventory": "Damaged or expired inventory removed",
    "return": "Customer return received"
}

transactions = []

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

for i in range(1, num_transactions + 1):
    item = inventory.sample(1).iloc[0]
    item_id = item["item_id"]

    transaction_timestamp = start_date + timedelta(
        days=random.randint(0, (end_date - start_date).days),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )

    event_type = random.choices(event_types, weights=event_weights, k=1)[0]

    if event_type == "customer_order":
        quantity_change = -random.randint(1, 25)
    elif event_type == "restock":
        quantity_change = random.randint(50, 1000)
    elif event_type == "inventory_adjustment":
        quantity_change = random.choice([-1, 1]) * random.randint(1, 20)
    elif event_type == "damaged_inventory":
        quantity_change = -random.randint(1, 15)
    else:
        quantity_change = random.randint(1, 10)

    transactions.append(
        {
            "transaction_id": f"TXN{i:06d}",
            "item_id": item_id,
            "transaction_timestamp": transaction_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "event_type": event_type,
            "quantity_change": quantity_change,
            "transaction_reason": transaction_reasons[event_type],
        }
    )

transactions_df = pd.DataFrame(transactions)

transactions_df.to_csv(OUTPUT_FILE, index=False)

print("inventory_transactions.csv created successfully.")
print(f"Rows created: {len(transactions_df)}")
print(f"Saved to: {OUTPUT_FILE}")