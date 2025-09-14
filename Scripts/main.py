import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
result = load_dotenv(".env")
conn_string = os.getenv("DATABASE_URL")
path = "./csv"

create_tables = {
'create_customers_table' : '''
                         CREATE TABLE IF NOT EXISTS customers
                         (
                             customer_id              varchar(50) PRIMARY KEY,
                             customer_unique_id       varchar(50),
                             customer_zip_code_prefix varchar(10),
                             customer_city            text,
                             customer_state           char(2)
                         );
                         ''',
'create_geolocation_table' : '''
                           CREATE TABLE IF NOT EXISTS geolocation
                           (
                               geolocation_zip_code_prefix varchar(10),
                               geolocation_lat             varchar(255),
                               geolocation_lng             varchar(255),
                               geolocation_city            text,
                               geolocation_state           char(3)
                           );
                           ''',
'create_order_items_table' : '''
                           CREATE TABLE IF NOT EXISTS order_items
                           (
                               order_id            varchar(50),
                               order_item_id       int,
                               product_id          varchar(50),
                               seller_id           varchar(50),
                               shipping_limit_date varchar(50),
                               price               numeric(8, 2),
                               freight_value       numeric(6, 2)
                           );
                           ''',
'create_order_payments_table' : '''
                              CREATE TABLE IF NOT EXISTS order_payments
                              (
                                  order_id             varchar(50),
                                  payment_sequential   int,
                                  payment_type         varchar(50),
                                  payment_installments char(100),
                                  payment_value        money
                              );
                              ''',
'create_order_reviews_table' : '''
                             CREATE TABLE IF NOT EXISTS order_reviews
                             (
                                 review_id               varchar(50),
                                 order_id                varchar(50),
                                 review_score            varchar(255),
                                 review_comment_title    varchar(255),
                                 review_comment_message  varchar(255),
                                 review_creation_date    varchar(255),
                                 review_answer_timestamp varchar(255)
                             );
                             ''',
'create_orders_table' : '''
                      CREATE TABLE IF NOT EXISTS orders
                      (
                          order_id                      varchar(50),
                          customer_id                   varchar(50),
                          order_status                  varchar(255),
                          order_purchase_timestamp      varchar(50),
                          order_approved_at             varchar(50),
                          order_delivered_carrier_date  varchar(50),
                          order_delivered_customer_date varchar(50),
                          order_estimated_delivery_date varchar(50)
                      );
                      ''',
'create_products_table' : '''
                        CREATE TABLE IF NOT EXISTS products
                        (
                            product_id                 varchar(50),
                            product_category_name      varchar(255),
                            product_name_lenght        varchar(255),
                            product_description_lenght varchar(255),
                            product_photos_qty         varchar(255),
                            product_weight_g           varchar(255),
                            product_length_cm          varchar(255),
                            product_height_cm          varchar(255),
                            product_width_cm           varchar(255)
                        );
                        ''',
'create_sellers_table' : '''
                       CREATE TABLE IF NOT EXISTS sellers
                       (
                           seller_id              varchar(50),
                           seller_zip_code_prefix varchar(10),
                           seller_city            varchar(255),
                           seller_state           char(5)
                       );
                       ''',
'create_product_category_name_translation_table' : '''
                                                 CREATE TABLE IF NOT EXISTS product_category_name_translation
                                                 (
                                                     product_category_name         varchar(255),
                                                     product_category_name_english varchar(255)
                                                 );
                                                 '''
}
tables_name = ['customers', 'geolocation', 'order_items', 'order_payments', 'order_reviews', 'orders', 'products',
               'sellers', 'product_category_name_translation']


def insert_into_db(create_string, table_name, file_name):
    try:
        with psycopg2.connect(conn_string) as conn:
            print("Connection established")
            with conn.cursor() as cur:
                cur.execute(create_string)
                with open(file_name, 'rt', encoding='utf-8') as f:
                    next(f)
                    cur.copy_from(f, table_name, sep=",")
                    print(f"Data from file {file_name}, was inserted to table {table_name}")
                conn.commit()
    except Exception as e:
        print("-"*20)
        print("Connection failed.")
        print(e)
        print("-"*20)


def init():
    print("Start inserting...")
    for table in tables_name:
        create_table_string = f"create_{table}_table"
        command_string = create_tables[create_table_string]
        if table == "product_category_name_translation":
            file = f"{path}/{table}.csv"
            if not os.path.exists(file):
                print(f"Warning: File {file} not found, skipping...")
                continue
            insert_into_db(command_string, table, file)
        else:
            file = f"{path}/olist_{table}_dataset.csv"
            if not os.path.exists(file):
                print(f"Warning: File {file} not found, skipping...")
                continue
            insert_into_db(command_string, table, file)

    print("Data inserted")

init()
