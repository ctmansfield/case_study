#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$DIR/.." && pwd)"
OUTDIR="$ROOT/data/exports"; mkdir -p "$OUTDIR"

. "$ROOT/tools/pandoc_common.sh"

SHORT=0
if [ "${1:-}" = "--short" ]; then SHORT=1; fi

datecode="$(date +%Y%m%d)"
out="$OUTDIR/case_study_handout_${datecode}${SHORT:+_short}.pdf"

inputs=()
for f in \
  docs/clinician_checklist.md \
  docs/genetics.md \
  docs/physician_brief.md docs/genetics_lay.md \
  data/analytics/correlations.md \
  docs/medication_effects.md
do
  [ -f "$ROOT/$f" ] && inputs+=("$ROOT/$f")
done
[ ${#inputs[@]} -eq 0 ] && { echo "No inputs found for handout"; exit 1; }

# Short mode: trim analytics so it fits
TMP=""
if [ $SHORT -eq 1 ] && [ -f "$ROOT/data/analytics/correlations.md" ]; then
  TMP="$(mktemp)"; awk 'NR<=30{print}' "$ROOT/data/analytics/correlations.md" > "$TMP"
  new=()
  for f in "${inputs[@]}"; do
    if [ "$f" = "$ROOT/data/analytics/correlations.md" ]; then new+=("$TMP"); else new+=("$f"); fi
  done
  inputs=("${new[@]}")
fi

# Tighten margins a bit more for short
if [ $SHORT -eq 1 ]; then
  export PANDOC_COMMON_OPTS=("${PANDOC_COMMON_OPTS[@]/geometry:margin=0.7in/geometry:margin=0.5in}")
fi

pandoc "${inputs[@]}" \
  "${PANDOC_COMMON_OPTS[@]}" \
  --metadata title="Clinician Handout — Checklist • Brief • Analytics" \
  -o "$out"

[ -n "$TMP" ] && rm -f "$TMP"
echo "Wrote $out"
