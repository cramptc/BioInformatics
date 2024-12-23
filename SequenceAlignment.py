from Bio.Seq import Seq
from Bio import Entrez
from Bio import SeqIO
from Bio import Align
from Bio import SeqIO
from Bio.Align.Applications import ClustalwCommandline
from Bio import pairwise2 as p2

mat = p2.substitution_matrices.load("blosum62")


Entrez.email="cramptc@hotmail.com"


#Ex 1

accession_numbers = ["NM_001362438.2", "NM_001317214.3"]
Seqs = []

for i in accession_numbers:
    handle = Entrez.efetch(db="nucleotide", id=i, rettype="gb", retmode="text")
    record = SeqIO.read(handle, "genbank")
    handle.close()
    nucleotide_sequence = record.seq
    code = nucleotide_sequence
    sequence = Seq(code)
    Seqs.append(sequence)

# Finding similarities
alignments = p2.align.globalxs(Seqs[0],Seqs[1],-10,-0.5)

result = alignments[0].score
norm = result*100/len(Seqs[0])
print(norm)
'''
accession_numbers = ["NP_001304143.1", "NP_001349367.1"]
Seqs = []

for i in accession_numbers:
    handle = Entrez.efetch(db="protein", id=i, rettype="gb", retmode="text")
    record = SeqIO.read(handle, "genbank")
    handle.close()
    nucleotide_sequence = record.seq
    code = nucleotide_sequence
    sequence = Seq(code)
    Seqs.append(sequence)

print(len(Seqs[0]))

# Finding similarities
alignments = p2.align.globalds(Seqs[0],Seqs[1],mat, 0,0)
print(alignments[0])
result = alignments[0].score
print(result)
norm = result*100/max(len(Seqs[0]),len(Seqs[1]))
print(norm)

'''
