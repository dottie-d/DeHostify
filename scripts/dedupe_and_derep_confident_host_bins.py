import os
import glob
from Bio import SeqIO

# Path to your non-host bins directory
non_host_bins_dir = "/tscc/lustre/ddn/scratch/mdothard/empathy_experiment_one/hostalign_on_bins_minimap2/parsed_summary/filtered_bins/confident_host_bins"

# Loop through all the bins in the non_host_bins directory
for bin_file in glob.glob(os.path.join(non_host_bins_dir, "*.host_mapped.fasta")):
    # Parse the fasta file for each bin
    print(f"Processing file: {bin_file}")
    
    # Load the contigs from the current bin
    contigs = list(SeqIO.parse(bin_file, "fasta"))
    print(f"Loaded {len(contigs)} contigs from {bin_file}")
    
    # Deduplicate by sequence (remove identical sequences)
    seen_sequences = set()
    unique_contigs = []
    for contig in contigs:
        # Use contig sequence to check for duplicates
        if str(contig.seq) not in seen_sequences:
            seen_sequences.add(str(contig.seq))
            unique_contigs.append(contig)
    
    print(f"After sequence deduplication: {len(unique_contigs)} unique contigs")
    
    # Deduplicate by name (remove duplicate names)
    seen_names = set()
    final_contigs = []
    for contig in unique_contigs:
        # Use contig ID to check for duplicates
        if contig.id not in seen_names:
            seen_names.add(contig.id)
            final_contigs.append(contig)
    
    print(f"After name deduplication: {len(final_contigs)} final contigs")
    
    # Save the deduplicated bin
    output_file = bin_file.replace(".host_mapped.fasta", "_deduped.fasta")
    with open(output_file, "w") as output_handle:
        SeqIO.write(final_contigs, output_handle, "fasta")
    
    print(f"Saved deduplicated bin: {output_file}")

print("Deduplication and dereplication complete!")
