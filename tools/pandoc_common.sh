#!/usr/bin/env bash
# Common options for all our Pandoc renders so tables don't truncate.
set -euo pipefail

# Choose engine: prefer wkhtmltopdf if present; else xelatex
PANDOC_ENGINE_OPTS=()
CSS_OPTS=()
LATEX_OPTS=()
if command -v wkhtmltopdf >/dev/null 2>&1; then
  PANDOC_ENGINE_OPTS=(--pdf-engine=wkhtmltopdf)
  [ -f tools/print.css ] && CSS_OPTS=(-c tools/print.css)
else
  # xelatex path with longtable and compact typesetting
  PANDOC_ENGINE_OPTS=(--pdf-engine=xelatex -V fontsize=10pt)
  LATEX_OPTS=(--include-in-header=docs/_includes/latex_tables.tex)
fi

# Common geometry; can be tightened by caller for short handouts
GEOM="-V geometry:margin=0.7in"

# Extensions: longtables + pipe tables + YAML metadata
FORMAT="markdown+pipe_tables+grid_tables+table_captions+yaml_metadata_block"

# Build a reusable array
PANDOC_COMMON_OPTS=(--from="$FORMAT" $GEOM "${PANDOC_ENGINE_OPTS[@]}" "${CSS_OPTS[@]}" "${LATEX_OPTS[@]}")
export PANDOC_COMMON_OPTS
