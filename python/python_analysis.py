import os
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

PASSWORD = quote_plus(os.environ["POSTGRES_PASSWORD"])

engine = create_engine(
    f"postgresql+psycopg://postgres:{PASSWORD}@localhost:5432/ecommerce_db"
)

query = """
SELECT
    DATE_TRUNC('month', order_purchase_timestamp::timestamp) AS month,
    COUNT(*) AS total_orders
FROM orders
GROUP BY month
ORDER BY month;
"""

df = pd.read_sql(query, engine)

print(df)
