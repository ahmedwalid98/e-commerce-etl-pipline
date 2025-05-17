import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime

engine = create_engine(
    "postgresql://postgres:password@127.0.0.1:5432/e_commerce_db")
dwh_engine = create_engine(
    "postgresql://postgres:password@127.0.0.1:5432/e_commerce_dwh")


def run_query(sql: str) -> pd.DataFrame:
    return pd.read_sql(sql, con=engine)


def extract_customer_data():
    return run_query("SELECT customer_id, city, state FROM customer")


def extract_product_data():
    return run_query("SELECT product_id, product_category FROM products")


def extract_order_data():
    return run_query("""
        SELECT order_id, order_status, order_purchase_date, 
               order_approved_at, order_delivered_carrier_date, 
               order_delivered_customer_date 
        FROM orders
    """)


def extract_order_items_data():
    df = run_query("""
        SELECT order_id, COUNT(order_item_id) AS quantity, product_id, 
               seller_id, shipping_limit_date, price, frieght 
        FROM order_item 
        GROUP BY order_id, shipping_limit_date, price, product_id, seller_id, frieght
    """)
    return df.drop(columns=['product_id', 'seller_id'])


def extract_seller_data():
    return run_query("SELECT seller_id, city, state FROM seller")


def dim_date():
    min_date = run_query("SELECT MIN(order_purchase_date) AS min_date FROM orders")[
        'min_date'].iloc[0]
    date_range = pd.date_range(start=min_date, end=datetime.now())

    df = pd.DataFrame({'date': date_range})
    df['date_key'] = df['date'].dt.strftime('%Y%m%d')
    df['year'] = df['date'].dt.year
    df['quarter'] = df['date'].dt.quarter
    df['month'] = df['date'].dt.month
    df['week'] = df['date'].dt.isocalendar().week
    df['day'] = df['date'].dt.day

    return df


def extract_fact_sales():
    sql = """
        WITH cte AS (
            SELECT 
                order_id, COUNT(order_item_id) AS quantity, product_id, 
                seller_id, shipping_limit_date, price, frieght
            FROM order_item
            GROUP BY order_id, shipping_limit_date, price, product_id, seller_id, frieght
        )
        SELECT  
            o.order_id AS order_key, 
            o.customer_id AS customer_key,
            ROW_NUMBER() OVER () AS order_item_key,
            TO_CHAR(o.order_purchase_date, 'YYYYMMDD') AS date_key,
            oi.product_id AS product_key,
            oi.seller_id AS seller_key,
            oi.quantity, oi.price, oi.frieght, 
            (oi.price * oi.quantity) + oi.frieght AS total_amount 
        FROM orders o
        JOIN cte oi ON o.order_id = oi.order_id
    """
    return run_query(sql)

