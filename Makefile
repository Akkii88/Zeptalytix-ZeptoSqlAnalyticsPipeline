VENV=.venv
PY=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

.PHONY: help setup deps run-eda exec-notebook docker-up etl pdf streamlit test all

help:
	@echo "Available targets: setup deps run-eda exec-notebook docker-up etl pdf streamlit test all"

setup:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip

deps:
	$(PIP) install -r requirements.txt

run-eda:
	$(PY) notebooks/EDA.py

exec-notebook:
	$(VENV)/bin/jupyter nbconvert --to notebook --execute notebooks/EDA.ipynb --output notebooks/EDA_executed.ipynb --ExecutePreprocessor.timeout=600

docker-up:
	docker-compose up -d

etl:
	$(PY) etl/etl.py

pdf:
	# Preferred: use pandoc (install pandoc separately)
	if command -v pandoc >/dev/null 2>&1; then \
		pandoc slides/Slide_Deck.md -o slides/Slide_Deck.pdf; \
	else \
		$(PY) scripts/md_to_pdf.py || echo "Install pandoc or ensure reportlab is available in the venv to build PDF."; \
	fi

streamlit:
	$(PIP) install streamlit || true
	streamlit run app/streamlit_app.py

test:
	$(PY) tests/data_quality.py

all: setup deps exec-notebook pdf
