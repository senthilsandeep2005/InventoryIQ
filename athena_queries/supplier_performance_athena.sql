SELECT
    s.supplier_id,
    s.supplier_name,
    s.reliability_score,
    s.on_time_delivery_rate,
    COUNT(i.item_id) AS sku_count,
    CAST(ROUND(SUM(i.inventory_value),2) AS DECIMAL(18,2)) AS inventory_value
FROM inventory_data_cleaning i
JOIN suppliers_data s
ON i.supplier_id = s.supplier_id
GROUP BY
    s.supplier_id,
    s.supplier_name,
    s.reliability_score,
    s.on_time_delivery_rate
ORDER BY inventory_value DESC;