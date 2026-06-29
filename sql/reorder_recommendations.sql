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