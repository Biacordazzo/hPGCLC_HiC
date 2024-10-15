#!/bin/bash
echo "-----------------------------" 
echo "Starting PGCLC12k_vs_Naive10k" 
bart3d --treatment matrix_individual_samples/PGCLC_12k/raw/40000/PGCLC_12k_40000.matrix \
--control matrix_individual_samples/Naive_10k/raw/40000/Naive_10k_40000.matrix \
--bedFileHicpro matrix_individual_samples/Naive_10k/raw/40000/Naive_10k_40000_abs.bed.corrected.bed \
--fileFormat hicpro \
--species hg38 \
--coverageNormalization \
--outdir bart3d_output/PGCLC_12k_vs_Naive_10k/
echo "-----------------------------"
echo "Starting PGCLC24k_vs_Naive25k"
bart3d --treatment matrix_individual_samples/PGCLC_24k/raw/40000/PGCLC_24k_40000.matrix \
--control matrix_individual_samples/Naive_25k/raw/40000/Naive_25k_40000.matrix \
--bedFileHicpro matrix_individual_samples/Naive_25k/raw/40000/Naive_25k_40000_abs.bed.corrected.bed \
--fileFormat hicpro \
--species hg38 \
--coverageNormalization \
--outdir bart3d_output/PGCLC_24k_vs_Naive_25k/
echo "-----------------------------" 
echo "Starting PGCLC25k_vs_Naive500k"
bart3d --treatment matrix_individual_samples/PGCLC_25k/raw/40000/PGCLC_25k_40000.matrix \
--control matrix_individual_samples/Naive_500k/raw/40000/Naive_500k_40000.matrix \
--bedFileHicpro matrix_individual_samples/Naive_500k/raw/40000/Naive_500k_40000_abs.bed.corrected.bed \
--fileFormat hicpro \
--species hg38 \
--coverageNormalization \
--outdir bart3d_output/PGCLC_25k_vs_Naive_500k/
