#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from analytics_common import (
    read_csv_smart, write_md, ensure_dir, pearson, safe_mean, fmt, save_plot, md_table
)

INP = "data/tracking/sleep.csv"
MD  = "data/analytics/sleep_summary.md"
PLOT_SLEEP = "data/plots/sleep_hours_trend.png"
PLOT_QUAL  = "data/plots/sleep_quality_trend.png"

def main():
    df = read_csv_smart(INP, dt_cols=["date"])
    if df.empty:
        write_md(MD, "# Sleep Summary\n\n> No data yet. Add rows to `data/tracking/sleep.csv`.\n")
        return

    for c in ["total_sleep_hours","restorative_sleep_score","middle_of_night_awakenings","next_day_SBP","next_day_glucose"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # correlations to next-day metrics
    c_sleep_sbp = pearson(df.get("total_sleep_hours", []), df.get("next_day_SBP", []))
    c_sleep_glu = pearson(df.get("total_sleep_hours", []), df.get("next_day_glucose", []))
    c_quality_glu = pearson(df.get("restorative_sleep_score", []), df.get("next_day_glucose", []))

    # plots
    try:
        if "total_sleep_hours" in df.columns:
            df.sort_values("date")[["total_sleep_hours"]].plot()
            plt.title("Total Sleep Hours")
            plt.xlabel("Date")
            plt.ylabel("h")
            save_plot(PLOT_SLEEP)
        if "restorative_sleep_score" in df.columns:
            df.sort_values("date")[["restorative_sleep_score"]].plot()
            plt.title("Restorative Sleep Score (0–5)")
            plt.xlabel("Date")
            plt.ylabel("score")
            save_plot(PLOT_QUAL)
    except Exception:
        pass

    rows = [
        ["Mean total sleep (h)", fmt(safe_mean(df.get("total_sleep_hours", [])))],
        ["Mean restorative score (0–5)", fmt(safe_mean(df.get("restorative_sleep_score", [])))],
        ["corr(total_sleep, next_day_SBP)", fmt(c_sleep_sbp)],
        ["corr(total_sleep, next_day_glucose)", fmt(c_sleep_glu)],
        ["corr(restorative_score, next_day_glucose)", fmt(c_quality_glu)],
        ["Plots", "sleep_hours_trend.png, sleep_quality_trend.png"],
    ]
    header = ["Metric", "Value"]

    md = ["# Sleep Summary\n", md_table(rows, header)]
    write_md(MD, "\n".join(md))

if __name__ == "__main__":
    main()
