# Medical Case Study (Private Repo)

This repository holds a living, clinician‑facing case study with full history, timeline, and supporting materials.
It is designed for incremental work across multiple sessions with your assistant.

## Layout
```
medical_case_study/
├── README.md
├── docs/
│   ├── case_study_outline.md
│   ├── symptom_log.md
│   ├── medication_history.md
│   ├── system_review.md
│   ├── timeline.md
│   └── physician_brief.md
├── data/
│   ├── lab_results/
│   ├── notes_raw/
│   └── exports/
└── meta/
    ├── version_log.md
    └── session_plan.md
```
## Working model

- We update a specific file per session (see `meta/session_plan.md`).
- Commit with clear messages (e.g., `feat(symptoms): add stress‑event cluster details`).
- Use `meta/version_log.md` to record a human‑readable changelog for clinicians.

## Build (optional)

If you have Pandoc installed, you can generate a unified PDF/Docx from Markdown:

```bash
./tools/generate.sh pdf   # or: docx
```

If you prefer GitHub to build automatically, enable the included workflow in `.github/workflows/export.yml`.

### Handout (concise printout)
- Normal: `./tools/render_handout.sh` → `data/exports/case_study_handout_YYYYMMDD.pdf`  
- **Short (1–2 pages):** `./tools/render_handout.sh --short` → `..._short.pdf`  
  Includes **Checklist + Physician Brief + trimmed Analytics** with compact layout.

### Changelog
- Auto-generated from session changes: [`CHANGELOG.md`](CHANGELOG.md)

- Genetics (clinician): `docs/genetic_findings.md`
- Genetics (plain language): `docs/genetics_lay.md`
