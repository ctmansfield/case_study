#!/usr/bin/env bash
# Minimal, reliable renderer for clinician handout.
# Inputs are added if present; no fragile awk edits.
set -e

SHORT=0
if [ "${1:-}" = "--short" ]; then SHORT=1; fi

OUT="data/exports/case_study_handout_$(date +%Y%m%d)"
[ "$SHORT" -eq 1 ] && OUT="${OUT}_short"
OUT="${OUT}.pdf"

# Collect inputs (order matters; add if file exists)
inputs=()

# Core handout sections you already maintain
for f in \
  docs/clinician_checklist.md \
  docs/physician_brief.md \
  data/analytics/correlations.md \
  docs/medication_effects.md
do
  [ -f "$f" ] && inputs+=("$f")
done

# Analytics summaries (new)
for f in \
  data/analytics/bp_hr_summary.md \
  data/analytics/glucose_summary.md \
  data/analytics/sleep_summary.md \
  data/analytics/med_response_summary.md
do
  [ -f "$f" ] && inputs+=("$f")
done

if [ ${#inputs[@]} -eq 0 ]; then
  echo "No inputs found for handout"; exit 1
fi

# Choose a PDF engine if available
engine=()
if command -v wkhtmltopdf >/dev/null 2>&1; then
  engine=(--pdf-engine=wkhtmltopdf)
elif command -v xelatex >/dev/null 2>&1; then
  engine=(--pdf-engine=xelatex)
fi

# Optional: tweak for short mode (e.g., fewer sections later if needed)

pandoc "${inputs[@]}" \
  --from=markdown+table_captions+yaml_metadata_block \
  --metadata title="Clinician Handout — Checklist • Brief • Analytics" \
  -V geometry:margin=0.7in \
  "${engine[@]}" \
  -o "$OUT"

echo "Wrote $OUT"
ls -lh "$OUT"
