import os
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# PostgreSQL password
PASSWORD = quote_plus(os.environ["POSTGRES_PASSWORD"])

engine = create_engine(
    f"postgresql+psycopg://postgres:{PASSWORD}@localhost:5432/ecommerce_db"
)


query = """
WITH seller_revenue AS (

SELECT
    s.seller_state,

    COUNT(DISTINCT oi.order_id) AS total_orders,

    SUM(oi.price) AS total_revenue

FROM sellers s

JOIN order_items oi
ON s.seller_id = oi.seller_id

GROUP BY s.seller_state

),

delivery_metrics AS (

SELECT
    s.seller_state,

    COUNT(DISTINCT CASE
        WHEN o.order_status = 'delivered'
        THEN o.order_id
    END) AS delivered_orders,

    COUNT(DISTINCT CASE
        WHEN o.order_status = 'canceled'
        THEN o.order_id
    END) AS cancelled_orders,

    ROUND(
        AVG(
            EXTRACT(
                DAY FROM (
                    o.order_delivered_customer_date::timestamp
                    -
                    o.order_purchase_timestamp::timestamp
                )
            )
        ),
        1
    ) AS avg_delivery_days

FROM sellers s

JOIN order_items oi
ON s.seller_id = oi.seller_id

JOIN orders o
ON oi.order_id = o.order_id

GROUP BY s.seller_state

)

SELECT

    sr.seller_state,

    COUNT(s.seller_id) AS total_sellers,

    sr.total_orders,

    ROUND(sr.total_revenue::numeric,2) AS total_revenue,

    dm.avg_delivery_days,

    dm.delivered_orders,

    dm.cancelled_orders,

    ROUND(
    (
        sr.total_revenue /
        SUM(sr.total_revenue) OVER() * 100
    )::numeric,
    2
) AS revenue_contribution_pct

FROM seller_revenue sr

LEFT JOIN delivery_metrics dm
ON sr.seller_state = dm.seller_state

LEFT JOIN sellers s
ON sr.seller_state = s.seller_state

GROUP BY

    sr.seller_state,
    sr.total_orders,
    sr.total_revenue,
    dm.avg_delivery_days,
    dm.delivered_orders,
    dm.cancelled_orders

ORDER BY total_revenue DESC;
"""

df = pd.read_sql(query, engine)

df.rename(
    columns={
        "revenue_contribution_pct": "Revenue Contribution %"
    },
    inplace=True
)

# Round numeric columns
df["total_revenue"] = df["total_revenue"].round(2)
df["avg_delivery_days"] = df["avg_delivery_days"].round(1)


# Average Revenue per Seller
df["Average Revenue per Seller"] = (
    df["total_revenue"] /
    df["total_sellers"]
).round(2)

df.to_csv(
    "operations_analysis.csv",
    index=False
)

print(df)

print("\n✅ Operations dataset exported successfully!")
print(f"Rows exported: {len(df)}")
print(f"Columns: {len(df.columns)}")
