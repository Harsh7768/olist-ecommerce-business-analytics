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
    DATE_TRUNC('month', o.order_purchase_timestamp::timestamp) AS month,

    COUNT(DISTINCT o.order_id) AS total_orders,

    ROUND(SUM(op.payment_value)::numeric, 2) AS revenue,

    ROUND(AVG(op.payment_value)::numeric, 2) AS avg_order_value,

    COUNT(DISTINCT o.customer_id) AS unique_customers

FROM orders o

JOIN order_payments op
ON o.order_id = op.order_id

GROUP BY month

ORDER BY month;
"""

df = pd.read_sql(query, engine)

# Month-over-Month Growth
df["MoM Growth %"] = (
    df["revenue"]
    .pct_change()
    .mul(100)
    .round(2)
)

# Total revenue earned up to each month
df["Cumulative Revenue"] = df["revenue"].cumsum()

# Revenue per unique customer
df["Revenue per Customer"] = (
    df["revenue"] / df["unique_customers"]
).round(2)

# Round numeric columns
df["revenue"] = df["revenue"].round(2)
df["Cumulative Revenue"] = df["Cumulative Revenue"].round(2)
df["avg_order_value"] = df["avg_order_value"].round(2)

# Print the final dataset
print(df)

# Export for Power BI
df.to_csv("executive_dataset.csv", index=False)

print("✅ Executive dataset exported successfully!")
print(f"Rows exported: {len(df)}")
print(f"Columns: {len(df.columns)}")
