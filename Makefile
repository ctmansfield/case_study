.PHONY: export summary handout short genetics_appendix appendix sharepack all

# Main integrated export from outline
export:
	./tools/generate.sh pdf || true

# Clinician summary (genetics included by renderer)
summary:
	./tools/render_summary.sh || true

# Handout full + short
handout:
	./tools/render_handout.sh || true

short:
	./tools/render_handout.sh --short || true

# Genetics appendix (full variant index)
genetics_appendix:
	./tools/render_genetics_appendix.sh || true

appendix: genetics_appendix

# Pack PDFs for sharing
sharepack:
	./tools/make_sharepack.sh || { echo "sharepack script not found; skipping"; true; }

# Convenience
all: export summary handout short genetics_appendix
