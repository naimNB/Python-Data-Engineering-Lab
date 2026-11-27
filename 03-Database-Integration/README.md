# Book Inventory Database Management System

A Python-based SQLite database integration project developed as part of the **Datheon Python for Data Engineering & Automation Internship**.

## Overview

This project imports cleaned book records from Task 02 into a relational SQLite database. It demonstrates database schema design, CSV ingestion, UPSERT operations, SQL querying, data integrity constraints, and automated testing.

The pipeline processes 100 book records and supports repeatable imports without creating duplicate product entries.

## Features

- SQLite database initialization using a SQL schema
- CSV data import using Python
- Bulk insert and UPSERT operations
- Duplicate prevention through unique product URLs
- Database constraints for required fields and positive prices
- SQL queries for searching, filtering, and sorting
- Six automated database tests using Pytest

## Technologies

- Python 3.10
- SQLite3
- CSV
- Pytest
- Conda

## Project Structure

```text
03-Database-Integration/
├── src/
│   ├── database.py
│   ├── import_data.py
│   └── query_books.py
├── sql/
│   └── schema.sql
├── data/
│   └── books.db
├── tests/
│   └── test_database.py
├── environment.yml
└── README.md
```

*Note: `books.db` is generated locally and is not intended to be tracked in Git.*

## Database Schema

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Auto-incrementing primary key |
| title | TEXT | Book title |
| price | REAL | Book price |
| currency | TEXT | Currency code |
| availability | TEXT | Availability status |
| rating | TEXT | Book rating |
| page | INTEGER | Original source page |
| product_url | TEXT | Unique product identifier |

## Installation

Clone the repository:

```bash
git clone https://github.com/bynaim/Python-Data-Engineering-Lab.git
cd Python-Data-Engineering-Lab/03-Database-Integration
```

Create and activate the Conda environment:

```bash
conda env create -f environment.yml
conda activate database-integration
```

## Usage

The repository must include the cleaned dataset from Task 02 at `02-Data-Cleaning/data/cleaned_books.csv`.

Initialize the database:

```bash
python src/database.py
```

Import the book records:

```bash
python src/import_data.py
```

Run SQL queries:

```bash
python src/query_books.py
```

Running the import script repeatedly updates existing records based on `product_url` rather than creating duplicates.

## Testing

Run the automated tests after importing the dataset:

```bash
python -m pytest tests/ -v
```

The project includes six tests covering database existence, table creation, imported record count, unique URL constraints, price constraints, and UPSERT behavior.

## Data Source

Book data originates from [Books to Scrape](https://books.toscrape.com/) and is cleaned in Task 02.

## License

This project is part of the Python Data Engineering Lab repository and is distributed under the MIT License.