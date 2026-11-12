
import csv
import sqlite3
from pathlib import Path

from database import DB_PATH, initialize_database

PROJECT_DIR = Path(__file__).resolve().parent.parent
REPO_DIR = PROJECT_DIR.parent

CSV_PATH = (
    REPO_DIR / "02-Data-Cleaning" / "data" / "cleaned_books.csv"
)


def import_books():
    initialize_database()

    if not CSV_PATH.is_file():
        raise FileNotFoundError(f"Dataset not found: {CSV_PATH}")

    with open(CSV_PATH, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        records = []

        for row in reader:
            records.append((
                row["title"],
                float(row["price"]),
                row["currency"],
                row["availability"],
                row["rating"],
                int(row["page"]),
                row["product_url"]
            ))

    if not records:
        raise ValueError("CSV dataset is empty!")

    query = """
        INSERT INTO books (
            title, price, currency, availability,
            rating, page, product_url
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(product_url) DO UPDATE SET
            title = excluded.title,
            price = excluded.price,
            currency = excluded.currency,
            availability = excluded.availability,
            rating = excluded.rating,
            page = excluded.page
    """

    with sqlite3.connect(DB_PATH) as connection:
        connection.executemany(query, records)

        total = connection.execute(
            "SELECT COUNT(*) FROM books"
        ).fetchone()[0]

    print(f"Processed records: {len(records)}")
    print(f"Total books in database: {total}")
    print("Data import completed successfully!")


if __name__ == "__main__":
    import_books()
