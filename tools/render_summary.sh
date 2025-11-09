#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$DIR/.." && pwd)"
OUTDIR="$ROOT/data/exports"; mkdir -p "$OUTDIR"

. "$ROOT/tools/pandoc_common.sh"

datecode="$(date +%Y%m%d)"
out="$OUTDIR/case_study_summary_${datecode}.pdf"

inputs=()
inputs+=(docs/genetics.md)
for f in \
  docs/case_study_outline.md \
  docs/physician_brief.md \
  docs/symptom_log.md \
  docs/mechanistic_map.md \
  docs/mechanisms.md \
  docs/mechanisms_neuroimmune.md \
  docs/allergies_intolerances.md \
  docs/lab_panels.md \
  docs/emergency_firstlook.md \
  data/analytics/correlations.md
do
  [ -f "$ROOT/$f" ] && inputs+=("$ROOT/$f")
done

# Render
pandoc "${inputs[@]}" \
  "${PANDOC_COMMON_OPTS[@]}" \
  --metadata title="Case Study — Integrated Summary" \
  -o "$out"

echo "Wrote $out"
