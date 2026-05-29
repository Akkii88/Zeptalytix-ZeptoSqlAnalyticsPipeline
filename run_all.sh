#!/usr/bin/env bash
set -euo pipefail

# Run full local workflow (requires docker for the DB step)

echo "1) Create venv and install deps"
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

echo "2) Execute notebook"
.venv/bin/jupyter nbconvert --to notebook --execute notebooks/EDA.ipynb --output notebooks/EDA_executed.ipynb --ExecutePreprocessor.timeout=600 || true

if command -v docker >/dev/null 2>&1; then
  echo "3) Start Postgres and run ETL"
  docker-compose up -d
  sleep 5
  .venv/bin/python etl/etl.py || true
else
  echo "Docker not found — skipping ETL. Start Docker and run 'docker-compose up -d' and 'python etl/etl.py' to load data."
fi

if command -v pandoc >/dev/null 2>&1; then
  echo "4) Build slides PDF"
  pandoc slides/Slide_Deck.md -o slides/Slide_Deck.pdf
else
  echo "Pandoc not found — slides/Slide_Deck.html is available as a fallback."
fi

echo "Done."
