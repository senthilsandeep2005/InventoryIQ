SELECT
    s.supplier_id,
    s.supplier_name,
    s.supplier_region,
    s.reliability_score,
    s.on_time_delivery_rate,
    s.supplier_risk_level,
    COUNT(p.po_id) AS total_purchase_orders,
    SUM(p.total_purchase_cost) AS total_purchase_spend
FROM suppliers_data s
LEFT JOIN purchase_orders p
    ON s.supplier_id = p.supplier_id
GROUP BY
    s.supplier_id,
    s.supplier_name,
    s.supplier_region,
    s.reliability_score,
    s.on_time_delivery_rate,
    s.supplier_risk_level
ORDER BY s.reliability_score DESC;