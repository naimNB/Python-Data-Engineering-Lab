
import json
import sys
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR / "src"))

import pipeline


def test_pipeline_success(tmp_path):
    # Mock subprocess: no real network calls
    completed = subprocess.CompletedProcess(
        args=["python", "test.py"],
        returncode=0,
        stdout="Step completed",
        stderr=""
    )

    with patch.object(pipeline.subprocess, "run", return_value=completed):
        with patch.object(pipeline, "save_report") as mock_report:
            assert pipeline.run_pipeline() is True

    assert mock_report.call_args.kwargs["status"] == "success"
    assert mock_report.call_args.kwargs["steps_completed"] == 5


def test_pipeline_failure():
    # Simulate a failed subprocess
    error = subprocess.CalledProcessError(
        returncode=1,
        cmd=["python", "test.py"],
        stderr="Simulated pipeline failure"
    )

    with patch.object(pipeline.subprocess, "run", side_effect=error):
        with patch.object(pipeline, "save_report") as mock_report:
            assert pipeline.run_pipeline() is False

    assert mock_report.call_args.kwargs["status"] == "failed"
    assert mock_report.call_args.kwargs["failed_step"] == "Web Scraping"
    assert mock_report.call_args.kwargs["steps_completed"] == 0


def test_save_report(tmp_path):
    with patch.object(pipeline, "PROJECT_DIR", tmp_path):
        started_at = datetime.now(timezone.utc)

        pipeline.save_report(
            status="success",
            started_at=started_at,
            steps_completed=5
        )

        report_file = tmp_path / "reports" / "pipeline_report.json"

        assert report_file.exists()

        report = json.loads(report_file.read_text(encoding="utf-8"))

        assert report["status"] == "success"
        assert report["steps_completed"] == 5
        assert report["total_steps"] == 5
        assert report["failed_step"] is None
        assert report["error"] is None
