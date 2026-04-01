#!/usr/bin/env bash

# Example second-pass Mutect2 force-calling script/template

set -euo pipefail

# Module loads
module load gatk/4.2.0.0
module load igenome-human/hg19

# Required inputs
REF="PATH_TO_REFERENCE_FASTA"
TUMOUR_BAM="PATH_TO_TUMOUR_BAM"
NORMAL_BAM="PATH_TO_MATCHED_NORMAL_BAM"
PON="PATH_TO_PANEL_OF_NORMALS_VCF"
ALLELE_VCF="PATH_TO_FORCE_CALL_ALLELES_VCF"

# Sample names
TUMOUR_SAMPLE_NAME="TUMOUR_SAMPLE_ID"
NORMAL_SAMPLE_NAME="NORMAL_SAMPLE_ID"

# Working/output directories
TMP_DIR="PATH_TO_TMP_DIR/${TUMOUR_SAMPLE_NAME}"
OUTPUT_FILE="PATH_TO_OUTPUT_DIR/${TUMOUR_SAMPLE_NAME}.forcecall.vcf.gz"
FILTERED_OUTPUT_FILE="PATH_TO_OUTPUT_DIR/${TUMOUR_SAMPLE_NAME}.forcecall.filtered.vcf.gz"

mkdir -p "${TMP_DIR}"

echo "Running force-call Mutect2 for ${TUMOUR_SAMPLE_NAME}"
echo "Matched normal: ${NORMAL_SAMPLE_NAME}"
echo "Allele list: ${ALLELE_VCF}"
echo "Output: ${OUTPUT_FILE}"

gatk Mutect2 \
    -R "${REF}" \
    -I "${TUMOUR_BAM}" \
    -I "${NORMAL_BAM}" \
    -normal "${NORMAL_SAMPLE_NAME}" \
    -alleles "${ALLELE_VCF}" \
    --panel-of-normals "${PON}" \
    --tmp-dir "${TMP_DIR}" \
    -O "${OUTPUT_FILE}"

gatk FilterMutectCalls \
    -V "${OUTPUT_FILE}" \
    -R "${REF}" \
    --tmp-dir "${TMP_DIR}" \
    -O "${FILTERED_OUTPUT_FILE}"