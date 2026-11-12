
import sqlite3
from pathlib import Path

# Locate project directory
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Database and schema paths
DB_PATH = PROJECT_DIR / "data" / "books.db"
SCHEMA_PATH = PROJECT_DIR / "sql" / "schema.sql"


def initialize_database():
    # Ensure database directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Connect to SQLite database
    with sqlite3.connect(DB_PATH) as connection:

        # Load SQL schema
        schema = SCHEMA_PATH.read_text(encoding="utf-8")

        # Execute schema
        connection.executescript(schema)

        print("Database initialized successfully!")

        # Verify table creation
        cursor = connection.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name='books'"
        )

        if cursor.fetchone():
            print("Table 'books' created successfully!")
        else:
            raise RuntimeError("Books table was not created!")


if __name__ == "__main__":
    initialize_database()
