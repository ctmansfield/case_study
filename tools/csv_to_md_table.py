#!/usr/bin/env python3
import csv, sys, os, re, statistics
from collections import defaultdict

SRC = sys.argv[1] if len(sys.argv) > 1 else "data/genetics/variant_index.csv"
OUT = "data/analytics/genetics_appendix.md"

def colfind(row, names):
    for n in names:
        for k in row.keys():
            if k.lower()==n.lower():
                return k
    return None

def get(row, *names):
    for n in names:
        for k in row.keys():
            if k.lower()==n.lower():
                return row.get(k,"").strip()
    return ""

def to_float(s):
    try:
        return float(s)
    except:
        return None

if not os.path.exists(SRC):
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT,"w") as f:
        f.write("# Genetics Appendix\n\n> No variant_index.csv found.\n")
    print(f"[csv_to_md_table] No source CSV; wrote stub {OUT}")
    raise SystemExit(0)

with open(SRC, newline='') as f:
    r = csv.DictReader(f)
    rows = [{(k or "").strip(): (v or "").strip() for k,v in row.items()} for row in r]

# Stable header order
headers = []
seen = set()
for row in rows:
    for k in row.keys():
        if k not in seen:
            seen.add(k); headers.append(k)

preferred = ["gene","rsid","chrom","pos","ref","alt","hgvs","zygosity",
             "variant","effect","impact","consequence","clinvar","gnomad_af",
             "source","note","notes"]
ordered = [h for h in preferred if h in headers] + [h for h in headers if h not in preferred]
headers = ordered

# Group by gene (case-insensitive)
groups = defaultdict(list)
for row in rows:
    gene = get(row, "gene") or "UNKNOWN"
    groups[gene.upper()].append(row)

# Score "width" of a gene group to pick top-3 for landscape:
def row_width_score(row):
    # length of HGVS + notes + number of non-empty columns
    w = len(get(row,"hgvs")) + len(get(row,"note","notes"))
    nonempty = sum(1 for h in headers if row.get(h,""))
    return w + 20*nonempty

gene_scores = {g: statistics.mean([row_width_score(r) for r in rs]) for g,rs in groups.items()}
landscape_genes = set(sorted(gene_scores, key=gene_scores.get, reverse=True)[:3])

# Helpers for highlighting
def is_pathogenic(s):
    s = (s or "").lower()
    return ("pathogenic" in s and "not" not in s) or "likely pathogenic" in s or "lp" == s.strip()

def is_high_impact(s):
    s = (s or "").lower()
    return s in {"high","moderate"} or "frameshift" in s or "stop_gained" in s or "splice" in s

def is_rare_af(s):
    v = to_float(s)
    return v is not None and v < 0.001

def style_cell(text, highlight=False):
    # Use bold + symbol in both HTML (wkhtml) and LaTeX engines
    if highlight:
        return f"**⚠ {text}**"
    return text

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT,"w",encoding="utf-8") as f:
    f.write("# Genetics Appendix (Full Variant Index)\n\n")
    f.write("> Source: `data/genetics/variant_index.csv`. Grouped by **GENE**. Long tables optimized for PDF.\n\n")
    f.write("_Auto-highlights_: **⚠** rows with (ClinVar Pathogenic/LP) or (impact HIGH/MODERATE) or (gnomAD AF < 0.001).\n\n")
    f.write("---\n\n")
    # Global font tweak (LaTeX path)
    f.write("<div style=\"font-size: 90%\">\n\n")

    for gene in sorted(groups.keys(), key=lambda s: (s=="UNKNOWN", s)):
        # Landscape switch for wide genes (LaTeX engines)
        landscape_open = gene in landscape_genes
        if landscape_open:
            f.write("\\begin{landscape}\n\n")
        f.write(f"## {gene}\n\n")
        f.write("| " + " | ".join(h.replace('|','/') for h in headers) + " |\n")
        f.write("|" + "|".join(["---"]*len(headers)) + "|\n")

        for row in groups[gene]:
            hl = is_pathogenic(get(row,"clinvar")) or is_high_impact(get(row,"impact","consequence")) or is_rare_af(get(row,"gnomad_af","gnomad"))
            vals=[]
            for h in headers:
                v = row.get(h,"")
                # trim very long fields but keep <details> for HTML; for LaTeX it'll just show short
                if h.lower() in ("hgvs","note","notes") and len(v) > 140:
                    short = v[:130].rstrip() + "…"
                    cell = f"{short}<br/><details><summary>more</summary>{v}</details>"
                else:
                    cell = v
                vals.append(style_cell(cell.replace('\n',' ').replace('|','/'), hl))
            f.write("| " + " | ".join(vals) + " |\n")
        f.write("\n")
        if landscape_open:
            f.write("\\end{landscape}\n\n")
        f.write("\\clearpage\n\n")
    f.write("</div>\n")
print(f"[csv_to_md_table] Wrote {OUT} (genes: {len(groups)})")
