#!/usr/bin/env bash
set -e
OUT="data/exports/case_study_summary_$(date +%Y%m%d).pdf"

inputs=()
for f in \
  docs/genetic_findings.md \
  docs/physician_brief.md \
  docs/case_study_outline.md
do
  [ -f "$f" ] && inputs+=("$f")
done
[ ${#inputs[@]} -eq 0 ] && { echo "No inputs for summary"; exit 1; }

engine=()
if command -v wkhtmltopdf >/dev/null 2>&1; then engine=(--pdf-engine=wkhtmltopdf)
elif command -v xelatex >/dev/null 2>&1; then engine=(--pdf-engine=xelatex); fi

pandoc "${inputs[@]}" \
  --from=markdown+table_captions+yaml_metadata_block \
  --metadata title="Case Study — Summary (with Genetics)" \
  -V geometry:margin=0.7in \
  "${engine[@]}" \
  -o "$OUT"

echo "Wrote $OUT"
ls -lh "$OUT"
