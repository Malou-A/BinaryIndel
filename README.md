## Binary Indel detection

This script was created for a phylogenetic analysis exercise during the course BINP29 Bioinformatics: DNA Sequencing Informatics II at Lund University.

Detecting insertion or deletions in different species can be informative when doing phylogenetic analysis, so I created this script that will detect indels in an aligned fasta file, which was an optional part of the exercise.

The script parses through each line and removes uninformative information. Gaps larger than one position will be added together, overlapping gaps will be removed and beginnings and endings of sequences will be trimmed.
The output file will consist of one line for each species, consisting of 1's and 0's where 1 represents a deletion, and 0 represents an insertion.

