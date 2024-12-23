from pronto import Ontology
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import networkx as nx
from itertools import combinations
import random
import textwrap

def generate_random_color_hex():
    rgb_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    hex_color = "#{:02x}{:02x}{:02x}".format(rgb_color[0], rgb_color[1], rgb_color[2])
    return hex_color
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
ontology_id_to_find = 'MONDO:0005071'
obo_file_path = 'mondo.obo'  # Replace with the path to your OBO file
ontology = Ontology(obo_file_path)
descendants = find_descendants(ontology, ontology_id_to_find)

genes= []
number = []
for r,i in df.loc[:,['gene_symbol','disease_curie',"classification_title"]].iterrows():
    if i[2] == "No Known Disease Relationship":
        continue
    if not i[1] in descendants:
        continue
    if i[0] in genes:
        number[genes.index(i[0])].append(i[1])
    else:
        genes.append(i[0])
        number.append([i[1]])
pairs = []
counts = []
for i in range(len(genes)):
    number[i] = list(set(number[i]))
    for t1,t2 in combinations(number[i],2):
        t1 = get_name_by_id(ontology,t1)
        t2 = get_name_by_id(ontology,t2)
        if t1==t2:
            continue
        pname = [t1,t2]
        pname.sort()
        pname = '::'.join(pname)
        if pname in pairs:
            counts[pairs.index(pname)] +=1
        else:
            pairs.append(pname)
            counts.append(1)

pairs = sorted(list(zip(pairs,counts)),key=lambda x: x[1], reverse=True)
strongpairs = [(x, y) for x, y in pairs if y >= 3]
nodes = []
labels = []
Net = nx.Graph()
c = 1
for x,y in strongpairs:
    ns = x.split('::')
    for j in ns:
        if not j in nodes:
            nodes.append(j)
            Net.add_node(j,label=c)
            c+=1
            print("Node "+str(c)+" is "+j)
Net.add_edges_from([(x.split('::'))[:2] for x,y in strongpairs])
communities = nx.algorithms.community.greedy_modularity_communities(Net)
# create a dict with the gene_id as key and community membership list as value
communityDict = dict()

# loop through the communities
for i, community in enumerate(communities):
    # loop through the diseases in the community
    for gene_id in community:
        # add the disease and community to the dictionary
        communityDict[gene_id] = i



# plot the graph with the communities coloured
# create a list of 18 colors
communityColours = [generate_random_color_hex() for i in communities]
nodeColours = [communityColours[communityDict[node]] for node in Net.nodes()]
#pos = nx.circular_layout(Net)
pos = nx.spring_layout(Net, k=3, iterations=500, scale=5)
nx.draw_networkx_nodes(Net, pos,node_color=nodeColours,node_size = 100,alpha=0.5)
nx.draw_networkx_edges(Net,pos, alpha=0.5)
node_labels = nx.get_node_attributes(Net, 'label')
nx.draw_networkx_labels(Net, pos, labels=node_labels)
print("Nodes: "+str(Net.number_of_nodes()))
print("Edges: "+ str(Net.number_of_edges()))
plt.show()

