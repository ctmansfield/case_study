# Session Plan & Checklists
_Last updated: 2025-11-08_

We will progress through these sessions. Each session includes a checklist and explicit prompts to ensure nothing is missed.

---

## Session 1 — Skeleton & Metadata
**Objectives**
- Create/confirm repository structure.
- Fill `docs/case_study_outline.md` with all sections.
- Populate patient profile placeholders and confidentiality notes.

**Checklist**
- [ ] Confirm private repo and access limited to you (+optional clinician).
- [ ] Add baseline metadata (DOB as YYYY only if you prefer, sex, handedness, dominant language).
- [ ] Decide preferred output formats (PDF/DOCX).

**Prompts to answer**
- Demographics (as you are comfortable sharing): year of birth, height/weight ranges, occupation.
- High‑level summary of current problems (one paragraph).

**Deliverables**
- `docs/case_study_outline.md` fully scaffolded (headings + TODOs).
- Initial `meta/version_log.md` entry.

---

## Session 2 — Core Symptom Inventory
**Objectives**
- Build `docs/symptom_log.md` with clusters, onset, duration, severity, triggers, recovery.

**Checklist**
- [ ] List each symptom cluster (cognitive, motor/coordination, autonomic, metabolic, sleep, mood).
- [ ] For each: onset pattern, frequency, duration, peak severity, triggers, alleviating factors, after‑effects.
- [ ] Note stress‑event specifics already known (see pre‑filled items).

**Prompts to answer**
- “Walk me through a typical stress event from start to finish.”
- “Which early warning signs precede the event?”

**Deliverables**
- Completed table rows for each cluster.
- Add unknowns as `TBD` so they’re not forgotten.

---

## Session 3 — Chronology & Event Mapping
**Objectives**
- Fill `docs/timeline.md` with dated events (month‑level is OK).

**Checklist**
- [ ] Add first onset of each major symptom cluster.
- [ ] Add notable flares/remissions, hospital/clinic visits, tests, interventions.
- [ ] Note any biomarker spikes (e.g., fasting glucose) around events.

**Prompts to answer**
- “Earliest memory of problem X and what was happening around then?”
- “Which interventions clearly helped or worsened things?”

**Deliverables**
- Timeline table entries with links to supporting docs in `data/` if available.

---

## Session 4 — Medication & Adverse Reaction Log
**Objectives**
- Complete `docs/medication_history.md` with detailed reactions + context.

**Checklist**
- [ ] For each drug/class: dose, duration, indication, reaction details, severity, stop date, clinician response.
- [ ] Mark contraindications and tolerated agents.

**Prompts to answer**
- “What exact reaction did you experience, how soon after the dose, and how long did it last?”

**Deliverables**
- Comprehensive med table. Known items pre‑seeded (opioids incl. tramadol: very bad reactions; gabapentin: severe personality changes; antidepressants: uncontrollable, strange behavior).

---

## Session 5 — Systems Review (ROS) & Functional Impact
**Objectives**
- Populate `docs/system_review.md` by organ system.
- Document functional limitations and day‑impact.

**Checklist**
- [ ] Neuro, cardiovascular, endocrine/metabolic, psychiatric, GI, GU, musculoskeletal, sleep.
- [ ] For each: symptoms, suspected mechanisms, tests done/pending, clinician impressions.
- [ ] Functional: cognition, coordination, injury risk, irritability, non‑restorative sleep, anxiety.

**Prompts to answer**
- “Which activities are hardest now, and what makes them easier?”

**Deliverables**
- System‑by‑system bullets with TBDs clearly marked.

---

## Session 6 — Integration & Physician Brief
**Objectives**
- Draft `docs/physician_brief.md` (1–2 pages).

**Checklist**
- [ ] One‑paragraph history summary.
- [ ] Problem list (numbered).
- [ ] Key negative/positive findings.
- [ ] Medication cautions.
- [ ] Focused asks for next clinician visit.

**Deliverables**
- Polished brief for clinic use.

---

## Session 7 — Export & Final Review
**Objectives**
- Generate PDF/DOCX, review for accuracy/consistency.
- Tag release (`v0.1`, `v0.2`...).

**Checklist**
- [ ] Cross‑check dates, severity scales.
- [ ] Ensure terminology is consistent.
- [ ] Update `meta/version_log.md`.

**Deliverables**
- Exported files in `data/exports/`.
