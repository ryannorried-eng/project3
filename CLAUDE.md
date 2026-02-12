# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Project Overview

`neew` is a Python data visualization project that compares Los Angeles February weather over the last 10 years (2016–2025). It fetches historical weather data from the Open-Meteo API and generates charts using matplotlib.

## Repository Structure

```
neew/
├── CLAUDE.md           # This file
├── README.md           # Project readme
├── .gitignore          # Git ignore rules
├── requirements.txt    # Python dependencies
├── fetch_weather.py    # Fetches weather data from Open-Meteo API
└── plot_weather.py     # Generates the 4-panel weather chart
```

## Commands

- **Install dependencies**: `pip install -r requirements.txt`
- **Install dev tools**: `pip install ruff mypy pytest types-requests pandas-stubs`
- **Fetch data only**: `python fetch_weather.py`
- **Generate chart**: `python plot_weather.py`
- **Lint**: `python3 -m ruff check .`
- **Format check**: `python3 -m ruff format --check .`
- **Type check**: `python3 -m mypy .`
- **Run tests**: `python3 -m pytest`

## How It Works

1. `fetch_weather.py` calls the Open-Meteo historical weather API for each February from 2016–2025
2. Data is cached locally in `la_february_weather.csv`
3. `plot_weather.py` loads the data and produces a 4-panel chart (`la_february_weather.png`):
   - Average February temperature by year
   - Average daily high & low temperatures by year
   - Total February rainfall by year
   - Daily average temperature throughout February (all years overlaid)

## Code Style

- Python 3.10+
- Type hints on function signatures
- Docstrings on all public functions
- Linting and formatting enforced by ruff (config in `pyproject.toml`)
- Type checking with mypy
