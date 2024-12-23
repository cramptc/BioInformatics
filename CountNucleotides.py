from Bio.Seq import Seq
from Bio import Entrez
from Bio import SeqIO
from Bio import AlignIO
from Bio import SeqIO
from Bio.Align.Applications import ClustalwCommandline
from Bio import pairwise2

# Define your DNA sequence
Entrez.email="cramptc@hotmail.com"

accession_number = "NP_001304115.1"
handle = Entrez.efetch(db="protein", id=accession_number, rettype="gb", retmode="text")
record = SeqIO.read(handle, "genbank")
handle.close()
nucleotide_sequence = record.seq
code = nucleotide_sequence
print(code)
print(len(code))
sequence = Seq(code)
proteins = record


# Count the occurrences of each nucleotide
num_A = sequence.count("A")
num_T = sequence.count("T")
num_C = sequence.count("C")
num_G = sequence.count("G")

# Calculate the percentage of each nucleotide
total_length = len(sequence)
percentage_A = (num_A / total_length) * 100
percentage_T = (num_T / total_length) * 100
percentage_C = (num_C / total_length) * 100
percentage_G = (num_G / total_length) * 100

# Print the results
print("Percentage of A:", percentage_A)
print("Percentage of T:", percentage_T)
print("Percentage of C:", percentage_C)
print("Percentage of G:", percentage_G)

#Count AminoACids in a protein
# Function to count letter frequencies in a string
def count_letter_frequencies(input_string):
    # Create an empty dictionary to store the counts
    letter_count = {}

    # Iterate through each character in the string
    for char in input_string:
        # Check if the character is a letter (ignore case)
        if char.isalpha():
            char = char.lower()  # Convert to lowercase for case-insensitivity
            if char in letter_count:
                letter_count[char] += 1
            else:
                letter_count[char] = 1

    return letter_count

# Input string
input_string = "This is a sample string with letter frequencies."

# Call the function to count letter frequencies
result = count_letter_frequencies(proteins)

# Display the results
for letter, count in sorted(result.items(), key=lambda item: item[1], reverse=True):
    print(f"{letter}: {count}")


alignment = AlignIO.read("your_protein_sequences.dnd", "clustal")

# Calculate similarity scores using BLOSUM matrix
from Bio.Align import substitution_matrices as sm
blosum62 = sm.blosum62
similarity_matrix = []
for i in range(len(sequences)):
    row = []
    for j in range(len(sequences)):
        if i == j:
            row.append(1.0)  # Identical to itself
        else:
            alignment1 = alignment[i].seq
            alignment2 = alignment[j].seq
            score = pairwise2.align.localds(alignment1, alignment2, blosum62, -10, -0.5, one_alignment_only=True)[0][2]
            row.append(score)
    similarity_matrix.append(row)
