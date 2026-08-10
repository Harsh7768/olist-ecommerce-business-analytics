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
SELECT
    c.customer_state,

    COUNT(DISTINCT c.customer_unique_id) AS total_customers,

    COUNT(DISTINCT o.order_id) AS total_orders,

    SUM(op.payment_value) AS total_revenue,

    AVG(op.payment_value) AS avg_order_value,

    AVG(orv.review_score) AS avg_review_score,

    AVG(
        o.order_delivered_customer_date::date -
        o.order_purchase_timestamp::date
    ) AS avg_delivery_days

FROM customers c

JOIN orders o
ON c.customer_id = o.customer_id

JOIN order_payments op
ON o.order_id = op.order_id

LEFT JOIN order_reviews orv
ON o.order_id = orv.order_id

WHERE
    o.order_status = 'delivered'

GROUP BY
    c.customer_state

ORDER BY
    total_revenue DESC;
"""

df = pd.read_sql(query, engine)

# Round numeric columns
df["total_revenue"] = df["total_revenue"].round(2)
df["avg_order_value"] = df["avg_order_value"].round(2)
df["avg_review_score"] = df["avg_review_score"].round(2)
df["avg_delivery_days"] = df["avg_delivery_days"].round(1)

# Revenue Contribution
df["Revenue Contribution %"] = (
    df["total_revenue"] / df["total_revenue"].sum() * 100
).round(2)

df.to_csv("customer_analysis.csv", index=False)

print(df)

print("\n✅ Customer dataset exported successfully!")
print(f"Rows exported: {len(df)}")
print(f"Columns: {len(df.columns)}")