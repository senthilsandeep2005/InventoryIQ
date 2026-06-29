SELECT
    transaction_type,
    COUNT(transaction_id) AS transaction_count,
    SUM(quantity) AS net_quantity_change
FROM inventory_transactions
GROUP BY transaction_type
ORDER BY transaction_count DESC;