# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Project Overview

**Tech Pack Assistant** is a Python CLI tool for fashion technical-design workflows. It helps designers create, manage, and export garment tech packs with style metadata, measurement specs, and revision history.

## Repository Structure

```
├── CLAUDE.md                       # This file
├── README.md                       # Project readme
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Python dependencies
├── pyproject.toml                  # Project config, ruff & mypy settings
├── app.py                          # Streamlit web UI
├── tech_pack_assistant.py          # Core data models and CLI
└── tests/
    └── test_tech_pack_assistant.py # Tests for the tech pack assistant
```

## Commands

- **Launch web UI**: `streamlit run app.py`
- **Create starter tech pack**: `python tech_pack_assistant.py init --out tech_pack.json`
- **Add measurement spec**: `python tech_pack_assistant.py add-spec --file tech_pack.json --pom "Chest Width" --size M --value 21.0 --tolerance 0.25`
- **Add revision**: `python tech_pack_assistant.py add-revision --file tech_pack.json --version v2 --author "Name" --summary "Updated specs"`
- **Export markdown**: `python tech_pack_assistant.py export-md --file tech_pack.json --out tech_pack.md`
- **Lint**: `python3 -m ruff check .`
- **Format check**: `python3 -m ruff format --check .`
- **Type check**: `python3 -m mypy .`
- **Run tests**: `python3 -m pytest`

## How It Works

1. `tech_pack_assistant.py` defines dataclasses for `StyleInfo`, `MeasurementSpec`, `Revision`, and `TechPack`
2. Tech packs are stored as JSON files
3. The CLI supports creating starter packs, adding measurement rows, adding revisions, and exporting to markdown
4. Markdown export generates a shareable document with style details, measurement spec tables, and revision history

## Code Style

- Python 3.10+
- Type hints on function signatures
- Docstrings on all public functions
- Linting and formatting enforced by ruff (config in `pyproject.toml`)
- Type checking with mypy
