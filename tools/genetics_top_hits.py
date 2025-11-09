#!/usr/bin/env python3
import csv, os, re

SRC = "data/genetics/variant_index.csv"
OUT = "data/analytics/genetics_top_hits.md"
os.makedirs(os.path.dirname(OUT), exist_ok=True)

if not os.path.exists(SRC):
    with open(OUT,"w") as f:
        f.write("## Genetics — Top Hits\n\n_No variant index found._\n")
    print(f"[top_hits] No source CSV; wrote stub {OUT}")
    raise SystemExit(0)

def get(row, name):
    for k in row.keys():
        if k.lower()==name.lower():
            return row[k].strip()
    return ""

def to_float(s):
    try: return float(s)
    except: return None

def is_hit(r):
    clin = get(r,"clinvar").lower()
    imp  = get(r,"impact").lower() or get(r,"consequence").lower()
    af   = to_float(get(r,"gnomad_af") or get(r,"gnomad"))
    return ("pathogenic" in clin and "not" not in clin) or ("likely pathogenic" in clin) \
           or imp in {"high","moderate"} \
           or (af is not None and af < 0.01)

rows=[]
with open(SRC, newline='') as f:
    r = csv.DictReader(f)
    for row in r:
        row = { (k or "").strip(): (v or "").strip() for k,v in row.items() }
        if is_hit(row):
            rows.append(row)

# light priority sort
def score(r):
    s=0
    clin = get(r,"clinvar").lower()
    imp  = (get(r,"impact") or get(r,"consequence")).lower()
    af   = to_float(get(r,"gnomad_af") or get(r,"gnomad"))
    if "pathogenic" in clin and "not" not in clin: s+=100
    if "likely pathogenic" in clin: s+=80
    if imp=="high": s+=70
    if imp=="moderate": s+=40
    if af is not None:
        if af < 1e-4: s+=50
        elif af < 1e-3: s+=30
        elif af < 1e-2: s+=15
    return -s

rows = sorted(rows, key=score)[:10]

with open(OUT,"w",encoding="utf-8") as f:
    f.write("## Genetics — Top Hits (auto-scan)\n\n")
    if not rows:
        f.write("_No variants met highlight criteria._\n")
    else:
        cols = ["gene","rsid","hgvs","impact","clinvar","gnomad_af","note"]
        f.write("| " + " | ".join(c.upper() for c in cols) + " |\n")
        f.write("|" + "|".join(["---"]*len(cols)) + "|\n")
        for r in rows:
            f.write("| " + " | ".join((r.get(c,"") or r.get(c.upper(),"")).replace("|","/") for c in cols) + " |\n")
    f.write("\nSee full appendix for details.\n")
print(f"[top_hits] Wrote {OUT} with {len(rows)} rows")
