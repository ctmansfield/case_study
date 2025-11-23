# Physician Brief (De-identified Case Summary)

> **Purpose:** Concise, clinician-facing overview of a complex stress-linked neuroimmune / autonomic / metabolic phenotype with MCAS-like features, endocrine clearance issues, and marked medication sensitivities. All names and dates are de-identified.

---

## 1. Patient Context

- Adult, assigned male at birth; formal diagnosis of **Autism Spectrum Disorder (ASD)**.
- Right-hand dominant; STEM / systems-engineering background; high health-literacy and data tracking.
- Key chronic issues:
  - Recurrent **stress-linked episodes** with multi-system involvement.
  - **Marked medication intolerance**, particularly to serotonergic and CNS-active agents.
  - **Endocrine / metabolic lability** (glucose, BP, sleep).
  - **MCAS-like symptom pattern** with histamine and folate sensitivity.

---

## 2. Core Phenotype (High-Level Summary)

The patient experiences **recurrent episodes** (autonomic / histamine flares) characterized by:

- **Neurocognitive:** acute degradation of working memory and executive function, slowed processing, word-finding difficulty, and post-episode amnesia for portions of the event.
- **Autonomic / cardiovascular:** paroxysmal **BP elevation**, tachycardia, presyncope, loss of coordination, falls, and a subjective sense of “runaway” adrenaline with impaired top-down control.
- **Metabolic:** stress-linked hyperglycemia; **headache if fasting glucose < ~110 mg/dL**; non-restorative sleep preceding episodes.
- **Neuroimmune / MCAS-like:** migraine, photophobia, edema (e.g., post-operative foot swelling), sensory hypersensitivity, and reproducible flares with **high-histamine foods** or **excess folate**.
- **Affective / behavioral:** agitation, irritability, emotional lability, and “out-of-character” behavior during peaks, with insight and remorse returning after recovery.

Episodes are reliably **stress-triggered** (psychological or physiological) and often **amplified by histamine load and sleep deficit**. Recovery can take days to weeks, with incomplete cognitive restitution after severe flares.

---

## 3. Episodic Pattern & Objective Tracking

**Pattern (self-reported and supported by logs):**

1. **Prodrome:** poor sleep, mounting stress, rising BG and BP, escalating agitation/sensory gain.
2. **Peak:** adrenergic “storm” (subjective loss of steering), cognitive disorganization, injury risk, and multi-system symptoms (neuro, autonomic, metabolic, MCAS-like).
3. **Recovery:** prolonged fatigue, cognitive “crash,” sleep dysregulation, and worsened baseline functioning for days–weeks.

**Objective data available in repo (CSV + Markdown summaries):**

- `data/tracking/bp_hr.csv` → BP/HR episodes, triggers, and response to interventions.  
  - Summary: `data/analytics/bp_hr_summary.md`.
- `data/tracking/glucose.csv` → fasting / post-prandial glucose vs histamine/folate load, stress markers, and sleep deficit.  
  - Summary: `data/analytics/glucose_summary.md`.
- `data/tracking/sleep.csv` → sleep duration/fragmentation vs next-day BP/BG and symptom severity.  
  - Summary: `data/analytics/sleep_summary.md`.
- `data/tracking/med_response.csv` → structured time-stamped medication trials and side-effects.  
  - Summary: `data/analytics/med_response_summary.md`.

> The **clinician handout PDF** (generated from the repo) includes the brief, checklist, and analytic summaries in 2 pages.

---

## 4. Neuroimmune / MCAS Axis

Features strongly suggest a **mast-cell / histamine-amplified** physiology:

- **Triggers:**
  - High-histamine foods → reproducible replication of full flare profile.
  - **Excess folate** → similar cascades.
  - Psychological / physiologic stress → similar but often stronger episodes.
- **Symptom clusters during flares:**
  - Migraine, photophobia, sensory hyperacusis.
  - Peripheral edema (e.g., surgical foot).
  - Insomnia / fragmented sleep with nocturnal hyperarousal.
  - Cognitive fog and fatigue the following day.
- **Responses:**
  - **Hydroxyzine (H1)** → improved sleep continuity, reduced sensory gain.
  - **Famotidine (H2)** → fewer nocturnal awakenings, smoother BP/HR.
  - **DAO enzyme** → decreased food-triggered flares when taken with high-histamine meals.

Relevant documents:

- `docs/mechanisms.md` — histamine, MCAS axis, and folate interaction.  
- `docs/mechanisms_neuroimmune.md` — stress–mast-cell–adrenergic–metabolic loop.  
- `docs/mitochondrial_findings.md` — lab-based mitochondrial/PLP context.

---

## 5. Endocrine / Genetics / Neurodevelopmental Context

### 5.1 Estrogen Metabolism & Clearance

Genetic findings (see **Genetics Appendix PDF** + `docs/genotype_phenotype_map.md`):

- **COMT rs4680 (Val158Met)** → reduced catechol methylation; slower clearance of catecholamines and catechol estrogens.
- **CYP3A4*22** + **CYP3A5*3** → decreased hepatic estradiol clearance.
- **UGT1A1*28 tag** → reduced glucuronidation, impacting estrogen metabolites and bilirubin.
- **SULT1E1 / SULT2A1 variants** → altered sulfation of estrogens and DHEA.
- **SHBG-increasing alleles** → higher SHBG, lower free T/E2, with sensitivity to relatively small changes.

