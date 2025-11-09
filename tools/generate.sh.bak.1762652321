#!/usr/bin/env bash
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

have() { command -v "$1" >/dev/null 2>&1; }

if ! have pandoc; then
  echo "Pandoc not found. Install pandoc or export manually."
  exit 1
fi

if [ "$fmt" = "pdf" ]; then
  engine=""
  if have xelatex; then engine="--pdf-engine=xelatex"; 
  elif have pdflatex; then engine="--pdf-engine=pdflatex";
  elif have wkhtmltopdf; then engine="--pdf-engine=wkhtmltopdf";
  else
    echo "No LaTeX engine or wkhtmltopdf found; falling back to DOCX."
    fmt="docx"
    out="data/exports/case_study_$(date +%Y%m%d).${fmt}"
  fi
  pandoc "${inputs[@]}" $engine -o "$out" || exit $?
else
  pandoc "${inputs[@]}" -o "$out" || exit $?
fi

echo "Wrote $out"
