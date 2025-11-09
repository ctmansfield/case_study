#!/usr/bin/env bash
# Simple generator for unified report using pandoc (if available).
# Usage: ./tools/generate.sh [pdf|docx]
fmt="${1:-pdf}"
out="data/exports/case_study_$(date +%Y%m%d).${fmt}"
inputs=(
  docs/case_study_outline.md
  docs/symptom_log.md
  docs/medication_history.md
  docs/system_review.md
  docs/timeline.md
  docs/physician_brief.md
)
if command -v pandoc >/dev/null 2>&1; then
  pandoc "${inputs[@]}" -o "$out"
  echo "Wrote $out"
else
  echo "Pandoc not found. Install pandoc or export manually."
fi
