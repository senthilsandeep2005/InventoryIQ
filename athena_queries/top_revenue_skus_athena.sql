SELECT
    s.item_id,
    i.category,
    COUNT(s.sales_order_id) AS total_orders,
    SUM(s.quantity_ordered) AS units_sold,
    CAST(ROUND(SUM(s.quantity_ordered * s.unit_price), 2) AS DECIMAL(18,2)) AS total_revenue
FROM sales_orders s
JOIN inventory_data_cleaning i
ON s.item_id = i.item_id
GROUP BY
    s.item_id,
    i.category
ORDER BY total_revenue DESC
LIMIT 25;