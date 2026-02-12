# neew

Compare Los Angeles February weather over the last 10 years (2016-2025). Fetches historical data from the [Open-Meteo API](https://open-meteo.com/) and generates a 4-panel chart using matplotlib.

## Charts produced

- Average February temperature by year
- Average daily high & low temperatures by year
- Total February rainfall by year
- Daily average temperature throughout February (all years overlaid)

## Setup

Requires Python 3.10+.

```bash
pip install -r requirements.txt
```

## Usage

Fetch the weather data:

```bash
python fetch_weather.py
```

Generate the chart (fetches data automatically if not cached):

```bash
python plot_weather.py
```

Output is saved to `la_february_weather.png`.

## Development

Install dev tools:

```bash
pip install ruff mypy pytest types-requests pandas-stubs
```

Run checks:

```bash
ruff check .          # lint
ruff format --check . # format check
mypy .                # type check
pytest                # tests
```
