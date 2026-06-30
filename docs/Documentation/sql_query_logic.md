# InventoryIQ SQL Query Logic

## Purpose of the SQL Analytics Layer

The SQL analytics layer is where InventoryIQ turns raw operational data into business insights. The CSV files store the data, but SQL allows us to ask structured business questions such as:

* Which SKUs are most at risk of stocking out?
* Which products should be reordered?
* Which categories hold the most inventory value?
* Which suppliers are the most reliable?
* Which product categories generate the most revenue?
* What types of inventory transactions happen most often?
* Which SKUs are most financially important?
* What are the top-level executive KPIs for the distribution center?

Each `.sql` file contains one main SQL query. Each query is designed to answer one business analytics question.

---

# SQL Concepts Used

## SELECT

`SELECT` tells SQL which columns or calculations we want to return.

Example:

```sql
SELECT item_id, category, stock_level
```

This means: show the item ID, category, and stock level columns.

---

## FROM

`FROM` tells SQL which table to pull data from.

Example:

```sql
FROM inventory_data_cleaning
```

This means: use the inventory table as the source data.

---

## WHERE

`WHERE` filters rows based on a condition.

Example:

```sql
WHERE stockout_risk = 'High'
```

This means: only show rows where the stockout risk is High.

---

## ORDER BY

`ORDER BY` sorts the result.

Example:

```sql
ORDER BY reorder_quantity DESC
```

This means: sort the results from highest reorder quantity to lowest.

---

## GROUP BY

`GROUP BY` groups rows together so we can summarize them.

Example:

```sql
GROUP BY category
```

This means: combine rows by product category so we can calculate totals or averages for each category.

---

## Aggregate Functions

Aggregate functions summarize multiple rows.

Common ones used in this project:

```sql
COUNT()
SUM()
AVG()
```

Examples:

```sql
COUNT(item_id)
```

Counts how many SKUs exist.

```sql
SUM(inventory_value)
```

Adds up total inventory value.

```sql
AVG(kpi_score)
```

Calculates the average inventory health score.

---

## JOIN

`JOIN` combines data from two tables.

Example:

```sql
JOIN inventory_data_cleaning i
    ON s.item_id = i.item_id
```

This means: connect sales orders to inventory records using the matching `item_id`.

This matters because sales orders only tell us what item was sold. The inventory table tells us the category, stock level, and other product information.

---

## LEFT JOIN

`LEFT JOIN` keeps every row from the left table, even if there is no matching row in the right table.

Example:

```sql
FROM suppliers_data s
LEFT JOIN purchase_orders p
    ON s.supplier_id = p.supplier_id
```

This means: keep every supplier, even if a supplier does not have purchase orders.

This is useful because in supplier analysis, we usually want to see all suppliers, not only the ones with matching orders.

---

## CASE

`CASE` creates conditional logic inside SQL.

Example:

```sql
CASE
    WHEN inventory_value >= 50000 THEN 'A'
    WHEN inventory_value >= 15000 THEN 'B'
    ELSE 'C'
END AS abc_class
```

This means:

* If inventory value is at least 50,000, classify it as A
* If inventory value is at least 15,000, classify it as B
* Otherwise, classify it as C

This is similar to an IF statement in Excel.

---

# 1. high_risk_skus.sql

## Business Question

Which inventory items are currently at the highest risk of stocking out?

## Query

```sql
SELECT
    item_id,
    category,
    stock_level,
    reorder_point,
    days_of_inventory,
    stockout_risk,
    reorder_quantity
FROM inventory_data_cleaning
WHERE stockout_risk = 'High'
ORDER BY reorder_quantity DESC;
```

## Logic

This query pulls inventory items from the main inventory table where `stockout_risk` equals `High`.

It selects the most important columns needed to understand the risk:

* `item_id`: identifies the SKU
* `category`: shows what type of product it is
* `stock_level`: shows how much inventory is currently available
* `reorder_point`: shows the threshold where replenishment should happen
* `days_of_inventory`: estimates how many days of stock remain
* `stockout_risk`: shows the risk level
* `reorder_quantity`: shows how much inventory is recommended to reorder

The query then sorts the result by `reorder_quantity` from highest to lowest.

## Why This Matters

This helps operations and procurement teams quickly identify which SKUs need attention first. Instead of reviewing all 3,204 SKUs manually, the query filters the dataset down to the highest-risk items.

