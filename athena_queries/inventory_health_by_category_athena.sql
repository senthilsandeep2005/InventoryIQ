SELECT
    category,
    ROUND(AVG(kpi_score), 3) AS avg_health_score,
    ROUND(AVG(days_of_inventory), 2) AS avg_days_inventory,
    COUNT(item_id) AS sku_count,
    SUM(CASE WHEN stockout_risk = 'High' THEN 1 ELSE 0 END) AS high_risk_skus
FROM inventory_data_cleaning
GROUP BY category
ORDER BY avg_health_score DESC;