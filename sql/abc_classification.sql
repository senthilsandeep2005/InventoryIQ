SELECT
    item_id,
    category,
    inventory_value,
    CASE
        WHEN inventory_value >= 50000 THEN 'A'
        WHEN inventory_value >= 15000 THEN 'B'
        ELSE 'C'
    END AS abc_class
FROM inventory_data_cleaning
ORDER BY inventory_value DESC;