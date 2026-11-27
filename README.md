# Python Data Engineering Lab

A collection of practical Python projects completed for the **Datheon — Python for Data Engineering & Automation Internship**. The repository demonstrates a three-stage data workflow: extract book data, clean and validate it, and load it into an SQLite database.

## Completed Internship Tasks

| Task | Project | Deliverables |
| --- | --- | --- |
| 01 | [Web Scraping](01-Web-Scraping/) | Requests + BeautifulSoup scraper; 100 book records from five pages; CSV and JSON export; 7 dataset tests |
| 02 | [Data Cleaning](02-Data-Cleaning/) | Pandas cleaning of a deliberately modified practice dataset; missing-value handling; duplicate removal; JSON quality report; 7 tests |
| 03 | [Database Integration](03-Database-Integration/) | SQLite schema; CSV import; UPSERT keyed by product URL; SQL queries; 6 database tests |

The data originates from [Books to Scrape](https://books.toscrape.com/), a public sandbox for scraping practice. Task 02 intentionally introduces synthetic data-quality problems; its imputed prices are **demonstration values, not verified product prices**.

## Data Flow

```text
Books to Scrape
       |
       v
01-Web-Scraping/data/books.csv
       |
       v
02-Data-Cleaning/data/messy_books.csv
       |
       v
02-Data-Cleaning/data/cleaned_books.csv
       |
       v
03-Database-Integration/data/books.db (generated locally)
```

## Requirements

- Python 3.10
- Conda (recommended)
- Project-specific dependencies listed in each `environment.yml`

Each project has its own setup instructions and tests in its linked README.

## Quick Start

Clone the full repository:

```bash
git clone https://github.com/naimNB/Python-Data-Engineering-Lab.git
cd Python-Data-Engineering-Lab
```

Create and activate the scraping environment:

```bash
conda env create -f 01-Web-Scraping/environment.yml
conda activate web-scraping
```

Run Task 01, then test it:

```bash
cd 01-Web-Scraping
python src/scraper.py
python -m pytest tests/ -v
cd ..
```

Create the cleaning environment and process Task 02:

```bash
conda env create -f 02-Data-Cleaning/environment.yml
conda activate data-cleaning
cd 02-Data-Cleaning
python src/generate_messy_data.py
python src/clean_data.py
python src/quality_report.py
python -m pytest tests/ -v
cd ..
```

Create the database environment and run Task 03:

```bash
conda env create -f 03-Database-Integration/environment.yml
conda activate database-integration
cd 03-Database-Integration
python src/database.py
python src/import_data.py
python src/query_books.py
python -m pytest tests/ -v
```

**Important:** The SQLite `books.db` file is generated locally and ignored by Git. Run the database initialization and import scripts **before** running Task 03 tests. All three task folders must remain next to each other because later tasks read the preceding task's datasets.

## Validation

- Task 01: 7 dataset checks
- Task 02: 7 data-quality checks
- Task 03: 6 database checks, including constraints and UPSERT behavior

These checks test generated outputs and selected database behaviors; they are not an exhaustive integration or network-failure test suite.

## Project Author

**Md Naim Babu** — B.Sc. in Computer Science and Engineering, Pundra University of Science & Technology, Bangladesh.

## License

MIT — see [LICENSE](LICENSE).
