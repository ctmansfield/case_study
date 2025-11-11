#!/usr/bin/env bash
set -e
OUT="data/exports/case_study_handout_$(date +%Y%m%d)_short.pdf"

inputs=()
for f in \
  data/analytics/genetics_top_hits.md \
  docs/genetic_findings.md \
  docs/genetic_findings.md \
  docs/clinician_checklist.md \
  docs/physician_brief.md \
  data/analytics/correlations.md \
  docs/medication_effects.md
  data/analytics/med_response_summary.md \
  data/analytics/sleep_summary.md \
  data/analytics/glucose_summary.md \
  data/analytics/bp_hr_summary.md \
do
  [ -f "$f" ] && inputs+=("$f")
done
[ ${#inputs[@]} -eq 0 ] && { echo "No inputs for handout"; exit 1; }

engine=()
if command -v wkhtmltopdf >/dev/null 2>&1; then engine=(--pdf-engine=wkhtmltopdf)
elif command -v xelatex >/dev/null 2>&1; then engine=(--pdf-engine=xelatex); fi

pandoc "${inputs[@]}" \
  --from=markdown+table_captions+yaml_metadata_block \
  --metadata title="Clinician Handout — Genetics • Checklist • Brief" \
  -V geometry:margin=0.7in \
  "${engine[@]}" \
  -o "$OUT"

echo "Wrote $OUT"
ls -lh "$OUT"
