SELECT
    COUNT(item_id) AS total_skus,
    SUM(inventory_value) AS total_inventory_value,
    AVG(kpi_score) AS avg_inventory_health_score,
    SUM(CASE WHEN stockout_risk = 'High' THEN 1 ELSE 0 END) AS high_risk_skus,
    SUM(reorder_quantity) AS total_reorder_quantity,
    AVG(order_fulfillment_rate) AS avg_order_fulfillment_rate,
    AVG(demand_growth_pct) AS avg_demand_growth_pct
FROM inventory_data_cleaning;