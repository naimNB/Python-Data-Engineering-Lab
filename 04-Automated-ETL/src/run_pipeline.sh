
#!/usr/bin/env bash
set -euo pipefail

# Resolve paths independently of the current directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Run with the existing ML Conda environment
PYTHON="$HOME/miniconda3/envs/ML/bin/python"

cd "$PROJECT_DIR"
"$PYTHON" src/pipeline.py
