# Automated ETL Pipeline & Scheduling

A Python-based automated ETL workflow developed for the **Datheon Python for Data Engineering & Automation Internship**.

## Overview

This project integrates three earlier data engineering tasks into a single executable pipeline. It extracts product records, prepares a controlled data-cleaning demonstration dataset, performs cleaning and quality validation, and loads the processed records into an SQLite database.

The pipeline supports execution logging, JSON reports, failure handling, and Linux cron-compatible scheduling.

## Features

- Automated execution of five processing steps
- Web scraping across multiple pages
- Data cleaning and quality validation
- SQLite database integration with UPSERT
- Subprocess-based workflow orchestration
- JSON execution reports for success and failure
- Execution logging
- Shell script for cron-compatible execution
- Three automated tests using Pytest

## Project Structure

```text
04-Automated-ETL/
├── src/
│   ├── pipeline.py
│   └── run_pipeline.sh
├── tests/
│   └── test_pipeline.py
├── logs/                 # Generated locally
├── reports/              # Generated locally
├── environment.yml
└── README.md
```

## Technology Stack

Python 3.10, Requests, BeautifulSoup4, Pandas, SQLite, Pytest, Bash, Conda and Linux Cron.

## Setup

Clone the complete repository:

```bash
git clone https://github.com/naimNB/Python-Data-Engineering-Lab.git
cd Python-Data-Engineering-Lab/04-Automated-ETL
```

Create the Conda environment:

```bash
conda env create -f environment.yml
conda activate automated-etl
```

The pipeline requires the three preceding project folders to remain in the repository because their scripts are reused.

## Run the Pipeline

```bash
python src/pipeline.py
```

Alternatively, make the shell script executable and run it:

```bash
chmod +x src/run_pipeline.sh
./src/run_pipeline.sh
```

**Note:** The shell script currently uses the author's local Miniconda `ML` environment path. Update the `PYTHON` variable for your own installation before using the shell runner or scheduling it.

## Processing Steps

1. Extract 100 book records using the web scraper.
2. Generate a controlled dataset with simulated quality issues.
3. Clean and validate the dataset.
4. Generate a JSON data-quality report.
5. Import cleaned records into SQLite using UPSERT.

The intentionally messy dataset is for educational demonstration, not a production data-processing requirement.

## Execution Reports

Every pipeline execution produces a report at:

`reports/pipeline_report.json`

The report records execution status, timestamps, duration, completed steps, failure details, and errors.

Runtime logs are written to:

`logs/pipeline.log`

Both output directories are excluded from Git tracking.

## Scheduling

The shell runner can be scheduled using Linux cron.

Example cron entry for daily execution at 9:00 AM:

```cron
0 9 * * * /absolute/path/to/04-Automated-ETL/src/run_pipeline.sh
```

Use an absolute path and configure the shell runner's Python interpreter before enabling the schedule.

The cron schedule is documented as an example and has not been activated by default.

## Testing

Run automated tests:

```bash
python -m pytest tests/ -v
```

The three tests verify successful pipeline execution, simulated subprocess failure handling, and JSON report generation. The subprocess scenarios are mocked to avoid real network requests and database changes.

## Current Results

- Five pipeline steps completed successfully
- 100 book records loaded into SQLite
- Execution summary generated
- Three automated tests passed

## Data Source

[Books to Scrape](https://books.toscrape.com/) — a web scraping demonstration website.

## License

MIT License. See the repository's root `LICENSE` file.