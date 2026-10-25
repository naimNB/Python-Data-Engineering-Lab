
from pathlib import Path
import pandas as pd

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "books.csv"


def test_csv_exists():
    assert DATA_FILE.exists(), "CSV file does not exist"


def test_record_count():
    df = pd.read_csv(DATA_FILE)
    assert len(df) >= 100, "Dataset must contain at least 100 records"


def test_required_columns():
    df = pd.read_csv(DATA_FILE)

    required = {"title", "price", "page"}

    assert required.issubset(df.columns), "Required columns missing"


def test_no_missing_values():
    df = pd.read_csv(DATA_FILE)

    assert not df[["title", "price", "page"]].isnull().any().any(), \
        "Dataset contains missing values"


def test_metadata_columns():
    df = pd.read_csv(DATA_FILE)

    required = {
        "title", "price", "currency",
        "availability", "rating",
        "page", "product_url"
    }

    assert required.issubset(df.columns)


def test_valid_prices():
    df = pd.read_csv(DATA_FILE)

    assert pd.api.types.is_numeric_dtype(df["price"])
    assert (df["price"] > 0).all()


def test_unique_product_urls():
    df = pd.read_csv(DATA_FILE)

    assert df["product_url"].notna().all()
    assert df["product_url"].str.startswith("https://").all()
    assert df["product_url"].is_unique
