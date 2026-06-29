SELECT
    i.category,
    SUM(s.sales_revenue) AS total_sales_revenue,
    SUM(s.quantity_ordered) AS total_units_sold,
    COUNT(s.sales_order_id) AS total_orders
FROM sales_orders s
JOIN inventory_data_cleaning i
    ON s.item_id = i.item_id
WHERE s.order_status = 'Fulfilled'
GROUP BY i.category
ORDER BY total_sales_revenue DESC;