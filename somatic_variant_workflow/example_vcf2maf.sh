#!/usr/bin/env bash

# Example VCF-to-MAF conversion script using vcf2maf

set -euo pipefail

# Required inputs
VCF_DIR="PATH_TO_FILTERED_VCF_DIR"
OUT_DIR="PATH_TO_MAF_OUTPUT_DIR"
REF_FASTA="PATH_TO_REFERENCE_FASTA"
VEP_PATH="PATH_TO_VEP_BIN_DIR"
VEP_DATA="PATH_TO_VEP_CACHE"

mkdir -p "${OUT_DIR}"

for vcf in "${VCF_DIR}"/*.vcf.gz; do
    base=$(basename "${vcf}" .vcf.gz)

    perl vcf2maf.pl \
        --input-vcf "${vcf}" \
        --output-maf "${OUT_DIR}/${base}.vep.maf" \
        --tumor-id "TUMOUR_SAMPLE_ID" \
        --normal-id "NORMAL_SAMPLE_ID" \
        --ref-fasta "${REF_FASTA}" \
        --vep-path "${VEP_PATH}" \
        --vep-data "${VEP_DATA}"
done