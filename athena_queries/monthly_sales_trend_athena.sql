SELECT
    date_format(CAST(order_date AS DATE), '%Y-%m') AS sales_month,
    COUNT(sales_order_id) AS total_orders,
    SUM(quantity_ordered) AS units_sold,
    CAST(ROUND(SUM(quantity_ordered * unit_price), 2) AS DECIMAL(18,2)) AS total_revenue
FROM sales_orders
GROUP BY date_format(CAST(order_date AS DATE), '%Y-%m')
ORDER BY sales_month;