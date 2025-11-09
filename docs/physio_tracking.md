
> **Goal:** provide structured, clinician-reviewable capture of vital and biochemical correlates observed during and between episodes.

---

## A. Vital Signs Snapshot

| Date | Time | Context | SBP/DBP (mmHg) | HR (bpm) | Temp (°C) | Notes |
|------|------|----------|----------------|----------|------------|-------|
| **TBD** | | Baseline AM | | | | |
| **TBD** | | During flare | | | | |
| **TBD** | | Post-episode | | | | |

---

## B. Metabolic Metrics

| Date | Fasting Glucose (mg/dL) | Post-meal (1 h) | Post-meal (2 h) | HbA1c (%) | Context/Trigger | Notes |
|------|--------------------------|------------------|------------------|------------|----------------|-------|
| **TBD** | | | | | | |

---

## C. Sleep & Recovery

| Date | Bedtime | Wake | Total hrs | Sleep Quality (0–10) | Fragmentation (%) | Dream Recall | Comments |
|------|----------|------|-----------|----------------------|-------------------|--------------|-----------|
| **TBD** | | | | | | | |

---

## D. Food / MCAS Log

| Date | Meal Components | Histamine Load (1–5) | Folate Intake (high/mod/low) | Reaction Latency (hr) | Symptom Severity (0–10) | DAO/H1/H2 Timing | Notes |
|------|-----------------|-----------------------|-------------------------------|------------------------|--------------------------|------------------|-------|
| **TBD** | | | | | | | |

---

### Summary Fields
- Correlation score between histamine/folate intake and flare severity → **TBD**  
- Baseline vs flare ΔBP / ΔHR / ΔBG → **TBD**  
- Avg sleep deficit preceding flare → **TBD**

---

*Cross-refs:*  
↳ `docs/mechanisms.md` (MCAS axis)  
↳ `docs/symptom_log.md` (episode clusters)

### Quick Analysis
- Append daily rows to **`data/tracking/physio.csv`** with columns:
  - `date,context,histamine_score(1–5),folate_level(0=low,1=mod,2=high),sbp,dbp,hr,fasting_glucose,sleep_deficit_hours,notes`
- Run: `python3 tools/track_corr.py`  
- See results: **`data/analytics/correlations.md`** (Pearson r for key pairs).
