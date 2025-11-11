#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from analytics_common import (
    read_csv_smart, write_md, ensure_dir, pearson, rolling_corr, safe_mean,
    fmt, save_plot, headache_threshold_hits, md_table
)

INP = "data/tracking/glucose.csv"
MD  = "data/analytics/glucose_summary.md"
PLOT_FAST = "data/plots/glucose_fasting_trend.png"
PLOT_POST = "data/plots/glucose_postprandial_trend.png"
PLOT_CORR = "data/plots/glucose_histamine_corr.png"

def main():
    df = read_csv_smart(INP, dt_cols=["timestamp"])
    if df.empty:
        write_md(MD, "# Glucose Summary\n\n> No data yet. Add rows to `data/tracking/glucose.csv`.\n")
        return

    for c in ["fasting_glucose","postprandial_glucose","meal_histamine_score","sleep_deficit_hours"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # headache threshold (<110 mg/dL) count from fasting values
    h_hits = headache_threshold_hits(df.get("fasting_glucose", []), 110.0)

    # correlations
    c_hist_fast = pearson(df.get("meal_histamine_score", []), df.get("fasting_glucose", []))
    c_hist_post = pearson(df.get("meal_histamine_score", []), df.get("postprandial_glucose", []))
    c_folate_fast = None
    c_folate_post = None
    if "folate_load" in df.columns:
        fol_map = {"low":0, "moderate":1, "high":2}
        fol = df["folate_load"].astype(str).str.lower().map(fol_map)
        c_folate_fast = pearson(fol, df.get("fasting_glucose", []))
        c_folate_post = pearson(fol, df.get("postprandial_glucose", []))

    # plots fail-soft
    try:
        if "fasting_glucose" in df.columns:
            df.sort_values("timestamp")[["fasting_glucose"]].plot()
            plt.title("Fasting Glucose Trend")
            plt.xlabel("Time" if "timestamp" in df.columns else "Index")
            plt.ylabel("mg/dL")
            save_plot(PLOT_FAST)
        if "postprandial_glucose" in df.columns:
            df.sort_values("timestamp")[["postprandial_glucose"]].plot()
            plt.title("Postprandial Glucose Trend")
            plt.xlabel("Time" if "timestamp" in df.columns else "Index")
            plt.ylabel("mg/dL")
            save_plot(PLOT_POST)
    except Exception:
        pass

    rows = [
        ["Fasting mean (mg/dL)", fmt(safe_mean(df.get("fasting_glucose", [])))],
        ["Postprandial mean (mg/dL)", fmt(safe_mean(df.get("postprandial_glucose", [])))],
        ["Headache-threshold hits (fasting <110 mg/dL)", fmt(h_hits, digits=0)],
        ["corr(histamine_score, fasting)", fmt(c_hist_fast)],
        ["corr(histamine_score, postprandial)", fmt(c_hist_post)],
        ["corr(folate_load, fasting)", fmt(c_folate_fast)],
        ["corr(folate_load, postprandial)", fmt(c_folate_post)],
        ["Plots", "glucose_fasting_trend.png, glucose_postprandial_trend.png"],
    ]
    header = ["Metric", "Value"]

    md = []
    md.append("# Glucose Summary\n")
    md.append("Correlations link **meal histamine/folate load** to fasting & postprandial glucose. Headache threshold (<110 mg/dL) tracked.\n\n")
    md.append(md_table(rows, header))
    write_md(MD, "\n".join(md))

if __name__ == "__main__":
    main()
