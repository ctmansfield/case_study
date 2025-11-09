#!/usr/bin/env bash
out="data/exports/case_study_summary_$(date +%Y%m%d).pdf"

inputs=(
  docs/summary_cover.md
  docs/case_study_outline.md
  docs/physician_brief.md
  docs/symptom_log.md
  docs/mechanisms.md
  docs/mechanisms_neuroimmune.md
  docs/mechanistic_map.md
  docs/physio_tracking.md
  docs/lab_tracking.md
  data/analytics/correlations.md
)

existing=()
for f in "${inputs[@]}"; do [ -f "$f" ] && existing+=("$f"); done
[ ${#existing[@]} -eq 0 ] && { echo "No inputs found; aborting." >&2; exit 1; }

engine=()
if command -v wkhtmltopdf >/dev/null 2>&1; then
  engine=(--pdf-engine=wkhtmltopdf)
elif command -v xelatex >/dev/null 2>&1; then
  engine=(--pdf-engine=xelatex)
fi

pandoc "${existing[@]}" \
  --from=markdown+table_captions+yaml_metadata_block \
  --toc --toc-depth=3 \
  --metadata title="Case Study — Integrated Summary" \
  "${engine[@]}" \
  -o "$out" || exit $?

echo "Wrote $out"
ls -lh "$out"
