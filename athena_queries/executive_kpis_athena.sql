SELECT
    COUNT(item_id) AS total_skus,
    CAST(ROUND(SUM(inventory_value),2) AS DECIMAL(18,2)) AS total_inventory_value,
    ROUND(AVG(kpi_score), 3) AS avg_inventory_health_score,
    SUM(CASE WHEN stockout_risk = 'High' THEN 1 ELSE 0 END) AS high_risk_skus,
    SUM(reorder_quantity) AS total_reorder_quantity,
    ROUND(AVG(order_fulfillment_rate), 3) AS avg_order_fulfillment_rate,
    ROUND(AVG(demand_growth_pct), 3) AS avg_demand_growth_pct
FROM inventory_data_cleaning;