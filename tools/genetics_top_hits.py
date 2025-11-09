#!/usr/bin/env python3
import csv, os

SRC = "data/genetics/variant_index.csv"
OUT = "data/analytics/genetics_top_hits.md"

AF_CUTOFF = 0.005
ALIASES_MAP = {
  'clinvar': ['clinvar','clinvar_significance','clinvar_clinicalsignificance','clinical_significance'],
  'gnomad_af': ['gnomad_af','gnomad','gnomad_exomes_af','gnomad_genomes_af','af','max_af','popmax_af'],
  'consequence': ['consequence','consequence(s)','vep_consequence','so','so_terms'],
  'impact': ['impact','vep_impact','impact_level']
}
  # <- adjusted per user
RELEVANT_CONSEQUENCES = {
    "stop_gained","nonsense","frameshift","splice_acceptor","splice_donor","splice_region",
    "missense","start_lost","inframe_insertion","inframe_deletion","inframe_variant",
    "regulatory_region","promoter","5_prime_utr","3_prime_utr","mature_miRNA","TF_binding_site",
    "coding_sequence_variant","protein_altering_variant"
}

def get(row, name):
    names=[name]+ALIASES_MAP.get(name.lower(),[])
    for n in names:
        for k in row.keys():
            if k.lower()==n.lower():
                return (row[k] or '').strip()
    return ''

    for k in row.keys():
        if k.lower()==name.lower():
            return row[k].strip()
    return ""

def to_float(s):
    try:
        if s is None: return None
        x = str(s).replace(',','').strip().rstrip('%')
        v = float(x)
        if str(s).strip().endswith('%'):
            v = v/100.0
        return v
    except:
        return None

    try: return float(s)
    except: return None

def consequence_match(s):
    s = (s or "").lower()
    return any(key in s for key in RELEVANT_CONSEQUENCES)

def is_hit(r):
    clin = get(r,"clinvar").lower()
    imp  = (get(r,"impact") or get(r,"consequence")).lower()
    cons = get(r,"consequence")
    af   = to_float(get(r,"gnomad_af") or get(r,"gnomad"))
    return ("pathogenic" in clin and "not" not in clin) or ("likely pathogenic" in clin) \
           or imp in {"high","moderate"} \
           or consequence_match(cons) \
           or (af is not None and af < AF_CUTOFF)

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
        elif af < 5e-3: s+=15  # cutoff now 0.005
    if consequence_match(get(r,"consequence")): s+=20
    return -s

os.makedirs(os.path.dirname(OUT), exist_ok=True)
if not os.path.exists(SRC):
    with open(OUT,"w") as f:
        f.write("## Genetics — Top Hits\n\n_No variant index found._\n")
    print(f"[top_hits] No source CSV; wrote stub {OUT}")
    raise SystemExit(0)

rows=[]
with open(SRC, newline='') as f:
    r = csv.DictReader(f)
    for row in r:
        row = { (k or "").strip(): (v or "").strip() for k,v in row.items() }
        if is_hit(row):
            rows.append(row)

rows = sorted(rows, key=score)[:10]

with open(OUT,"w",encoding="utf-8") as f:
    f.write(f"## Genetics — Top Hits (AF<{AF_CUTOFF}, P/LP, HIGH/MOD, or relevant consequence)\n\n")
    if not rows:
        f.write("_No variants met criteria._\n")
    else:
        cols = ["gene","rsid","hgvs","impact","consequence","clinvar","gnomad_af","note"]
        f.write("| " + " | ".join(c.upper() for c in cols) + " |\n")
        f.write("|" + "|".join(["---"]*len(cols)) + "|\n")
        for r in rows:
            f.write("| " + " | ".join((r.get(c,"") or r.get(c.upper(),"")).replace("|","/") for c in cols) + " |\n")
    f.write("\nSee full appendix for details.\n")
print(f"[top_hits] Wrote {OUT} with {len(rows)} rows")
