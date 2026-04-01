#!/usr/bin/env bash

# Example OncoKB annotation script/template

set -euo pipefail

# Required inputs
INPUT_MAF="PATH_TO_INPUT_MAF"
OUTPUT_FILE="PATH_TO_OUTPUT_ONCOKB_FILE"
CLINICAL_FILE="PATH_TO_CLINICAL_FILE"
ONCOKB_TOKEN="ONCOKB_TOKEN"

python MafAnnotator.py \
    -i "${INPUT_MAF}" \
    -o "${OUTPUT_FILE}" \
    -c "${CLINICAL_FILE}" \
    -b "${ONCOKB_TOKEN}"