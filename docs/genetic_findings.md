# Genetic Findings — Estrogen Handling, Methylation, and Neuro-Adrenergic Context

> **Purpose:** Document genotype patterns that plausibly influence estrogen metabolism/clearance, catechol & histamine handling, and stress responses.  
> **Scope:** This is clinical context, not a diagnosis. Use alongside labs and phenotype.

---

## A. Curated, Clinically Salient Variants (with plain-language effect)

> These are the high-impact alleles you asked to prioritize. Full exhaustive list is in **`data/genetics/variant_index.csv`**.

### Estrogen metabolism & clearance

| Gene | Variant | Typical functional effect (literature) | Expected clinical direction (context here) | Notes/Refs |
|---|---|---|---|---|
| **COMT** | rs4680 (Val158Met; Met allele) | ↓ COMT activity → slower methylation of catechol estrogens & catecholamines | ↑ catechol “noise” under stress; can worsen anxiety/hyperarousal; raises methylation demand | See refs/estrogen_genetics.md |
| **CYP1A2** | rs762551 (*1F context) | Alters inducibility/clearance (caffeine/aryl amines) | Phenoconversion-sensitive; if low inducibility → slower 2-hydroxylation backup | refs/estrogen_genetics.md |
| **CYP3A4** | *22 (rs35599367) | ↓ hepatic 3A4 expression | Slower E2 clearance; higher exposure at given aromatization rate | refs/estrogen_genetics.md |
| **CYP3A5** | *3 (rs776746) non-expressor | Loss of 3A5; burden shifts to 3A4 | Accentuates *22 impact (net slower 3A throughput) | refs/estrogen_genetics.md |
| **UGT1A1** | rs887829 (tags *28 TA7) | ↓ glucuronidation capacity | Slower E2 metabolite clearance; ↑ unconjugated bilirubin tendency (Gilbert-like) | refs/estrogen_genetics.md |
| **SULT1E1** | rs3736599 (promoter) | Reported ↓ expression in some cohorts | Prolongs active E2 half-life when sulfation lower | refs/estrogen_genetics.md |
| **SULT2A1** | rs2637125 | Alters DHEA sulfation | Tracks with low DHEAS labs; affects adrenal balance | refs/estrogen_genetics.md |
| **SHBG** | rs1799941 / rs12150660 / rs6259 | Common alleles shift SHBG | Higher SHBG → lower free T/E2 (total may look higher) | refs/estrogen_genetics.md |

**Integrated read:** Slower **Phase II** (COMT-Met, UGT1A1*28, SULT1E1 var) plus reduced **CYP3A** throughput (*3A4*22 with *3A5*3*) ⇒ favors higher circulating E2 and catechol persistence; requires careful anastrozole titration and monitoring of free fractions (with SHBG context).

### Methylation, monoamines & histamine

| Pathway | Gene/Variant | Effect | Clinical direction | Notes/Refs |
|---|---|---|---|---|
| Catechol/Histamine methylation | **COMT** rs4680 Met | ↓ methylation rate | ↑ adrenergic tone under stress; interacts with histamine load | refs/methylation_histamine.md |
| Histamine inactivation | **HNMT** (if present in index) | (populate from index if present) | Alignment with histamine intolerance/MCAS phenotype | refs/methylation_histamine.md |

> We will auto-pull any HNMT or related alleles from the full index (below).

---

## B. Exhaustive Variant Index (from uploaded scans)

All parsed variants (deduplicated) are consolidated here: **`data/genetics/variant_index.csv`**.  
If you want, we can render it into a paginated appendix PDF later.

---

## C. Clinical Hooks (how it changes management)

- Keep **free E2** in lower-physiologic range; titrate **anastrozole** cautiously.  
- Support **methylation** (methyl-B complex, **SAMe** as tolerated) and **methylation-sparing** (**creatine**) to aid **COMT/HNMT** throughput.  
- Avoid high histamine/folate spikes that trigger flares; continue **H1/H2/DAO** strategy as needed.  
- Use sympatholysis (**clonidine**) during surges to blunt adrenergic amplification that interacts with mast cells.

---

## D. References (selected)
See: `refs/estrogen_genetics.md`, `refs/methylation_histamine.md`. Add phenotype-specific papers as labs accrue.

