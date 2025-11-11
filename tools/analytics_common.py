#!/usr/bin/env python3
import os, sys, csv, math, pathlib, statistics as stats
from datetime import datetime, date
from typing import List, Dict, Any, Tuple, Optional

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---- IO helpers ----
def ensure_dir(path:str):
    os.makedirs(path, exist_ok=True)

def read_csv_smart(path: str, dt_cols: List[str] = None) -> pd.DataFrame:
    if not os.path.exists(path):
        return pd.DataFrame()
    try:
        df = pd.read_csv(path, comment="#")
    except Exception:
        # try ; delimiter fallback
        df = pd.read_csv(path, sep=";", comment="#")
    if dt_cols:
        for c in dt_cols:
            if c in df.columns:
                df[c] = pd.to_datetime(df[c], errors="coerce")
    return df

def write_md(path: str, text: str):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def save_plot(path: str):
    ensure_dir(os.path.dirname(path))
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()

# ---- math helpers ----
def pearson(a: pd.Series, b: pd.Series) -> Optional[float]:
    a = pd.to_numeric(a, errors="coerce")
    b = pd.to_numeric(b, errors="coerce")
    m = a.notna() & b.notna()
    if m.sum() < 3:
        return None
    try:
        return float(np.corrcoef(a[m], b[m])[0,1])
    except Exception:
        return None

def rolling_corr(df: pd.DataFrame, x: str, y: str, window: int = 10) -> pd.Series:
    if x not in df.columns or y not in df.columns:
        return pd.Series(dtype=float)
    s = pd.concat([pd.to_numeric(df[x], errors="coerce"),
                   pd.to_numeric(df[y], errors="coerce")], axis=1)
    s = s.dropna()
    if s.empty:
        return pd.Series(dtype=float)
    return s[x].rolling(window).corr(s[y])

def safe_mean(s: pd.Series) -> Optional[float]:
    s = pd.to_numeric(s, errors="coerce")
    s = s.dropna()
    return float(s.mean()) if len(s) else None

def fmt(v, digits=3):
    if v is None or (isinstance(v, float) and (math.isnan(v) or math.isinf(v))):
        return "—"
    try:
        return f"{float(v):.{digits}f}"
    except Exception:
        return str(v)

# ---- domain helpers ----
def headache_threshold_hits(glucose_series: pd.Series, threshold: float = 110.0) -> int:
    g = pd.to_numeric(glucose_series, errors="coerce")
    return int((g.notna()) & (g < threshold)).sum()

def flag_to_bool(s: pd.Series) -> pd.Series:
    if s.dtype == bool:
        return s
    return s.astype(str).str.lower().isin(["1","true","yes","y"])

# ---- markdown helpers ----
def md_table(rows: List[List[Any]], header: List[str]) -> str:
    if not rows:
        rows = [["—"] * len(header)]
    out = []
    out.append("| " + " | ".join(header) + " |")
    out.append("|" + "|".join(["---"]*len(header)) + "|")
    for r in rows:
        out.append("| " + " | ".join("" if x is None else str(x) for x in r) + " |")
    return "\n".join(out)

# --- PATCH: corrected headache_threshold_hits (override) ---
def headache_threshold_hits(series, threshold):
    """
    Count how many numeric entries are strictly below 'threshold'.
    Accepts list/Series-like; coercion to numeric with NaNs ignored.
    """
    import pandas as _pd
    try:
        g = _pd.to_numeric(_pd.Series(series), errors="coerce")
    except Exception:
        return 0
    try:
        thr = float(threshold)
    except Exception:
        thr = 110.0
    return int(((g.notna()) & (g < thr)).sum())
