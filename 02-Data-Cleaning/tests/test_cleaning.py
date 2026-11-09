
import json
from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = PROJECT_DIR / "data" / "messy_books.csv"
CLEAN_FILE = PROJECT_DIR / "data" / "cleaned_books.csv"
REPORT_FILE = PROJECT_DIR / "reports" / "quality_report.json"


def test_cleaned_file_exists():
    assert CLEAN_FILE.exists()


def test_required_columns():
    df = pd.read_csv(CLEAN_FILE)

    required = {
        "title", "price", "currency",
        "availability", "rating",
        "page", "product_url"
    }

    assert required.issubset(df.columns)


def test_no_missing_values():
    df = pd.read_csv(CLEAN_FILE)

    assert not df.isnull().any().any()


def test_no_duplicate_urls():
    df = pd.read_csv(CLEAN_FILE)

    assert df["product_url"].is_unique


def test_valid_prices():
    df = pd.read_csv(CLEAN_FILE)

    assert pd.api.types.is_numeric_dtype(df["price"])
    assert (df["price"] > 0).all()


def test_expected_record_count():
    df = pd.read_csv(CLEAN_FILE)

    assert len(df) == 100


def test_quality_report():
    assert RAW_FILE.exists()
    assert REPORT_FILE.exists()

    raw_df = pd.read_csv(RAW_FILE)
    clean_df = pd.read_csv(CLEAN_FILE)

    with open(REPORT_FILE, encoding="utf-8") as file:
        report = json.load(file)

    assert report["before_cleaning"]["rows"] == len(raw_df)
    assert report["after_cleaning"]["rows"] == len(clean_df)
    assert report["rows_removed"] == len(raw_df) - len(clean_df)
