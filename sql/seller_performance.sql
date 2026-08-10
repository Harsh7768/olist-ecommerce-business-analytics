SELECT
    s.seller_id,
    s.seller_state,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    ROUND(SUM(oi.price)::numeric, 2) AS total_revenue,
    ROUND(AVG(oi.price)::numeric, 2) AS avg_item_price

FROM sellers s

JOIN order_items oi
ON s.seller_id = oi.seller_id

GROUP BY
    s.seller_id,
    s.seller_state

ORDER BY total_revenue DESC

LIMIT 10;
