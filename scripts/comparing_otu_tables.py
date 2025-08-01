import pandas as pd

# === Load feature tables ===
df_original = pd.read_csv(
    "/tscc/lustre/ddn/scratch/mdothard/empathy_experiment_one/optimizing/woltka_or_kraken2/woltka_outputs/merged_filtered_data.csv",
    sep=",",
    index_col=0
)

df_double = pd.read_csv(
    "/tscc/lustre/ddn/scratch/mdothard/empathy_experiment_one/twice_host_filtered_map_classify_outputs/woltka_outputs/merged_twice_filtered_data.csv",
    sep=",",
    index_col=0
)

# === Sanity check: Preview ===
print("Original (once-filtered) table preview:")
print(df_original.head())
print("\nDouble-filtered table preview:")
print(df_double.head())

# === OTU ID set comparisons ===
otus_original = set(df_original.index)
otus_double = set(df_double.index)

shared = otus_original & otus_double
only_in_original = otus_original - otus_double
only_in_double = otus_double - otus_original

# === Output stats ===
print("\n=== OTU Comparison Summary ===")
print(f"Total OTUs in once-filtered: {len(otus_original)}")
print(f"Total OTUs in double-filtered: {len(otus_double)}")
print(f"Shared OTUs: {len(shared)}")
print(f"Only in once-filtered: {len(only_in_original)}")
print(f"Only in double-filtered: {len(only_in_double)}")

# === Save OTU ID lists ===
with open("otus_only_in_once_filtered.txt", "w") as f:
    f.write("\n".join(sorted(only_in_original)))

with open("otus_only_in_twice_filtered.txt", "w") as f:
    f.write("\n".join(sorted(only_in_double)))

with open("otus_shared.txt", "w") as f:
    f.write("\n".join(sorted(shared)))

# === Optional: Top 10 most abundant OTUs (sum across all samples) ===
print("\n=== Top 10 OTUs by Total Abundance (Once-filtered) ===")
print(df_original.sum(axis=1).sort_values(ascending=False).head(10))

print("\n=== Top 10 OTUs by Total Abundance (Double-filtered) ===")
print(df_double.sum(axis=1).sort_values(ascending=False).head(10))
