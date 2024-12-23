from pronto import Ontology
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

def get_name_by_id(ontology, ontology_id):

    term = ontology.get(ontology_id)
    if term:
        return term.name
    else:
        return None
    
def read_tsv_file(file_path):
    try:
        # Read the TSV file into a DataFrame
        data = pd.read_csv(file_path, sep='\t')
        return data
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

    # Example usage:
    # Replace 'your_file.tsv' with the path to your TSV file
file_path = 'gencc-submissions.tsv'
df = read_tsv_file(file_path)

def find_descendants(ontology, ontology_id):
    term = ontology[ontology_id]
    descendants = list(term.subclasses())
    return [desc.id for desc in descendants]

obo_file_path = 'mondo.obo'  # Replace with the path to your OBO file
ontology = Ontology(obo_file_path)

    # Specify the ontology ID for which you want to find descendants
ontology_id_to_find = 'MONDO:0005071'  # Replace with the ID you want to search for

    # Find descendants for the specified ontology ID
descendants = find_descendants(ontology, ontology_id_to_find)
print("MONDO:0100038" in descendants)

types = []
number = []
titles = []
for r,i in df.loc[:,['disease_curie','disease_title','classification_title']].iterrows():
    if i[2] == "No Known Disease Relationship":
        continue
    if i[0] in descendants:
        if i[0] in types:
            number[types.index(i[0])] +=1
        else:
            types.append(i[0])
            number.append(1)
            titles.append(i[1])
print(len(types))
for i in sorted(list(zip(types,number,titles)),key=lambda x: x[1], reverse=True)[:10]:
    print(i)

genes = []
num = []
titlesgen = []
for r,i in df.loc[:,['disease_curie','disease_title','gene_symbol','classification_title']].iterrows():
    if i[3] == "No Known Disease Relationship":
        continue
    if i[0] in descendants:
        if i[2] in genes:
            num[genes.index(i[2])] +=1
        else:
            genes.append(i[2])
            num.append(1)
            titlesgen.append(i[1])

print(len(genes))
for i in sorted(list(zip(genes,num,titlesgen)),key=lambda x: x[1], reverse=True)[:10]:
    print(i)
