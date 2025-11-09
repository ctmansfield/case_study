#!/usr/bin/env bash
out="data/exports/case_study_summary_$(date +%Y%m%d).pdf"

# assemble in this order; missing files are skipped gracefully
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
for f in "${inputs[@]}"; do
  [ -f "$f" ] && existing+=("$f")
done

if [ ${#existing[@]} -eq 0 ]; then
  echo "No inputs found; aborting." >&2
  exit 1
fi

# prefer wkhtmltopdf via pandoc if available; otherwise let pandoc choose
pandoc "${existing[@]}" \
  --from=markdown+table_captions+yaml_metadata_block \
  --toc --toc-depth=3 \
  --metadata title="Case Study — Integrated Summary" \
  -o "$out" || exit $?

echo "Wrote $out"
ls -lh "$out"
