import pandas as pd
from sqlalchemy import create_engine, text
import logging
logging.basicConfig('%(levelname)s: %(message)s', format=logging.INFO)

engine = create_engine(
    "postgresql+psycopg2://postgres:password@localhost:5432/e_commerce_db")


def extract_customer_data():
    df = pd.read_csv(
        '/home/ahmed-walid/e-commerce-etl-pipline/Data/olist_customers_dataset.csv')
    df = df.rename(columns={'customer_zip_code_prefix': 'zip_code',
                            'customer_city': 'city',
                            'customer_state': 'state'}).drop('customer_unique_id', axis=1)
    df.columns = df.columns.str.lower()
    return df


def extrct_orders_data():
    df = pd.read_csv('/home/ahmed-walid/e-commerce-etl-pipline/Data/olist_orders_dataset.csv')
    df = df.rename(
        columns={'order_purchase_timestamp': 'order_purchase_date'}).drop('order_estimated_delivery_date', axis=1)
    df.columns = df.columns.str.lower()
    return df


def extract_orders_item_data():
    df = pd.read_csv('/home/ahmed-walid/e-commerce-etl-pipline/Data/olist_order_items_dataset.csv')
    df = df.rename(columns={'freight_value': 'frieght'})
    df.columns = df.columns.str.lower()
    return df


def extract_products_data():
    df = pd.read_csv('/home/ahmed-walid/e-commerce-etl-pipline/Data/olist_products_dataset.csv')
    df = df.rename(columns={'product_category_name': 'product_category'}
                   ).drop('product_photos_qty', axis=1)
    df.columns = df.columns.str.lower()
    return df


def extract_review_data():
    df = pd.read_csv('/home/ahmed-walid/e-commerce-etl-pipline/Data/olist_order_reviews_dataset.csv')
    df = df.rename(columns={'review_comment_title': 'comment_title',
                            'review_comment_message': 'comment_message',
                            'review_score': 'score'})
    df.columns = df.columns.str.lower()
    return df


def extract_seller_data():
    df = pd.read_csv('/home/ahmed-walid/e-commerce-etl-pipline/Data/olist_sellers_dataset.csv')
    df = df.rename(columns={'seller_zip_code_prefix': 'zip_code',
                            'seller_city': 'city',
                            'seller_state': 'state'})
    df.columns = df.columns.str.lower()
    return df


def stage_data_into_postgres():
    datasets = {
        'customer': extract_customer_data(),
        'orders': extrct_orders_data(),
        'products': extract_products_data(),
        'seller': extract_seller_data(),
        'order_item': extract_orders_item_data(),
        'review': extract_review_data()
    }

    try:
        for table, df in datasets.items():
            df.to_sql(name=table, con=engine,
                      if_exists='append', index=False, method='multi')
            logging.info(f'{len(df)} rows inserted into {table} table')
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == '__main__':
    stage_data_into_postgres()
