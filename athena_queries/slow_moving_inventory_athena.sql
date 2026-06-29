SELECT
    item_id,
    category,
    stock_level,
    days_of_inventory,
    inventory_value,
    demand_growth_pct,
    stockout_risk
FROM inventory_data_cleaning
WHERE days_of_inventory > 30
ORDER BY days_of_inventory DESC;