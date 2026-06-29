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