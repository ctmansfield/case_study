export SHELL := /bin/bash

DATE := $(shell date +%Y%m%d)
OUTDIR := data/exports
HANDOUT := $(OUTDIR)/case_study_handout_$(DATE).pdf
SHORT := $(OUTDIR)/case_study_handout_$(DATE)_short.pdf
SUMMARY := $(OUTDIR)/case_study_summary_$(DATE).pdf
MAIN := $(OUTDIR)/case_study_$(DATE).pdf
ZIP := $(OUTDIR)/case_study_sharepack_$(DATE).zip

.PHONY: all export summary handout short validate new-episode sharepack
all: export summary handout short validate

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

# Append a new episode template instance with datestamp
new-episode:
	@echo "### Episode note for $$(date '+%Y-%m-%d')" >> docs/symptom_log.md
	@echo "" >> docs/symptom_log.md
	@cat docs/episode_template.md >> docs/symptom_log.md
	@git add docs/symptom_log.md
	@git commit -m "log: add new episode template for $$(date '+%Y-%m-%d')" || true
	@GIT_SSH_COMMAND='ssh -i ~/.ssh/id_ed25519_chad -o IdentitiesOnly=yes -o IdentityAgent=none' git push || true
	@echo "→ Appended new episode template and pushed."

# Bundle ready-to-share package (handouts + summaries)
sharepack: export summary handout short
	@echo "Creating share pack..."
	@zip -j "$(ZIP)" "$(MAIN)" "$(SUMMARY)" "$(HANDOUT)" "$(SHORT)" >/dev/null 2>&1 || true
	@ls -lh "$(ZIP)" || true
	@echo "→ Sharepack ready: $(ZIP)"

# Build the main PDF (already supported by tools/generate.sh)
export:
	./tools/generate.sh pdf || true

# Build clinician summary (genetics included by your updated renderer)
summary:
	./tools/render_summary.sh || true

# Build handout (short variant included by flag)
handout:
	./tools/render_handout.sh || true

short:
	./tools/render_handout.sh --short || true

# Build full Genetics Appendix PDF from variant_index.csv
genetics_appendix:
	./tools/render_genetics_appendix.sh || true

appendix: genetics_appendix
