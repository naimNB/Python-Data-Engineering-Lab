# E-commerce Product Web Scraper

A Python-based web scraper developed as part of the **Python for Data Engineering & Automation Internship** at Datheon.

## Overview

This project extracts structured book information from [Books to Scrape](https://books.toscrape.com/), a website designed for practicing web scraping.

The scraper collects 100 book records across five pages and exports the results to CSV and JSON formats.

## Features

- Multi-page web scraping with pagination
- Extraction of book titles, prices, ratings, availability, and product URLs
- HTTP retry configuration and basic exception handling
- UTF-8 character encoding support
- Data validation before export
- CSV and JSON export using Pandas
- Seven automated dataset tests using Pytest

## Technologies

- Python 3.10
- Requests
- BeautifulSoup4
- Pandas
- Pytest
- Conda

## Dataset Structure

| Column | Description |
|---|---|
| `title` | Book title |
| `price` | Book price as a numeric value |
| `currency` | Currency code (GBP) |
| `availability` | Stock availability |
| `rating` | Book rating |
| `page` | Source page number |
| `product_url` | Book detail page URL |

## Installation

Clone the repository:

```bash
git clone https://github.com/naimNB/Python-Data-Engineering-Lab.git
cd Python-Data-Engineering-Lab/01-Web-Scraping
```

Create a Conda environment:

```bash
conda env create -f environment.yml
conda activate web-scraping
```

## Usage

Run the scraper:

```bash
python src/scraper.py
```

The generated datasets are saved to:

- `data/books.csv`
- `data/books.json`

## Testing

Run the automated tests after generating the dataset:

```bash
python -m pytest tests/ -v
```

Seven dataset validation tests are included.

## Project Status

The scraper successfully collected 100 book records with seven fields, and all seven dataset tests passed in the latest local run.

## Data Source

[Books to Scrape](https://books.toscrape.com/) — a demonstration website for web scraping practice.

## License

This project is part of the Python Data Engineering Lab repository, licensed under the MIT License.