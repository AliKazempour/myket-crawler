#!/usr/bin/env bash

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"


mkdir -p logs
PYTHON_BIN="$PROJECT_DIR/venv/bin/python3"


TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")


echo "[$TIMESTAMP] Starting Myket Scraper..." >> "$PROJECT_DIR/logs/crawler.log"
$PYTHON_BIN runner.py >> "$PROJECT_DIR/logs/crawler.log" 2>&1
echo "[$TIMESTAMP] Scraper finished with exit code $?." >> "$PROJECT_DIR/logs/crawler.log"