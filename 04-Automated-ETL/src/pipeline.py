
import json
import logging
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
REPO_DIR = PROJECT_DIR.parent

LOG_DIR = PROJECT_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "pipeline.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

STEPS = [
    ("Web Scraping", "01-Web-Scraping", "scraper.py"),
    ("Generate Test Dataset", "02-Data-Cleaning", "generate_messy_data.py"),
    ("Data Cleaning", "02-Data-Cleaning", "clean_data.py"),
    ("Quality Report", "02-Data-Cleaning", "quality_report.py"),
    ("Database Import", "03-Database-Integration", "import_data.py"),
]

def save_report(status, started_at, steps_completed, failed_step=None, error=None):
    finished_at = datetime.now(timezone.utc)

    report = {
        "status": status,
        "started_at": started_at.isoformat(),
        "finished_at": finished_at.isoformat(),
        "duration_seconds": round(
            (finished_at - started_at).total_seconds(), 2
        ),
        "steps_completed": steps_completed,
        "total_steps": len(STEPS),
        "failed_step": failed_step,
        "error": error
    }

    report_dir = PROJECT_DIR / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / "pipeline_report.json"

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print(f"Execution report saved: {report_path}")



def run_pipeline():
    started_at = datetime.now(timezone.utc)
    steps_completed = 0

    print(f"ETL Pipeline started: {started_at.isoformat()}")
    logging.info("Pipeline started")

    for name, folder, script in STEPS:
        script_path = REPO_DIR / folder / "src" / script

        print(f"\nRunning: {name}")
        logging.info("Starting step: %s", name)

        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=REPO_DIR / folder,
                capture_output=True,
                text=True,
                check=True,
                timeout=180
            )

            print(result.stdout)
            steps_completed += 1
            logging.info("Completed step: %s", name)

        except (
            subprocess.CalledProcessError,
            subprocess.TimeoutExpired,
            OSError
        ) as error:
            error_message = (
                getattr(error, "stderr", None) or str(error)
            )

            if isinstance(error_message, bytes):
                error_message = error_message.decode(
                    "utf-8", errors="replace"
                )

            logging.error(
                "Pipeline failed at %s: %s",
                name, error_message
            )

            save_report(
                status="failed",
                started_at=started_at,
                steps_completed=steps_completed,
                failed_step=name,
                error=error_message
            )

            print(f"Pipeline failed at: {name}")
            print(error_message)
            return False

    save_report(
        status="success",
        started_at=started_at,
        steps_completed=steps_completed
    )

    print("\nETL Pipeline completed successfully!")
    logging.info("Pipeline completed successfully")
    return True


if __name__ == "__main__":
    success = run_pipeline()
    sys.exit(0 if success else 1)
