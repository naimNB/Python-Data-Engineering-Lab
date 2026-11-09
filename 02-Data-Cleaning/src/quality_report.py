
import json
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd

# Project paths
project_dir = Path(__file__).resolve().parent.parent

raw_path = project_dir / "data" / "messy_books.csv"
clean_path = project_dir / "data" / "cleaned_books.csv"
report_path = project_dir / "reports" / "quality_report.json"

# Load datasets
raw_df = pd.read_csv(raw_path)
clean_df = pd.read_csv(clean_path)

# Create quality report
report = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "source": "messy_books.csv",
    "cleaned_file": "cleaned_books.csv",
    "before_cleaning": {
        "rows": len(raw_df),
        "missing_values": int(raw_df.isnull().sum().sum()),
        "duplicate_urls": int(
            raw_df["product_url"].duplicated().sum()
        )
    },
    "after_cleaning": {
        "rows": len(clean_df),
        "missing_values": int(clean_df.isnull().sum().sum()),
        "duplicate_urls": int(
            clean_df["product_url"].duplicated().sum()
        )
    },
    "rows_removed": len(raw_df) - len(clean_df)
}

# Save report
report_path.parent.mkdir(parents=True, exist_ok=True)

with open(report_path, "w", encoding="utf-8") as file:
    json.dump(report, file, indent=4, ensure_ascii=False)

print(json.dumps(report, indent=4))
print("\nQuality report saved successfully!")
