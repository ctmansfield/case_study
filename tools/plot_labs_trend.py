#!/usr/bin/env python3
import os
import math
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

IN_CSV = "data/labs_trend.csv"
OUT_DIR = "data/plots"

def ensure_outdir(path):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)

def load_trend(path):
    df = pd.read_csv(path)
    # Normalize column names just in case
    df.columns = [c.strip() for c in df.columns]
    # Parse date
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.sort_values('date')
    return df

def annotate_points(ax, x, y, labels, yoffset=0.0):
    # Minimal overlap avoidance: alternate offsets
    for i, (xi, yi, lbl) in enumerate(zip(x, y, labels)):
        if pd.isna(xi) or pd.isna(yi) or (lbl is None):
            continue
        dy = (0.02 if i % 2 == 0 else -0.03) + yoffset
        ax.text(xi, yi + dy, str(lbl), ha='center', va='bottom', fontsize=8, rotation=25)

def lineplot(df, cols, title, ylabel, fname, annotate=True, markers=True):
    # Filter rows where at least one of cols is present
    dff = df[['date', 'context'] + cols].copy()
    dff = dff.dropna(subset=cols, how='all')
    if dff.empty:
        print(f"[skip] No data for {title} -> {cols}")
        return
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for c in cols:
        if c in dff and dff[c].notna().any():
            ax.plot(dff['date'], dff[c], marker='o' if markers else None, label=c.replace('_', ' '))
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Date")
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.6)
    # annotate with context on the first non-null column
    if annotate:
        ref_col = None
        for c in cols:
            if dff[c].notna().any():
                ref_col = c
                break
        if ref_col:
            annotate_points(ax, dff['date'], dff[ref_col], dff['context'])
    ax.legend(loc='best', fontsize=9)
    fig.tight_layout()
    png = os.path.join(OUT_DIR, f"{fname}.png")
    svg = os.path.join(OUT_DIR, f"{fname}.svg")
    fig.savefig(png, dpi=300)
    fig.savefig(svg)
    plt.close(fig)
    print(f"[ok] Wrote {png} and {svg}")

def main():
    ensure_outdir(OUT_DIR)
    if not os.path.exists(IN_CSV):
        print(f"[error] Missing {IN_CSV}. Create it first.")
        return
    df = load_trend(IN_CSV)

    # Column names expected in labs_trend.csv
    # date,context,glucose_fasting_mg_dl,insulin_uIU_ml,c_peptide_ng_ml,bhb_mmol_l,
    # cortisol_am_ug_dl,dheas_ug_dl,alt_u_l,ast_u_l,ldl_mg_dl,hdl_mg_dl,triglycerides_mg_dl,platelets_k_ul,notes

    lineplot(
        df,
        cols=['glucose_fasting_mg_dl'],
        title="Fasting Glucose Trend",
        ylabel="mg/dL",
        fname="glucose_fasting_trend",
    )

    lineplot(
        df,
        cols=['insulin_uIU_ml', 'c_peptide_ng_ml'],
        title="Insulin & C-Peptide Trend",
        ylabel="insulin (µIU/mL), C-peptide (ng/mL)",
        fname="insulin_cpeptide_trend",
    )

    lineplot(
        df,
        cols=['bhb_mmol_l'],
        title="β-Hydroxybutyrate (BHB) Trend",
        ylabel="mmol/L",
        fname="bhb_trend",
    )

    lineplot(
        df,
        cols=['cortisol_am_ug_dl', 'dheas_ug_dl'],
        title="Cortisol & DHEA-S Trend",
        ylabel="µg/dL (cortisol), µg/dL (DHEA-S)",
        fname="cortisol_dheas_trend",
    )

    lineplot(
        df,
        cols=['alt_u_l', 'ast_u_l'],
        title="Liver Enzymes (ALT & AST) Trend",
        ylabel="U/L",
        fname="alt_ast_trend",
    )

    lineplot(
        df,
        cols=['ldl_mg_dl', 'hdl_mg_dl', 'triglycerides_mg_dl'],
        title="Lipids Trend (LDL, HDL, TG)",
        ylabel="mg/dL",
        fname="lipids_trend",
    )

    lineplot(
        df,
        cols=['platelets_k_ul'],
        title="Platelets Trend",
        ylabel="K/µL",
        fname="platelets_trend",
    )

if __name__ == "__main__":
    main()
