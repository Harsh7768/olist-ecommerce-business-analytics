import os
import pandas as pd
from sqlalchemy import create_engine

from urllib.parse import quote_plus

PASSWORD = quote_plus(os.environ["POSTGRES_PASSWORD"])

engine = create_engine(
    f"postgresql+psycopg://postgres:{PASSWORD}@localhost:5432/ecommerce_db"
)

folder = r"C:\Users\Lemon\Downloads\Brazilian E-Commerce Public Dataset by Olist"

files = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "category_translation": "product_category_name_translation.csv"
}

for table, filename in files.items():
    print(f"Importing {table}...")
    df = pd.read_csv(os.path.join(folder, filename))
    df.to_sql(table, engine, if_exists="replace", index=False)
    print(f"✓ Imported {len(df)} rows into {table}")

print("\n🎉 ALL TABLES IMPORTED SUCCESSFULLY!")