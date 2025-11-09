#!/usr/bin/env bash
# Usage: ./tools/generate.sh pdf [INPUT_MD]
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$DIR/.." && pwd)"
OUTDIR="$ROOT/data/exports"; mkdir -p "$OUTDIR"

# shellcheck source=tools/pandoc_common.sh
. "$ROOT/tools/pandoc_common.sh"

cmd="${1:-}"
input="${2:-docs/case_study_outline.md}"

if [ "$cmd" != "pdf" ]; then
  echo "Usage: $0 pdf [input.md]"; exit 1
fi

datecode="$(date +%Y%m%d)"
out="$OUTDIR/case_study_${datecode}.pdf"

pandoc "$input" \
  "${PANDOC_COMMON_OPTS[@]}" \
  -o "$out"

echo "Wrote $out"
