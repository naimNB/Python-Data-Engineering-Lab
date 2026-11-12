
import sqlite3

from database import DB_PATH


def query_books():
    with sqlite3.connect(DB_PATH) as connection:

        # Query 1: Total number of books
        total = connection.execute(
            "SELECT COUNT(*) FROM books"
        ).fetchone()[0]

        print("Total Books:", total)

        # Query 2: Five most expensive books
        expensive_books = connection.execute(
            """
            SELECT title, price
            FROM books
            ORDER BY price DESC
            LIMIT 5
            """
        ).fetchall()

        print("\nTop 5 Most Expensive Books:")
        for title, price in expensive_books:
            print(f"{title}: £{price:.2f}")

        # Query 3: Books cheaper than £20
        affordable_books = connection.execute(
            """
            SELECT title, price
            FROM books
            WHERE price < ?
            ORDER BY price ASC
            LIMIT 5
            """,
            (20,)
        ).fetchall()

        print("\nBooks Under £20:")
        for title, price in affordable_books:
            print(f"{title}: £{price:.2f}")


if __name__ == "__main__":
    query_books()
