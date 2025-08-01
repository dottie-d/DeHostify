# DeHostify
A protocol that personalizes host decontamination in metagenomic sequences via aligning once-filtered host reads to de novo assembled host material from taxonomically unclassifiable reads


> Origin Story 
This little project came about when I was getting very low numbers of my shotgun metagenomic reads being classified by taxonomic classifiers like Wotlka or Kraken2, and I noticed that my host filtering rates were also very low.

In an effort to squeeze out as much microbial information as I could from my sequences, I reasoned that more host reads might be hidiing in the unclassified sequences, which could also have been obfuscating my classifier's ability to identify microbial reads. To solve this issue, I took the unclassifed reads from Kraken2 and assembled them de novo, aligned the subsequent bins to the original host genome, and then indexed the bins that mapped to the host genome as a personalized host decontamination reference, and aligned the host-filtered reads to the new personalized reference. It increased my host filtering by 0.5-5% per samples and my mapping rates 1-5% as well, but I felt that this concept could help others as well. Feel free to modify as needed! 

>TL, DR Project Overview
What it does:
Personalized host decontamination protocol for metagenomic sequences.
Uses unclassifiable reads for de novo assembly of host material, improving host read filtering.
Best use is on an HPC 

> Software and tools:

Kraken (for read classification)

MEGAHIT (for de novo assembly)

MetaBAT2 and MaxBin2 (for binning)

Bowtie2 (for alignment)

> Installing tools
🐙 Kraken2
Official GitHub Repository: https://github.com/DerrickWood/kraken2
Installation Instructions: https://github.com/DerrickWood/kraken2/wiki/Manual

🧬 MEGAHIT
Official GitHub Repository: https://github.com/voutcn/megahit
Bioconda Installation: conda install -c bioconda megahit
Installation Instructions: https://github.com/voutcn/megahit

🧱 MetaBAT2
Official GitHub Repository: https://bitbucket.org/berkeleylab/metabat
Bioconda Installation: conda install -c bioconda metabat2
Installation Instructions: https://bitbucket.org/berkeleylab/metabat

🧩 MaxBin2
Official SourceForge Page: https://sourceforge.net/projects/maxbin2/
Bioconda Installation: conda install -c bioconda maxbin2
Installation Instructions: https://sourceforge.net/projects/maxbin2/

✅ CheckM 

Installed with binnings tools like Maxbi2


🧵 Bowtie2
Official SourceForge Page: https://bowtie-bio.sourceforge.net/bowtie2/index.shtml
Bioconda Installation: conda install -c bioconda bowtie2
Installation Instructions: https://bowtie-bio.sourceforge.net/bowtie2/index.shtml

>Running the Protocol

Step 1: Classify the once-host filtered reads to grab the unclassified reads

kraken2 --db /path/to/kraken_db --paired reads_1.fastq reads_2.fastq --output classified_reads.txt --unclassified-out unclassified_reads.fastq

Step 2: Assemble de novo using MEGAHIT

megahit -1 reads_1.fastq -2 reads_2.fastq -o megahit_output

Step 3: Binning with MetaBAT2:

run_MetaBAT2 -i megahit_output/contigs.fa -o bins/


Step 5: Mapping bins to the host genome

bowtie2 -x host_genome_index -1 bins/bin_1.fasta -2 bins/bin_2.fasta -S host_mapped_reads.sam

Step 6: Filter reads based on mapping quality 

filtering_host_mapped_bins.py  (included in scripts section)

Step 7: Combine, deduplicate, and dereplicate high-quality host-mapped bins

merge_confident_host_bins.sh combines the confident host bins (included in scripts section)

dedupe_and_derep_confident_host_bins.py deduplicates and dereplicates (by sequence and by name) bins (included in scripts section)

Step 8: Index the combined reads using Bowtie2

bowtie2-build combined_reads.bam combined_reads_index

Step 9:Re-align host-filtered reads

bowtie2 -x combined_reads_index -1 host_filtered_reads_1.fastq -2 host_filtered_reads_2.fastq -S final_alignment.sam

I also have some scripts to compare the outputs, including: 

comparing_otu_tables.py (included in scripts section)

Which compares the otu tables after taking the twice filtered reads through a classifier


>Expected Results:
Improved host filtering: The protocol should result in a higher proportion of non-host reads after filtering.

>Potential use cases
This approach is useful for metagenomic datasets where host reads make up a significant portion of the data.




