#!/usr/bin/env python3
import csv, glob, os, re

IN_GLOB = "data/genetics/*.csv"
OUT = "data/genetics/variant_index.csv"

# Canonical column names we want to emit
CANON = [
  "gene","rsid","chrom","pos","ref","alt","hgvs","zygosity",
  "variant","effect","impact","consequence","clinvar","gnomad_af",
  "source","note"
]

# Aliases per canonical field (lowercase compare)
ALIASES = {
  "gene": ["gene","symbol","GENE","Gene"],
  "rsid": ["rsid","rsID","RSID","dbsnp","dbSNP","rs"],
  "chrom":["chrom","chr","Chromosome","CHROM"],
  "pos":  ["pos","position","POS","start","Start"],
  "ref":  ["ref","REF","reference","Ref"],
  "alt":  ["alt","ALT","alternate","Alt"],
  "hgvs": ["hgvs","HGVS","HGVS_c","HGVSc","HGVSp","Transcript_HGVS","Protein_HGVS"],
  "zygosity": ["zygosity","Zygosity","genotype","Genotype"],
  "variant": ["variant","allele","Allele","AltAllele"],
  "effect": ["effect","Effect","impact_effect","SO_term","vep_impact"],
  "impact": ["impact","Impact","IMPACT","vep_impact_level"],
  "consequence": [
    "consequence","Consequence","Consequence(s)","vep_consequence","so","SO_terms"
  ],
  "clinvar": [
    "clinvar","ClinVar","ClinVar_Significance","ClinVar_ClinicalSignificance",
    "clinical_significance","ClinicalSignificance"
  ],
  "gnomad_af": [
    "gnomad_af","gnomAD_AF","gnomad","gnomad_exomes_af","gnomad_genomes_af",
    "AF","af","max_af","popmax_af"
  ],
  "source": ["source","Source","panel","Panel","origin"],
  "note":   ["note","notes","Notes","comment","Comment","annotation"]
}

def normkey(k): return (k or "").strip().lower()

def pick(row, names):
  rowl = { normkey(k): v for k,v in row.items() }
  for n in names:
    for k in row.keys():
      if normkey(k)==normkey(n):
        return row[k].strip()
  return ""

def first_nonempty(*vals):
  for v in vals:
    if v and str(v).strip():
      return str(v).strip()
  return ""

def to_float(x):
  try:
    s = str(x).replace(",","")
    # support scientific notation or percent-like strings
    s = s.strip().rstrip("%")
    v = float(s)
    # if percent was provided, convert to fraction
    if str(x).strip().endswith("%"):
      v = v/100.0
    return v
  except:
    return None

files = sorted(glob.glob(IN_GLOB))
rows_out=[]

for path in files:
  if os.path.basename(path).startswith("variant_index"):  # skip prior outputs
    continue
  with open(path, newline='') as f:
    r = csv.DictReader(f)
    for row in r:
      out={}
      for canon in CANON:
        aliases = ALIASES.get(canon,[canon])
        out[canon] = pick(row, aliases)
      # try to fill HGVS if missing from other fields
      if not out["hgvs"]:
        out["hgvs"] = first_nonempty(row.get("HGVSc"), row.get("HGVSp"), row.get("HGVS"))
      # standardize AF to decimal fraction if possible
      af = to_float(out["gnomad_af"])
      if af is not None:
        out["gnomad_af"] = f"{af:.6g}"
      # annotate source with filename if empty
      if not out["source"]:
        out["source"] = os.path.basename(path)
      rows_out.append(out)

# Write merged index (dedupe simple exact duplicates)
seen=set()
dedup=[]
for r in rows_out:
  key = tuple((r.get(k,"") for k in CANON))
  if key in seen: continue
  seen.add(key); dedup.append(r)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT,"w",newline='',encoding="utf-8") as f:
  w = csv.DictWriter(f, fieldnames=CANON)
  w.writeheader()
  for r in dedup:
    w.writerow(r)

print(f"[merge_variants] Wrote {OUT} with {len(dedup)} rows from {len(files)} files.")
