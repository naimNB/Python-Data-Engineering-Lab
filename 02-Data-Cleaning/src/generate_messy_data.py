
from pathlib import Path
import pandas as pd

project_dir = Path(__file__).resolve().parent.parent
repo_dir = project_dir.parent

input_path = repo_dir / "01-Web-Scraping" / "data" / "books.csv"
output_path = project_dir / "data" / "messy_books.csv"

# Load original dataset
df = pd.read_csv(input_path)

# Work on a copy
messy_df = df.copy()

# Introduce missing values
messy_df.loc[0, "price"] = None
messy_df.loc[3, "rating"] = None

# Introduce inconsistent text
messy_df.loc[5, "title"] = "  " + str(messy_df.loc[5, "title"]) + "  "

# Introduce duplicate records
messy_df = pd.concat(
    [messy_df, messy_df.iloc[[1, 2]]],
    ignore_index=True
)

# Save messy dataset
output_path.parent.mkdir(parents=True, exist_ok=True)
messy_df.to_csv(output_path, index=False)

print("Messy dataset created successfully!")
print("Dataset Shape:", messy_df.shape)
print("Missing Values:")
print(messy_df.isnull().sum())
print("Duplicate Records:", messy_df.duplicated().sum())
