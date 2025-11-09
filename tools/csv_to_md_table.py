#!/usr/bin/env python3
import csv, sys, os, re, statistics
from collections import defaultdict

SRC = sys.argv[1] if len(sys.argv) > 1 else "data/genetics/variant_index.csv"
OUT = "data/analytics/genetics_appendix.md"

AF_CUTOFF = 0.005  # <- adjusted per user

# Consequences we want to treat as relevant (case-insensitive substring match)
RELEVANT_CONSEQUENCES = {
    "stop_gained","nonsense","frameshift","splice_acceptor","splice_donor","splice_region",
    "missense","start_lost","inframe_insertion","inframe_deletion","inframe_variant",
    "regulatory_region","promoter","5_prime_utr","3_prime_utr","mature_miRNA","TF_binding_site",
    "coding_sequence_variant","protein_altering_variant"
}

def colget(row, name):
    # prefer alias-aware lookup if key is known
    v = colget_alias(row, name)
    if v!='': return v

    for k in row.keys():
        if k.lower()==name.lower():
            return row[k].strip()
    return ""

def to_float(s):
    try: return float(s)
    except: return None

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

ALIASES_MAP = {
  'clinvar': ['clinvar','clinvar_significance','clinvar_clinicalsignificance','clinical_significance','clinvar_s'],
  'gnomad_af': ['gnomad_af','gnomad','gnomad_exomes_af','gnomad_genomes_af','af','max_af','popmax_af'],
  'consequence': ['consequence','consequence(s)','vep_consequence','so','so_terms'],
  'impact': ['impact','vep_impact','impact_level'],
  'rsid': ['rsid','dbsnp','dbsnp_id','rs']
}

def colget_alias(row, key, fallback=None):
    names=[key] + ALIASES_MAP.get(key.lower(), [])
    for n in names:
        for k in row.keys():
            if k.lower()==n.lower():
                return (row.get(k,'') or '').strip()
    return fallback or ''

preferred = ["gene","rsid","chrom","pos","ref","alt","hgvs","zygosity",
             "variant","effect","impact","consequence","clinvar","gnomad_af",
             "source","note","notes"]
headers = [h for h in preferred if h in headers] + [h for h in headers if h not in preferred]

# Group by gene
groups = defaultdict(list)
for row in rows:
    gene = colget(row,"gene") or "UNKNOWN"
    groups[gene.upper()].append(row)

def row_width_score(row):
    w = len(colget(row,"hgvs")) + len(colget(row,"note") or colget(row,"notes"))
    nonempty = sum(1 for h in headers if row.get(h,""))
    return w + 20*nonempty

gene_scores = {g: statistics.mean([row_width_score(r) for r in rs]) for g,rs in groups.items()}
landscape_genes = set(sorted(gene_scores, key=gene_scores.get, reverse=True)[:3])

def is_pathogenic(s):
    s = (s or "").lower()
    return ("pathogenic" in s and "not" not in s) or ("likely pathogenic" in s)

def is_high_impact(impact, consequence):
    imp = (impact or "").lower()
    if imp in {"high","moderate"}:
        return True
    cons = (consequence or "").lower()
    return any(key in cons for key in RELEVANT_CONSEQUENCES)

def is_rare_af(af):
    v = to_float(af)
    return v is not None and v < AF_CUTOFF

def highlight(row):
    return is_pathogenic(colget(row,"clinvar")) or \
           is_high_impact(colget(row,"impact"), colget(row,"consequence")) or \
           is_rare_af(colget(row,"gnomad_af") or colget(row,"gnomad"))

def style_cell(text, hl=False):
    return f"**⚠ {text}**" if hl else text

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT,"w",encoding="utf-8") as f:
    f.write("# Genetics Appendix (Full Variant Index)\n\n")
    f.write(f"> Source: `data/genetics/variant_index.csv`. Grouped by **GENE**. AF cutoff for highlight: < {AF_CUTOFF}.\n\n")
    f.write("_Auto-highlights_: **⚠** ClinVar Pathogenic/LP **or** impact HIGH/MODERATE **or** relevant consequence **or** gnomAD AF below cutoff.\n\n")
    f.write("---\n\n")
    f.write("<div style=\"font-size: 90%\">\n\n")

    for gene in sorted(groups.keys(), key=lambda s: (s=="UNKNOWN", s)):
        if gene in landscape_genes:
            f.write("\\begin{landscape}\n\n")
        f.write(f"## {gene}\n\n")
        f.write("| " + " | ".join(h.replace('|','/') for h in headers) + " |\n")
        f.write("|" + "|".join(["---"]*len(headers)) + "|\n")
        for row in groups[gene]:
            hl = highlight(row)
            vals=[]
            for h in headers:
                v = row.get(h,"")
                if h.lower() in ("hgvs","note","notes") and len(v) > 140:
                    short = v[:130].rstrip() + "…"
                    cell = f"{short}<br/><details><summary>more</summary>{v}</details>"
                else:
                    cell = v
                vals.append(style_cell(cell.replace('\n',' ').replace('|','/'), hl))
            f.write("| " + " | ".join(vals) + " |\n")
        f.write("\n")
        if gene in landscape_genes:
            f.write("\\end{landscape}\n\n")
        f.write("\\clearpage\n\n")
    f.write("</div>\n")
print(f"[csv_to_md_table] Wrote {OUT} (genes: {len(groups)})")
