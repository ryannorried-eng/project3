# Tech Pack Assistant (MVP)

A small Python tool to help with early technical-design workflows for fashion products.

This MVP focuses on the core of a tech pack:
- Style details (style number, name, season, fabric, trims)
- Measurement spec rows (POM, size, value, tolerance, notes)
- Revision tracking (version, author, summary, timestamp)
- Markdown export for sharing

## Setup

Requires Python 3.10+.

```bash
pip install -r requirements.txt
```

## CLI Usage

Create a starter tech pack JSON:

```bash
python tech_pack_assistant.py init --out tech_pack.json
```

Add a measurement spec row:

```bash
python tech_pack_assistant.py add-spec \
  --file tech_pack.json \
  --pom "Chest Width (1\" below AH)" \
  --size M \
  --value 21.0 \
  --tolerance 0.25 \
  --notes "Laid flat"
```

Add a revision entry:

```bash
python tech_pack_assistant.py add-revision \
  --file tech_pack.json \
  --version v2 \
  --author "Your Name" \
  --summary "Updated chest width and neck opening"
```

Export markdown:

```bash
python tech_pack_assistant.py export-md --file tech_pack.json --out tech_pack.md
```

## Development checks

```bash
ruff check .
ruff format --check .
mypy .
pytest
```
