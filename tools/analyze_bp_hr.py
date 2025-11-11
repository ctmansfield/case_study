#!/usr/bin/env python3
import os
import pandas as pd
import matplotlib.pyplot as plt
from analytics_common import (
    read_csv_smart, write_md, ensure_dir, pearson, rolling_corr, safe_mean,
    fmt, save_plot, flag_to_bool
)

INP = "data/tracking/bp_hr.csv"
MD  = "data/analytics/bp_hr_summary.md"
PLOT_BP = "data/plots/bp_trend.png"
PLOT_HR = "data/plots/hr_trend.png"
PLOT_CORR = "data/plots/hr_bp_corr_rolling.png"

def main():
    df = read_csv_smart(INP, dt_cols=["timestamp"])
    ensure_dir(os.path.dirname(MD))

    if df.empty:
        write_md(MD, "# BP/HR Summary\n\n> No data yet. Add rows to `data/tracking/bp_hr.csv`.\n")
        return

    # normalize fields
    for c in ["SBP","DBP","HR","sleep_deficit_hours"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    if "episode_flag" in df.columns:
        df["episode_flag"] = flag_to_bool(df["episode_flag"])

    # Basic stats
    sbp_mean = safe_mean(df.get("SBP", pd.Series()))
    dbp_mean = safe_mean(df.get("DBP", pd.Series()))
    hr_mean  = safe_mean(df.get("HR",  pd.Series()))

    # Pearson correlations
    corr_hr_sbp = pearson(df.get("HR", pd.Series()), df.get("SBP", pd.Series()))
    corr_hr_dbp = pearson(df.get("HR", pd.Series()), df.get("DBP", pd.Series()))
    corr_sleep_sbp = pearson(df.get("sleep_deficit_hours", pd.Series()), df.get("SBP", pd.Series()))
    corr_sleep_hr  = pearson(df.get("sleep_deficit_hours", pd.Series()), df.get("HR", pd.Series()))

    # Plots (fail-soft)
    try:
        if "timestamp" in df.columns:
            df_sorted = df.sort_values("timestamp")
        else:
            df_sorted = df.copy()

        if "SBP" in df_sorted.columns and "DBP" in df_sorted.columns:
            df_sorted[["SBP","DBP"]].plot()
            plt.title("BP Trend (SBP/DBP)")
            plt.xlabel("Index" if "timestamp" not in df_sorted.columns else "Time")
            plt.ylabel("mmHg")
            save_plot(PLOT_BP)

        if "HR" in df_sorted.columns:
            df_sorted["HR"].plot()
            plt.title("HR Trend")
            plt.xlabel("Index" if "timestamp" not in df_sorted.columns else "Time")
            plt.ylabel("bpm")
            save_plot(PLOT_HR)

        # Rolling corr HR~SBP
        if "HR" in df_sorted.columns and "SBP" in df_sorted.columns:
            rc = rolling_corr(df_sorted, "HR", "SBP", window=10)
            rc.plot()
            plt.title("Rolling Correlation: HR vs SBP (window=10)")
            plt.xlabel("Index")
            plt.ylabel("r")
            save_plot(PLOT_CORR)
    except Exception:
        pass

    # Recent episodes table (last 10 flagged)
    recent = []
    if "episode_flag" in df.columns and df["episode_flag"].any():
        cols = [c for c in ["timestamp","SBP","DBP","HR","trigger_type","intervention","response","notes"]
                if c in df.columns]
        recent_df = df[df["episode_flag"]==True].sort_values("timestamp", ascending=False).head(10)
        for _, r in recent_df[cols].iterrows():
            recent.append([str(r.get(c,"")) for c in cols])
        recent_header = [c.upper() for c in cols]
    else:
        recent_header = ["INFO"]
        recent = [["No flagged episodes yet. Mark `episode_flag=1` to include here."]]

    # Markdown report
    rows = [
        ["SBP mean (mmHg)", fmt(sbp_mean)],
        ["DBP mean (mmHg)", fmt(dbp_mean)],
        ["HR mean (bpm)",   fmt(hr_mean)],
        ["corr(HR,SBP)",    fmt(corr_hr_sbp)],
        ["corr(HR,DBP)",    fmt(corr_hr_dbp)],
        ["corr(SleepDef,SBP)", fmt(corr_sleep_sbp)],
        ["corr(SleepDef,HR)",  fmt(corr_sleep_hr)],
        ["Plots", "bp_trend.png, hr_trend.png, hr_bp_corr_rolling.png"],
    ]
    header = ["Metric", "Value"]

    md = []
    md.append("# BP/HR Summary\n")
    md.append("## Overview\n")
    md.append("Key summary statistics and correlations. Higher HR–SBP coupling supports adrenergic surges during episodes.\n\n")
    md.append("### Metrics\n")
    md.append(md_table(rows, header))
    md.append("\n\n### Recent Flagged Episodes\n")
    md.append(md_table(recent, recent_header))
    write_md(MD, "\n".join(md))

if __name__ == "__main__":
    from analytics_common import md_table
    main()
