
from pathlib import Path
import pandas as pd

# Define file paths
project_dir = Path(__file__).resolve().parent.parent

input_path = project_dir / "data" / "messy_books.csv"
output_path = project_dir / "data" / "cleaned_books.csv"

# Load messy dataset
df = pd.read_csv(input_path)

print("Before Cleaning:")
print("Rows:", len(df))
print("Missing Values:", df.isnull().sum().sum())
print("Duplicate Rows:", df.duplicated().sum())

# 1. Remove leading and trailing whitespace
text_columns = [
    "title", "currency", "availability",
    "rating", "product_url"
]

for col in text_columns:
    df[col] = df[col].str.strip()

# 2. Remove duplicates based on product URL
df = df.drop_duplicates(subset=["product_url"])

# 3. Handle missing prices
# Use median price for this demonstration
df["price"] = df["price"].fillna(df["price"].median())

# 4. Handle missing ratings
df["rating"] = df["rating"].fillna("Unknown")

# 5. Save cleaned dataset
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print("\nAfter Cleaning:")
print("Rows:", len(df))
print("Missing Values:", df.isnull().sum().sum())
print("Duplicate URLs:", df["product_url"].duplicated().sum())
print("Cleaned dataset saved successfully!")
