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
    ct.product_category_name_english AS category,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(oi.order_item_id) AS items_sold,
    SUM(oi.price) AS revenue,
    AVG(oi.price) AS avg_item_price
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id
JOIN category_translation ct
    ON p.product_category_name = ct.product_category_name
WHERE o.order_status = 'delivered'
GROUP BY ct.product_category_name_english
ORDER BY revenue DESC;
"""

df = pd.read_sql(query, engine)

# Round numeric columns
df["revenue"] = df["revenue"].round(2)
df["avg_item_price"] = df["avg_item_price"].round(2)

# Revenue Contribution %
df["Revenue Contribution %"] = (
    df["revenue"] / df["revenue"].sum() * 100
).round(2)

# Revenue per Order
df["Revenue per Order"] = (
    df["revenue"] / df["total_orders"]
).round(2)

df.to_csv("category_analysis.csv", index=False)

print(df)

print("\n✅ Category dataset exported successfully!")
print(f"Rows exported: {len(df)}")
print(f"Columns: {len(df.columns)}")
