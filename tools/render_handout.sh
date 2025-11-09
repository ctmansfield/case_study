#!/usr/bin/env bash
set -e

SHORT=0
if [ "${1:-}" = "--short" ]; then SHORT=1; fi

OUT="data/exports/case_study_handout_$(date +%Y%m%d)${SHORT:+_short}.pdf"

# Build input list (skip missing)
inputs=()
for f in \
  docs/clinician_checklist.md \
  docs/physician_brief.md \
  data/analytics/correlations.md \
  docs/medication_effects.md
do
  [ -f "$f" ] && inputs+=("$f")
done
[ ${#inputs[@]} -eq 0 ] && { echo "No inputs found for handout"; exit 1; }

# If short mode, create a trimmed analytics file (top ~30 lines)
TMP_CORR=""
if [ $SHORT -eq 1 ] && [ -f "data/analytics/correlations.md" ]; then
  TMP_CORR=$(mktemp)
  # keep title + header + ~25 rows max
  awk 'NR<=30{print}' data/analytics/correlations.md > "$TMP_CORR"
  # rebuild inputs replacing the full correlations with trimmed one
  new_inputs=()
  for f in "${inputs[@]}"; do
    if [ "$f" = "data/analytics/correlations.md" ]; then
      new_inputs+=("$TMP_CORR")
    else
      new_inputs+=("$f")
    fi
  done
  inputs=("${new_inputs[@]}")
fi

engine=() css=()
if command -v wkhtmltopdf >/dev/null 2>&1; then
  engine=(--pdf-engine=wkhtmltopdf)
  [ -f tools/handout.css ] && css=(-c tools/handout.css)
elif command -v xelatex >/dev/null 2>&1; then
  engine=(--pdf-engine=xelatex -V fontsize=10pt)
fi

# Slightly tighter margins for short mode
geom="-V geometry:margin=0.7in"
[ $SHORT -eq 1 ] && geom="-V geometry:margin=0.5in"

pandoc "${inputs[@]}" \
  --from=markdown+table_captions+yaml_metadata_block \
  --metadata title="Clinician Handout — Checklist • Brief • Analytics" \
  $geom \
  "${engine[@]}" \
  "${css[@]}" \
  -o "$OUT"

[ -n "$TMP_CORR" ] && rm -f "$TMP_CORR"
echo "Wrote $OUT"
ls -lh "$OUT"
