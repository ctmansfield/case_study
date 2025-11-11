#!/usr/bin/env python3
import pandas as pd
from analytics_common import (
    read_csv_smart, write_md, fmt, safe_mean, md_table
)

INP = "data/tracking/med_response.csv"
MD  = "data/analytics/med_response_summary.md"

def main():
    df = read_csv_smart(INP, dt_cols=["timestamp"])
    if df.empty:
        write_md(MD, "# Medication Response Summary\n\n> No data yet. Add rows to `data/tracking/med_response.csv`.\n")
        return

    # normalize
    if "effectiveness_0_to_10" in df.columns:
        df["effectiveness_0_to_10"] = pd.to_numeric(df["effectiveness_0_to_10"], errors="coerce")

    by_med = []
    header = ["Medication","N","Mean Effect (0–10)","Most Common Side-Effect"]
    if "medication" in df.columns:
        for med, g in df.groupby(df["medication"].astype(str).str.strip().str.lower()):
            n = len(g)
            mean_eff = safe_mean(g.get("effectiveness_0_to_10", []))
            se = "—"
            if "side_effects" in g.columns:
                se = g["side_effects"].dropna().astype(str).str.lower().str.strip()
                se = se[se!=""].mode().iat[0] if len(se) else "—"
            by_med.append([med, n, fmt(mean_eff), se])

    # recent entries
    recent = []
    cols = [c for c in ["timestamp","medication","dose","effectiveness_0_to_10","episode_triggered","notes"] if c in df.columns]
    recent_df = df.sort_values("timestamp", ascending=False).head(10)
    for _, r in recent_df[cols].iterrows():
        recent.append([str(r.get(c,"")) for c in cols])

    md = []
    md.append("# Medication Response Summary\n")
    md.append("Aggregated effectiveness and side-effect profile by medication.\n\n")
    md.append("## By Medication\n")
    md.append(md_table(by_med, header))
    md.append("\n\n## Recent Entries\n")
    md.append(md_table(recent, [c.upper() for c in cols]))
    write_md(MD, "\n".join(md))

if __name__ == "__main__":
    main()
