#!/usr/bin/env bash

REPO=/mnt/nas_storage/repos/case_study
cd "$REPO" || { echo "repo not found"; exit 1; }

IN_MD="data/analytics/genetics_appendix.md"
OUT="data/exports/case_study_genetics_appendix_$(date +%Y%m%d).pdf"

mkdir -p "$(dirname "$OUT")"

if [ ! -f "$IN_MD" ]; then
  echo "Genetics appendix source not found: $IN_MD"
  exit 0
fi

engine=()
if command -v xelatex >/dev/null 2>&1; then
  engine=(--pdf-engine=xelatex)
elif command -v wkhtmltopdf >/dev/null 2>&1; then
  engine=(--pdf-engine=wkhtmltopdf)
fi

pandoc "$IN_MD" \
  --from=markdown+table_captions+yaml_metadata_block \
  --metadata title="Genetics Appendix — Variant Inventory & Interpretation" \
  -V geometry:margin=0.7in \
  -H docs/latex_header_genetics.tex \
  "${engine[@]}" \
  -o "$OUT" || echo "[warn] pandoc reported an error while building genetics appendix"

echo "Wrote $OUT"
ls -lh "$OUT" 2>/dev/null || true
