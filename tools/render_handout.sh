#!/usr/bin/env bash
set -e

OUT="data/exports/case_study_handout_$(date +%Y%m%d).pdf"

# choose inputs (skip if missing)
inputs=()
for f in \
  docs/clinician_checklist.md \
  docs/physician_brief.md \
  data/analytics/correlations.md \
  docs/medication_effects.md
do
  [ -f "$f" ] && inputs+=("$f")
done

if [ ${#inputs[@]} -eq 0 ]; then
  echo "No inputs found for handout"; exit 1
fi

engine=()
if command -v wkhtmltopdf >/dev/null 2>&1; then
  engine=(--pdf-engine=wkhtmltopdf)
elif command -v xelatex >/dev/null 2>&1; then
  engine=(--pdf-engine=xelatex)
fi

pandoc "${inputs[@]}" \
  --from=markdown+table_captions+yaml_metadata_block \
  --metadata title="Clinician Handout — Checklist • Brief • Analytics" \
  --toc=false \
  -V geometry:margin=0.7in \
  "${engine[@]}" \
  -o "$OUT"

echo "Wrote $OUT"
ls -lh "$OUT"
