SELECT
    category,
    SUM(inventory_value) AS total_inventory_value,
    AVG(inventory_value) AS average_inventory_value,
    COUNT(item_id) AS sku_count
FROM inventory_data_cleaning
GROUP BY category
ORDER BY total_inventory_value DESC;
