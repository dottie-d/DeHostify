#!/bin/bash
# merge_confident_host_bins.sh

# Path to the directory of confident host‐mapped FASTAs
BIN_DIR="/tscc/lustre/ddn/scratch/mdothard/empathy_experiment_one/hostalign_on_bins_minimap2/parsed_summary/filtered_bins/confident_host_bins"
OUT_FASTA="confident_host_bins_merged.fasta"

echo "🧬 Merging all FASTAs in $BIN_DIR into $OUT_FASTA"
> "$OUT_FASTA"

for fasta in "$BIN_DIR"/*.fasta; do
  if [[ -s "$fasta" ]]; then
    echo "📦 Adding: $(basename "$fasta")"
    cat "$fasta" >> "$OUT_FASTA"
  else
    echo "⚠️  Skipping empty or missing file: $(basename "$fasta")"
  fi
done

echo "✅ Merge complete — output at: $OUT_FASTA"