Clinical correlation:

- Clear symptomatic sensitivity when estradiol rises above the patient’s narrow tolerated band.  
- Requires **careful anastrozole titration** to maintain a physiologic T:E2 ratio with stable mood and metabolic profile.

### 5.2 ASD and Autonomic / Stress Physiology

Formal **ASD diagnosis** is relevant because:

- Autistic adults commonly show **elevated baseline sympathetic tone** and reduced vagal flexibility.
- Interoceptive processing differences can **amplify physiologic stress responses** without implying a primary psychiatric etiology.
- Medication sensitivities and paradoxical CNS responses are more common in ASD and match this patient’s history.

The ASD context helps explain:

- The “runaway adrenaline with no steering” episodes (autonomic inertia).  
- The combination of high catecholamine reactivity with **COMT Met** and impaired estrogen clearance.
- A tight coupling between social/psychological stressors, neuroimmune activation, and metabolic derangement.

---

## 6. Mitochondrial / Nutrient Findings

Prior labs (see `docs/mitochondrial_findings.md`) have shown:

- **“Alcoholic pattern” AST/ALT profile** despite minimal/no alcohol use, interpreted as suggesting **mitochondrial stress** rather than primary alcoholic injury.
- Evidence of **functional vitamin B6 (PLP) insufficiency** on at least one set of labs.

Interpretation:

- Under adrenergic and histamine load, mitochondrial bottlenecks may force increased glycolytic reliance and lower fatigue threshold.
- PLP-dependent neurotransmitter and amino-acid pathways may be more vulnerable during stress, contributing to the cognitive/mood instability observed.

---

## 7. Medication Response Pattern (Abbreviated)

See `docs/medication_effects.md` and `docs/mechanistic_map.md` for full tables.

### 7.1 Helpful / Beneficial Agents (non-exhaustive)

- **Clonidine** (central α2 agonist): reliably attenuates adrenergic surges, stabilizes BP, and reduces hyperarousal.
- **Hydroxyzine / Famotidine / DAO**: improve sleep continuity and reduce histamine-triggered flares.
- **Testosterone + Anastrozole**: when carefully titrated, support mood, energy, and glucose handling within a narrow E2 window.
- **Creatine, methylated B-complex, SAMe (cautious use), probiotics, HMB**: support energy and methylation balance; creatine helps reduce methylation burden, which may improve histamine handling.
- **CBN/CBD/THC (low-dose, targeted)**: used selectively for sleep and pain without the destabilization seen with serotonergic agents.

### 7.2 Adverse / Poorly Tolerated Agents

Markedly abnormal reactions to:

- **SSRIs/SNRIs and related:** escitalopram, fluoxetine, venlafaxine, duloxetine, bupropion — behavioral disinhibition, severe agitation, or non-baseline behavior.
- **Mood stabilizers / anticonvulsants:** lithium, valproate, lamotrigine, gabapentin — cognitive blunting, personality change, or paradoxical mood effects.
- **Cardiovascular meds:** lisinopril, metoprolol, amlodipine, spironolactone — poor tolerability or paradoxical symptom exacerbation.
- **Opioids (including tramadol):** very bad reactions; avoided.

These patterns support a **non-psychiatric primary etiology** with extreme pharmacodynamic sensitivity rather than a straightforward mood-/anxiety-disorder framework.

---

## 8. What the Patient is Asking You To Help With

1. **Diagnostic clarification** along the following axes (without forcing a single label):
   - MCAS / histamine-driven mast-cell activation.
   - Autonomic dysregulation / adrenergic hyperresponsiveness.
   - Endocrine clearance / estrogen-handling phenotype.
   - Stress-linked metabolic dysregulation and mitochondrial stress.
   - How ASD and genotype interact with the above.

2. **Review of existing objective data** (BP/HR, glucose, sleep, medication response, and genetics) to determine:
   - Whether the pattern is sufficiently coherent and reproducible for a **formal case study**, and
   - Which additional tests (imaging, autonomic testing, MCAS workup, endocrine labs) would best strengthen diagnostic confidence.

3. **Collaborative treatment planning**:
   - Safe optimization of clonidine, histamine axis (H1/H2/DAO), endocrine regimen, and metabolic supports.
   - Guardrails for any future pharmacologic trials given the history of severe adverse responses.

For navigation, the repo includes:

- `docs/diagnostic_alignment.md` — criteria-aligned summary (MCAS, autonomic, endocrine, metabolic, ASD).  
- `data/exports/` — full **case study**, **summary**, **clinician handout**, and **genetics appendix** PDFs.  
- `docs/genotype_phenotype_map.md` — gene → pathway → phenotype mapping.  
- `docs/mitochondrial_findings.md` — mitochondrial/B6 interpretation.

**Mitochondrial phenotype:**  
Lifelong exertional intolerance, asymmetric limb involvement, “alcoholic-pattern” liver enzymes without alcohol, and treadmill findings suggest a **mitochondrial / metabolic myopathy** with hepatic involvement.  
See `docs/mitochondrial_findings.md` and `case_study/mitochondrial_evidence.md` for integrated summary.
