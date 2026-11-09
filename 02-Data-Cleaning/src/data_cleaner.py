
from pathlib import Path
import pandas as pd

# Locate project directories
project_dir = Path(__file__).resolve().parent.parent
repo_dir = project_dir.parent

# Import dataset from Task 01
csv_path = repo_dir / "01-Web-Scraping" / "data" / "books.csv"

df = pd.read_csv(csv_path)

# Basic data inspection
print("Dataset Shape:", df.shape)

print("\nFirst 5 Records:")
print(df.head())

print("\nColumn Data Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:", df.duplicated().sum())
