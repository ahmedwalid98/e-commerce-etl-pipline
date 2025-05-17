import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from extract_and_transform import (
    extract_customer_data,
    extract_product_data,
    extract_order_data,
    extract_order_items_data,
    extract_seller_data,
    dim_date,
    extract_fact_sales,
)
import logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

dwh_engine = create_engine(
    "postgresql://postgres:password@127.0.0.1:5432/e_commerce_dwh")

def skip_conflict_rows(table, conn, keys, data_iter):
    data = [dict(zip(keys, row)) for row in data_iter]
    insert_stmt = insert(table.table).values(data)
    onconflic_skip_stmt = insert_stmt.on_conflict_do_nothing()
    conn.execute(onconflic_skip_stmt)

def load_to_dwh(df: pd.DataFrame, table_name: str):
    with dwh_engine.connect() as conn:
        df.to_sql(table_name, con=conn, if_exists='append',
                  index=False, method=skip_conflict_rows)
        logging.info(f"✅ {table_name} loaded successfully.")

def load_dim_tables():
    dim_datasets = {
        'dim_customer': extract_customer_data(),
        'dim_order': extract_order_data(),
        'dim_product': extract_product_data(),
        'dim_seller': extract_seller_data(),
        'dim_order_item': extract_order_items_data(),
        'dim_date': dim_date()
    }

    for table, df in dim_datasets.items():
        load_to_dwh(df, table)

if __name__ == '__main__':

    print("📦 Loading dimension tables...")
    load_dim_tables()
    print("📥 Extracting and loading fact_sales...")
    fact_sales_df = extract_fact_sales()
    load_to_dwh(fact_sales_df, 'fact_sales')
