import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import obonet

def read_tsv_file(file_path):
    try:
        # Read the TSV file into a DataFrame
        data = pd.read_csv(file_path, sep='\t')
        return data
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

file_path = 'gencc-submissions.tsv'
df = read_tsv_file(file_path)

rowcount = 0
MOIs = 0
uniqueMois = []
number = []
for index,row in df.loc[:,['uuid','moi_curie']].iterrows():
        if not row[0].startswith("GENCC_"):
            continue
        rowcount+=1
        if len(row[1].split(":")) == 2:
            if not row[1] in uniqueMois:
                uniqueMois.append(row[1])
                number.append(1)
            else:
                number[uniqueMois.index(row[1])] += 1
            MOIs += 1

print(uniqueMois)
print(df.shape)
print(rowcount)
print(MOIs)
print(MOIs/rowcount)

def parse_obo_file(file_path):
 # Initialize an empty dictionary to store the ontology data
    ontology_data = {}

    # Use the obonet library to parse the OBO file
    graph = obonet.read_obo(file_path)

    # Iterate through ontology terms and their data
    for node_id, data in graph.nodes(data=True):
        ontology_data[node_id] = data

    return ontology_data

def get_name_by_id(ontology_data, id_to_find):
    if id_to_find in ontology_data:
        return ontology_data[id_to_find]['name']
    else:
        return None
    
obo_file_path = 'hp.obo'  # Replace with the path to your OBO file
ontology_data = parse_obo_file(obo_file_path)

for i in range(len(uniqueMois)):
    print(uniqueMois[i])
    print(get_name_by_id(ontology_data, uniqueMois[i]))
    print(number[i])
    print()

