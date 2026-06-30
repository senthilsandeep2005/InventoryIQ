#Purpose: Calculates total inventory value and SKU count by category.
#SELECT
    category,
    CAST(ROUND(SUM(inventory_value), 2) AS DECIMAL(18,2)) AS total_inventory_value,
    CAST(ROUND(AVG(inventory_value), 2) AS DECIMAL(18,2)) AS avg_inventory_value,
    COUNT(item_id) AS sku_count
FROM inventory_data_cleaning
GROUP BY category
ORDER BY total_inventory_value DESC;