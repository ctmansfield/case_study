#!/usr/bin/env python3
import csv, os, math
from statistics import mean
import numpy as np

INP = "data/tracking/physio.csv"
OUT = "data/analytics/correlations.md"
PLOT_DIR = "data/analytics/plots"

pairs = [
    ("histamine_score","sbp"),
    ("histamine_score","dbp"),
    ("histamine_score","hr"),
    ("histamine_score","fasting_glucose"),
    ("folate_level","sbp"),
    ("folate_level","dbp"),
    ("folate_level","hr"),
    ("folate_level","fasting_glucose"),
    ("sleep_deficit_hours","fasting_glucose"),
    ("sleep_deficit_hours","sbp"),
    ("sleep_deficit_hours","hr"),
]

def load_rows(path):
    rows=[]
    if not os.path.exists(path):
        return rows
    with open(path, newline='') as f:
        r=csv.DictReader(f)
        for row in r:
            rows.append({k.strip().lower(): (row[k].strip() if k in row else "") for k in r.fieldnames})
    return rows

def to_float(v):
    try:
        return float(v)
    except:
        return None

def pearson(x,y):
    xv=[to_float(a) for a in x]; yv=[to_float(b) for b in y]
    pts=[(a,b) for a,b in zip(xv,yv) if a is not None and b is not None]
    if len(pts)<3: return None, len(pts)
    xa,ya=zip(*pts)
    r = float(np.corrcoef(xa,ya)[0,1])
    return r, len(pts)



import argparse
ap=argparse.ArgumentParser()
ap.add_argument('--plots', action='store_true', help='emit scatter plots to data/analytics/plots/')
args=ap.parse_args()
rows = load_rows(INP)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT,"w") as f:
    f.write("# Correlation Snapshot\n\n")
    if not rows:
        f.write("> No data yet. Add rows to `data/tracking/physio.csv` and rerun:\n")
        f.write("`python3 tools/track_corr.py`\n")
    else:
        cols = list(rows[0].keys())
        f.write("Source: `data/tracking/physio.csv`\n\n")
        f.write("| Pair | r (Pearson) | n |\n|---|---:|--:|\n")
        for a,b in pairs:
            x=[r.get(a,"") for r in rows]
            y=[r.get(b,"") for r in rows]
            r,n = pearson(x,y)
            rs = f"{r:.3f}" if r is not None else "—"
            f.write(f"| {a} ↔ {b} | {rs} | {n} |\n")
        f.write("\n> Interpret: |r| ~ 0.1 weak · 0.3 moderate · 0.5+ strong (directional).\n")
print(f"Wrote {OUT}")

if args.plots:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    os.makedirs(PLOT_DIR, exist_ok=True)
    for a,b in pairs:
        x=[to_float(r.get(a,'')) for r in rows]
        y=[to_float(r.get(b,'')) for r in rows]
        pts=[(xa,ya) for xa,ya in zip(x,y) if xa is not None and ya is not None]
        if len(pts) < 3: continue
        xa,ya=zip(*pts)
        plt.figure()
        plt.scatter(xa,ya)
        plt.xlabel(a); plt.ylabel(b); plt.title(f"{a} vs {b}")
        fn = f"{a}_vs_{b}.png".replace('/','-')
        plt.tight_layout()
        plt.savefig(os.path.join(PLOT_DIR, fn))
        plt.close()
