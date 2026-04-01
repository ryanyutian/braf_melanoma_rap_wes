# Somatic SNV/indel calling and annotation workflow

## Overview

Somatic SNVs and indels were identified from paired tumour-normal whole-exome sequencing data using a two-pass Mutect2 workflow followed by vcf2maf conversion and OncoKB annotation.

The overall workflow was:

1. initial matched tumour-normal somatic calling with Mutect2
2. construction of a union set of candidate alleles across samples
3. force-calling of the union allele set in each tumour-normal pair using Mutect2
4. filtering of force-called variants using FilterMutectCalls
5. conversion of filtered VCF files to MAF format using vcf2maf
6. annotation of MAF files using the OncoKB MafAnnotator workflow

This repository provides simplified representative example scripts for these steps.