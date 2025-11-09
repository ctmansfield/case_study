#!/usr/bin/env bash
# Keep fail-soft behavior per your preference

OUT="data/exports/case_study_genetics_appendix_$(date +%Y%m%d).pdf"
mkdir -p data/analytics data/exports

# regenerate appendix MD + top-hits
python3 tools/genetics_top_hits.py || true
python3 tools/csv_to_md_table.py data/genetics/variant_index.csv || true

INPUT="data/analytics/genetics_appendix.md"
[ -f "$INPUT" ] || { echo "Appendix markdown not found: $INPUT"; exit 0; }

engine=()
title="Case Study — Genetics Appendix (Full Variant Index)"
if command -v xelatex >/dev/null 2>&1; then
  engine=(--pdf-engine=xelatex -V geometry:margin=0.6in -V papersize:a4)
elif command -v wkhtmltopdf >/dev/null 2>&1; then
  engine=(--pdf-engine=wkhtmltopdf -V geometry:margin=0.6in)
fi

pandoc "$INPUT" \
  --from=markdown+table_captions+yaml_metadata_block+raw_tex \
  -V linkcolor:black \
  --metadata title="$title" \
  "${engine[@]}" \
  -o "$OUT"

echo "Wrote $OUT"
ls -lh "$OUT" 2>/dev/null || true
