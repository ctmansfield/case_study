# Genetics – Estrogen Handling, Methylation & Neuro-Adrenergic Modulation

> **Use:** Clinical framing, not destiny. Phenoconversion (illness, sleep loss, diet, meds) can outweigh genotype.
> **Actionables:** Track free E2/T with SHBG; interpret alongside thyroid & liver markers.

## A. Key variants (patient-reported / scan-confirmed)
| Pathway | Gene / Variant | Typical functional effect | Expected clinical direction |
|---|---|---|---|
| Catechol & catechol-estrogen methylation | **COMT rs4680 (Val158Met, Met allele)** | Lower thermal stability/activity → slower methylation of catechols | ↑ catechol “noise” under stress; adrenergic amplification; anxiety/insomnia risk |
| Phase I alternate hydroxylation | **CYP1A2 rs762551 (*1F context)** | Alters inducibility; context-dependent | If low/phenoconverted: slower aryl/xanthine metabolism; sleep/stress interactions |
| Hepatic estrogen clearance | **CYP3A4*22 (rs35599367)** | ↓ 3A4 expression/activity | Slower E2 clearance; higher exposure at same aromatase rate |
| Hepatic estrogen clearance (redundancy) | **CYP3A5*3 (rs776746) non-expressor** | Loss of 3A5; shifts burden to 3A4 | Accentuates *22 effect (more load on 3A4) |
| Glucuronidation of bilirubin/E2 metabolites | **UGT1A1*28 (rs887829 tag)** | ↓ expression → reduced glucuronidation | Slower E2 metabolite clearance; ↑ unconjugated bilirubin tendency (Gilbert-like) |
| Estradiol sulfation | **SULT1E1 rs3736599 (promoter)** | Reported ↓ expression in some cohorts | Prolonged active E2 half-life when sulfation low |
| DHEA sulfation | **SULT2A1 rs2637125** | Research variant | May lower DHEA-S; aligns with low DHEAS labs |
| Binding pool | **SHBG rs6259/rs12150660/rs1799941** | Common alleles shift SHBG levels | Alters free vs total T/E2; interacts with thyroid & liver status |

**Integrated interpretation:** Pattern favors slower Phase II (COMT-Met, UGT1A1*28, SULT1E1 var) plus reduced CYP3A throughput (CYP3A4*22 with CYP3A5*3) ⇒ tendency toward higher circulating E2 and catechol buildup under stress → explains sensitivity to estradiol excursions and benefit from careful anastrozole titration.

## B. Practical hooks
- Keep **free E2** in lower-physiologic band; titrate **anastrozole** cautiously to avoid oversuppression.  
- Monitor **SHBG** and compute free hormones after dose changes.  
- Support **Phase II** conjugation nutritionally; avoid large **folate spikes** that can perturb methyl flux in this phenotype.  
- Maintain **creatine** (methyl-sparing) and **methyl-B/SAMe** balance to aid COMT/HNMT function.
- Given adrenergic sensitivity (COMT-Met), maintain **sympatholytic reserve** (e.g., clonidine per clinician).

## C. Mitochondrial/“alcoholic-pattern” labs (context)
Macrocytosis, AST>ALT with normal GGT, low ALP/phosphate, and low PLP (B6) have been observed historically, consistent with oxidative stress and **functional B6 deficiency**—can worsen catechol/monoamine handling and fatigue. Tie-in with methylation and histamine loads appears clinically relevant.

## D. Variant index (data)
A merged, deduplicated variant table should live at: `data/genetics/variant_index.csv` with columns: gene, rsid, zygosity, effect, note, source.

## E. References
See `refs/clonidine.md`, `refs/creatine_methylation.md`, `refs/histamine_axis.md` and add estrogen-genetics items in `refs/estrogen_genetics.md`.
