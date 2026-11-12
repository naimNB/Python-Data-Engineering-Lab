
import sqlite3
import sys
from pathlib import Path

import pytest

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR / "src"))

from database import DB_PATH, SCHEMA_PATH


@pytest.fixture
def connection():
    # Isolated in-memory database for each test
    conn = sqlite3.connect(":memory:")
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))

    yield conn

    conn.close()


def test_database_exists():
    assert DB_PATH.is_file()


def test_books_table_exists(connection):
    result = connection.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type='table' AND name='books'"
    ).fetchone()

    assert result is not None


def test_imported_record_count():
    with sqlite3.connect(DB_PATH) as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM books"
        ).fetchone()[0]

    assert count == 100


def test_unique_product_url(connection):
    values = (
        "Test Book", 25.50, "GBP",
        "In stock", "Four", 1,
        "https://example.com/book-1"
    )

    sql = """
        INSERT INTO books (
            title, price, currency, availability,
            rating, page, product_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    connection.execute(sql, values)

    with pytest.raises(sqlite3.IntegrityError):
        connection.execute(sql, values)


def test_price_constraint(connection):
    values = (
        "Invalid Book", -10.0, "GBP",
        "In stock", "Three", 1,
        "https://example.com/invalid"
    )

    sql = """
        INSERT INTO books (
            title, price, currency, availability,
            rating, page, product_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    with pytest.raises(sqlite3.IntegrityError):
        connection.execute(sql, values)


def test_upsert_updates_price(connection):
    sql = """
        INSERT INTO books (
            title, price, currency, availability,
            rating, page, product_url
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(product_url) DO UPDATE SET
            price = excluded.price
    """

    original = (
        "Test Book", 25.50, "GBP",
        "In stock", "Four", 1,
        "https://example.com/book-1"
    )

    updated = (
        "Test Book", 30.00, "GBP",
        "In stock", "Four", 1,
        "https://example.com/book-1"
    )

    connection.execute(sql, original)
    connection.execute(sql, updated)

    result = connection.execute(
        "SELECT price FROM books WHERE product_url = ?",
        ("https://example.com/book-1",)
    ).fetchone()

    count = connection.execute(
        "SELECT COUNT(*) FROM books"
    ).fetchone()[0]

    assert result[0] == 30.00
    assert count == 1
