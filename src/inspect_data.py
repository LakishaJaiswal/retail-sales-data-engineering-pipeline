import pandas as pd

file_path = "data/raw/sales.csv"

df = pd.read_csv(file_path)

print("\n--- Dataset Shape ---")
print(df.shape)

print("\n--- First 5 Rows ---")
print(df.head())

print("\n--- Data Types ---")
print(df.dtypes)

print("\n--- Missing Values ---")
print(df.isnull().sum())

print("\n--- Duplicate Orders ---")
print(df[df.duplicated("order_id", keep=False)])

print("\n--- Invalid Quantities ---")
print(df[df["quantity"] <= 0])
