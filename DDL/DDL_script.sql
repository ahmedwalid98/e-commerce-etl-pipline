-- Active: 1742841061141@@127.0.0.1@5432@e_commerce_db
CREATE DATABASE e_commerce_db;
DROP TABLE order_item;
DROP TABLE review;
DROP TABLE seller;
DROP TABLE products;
DROP TABLE customer CASCADE;  
DROP TABLE orders;

CREATE TABLE IF NOT EXISTS products
(
  product_id VARCHAR(50) PRIMARY KEY,
  product_category VARCHAR(100),
  product_name_lenght int,
  product_description_lenght int,
  product_photos_qty int,
  product_weight_g int,
  product_length_cm int,
  product_height_cm int,
  product_width_cm int
); 

CREATE Table if not exists seller
(
  seller_id VARCHAR(50) PRIMARY KEY,
  zip_code int,
  city VARCHAR(50),
  state VARCHAR(3)
)

CREATE Table if not exists customer
(
  customer_id VARCHAR(50) PRIMARY KEY,
  zip_code int,
  city VARCHAR(100),
  state VARCHAR(3)
)

CREATE TABLE IF NOT EXISTS review
(
  review_id VARCHAR(50),
  score int,
  order_id VARCHAR(50),
  comment_title VARCHAR(100),
  comment_message VARCHAR(500),
  review_creation_date date,
  review_answer_timestamp date
)


CREATE TABLE IF NOT EXISTS orders
(
  order_id VARCHAR(50) PRIMARY KEY,
  customer_id VARCHAR(50),
  order_status VARCHAR(20),
  order_purchase_date DATE,
  order_approved_at DATE,
  order_delivered_carrier_date DATE,
  order_delivered_customer_date DATE,
  constraint FK_cust_const FOREIGN KEY(customer_id) REFERENCES customer(customer_id) ON DELETE CASCADE
)

alter table review add constraint
FK_order FOREIGN KEY(order_id) REFERENCES orders(order_id)

create Table IF NOT EXISTS order_item
(

  order_id VARCHAR(50) REFERENCES orders(order_id),
  order_item_id int,
  product_id VARCHAR(50) REFERENCES products(product_id ),
  seller_id VARCHAR(50) REFERENCES seller(seller_id),
  shipping_limit_date DATE,
  price  DECIMAL(10,2),
  frieght DECIMAL(10,2)
)

