#!/usr/bin/env python3
import csv, sys, os, re
from collections import defaultdict

SRC = sys.argv[1] if len(sys.argv) > 1 else "data/genetics/variant_index.csv"
OUT = "data/analytics/genetics_appendix.md"

# Load CSV
if not os.path.exists(SRC):
    print(f"[csv_to_md_table] Source CSV not found: {SRC}")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT,"w") as f:
        f.write("# Genetics Appendix\n\n> No variant_index.csv found.\n")
    sys.exit(0)

with open(SRC, newline='') as f:
    r = csv.DictReader(f)
    rows = [ { (k or "").strip(): (v or "").strip() for k,v in row.items() } for row in r ]

# Normalize headers (stable order)
headers = []
seen = set()
for row in rows:
    for k in row.keys():
        if k not in seen:
            seen.add(k); headers.append(k)

# Choose useful display order if present
preferred = ["gene","rsid","chrom","pos","ref","alt","hgvs","zygosity","variant",
             "effect","impact","consequence","source","note"]
ordered = [h for h in preferred if h in headers] + [h for h in headers if h not in preferred]
headers = ordered

# Group by gene (case-insensitive), with 'UNKNOWN' fallback
groups = defaultdict(list)
for row in rows:
    gene = row.get("gene") or row.get("GENE") or row.get("Gene") or "UNKNOWN"
    groups[gene.upper()].append(row)

# Write Markdown
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT,"w",encoding="utf-8") as f:
    f.write("# Genetics Appendix (Full Variant Index)\n\n")
    f.write("> Source: `data/genetics/variant_index.csv`. Grouped by **GENE**. Long tables are enabled via LaTeX longtable when available.\n\n")
    f.write("---\n\n")

    for gene in sorted(groups.keys(), key=lambda s: (s=="UNKNOWN", s)):
        f.write(f"## {gene}\n\n")
        f.write("| " + " | ".join(h.replace('|','/') for h in headers) + " |\n")
        f.write("|" + "|".join(["---"]*len(headers)) + "|\n")
        for row in groups[gene]:
            vals=[]
            for h in headers:
                v = row.get(h,"")
                # compact overly long HGVS/notes to avoid table blowouts; keep full content in <details>
                if h.lower() in ("hgvs","note","notes") and len(v) > 120:
                    short = v[:110].rstrip() + "…"
                    cell = f"{short}<br/><details><summary>more</summary>{v}</details>"
                else:
                    cell = v
                vals.append(cell.replace('\n',' ').replace('|','/'))
            f.write("| " + " | ".join(vals) + " |\n")
        f.write("\n\n")
print(f"[csv_to_md_table] Wrote {OUT} (genes: {len(groups)})")
