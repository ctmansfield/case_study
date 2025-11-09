export SHELL := /bin/bash

.PHONY: all export summary handout short validate
all: export summary

export:
	./tools/generate.sh pdf || true

summary:
	./tools/render_summary.sh || true

handout:
	./tools/render_handout.sh || true

short:
	./tools/render_handout.sh --short || true

validate:
	python3 tools/validate_tracking.py
