# Tech Pack Assistant (MVP)

A small Python tool for early **fashion technical design** workflows.

It helps with core tech-pack tasks:
- Style metadata
- Measurement specs (POM, size, value, tolerance, notes)
- Revision history
- Validation checks for common spec mistakes
- Export to Markdown and CSV

## Setup

Requires Python 3.10+.

```bash
pip install -r requirements.txt
```

## CLI Usage

### 1) Create a starter pack

```bash
python tech_pack_assistant.py init --out tech_pack.json
```

### 2) Add measurement specs

```bash
python tech_pack_assistant.py add-spec \
  --file tech_pack.json \
  --pom "Chest Width (1\" below AH)" \
  --size M \
  --value 21.0 \
  --tolerance 0.25 \
  --notes "Laid flat"
```

### 3) Add a revision

```bash
python tech_pack_assistant.py add-revision \
  --file tech_pack.json \
  --version v2 \
  --author "Your Name" \
  --summary "Updated chest width and neck opening"
```

### 4) Validate before sharing

```bash
python tech_pack_assistant.py validate --file tech_pack.json
```

### 5) Export

```bash
python tech_pack_assistant.py export-md --file tech_pack.json --out tech_pack.md
python tech_pack_assistant.py export-csv --file tech_pack.json --out measurements.csv
```

## Development checks

```bash
ruff check .
ruff format --check .
mypy .
pytest
```
