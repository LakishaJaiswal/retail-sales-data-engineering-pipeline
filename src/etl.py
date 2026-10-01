import pandas as pd
from pathlib import Path


RAW_FILE = Path("data/raw/sales.csv")
PROCESSED_FILE = Path("data/processed/clean_sales.csv")


def extract_data():
    """Extract raw sales data from CSV."""
    print("Extracting data...")
    return pd.read_csv(RAW_FILE)


def transform_data(df):
    """Clean, validate, and transform sales data."""

    print("Starting transformation...")

    initial_rows = len(df)

    # Convert date column
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    # Remove duplicate orders
    df = df.drop_duplicates(subset=["order_id"], keep="first")

    # Remove records with invalid quantities
    df = df[df["quantity"] > 0]

    # Remove records with missing critical values
    df = df.dropna(
        subset=[
            "customer_id",
            "product_id",
            "order_date",
            "quantity",
            "unit_price",
        ]
    )

    # Calculate revenue
    df["revenue"] = df["quantity"] * df["unit_price"]

    # Add useful time attributes
    df["year"] = df["order_date"].dt.year
    df["month"] = df["order_date"].dt.month
    df["month_name"] = df["order_date"].dt.strftime("%B")

    final_rows = len(df)

    print(f"Initial rows: {initial_rows}")
    print(f"Final rows: {final_rows}")
    print(f"Rows removed: {initial_rows - final_rows}")

    return df


def load_data(df):
    """Save cleaned data for loading into the warehouse."""

    print("Saving processed data...")

    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(PROCESSED_FILE, index=False)

    print(f"Processed data saved to: {PROCESSED_FILE}")


def main():
    df = extract_data()
    df = transform_data(df)
    load_data(df)

    print("\nETL pipeline completed successfully!")


if __name__ == "__main__":
    main()
