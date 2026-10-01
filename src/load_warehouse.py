import os
import pandas as pd
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROCESSED_FILE = Path("data/processed/clean_sales.csv")

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def load_dimensions(df, connection):
    cursor = connection.cursor()

    # Load customers
    customers = df[["customer_id", "region"]].drop_duplicates()

    for _, row in customers.iterrows():
        cursor.execute(
            """
            INSERT INTO dim_customer (customer_id, region)
            VALUES (%s, %s)
            ON CONFLICT (customer_id) DO NOTHING;
            """,
            (row["customer_id"], row["region"])
        )

    # Load products
    products = df[["product_id", "category"]].drop_duplicates()

    for _, row in products.iterrows():
        cursor.execute(
            """
            INSERT INTO dim_product (product_id, category)
            VALUES (%s, %s)
            ON CONFLICT (product_id) DO NOTHING;
            """,
            (row["product_id"], row["category"])
        )

    # Load dates
    dates = df[["order_date", "year", "month", "month_name"]].drop_duplicates()

    for _, row in dates.iterrows():
        date_key = int(row["order_date"].strftime("%Y%m%d"))

        cursor.execute(
            """
            INSERT INTO dim_date
                (date_key, full_date, year, month, month_name)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (date_key) DO NOTHING;
            """,
            (
                date_key,
                row["order_date"],
                row["year"],
                row["month"],
                row["month_name"]
            )
        )

    connection.commit()
    cursor.close()


def load_fact_table(df, connection):
    cursor = connection.cursor()

    for _, row in df.iterrows():

        customer_id = row["customer_id"]
        product_id = row["product_id"]
        date_key = int(row["order_date"].strftime("%Y%m%d"))

        cursor.execute(
            """
            SELECT customer_key
            FROM dim_customer
            WHERE customer_id = %s;
            """,
            (customer_id,)
        )

        customer_key = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT product_key
            FROM dim_product
            WHERE product_id = %s;
            """,
            (product_id,)
        )

        product_key = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO fact_sales
                (
                    order_id,
                    customer_key,
                    product_key,
                    date_key,
                    quantity,
                    unit_price,
                    revenue
                )
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (order_id) DO NOTHING;            """,
            (
                row["order_id"],
                customer_key,
                product_key,
                date_key,
                row["quantity"],
                row["unit_price"],
                row["revenue"]
            )
        )

    connection.commit()
    cursor.close()


def main():

    print("Loading processed data...")

    df = pd.read_csv(
        PROCESSED_FILE,
        parse_dates=["order_date"]
    )

    connection = get_connection()

    print("Loading dimension tables...")
    load_dimensions(df, connection)

    print("Loading fact table...")
    load_fact_table(df, connection)

    connection.close()

    print("\nWarehouse loading completed successfully!")


if __name__ == "__main__":
    main()
