-- Active: 1742841061141@@127.0.0.1@5432@e_commerce_dwh@public
CREATE DATABASE e_commerce_dwh;

CREATE TABLE IF NOT EXISTS dim_customer 
(
  customer_id VARCHAR(50) PRIMARY KEY,
  city VARCHAR(100),
  state VARCHAR(3)
)

CREATE TABLE IF NOT EXISTS dim_order
(
  order_id VARCHAR(50) PRIMARY KEY,
  order_status VARCHAR(20),
  order_purchase_date DATE,
  order_approved_at DATE,
  order_delivered_carrier_date DATE,
  order_delivered_customer_date DATE
)

CREATE TABLE IF NOT EXISTS dim_product
(
  product_id VARCHAR(50) PRIMARY KEY,
  product_category VARCHAR(100)
)

CREATE TABLE IF NOT EXISTS dim_review
(
  review_id VARCHAR(50),
  score int,
  comment_title VARCHAR(100),
  comment_message VARCHAR(500),
  review_creation_date date,
  review_answer_timestamp date
)

CREATE TABLE IF NOT EXISTS dim_seller
(
  seller_id VARCHAR(50) PRIMARY KEY,
  city VARCHAR(50),
  state VARCHAR(3)
)

CREATE TABLE IF NOT EXISTS dim_order_item
(
  order_item_id SERIAL PRIMARY KEY , 
  order_id VARCHAR(50),
  quantity int,
  product_id VARCHAR(50),
  shipping_limit_date DATE,
  price  DECIMAL(10,2),
  frieght DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS dim_date
(
    date_key int PRIMARY KEY,  -- Surrogate Key
    Date DATE NOT NULL,  
    Year INT NOT NULL,
    Quarter INT NOT NULL,
    Month INT NOT NULL,
    Week INT NOT NULL,
    Day INT NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_sales
(
  sales_id SERIAL PRIMARY KEY ,
  customer_key VARCHAR(50),
  product_key VARCHAR(50),
  order_key VARCHAR(50),
  order_item_key INTEGER,
  seller_key VARCHAR(50),
  date_key int,
  quantity int,
  price int,
  frieght int,
  total_amount int,
  CONSTRAINT customer_fk FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_id),
  CONSTRAINT product_fk FOREIGN KEY (product_key) REFERENCES dim_product(product_id),
  CONSTRAINT order_fk FOREIGN KEY (order_key) REFERENCES dim_order(order_id),
  CONSTRAINT order_item_fk FOREIGN KEY (order_item_key) REFERENCES dim_order_item(order_item_id),
  CONSTRAINT seller_fk FOREIGN KEY (seller_key) REFERENCES dim_seller(seller_id),
  CONSTRAINT date_fk FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
)