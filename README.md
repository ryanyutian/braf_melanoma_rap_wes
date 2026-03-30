# Multi-site whole-exome sequencing and ploidy-aware copy-number analysis reveal inter-patient heterogeneity in BRAF-mutant metastatic melanoma

This repository contains custom downstream analysis and plotting code associated with the manuscript:

**Ryan Y. Tian, Megan Crumbaker, Soroush Samadian, Marcus O. Butler, Sam Saibil, David Hogg, Anna Spreafico, Anthony M. Joshua, Trevor J. Pugh**  
*Multi-site whole-exome sequencing and ploidy-aware copy-number analysis reveal inter-patient heterogeneity in BRAF-mutant metastatic melanoma*

## Overview

This study analyzed whole-exome sequencing data from 48 metastatic tumour samples obtained from 7 patients with BRAF-mutant metastatic melanoma collected through a rapid autopsy program. The main downstream analyses in this repository include:

- somatic SNV/indel post-processing and cohort-level summarization
- annotation summarization using OncoKB/COSMIC-derived calls
- Sequenza-derived tumour cellularity, ploidy, and copy-number processing
- ploidy-adjusted relative copy-number analysis
- chromosome-arm and focal CNV event summarization
- plotting code for main and supplementary figures

## Scope

This repository documents the custom downstream analysis used in the manuscript. It does not provide the full upstream processing pipeline from raw sequencing reads.

External tools used in the study include:

- BWA-MEM
- Picard
- GATK Mutect2 / FilterMutectCalls
- vcf2maf
- OncoKB Annotator
- Sequenza
- GISTIC
- IGV

Where relevant, custom bash scripts, command notes and software versions are described in the repository.


## Contact

For manuscript-related questions, please contact the corresponding authors:

- Anthony M. Joshua — Anthony.joshua@svha.org.au
- Trevor J. Pugh — trevor.pugh@uhn.ca
