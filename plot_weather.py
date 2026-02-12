"""Generate weather charts comparing LA February weather over 10 years."""

import sys

import matplotlib.pyplot as plt
import pandas as pd

from fetch_weather import fetch_all_years


def load_data() -> pd.DataFrame:
    """Load data from CSV cache or fetch from API."""
    try:
        df = pd.read_csv("la_february_weather.csv")
        df["date"] = pd.to_datetime(df["time"])
        print("Loaded cached data from la_february_weather.csv")
    except FileNotFoundError:
        print("No cached data found, fetching from API...")
        df = fetch_all_years()
        df.to_csv("la_february_weather.csv", index=False)
    return df


def plot_avg_temperature(df: pd.DataFrame, ax: plt.Axes) -> None:
    """Plot average February temperature by year."""
    yearly_avg = df.groupby("year")["temperature_2m_mean"].mean()
    bars = ax.bar(yearly_avg.index, yearly_avg.values, color="#4A90D9", edgecolor="white")
    ax.set_title("Average February Temperature", fontsize=13, fontweight="bold")
    ax.set_ylabel("Temperature (\u00b0F)")
    ax.set_xticks(yearly_avg.index)
    ax.set_xticklabels(yearly_avg.index, rotation=45)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.3,
                f"{height:.1f}", ha="center", va="bottom", fontsize=8)


def plot_high_low(df: pd.DataFrame, ax: plt.Axes) -> None:
    """Plot average daily high and low temperatures by year."""
    yearly = df.groupby("year").agg(
        high=("temperature_2m_max", "mean"),
        low=("temperature_2m_min", "mean"),
    )
    x = yearly.index
    width = 0.35
    ax.bar(x - width / 2, yearly["high"], width, label="Avg High", color="#E74C3C", edgecolor="white")
    ax.bar(x + width / 2, yearly["low"], width, label="Avg Low", color="#3498DB", edgecolor="white")
    ax.set_title("Avg Daily High & Low in February", fontsize=13, fontweight="bold")
    ax.set_ylabel("Temperature (\u00b0F)")
    ax.set_xticks(x)
    ax.set_xticklabels(x, rotation=45)
    ax.legend()


def plot_rainfall(df: pd.DataFrame, ax: plt.Axes) -> None:
    """Plot total February rainfall by year."""
    yearly_rain = df.groupby("year")["precipitation_sum"].sum()
    bars = ax.bar(yearly_rain.index, yearly_rain.values, color="#27AE60", edgecolor="white")
    ax.set_title("Total February Rainfall", fontsize=13, fontweight="bold")
    ax.set_ylabel("Rainfall (inches)")
    ax.set_xticks(yearly_rain.index)
    ax.set_xticklabels(yearly_rain.index, rotation=45)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.05,
                f"{height:.2f}", ha="center", va="bottom", fontsize=8)


def plot_temp_trend(df: pd.DataFrame, ax: plt.Axes) -> None:
    """Plot daily temperature range as a band for each year."""
    cmap = plt.cm.coolwarm
    years = sorted(df["year"].unique())
    for i, year in enumerate(years):
        ydf = df[df["year"] == year].sort_values("day")
        color = cmap(i / (len(years) - 1))
        ax.plot(ydf["day"], ydf["temperature_2m_mean"], label=str(year),
                color=color, alpha=0.7, linewidth=1.2)
    ax.set_title("Daily Avg Temp Throughout February", fontsize=13, fontweight="bold")
    ax.set_xlabel("Day of February")
    ax.set_ylabel("Temperature (\u00b0F)")
    ax.legend(fontsize=7, ncol=2, loc="upper right")


def main() -> None:
    df = load_data()

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Los Angeles February Weather (2016\u20132025)", fontsize=16, fontweight="bold")

    plot_avg_temperature(df, axes[0, 0])
    plot_high_low(df, axes[0, 1])
    plot_rainfall(df, axes[1, 0])
    plot_temp_trend(df, axes[1, 1])

    plt.tight_layout()

    output = "la_february_weather.png"
    fig.savefig(output, dpi=150, bbox_inches="tight")
    print(f"Chart saved to {output}")

    # Also show if running interactively
    if "ipykernel" in sys.modules:
        plt.show()


if __name__ == "__main__":
    main()
