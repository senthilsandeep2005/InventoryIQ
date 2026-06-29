import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FOLDER = PROJECT_ROOT / "data"

INVENTORY_FILE = DATA_FOLDER / "inventory_data_cleaning.csv"
SALES_ORDERS_FILE = DATA_FOLDER / "sales_orders.csv"
OUTPUT_FILE = DATA_FOLDER / "inventory_data_cleaning.csv"

inventory = pd.read_csv(INVENTORY_FILE)
sales_orders = pd.read_csv(SALES_ORDERS_FILE)

sales_orders["order_date"] = pd.to_datetime(sales_orders["order_date"])

latest_date = sales_orders["order_date"].max()

recent_start = latest_date - pd.Timedelta(days=90)
previous_start = latest_date - pd.Timedelta(days=180)

recent_sales = sales_orders[
    sales_orders["order_date"] > recent_start
]

previous_sales = sales_orders[
    (sales_orders["order_date"] > previous_start) &
    (sales_orders["order_date"] <= recent_start)
]

recent_demand = (
    recent_sales
    .groupby("item_id")["quantity_ordered"]
    .sum()
    .reset_index()
    .rename(columns={"quantity_ordered": "recent_90d_demand"})
)

previous_demand = (
    previous_sales
    .groupby("item_id")["quantity_ordered"]
    .sum()
    .reset_index()
    .rename(columns={"quantity_ordered": "previous_90d_demand"})
)

demand_growth = pd.merge(
    previous_demand,
    recent_demand,
    on="item_id",
    how="outer"
).fillna(0)

demand_growth["demand_growth_pct"] = demand_growth.apply(
    lambda row: 0 if row["previous_90d_demand"] == 0
    else (row["recent_90d_demand"] - row["previous_90d_demand"]) / row["previous_90d_demand"],
    axis=1
)

inventory = inventory.drop(columns=["demand_growth_pct"], errors="ignore")

inventory = inventory.merge(
    demand_growth[["item_id", "demand_growth_pct"]],
    on="item_id",
    how="left"
)

inventory["demand_growth_pct"] = inventory["demand_growth_pct"].fillna(0)

inventory.to_csv(OUTPUT_FILE, index=False)

print("demand_growth_pct updated successfully.")
print(f"Latest sales order date: {latest_date.date()}")
print(f"Saved to: {OUTPUT_FILE}")