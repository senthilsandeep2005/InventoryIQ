SELECT
    event_type,
    COUNT(transaction_id) AS transaction_count,
    SUM(quantity_change) AS net_quantity_change
FROM inventory_transactions
GROUP BY event_type
ORDER BY transaction_count DESC;