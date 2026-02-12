# Tech Pack Assistant (MVP)

A Python tool to help with early technical-design workflows for fashion products.

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

## Web UI (recommended)

Launch the browser-based interface — no coding skills needed:

```bash
streamlit run app.py
```

This opens a local web page where you can:
- Edit style details (name, season, fabric, trims, etc.)
- Add and remove measurement specs
- Track revisions
- Download your tech pack as Markdown or JSON

## CLI Usage

You can also use the command-line interface directly:

```bash
# Create a starter tech pack
python tech_pack_assistant.py init --out tech_pack.json

# Add a measurement spec row
python tech_pack_assistant.py add-spec \
  --file tech_pack.json \
  --pom "Chest Width (1\" below AH)" \
  --size M \
  --value 21.0 \
  --tolerance 0.25 \
  --notes "Laid flat"

# Add a revision entry
python tech_pack_assistant.py add-revision \
  --file tech_pack.json \
  --version v2 \
  --author "Your Name" \
  --summary "Updated chest width and neck opening"

# Export markdown
python tech_pack_assistant.py export-md --file tech_pack.json --out tech_pack.md
```

## Development checks

```bash
ruff check .
ruff format --check .
mypy .
pytest
```