## Interview Explanation

I would explain this query by saying:

“This query identifies SKUs with high stockout risk and ranks them by reorder quantity. The goal is to help inventory or procurement teams prioritize the products that need replenishment most urgently.”

---

# 2. reorder_recommendations.sql

## Business Question

Which SKUs should be reordered, and how much should be reordered?

## Query

```sql
SELECT
    item_id,
    category,
    stock_level,
    reorder_point,
    reorder_quantity,
    safety_stock,
    stockout_risk
FROM inventory_data_cleaning
WHERE reorder_quantity > 0
ORDER BY reorder_quantity DESC;
```

## Logic

This query looks for inventory items where `reorder_quantity` is greater than zero.

The logic is simple:

* If `reorder_quantity = 0`, the item does not need immediate replenishment.
* If `reorder_quantity > 0`, the item is below its target level and should be reordered.

The selected columns explain why the item needs to be reordered:

* `stock_level`: current available inventory
* `reorder_point`: the threshold that triggers replenishment
* `reorder_quantity`: how much should be ordered
* `safety_stock`: buffer inventory used to reduce stockout risk
* `stockout_risk`: risk category for the SKU

The results are sorted from the largest reorder quantity to the smallest.

## Why This Matters

This turns inventory data into a replenishment action list. A manager could use this output to decide which purchase orders to create first.

## Interview Explanation

I would explain this query by saying:

“This query creates a reorder recommendation list by filtering for SKUs with positive reorder quantities. It helps translate inventory risk into an actionable procurement decision.”

---

# 3. inventory_value_by_category.sql

## Business Question

Which product categories have the most money tied up in inventory?

## Query

```sql
SELECT
    category,
    SUM(inventory_value) AS total_inventory_value,
    AVG(inventory_value) AS average_inventory_value,
    COUNT(item_id) AS sku_count
FROM inventory_data_cleaning
GROUP BY category
ORDER BY total_inventory_value DESC;
```

## Logic

This query groups inventory records by `category`.

For each category, it calculates:

* `SUM(inventory_value)`: total dollar value of inventory in that category
* `AVG(inventory_value)`: average inventory value per SKU in that category
* `COUNT(item_id)`: number of SKUs in that category

The query then sorts categories by total inventory value from highest to lowest.

## Why This Matters

Inventory value shows where the company has the most capital tied up. High-value categories may need closer monitoring because excess inventory in those categories can be expensive.

## Interview Explanation

I would explain this query by saying:

“This query summarizes inventory value by category to show where the distribution center has the most capital tied up. It helps leaders identify which categories are financially most important from an inventory management perspective.”

---

# 4. supplier_performance.sql

## Business Question

Which suppliers are most reliable, and how much purchase spend is tied to each supplier?

## Query

```sql
SELECT
    s.supplier_id,
    s.supplier_name,
    s.supplier_region,
    s.reliability_score,
    s.on_time_delivery_rate,
    s.supplier_risk_level,
    COUNT(p.po_id) AS total_purchase_orders,
    SUM(p.total_purchase_cost) AS total_purchase_spend
FROM suppliers_data s
LEFT JOIN purchase_orders p
    ON s.supplier_id = p.supplier_id
GROUP BY
    s.supplier_id,
    s.supplier_name,
    s.supplier_region,
    s.reliability_score,
    s.on_time_delivery_rate,
    s.supplier_risk_level
ORDER BY s.reliability_score DESC;
```

## Logic

This query combines the supplier table with the purchase orders table.

The supplier table contains supplier details:

* supplier name
* region
* reliability score
* on-time delivery rate
* supplier risk level

The purchase orders table contains order activity and purchase spend.

The query uses a `LEFT JOIN` so every supplier remains in the result, even if they do not have matching purchase orders.

The table aliases make the query easier to read:

* `s` means `suppliers_data`
* `p` means `purchase_orders`

The join condition is:

```sql
ON s.supplier_id = p.supplier_id
```

This means supplier records and purchase orders are connected using the supplier ID.

Then the query groups by each supplier and calculates:

* `COUNT(p.po_id)`: number of purchase orders connected to the supplier
* `SUM(p.total_purchase_cost)`: total purchase spend connected to the supplier

