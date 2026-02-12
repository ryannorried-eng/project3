"""Fetch February weather data for Los Angeles over the last 10 years."""

import requests
import pandas as pd

# Los Angeles coordinates
LAT = 34.0522
LON = -118.2437

# Open-Meteo historical weather API (free, no key needed)
BASE_URL = "https://archive-api.open-meteo.com/v1/archive"


def fetch_february_data(year: int) -> pd.DataFrame:
    """Fetch daily weather data for February of a given year."""
    # Handle leap years
    end_day = 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28

    params = {
        "latitude": LAT,
        "longitude": LON,
        "start_date": f"{year}-02-01",
        "end_date": f"{year}-02-{end_day}",
        "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum",
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
        "timezone": "America/Los_Angeles",
    }

    resp = requests.get(BASE_URL, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()["daily"]

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["time"])
    df["day"] = df["date"].dt.day
    df["year"] = year
    return df


def fetch_all_years(start_year: int = 2016, end_year: int = 2025) -> pd.DataFrame:
    """Fetch February data for a range of years."""
    frames = []
    for year in range(start_year, end_year + 1):
        print(f"Fetching {year}...")
        frames.append(fetch_february_data(year))
    return pd.concat(frames, ignore_index=True)


if __name__ == "__main__":
    df = fetch_all_years()
    df.to_csv("la_february_weather.csv", index=False)
    print(f"Saved {len(df)} rows to la_february_weather.csv")
