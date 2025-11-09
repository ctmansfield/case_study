#!/usr/bin/env python3
import csv, os, math

SRC = "data/genetics/variant_index.csv"
OUT = "data/analytics/genetics_top_hits.md"
DBG = "data/analytics/genetics_top_hits_debug.txt"

AF_CUTOFF = 0.005

ALIASES_MAP = {
  'clinvar': ['clinvar','clinvar_significance','clinvar_clinicalsignificance','clinical_significance'],
  'gnomad_af': ['gnomad_af','gnomad','gnomad_exomes_af','gnomad_genomes_af','af','max_af','popmax_af'],
  'consequence': ['consequence','consequence(s)','vep_consequence','so','so_terms'],
  'impact': ['impact','vep_impact','impact_level'],
  'cadd': ['cadd','cadd_phred','cadd_raw','cadd_phred_score'],
  'revel': ['revel','revel_score'],
  'sift': ['sift','sift_pred','sift_prediction'],
  'polyphen': ['polyphen','polyphen_pred','polyphen_prediction','polyphen2'],
  'spliceai': ['spliceai','splice_ai','spliceai_delta','spliceai_max'],
  'loftee': ['loftee','loftee_flag','lof']
}

RELEVANT_CONSEQUENCES = {
  "stop_gained","nonsense","frameshift",
  "splice_acceptor","splice_donor","splice_region",
  "missense","start_lost",
  "inframe_insertion","inframe_deletion","inframe_variant",
  "regulatory_region","promoter","5_prime_utr","3_prime_utr",
  "mature_mirna","tf_binding_site",
  "coding_sequence_variant","protein_altering_variant",
  "loss_of_function","gain_of_function"
}

def get(row, name):
  names=[name]+ALIASES_MAP.get(name.lower(),[])
  for n in names:
    for k in row.keys():
      if (k or "").lower()==n.lower():
        return (row[k] or '').strip()
  return ""

def to_float(s):
  try:
    if s is None: return None
    x=str(s).strip()
    if x in {"", ".", "NA", "na", "N/A", "n/a"}: return None
    x=x.replace(",","").rstrip("%")
    v=float(x)
    if str(s).strip().endswith("%"): v=v/100.0
    return v
  except:
    return None

def consequence_match(s):
  s=(s or "").lower()
  return any(key in s for key in RELEVANT_CONSEQUENCES)

def clinvar_hit(s):
  s=(s or "").lower()
  return ("pathogenic" in s and "not" not in s) or ("likely pathogenic" in s)

def impact_hit(s):
  s=(s or "").lower()
  return s in {"high","moderate"}

def af_hit(s):
  v = to_float(s)
  return v is not None and v < AF_CUTOFF

def predictor_hit(row):
  # any of these qualifies as supportive
  cadd = to_float(get(row,"cadd"))
  revel = to_float(get(row,"revel"))
  sift = (get(row,"sift") or "").lower()
  poly = (get(row,"polyphen") or "").lower()
  splice = to_float(get(row,"spliceai"))
  loftee = (get(row,"loftee") or "").lower()
  return (cadd is not None and cadd >= 20) \
      or (revel is not None and revel >= 0.5) \
      or ("deleterious" in sift) \
      or ("probably_damaging" in poly or "possibly_damaging" in poly) \
      or (splice is not None and splice >= 0.2) \
      or ("hc" in loftee or "high_confidence" in loftee)

def is_hit(row):
  return clinvar_hit(get(row,"clinvar")) \
      or impact_hit(get(row,"impact")) \
      or consequence_match(get(row,"consequence")) \
      or af_hit(get(row,"gnomad_af")) \
      or (predictor_hit(row) and af_hit(get(row,"gnomad_af")))

def score(row):
  s=0
  clin = get(row,"clinvar").lower()
  imp  = (get(row,"impact") or get(row,"consequence")).lower()
  af   = to_float(get(row,"gnomad_af"))
  if "pathogenic" in clin and "not" not in clin: s+=120
  if "likely pathogenic" in clin: s+=90
  if imp=="high": s+=70
  if imp=="moderate": s+=40
  if consequence_match(get(row,"consequence")): s+=25
  if af is not None:
    if af < 1e-4: s+=50
    elif af < 1e-3: s+=30
    elif af < 5e-3: s+=15
  if predictor_hit(row): s+=20
  return -s

def load_rows(path):
  if not os.path.exists(path): return []
  with open(path, newline='') as f:
    r = csv.DictReader(f)
    return [{(k or "").strip(): (v or "").strip() for k,v in row.items()} for row in r]

rows = load_rows(SRC)

# Debug counters
dbg = {
  "total": len(rows),
  "clinvar": 0,
  "impact": 0,
  "consequence": 0,
  "af": 0,
  "predictor_and_af": 0,
}
hits=[]
for row in rows:
  c = clinvar_hit(get(row,"clinvar"))
  i = impact_hit(get(row,"impact"))
  m = consequence_match(get(row,"consequence"))
  a = af_hit(get(row,"gnomad_af"))
  p = predictor_hit(row)
  if c: dbg["clinvar"]+=1
  if i: dbg["impact"]+=1
  if m: dbg["consequence"]+=1
  if a: dbg["af"]+=1
  if p and a: dbg["predictor_and_af"]+=1
  if c or i or m or a or (p and a):
    hits.append(row)

# If nothing matched, fallback to heuristic top-10 by score
if not hits:
  rows_sorted = sorted(rows, key=score)[:10]
  hits = rows_sorted

# Write Top Hits table
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT,"w",encoding="utf-8") as f:
  f.write(f"## Genetics — Top Hits (AF<{AF_CUTOFF} or functional evidence)\n\n")
  if not hits:
    f.write("_No variants available._\n")
  else:
    cols = ["gene","rsid","hgvs","impact","consequence","clinvar","gnomad_af","note"]
    f.write("| " + " | ".join(c.upper() for c in cols) + " |\n")
    f.write("|" + "|".join(["---"]*len(cols)) + "|\n")
    for r in hits[:10]:
      f.write("| " + " | ".join((r.get(c,"") or r.get(c.upper(),"")).replace("|","/") for c in cols) + " |\n")
  f.write("\nSee full appendix for details.\n")

# Write debug file
with open(DBG,"w") as d:
  for k in ["total","clinvar","impact","consequence","af","predictor_and_af"]:
    d.write(f"{k}: {dbg[k]}\n")
  d.write("\nColumns seen (union):\n")
  seen=set()
  for r in rows:
    seen.update([k for k in r.keys()])
  for k in sorted(seen):
    d.write(f"- {k}\n")

print(f"[top_hits] Wrote {OUT} with {min(len(hits),10)} rows; debug -> {DBG}")