The results are sorted by reliability score from highest to lowest.

## Why This Matters

Supplier performance is important in inventory management because unreliable suppliers can increase stockout risk. A supplier with low reliability or poor on-time delivery may cause late replenishment, which can affect customer fulfillment.

## Interview Explanation

I would explain this query by saying:

“This query joins supplier master data with purchase order activity to compare supplier reliability, risk, order volume, and purchase spend. It helps evaluate which suppliers are dependable and which ones may create operational risk.”

---

# 5. sales_revenue_by_category.sql

## Business Question

Which product categories generate the most sales revenue?

## Query

```sql
SELECT
    i.category,
    SUM(s.sales_revenue) AS total_sales_revenue,
    SUM(s.quantity_ordered) AS total_units_sold,
    COUNT(s.sales_order_id) AS total_orders
FROM sales_orders s
JOIN inventory_data_cleaning i
    ON s.item_id = i.item_id
WHERE s.order_status = 'Fulfilled'
GROUP BY i.category
ORDER BY total_sales_revenue DESC;
```

## Logic

This query combines sales order data with inventory data.

The sales orders table tells us:

* which item was ordered
* quantity ordered
* sales revenue
* order status

The inventory table tells us:

* what category each item belongs to

The query joins the two tables using `item_id`.

The aliases are:

* `s` means `sales_orders`
* `i` means `inventory_data_cleaning`

The join condition is:

```sql
ON s.item_id = i.item_id
```

This means each sales order is matched to the correct inventory item.

The query filters only fulfilled orders:

```sql
WHERE s.order_status = 'Fulfilled'
```

This is important because cancelled or backordered orders should not be counted as completed revenue.

Then the query groups by product category and calculates:

* `SUM(s.sales_revenue)`: total fulfilled sales revenue by category
* `SUM(s.quantity_ordered)`: total units sold by category
* `COUNT(s.sales_order_id)`: number of fulfilled orders by category

The result is sorted by total sales revenue from highest to lowest.

## Why This Matters

This query shows which categories drive the most revenue. A business can use this to prioritize inventory planning for high-revenue categories.

## Interview Explanation

I would explain this query by saying:

“This query joins sales orders to inventory data so revenue can be analyzed by product category. It filters for fulfilled orders only, then calculates total revenue, units sold, and order volume by category.”

---

# 6. transaction_activity.sql

## Business Question

What types of inventory transactions happen most often, and what is their net impact on inventory quantity?

## Query

```sql
SELECT
    event_type,
    COUNT(transaction_id) AS transaction_count,
    SUM(quantity_change) AS net_quantity_change
FROM inventory_transactions
GROUP BY event_type
ORDER BY transaction_count DESC;
```

## Logic

This query uses the inventory transactions table.

Each transaction records an inventory event, such as:

* customer order
* restock
* return
* damaged inventory
* inventory adjustment

The query groups by `event_type`.

For each event type, it calculates:

* `COUNT(transaction_id)`: how many times that event type occurred
* `SUM(quantity_change)`: the net quantity impact of that event type

The `quantity_change` column can be positive or negative:

* Customer orders reduce inventory, so they are negative.
* Restocks increase inventory, so they are positive.
* Returns usually increase inventory.
* Damaged inventory reduces inventory.
* Adjustments can be positive or negative.

The result is sorted by transaction count from highest to lowest.

## Why This Matters

This helps show the operational movement of inventory. It tells us whether most inventory activity is coming from sales demand, restocking, returns, damage, or adjustments.

## Interview Explanation

I would explain this query by saying:

“This query summarizes inventory transaction activity by event type. It shows both how frequently each event occurs and the net quantity impact on inventory.”

---

# 7. abc_classification.sql

## Business Question

Which SKUs are the most financially important based on inventory value?

## Query

```sql
SELECT
    item_id,
    category,
    inventory_value,
    CASE
        WHEN inventory_value >= 50000 THEN 'A'
        WHEN inventory_value >= 15000 THEN 'B'
        ELSE 'C'
    END AS abc_class
FROM inventory_data_cleaning
ORDER BY inventory_value DESC;
```

## Logic

This query classifies each SKU into an ABC class based on inventory value.

The `CASE` statement creates the classification:

* A items: inventory value greater than or equal to 50,000
* B items: inventory value greater than or equal to 15,000
* C items: inventory value below 15,000

