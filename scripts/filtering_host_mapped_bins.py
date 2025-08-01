import os
import pandas as pd
from pathlib import Path
import shutil

# Set paths
parsed_summary_dir = Path("/tscc/lustre/ddn/scratch/mdothard/empathy_experiment_one/hostalign_on_bins_minimap2/parsed_summary")
output_base_dir = parsed_summary_dir / "filtered_bins"
fasta_root_dir = parsed_summary_dir.parent  # goes up one level to /hostalign_on_bins_minimap2

# Create output folders
categories = {
    "confident_host_bins": [],
    "low_confidence_host_bins": [],
    "non_host_bins": [],
}
for category in categories:
    (output_base_dir / category).mkdir(parents=True, exist_ok=True)

# Iterate over summary files
summary_files = parsed_summary_dir.glob("*.parsed_sam.tsv")
for file in summary_files:
    df = pd.read_csv(file, sep="\t")
    for _, row in df.iterrows():
        sample = row["sample"]
        tool = row["tool"]
        bin_id = row["bin"]
        pct_mapped = row["percent_mapped"]
        mapq = row["avg_mapq"]

        if pd.isna(bin_id) or bin_id.strip() == "":
            continue

        # Build source path
        fasta_path = fasta_root_dir / sample / tool / f"{bin_id}.host_mapped.fasta"
        if not fasta_path.exists():
            continue

        # Classification logic
        if pct_mapped >= 1 and mapq > 0:
            category = "confident_host_bins"
        elif pct_mapped >= 1 or mapq > 0:
            category = "low_confidence_host_bins"
        else:
            category = "non_host_bins"

        # Copy file to new category folder
        dest_path = output_base_dir / category / fasta_path.name
        shutil.copy2(fasta_path, dest_path)
        categories[category].append(dest_path)

# Output summary
summary_df = pd.DataFrame.from_dict(
    {k: len(v) for k, v in categories.items()},
    orient="index", columns=["num_bins"]
)
summary_df.index.name = "Category"
summary_df.to_csv(output_base_dir / "filtering_summary.tsv", sep="\t")

print("✅ Done! Summary:")
print(summary_df)
