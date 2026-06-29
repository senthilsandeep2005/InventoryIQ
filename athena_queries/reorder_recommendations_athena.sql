SELECT
    item_id,
    category,
    stock_level,
    reorder_point,
    reorder_quantity,
    stockout_risk,
    supplier_id,
    lead_time_days
FROM inventory_data_cleaning
WHERE reorder_quantity > 0
ORDER BY reorder_quantity DESC;