The result is sorted by inventory value from highest to lowest.

## Why This Matters

ABC classification is a common inventory management method.

The basic idea is:

* A items are the most important and should be monitored closely.
* B items are moderately important.
* C items are lower value and usually need less attention.

This helps companies prioritize inventory control efforts instead of treating every SKU equally.

## Important Note

This project uses a simple threshold-based ABC classification for Version 1. A more advanced version could classify SKUs based on cumulative percentage of total inventory value.

For example:

* Top 80 percent of inventory value = A
* Next 15 percent = B
* Final 5 percent = C

That could be a future improvement.

## Interview Explanation

I would explain this query by saying:

“This query uses a CASE statement to classify SKUs into A, B, and C groups based on inventory value. It helps prioritize the highest-value items for closer monitoring and inventory control.”

---

# 8. executive_kpis.sql

## Business Question

What are the top-level inventory KPIs for the entire distribution center?

## Query

```sql
SELECT
    COUNT(item_id) AS total_skus,
    SUM(inventory_value) AS total_inventory_value,
    AVG(kpi_score) AS avg_inventory_health_score,
    SUM(CASE WHEN stockout_risk = 'High' THEN 1 ELSE 0 END) AS high_risk_skus,
    SUM(reorder_quantity) AS total_reorder_quantity,
    AVG(order_fulfillment_rate) AS avg_order_fulfillment_rate,
    AVG(demand_growth_pct) AS avg_demand_growth_pct
FROM inventory_data_cleaning;
```

## Logic

This query creates an executive-level summary of the inventory dataset.

It calculates:

* `COUNT(item_id)`: total number of SKUs
* `SUM(inventory_value)`: total value of inventory
* `AVG(kpi_score)`: average inventory health score
* `SUM(CASE WHEN stockout_risk = 'High' THEN 1 ELSE 0 END)`: number of high-risk SKUs
* `SUM(reorder_quantity)`: total recommended reorder quantity
* `AVG(order_fulfillment_rate)`: average fulfillment rate
* `AVG(demand_growth_pct)`: average demand growth percentage

The most important part is this line:

```sql
SUM(CASE WHEN stockout_risk = 'High' THEN 1 ELSE 0 END) AS high_risk_skus
```

This counts how many SKUs are high risk.

The logic is:

* If stockout risk is High, count it as 1.
* Otherwise, count it as 0.
* Then add up all the 1s.

This is a common SQL technique for counting rows that meet a condition.

## Why This Matters

This query creates dashboard KPI cards for executives or managers. It provides a quick overview of inventory health without requiring someone to look through thousands of rows.

## Interview Explanation

I would explain this query by saying:

“This query summarizes the inventory dataset into executive KPIs, including total SKUs, total inventory value, average inventory health, number of high-risk SKUs, reorder needs, fulfillment rate, and demand growth.”

---

# How the Queries Work Together

The eight SQL queries work together to cover different parts of the inventory business:

## Inventory Risk

Covered by:

* `high_risk_skus.sql`
* `reorder_recommendations.sql`

These queries identify stockout risk and replenishment needs.

## Inventory Value

Covered by:

* `inventory_value_by_category.sql`
* `abc_classification.sql`

These queries show where the company has the most capital tied up and which SKUs are most financially important.

## Supplier Performance

Covered by:

* `supplier_performance.sql`

This query connects supplier reliability and risk to purchase order activity.

## Sales and Demand

Covered by:

* `sales_revenue_by_category.sql`

This query shows which categories generate the most fulfilled revenue and unit demand.

## Inventory Movement

Covered by:

* `transaction_activity.sql`

This query summarizes operational movement in and out of inventory.

## Executive Summary

Covered by:

* `executive_kpis.sql`

This query provides top-level metrics for dashboard KPI cards.

---

# Interview Summary

A strong way to explain the SQL analytics layer is:

“I built a SQL analytics layer for InventoryIQ that transforms raw inventory, supplier, purchase order, sales order, and transaction data into business insights. Each SQL file answers a specific business question, such as identifying high-risk SKUs, generating reorder recommendations, analyzing supplier performance, summarizing sales revenue by category, classifying inventory using ABC logic, and producing executive KPI metrics. This made the data dashboard-ready and helped connect the technical data model to real supply chain decision-making.”
