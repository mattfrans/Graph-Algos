import pandas as pd
import numpy as np

# Ask the user if the graph is directed
is_directed = input("Is the graph directed? (yes/no): ").lower() == "yes"

# Load the graph from the file
df = pd.read_csv('edges_1_27307')

# Create the adjacency matrix
vertices = pd.concat([df['Vertex1'], df['Vertex2']]).unique()
adjacency_matrix = pd.DataFrame(np.zeros((len(vertices), len(vertices))), index=vertices, columns=vertices)

for _, row in df.iterrows():
    adjacency_matrix.loc[row['Vertex1'], row['Vertex2']] = 1
    if not is_directed:
        adjacency_matrix.loc[row['Vertex2'], row['Vertex1']] = 1

# Save the adjacency matrix to a file
adjacency_matrix.to_csv('adjacency_matrix.csv')

# Create the adjacency list
adjacency_list = {vertex: [] for vertex in vertices}

for _, row in df.iterrows():
    adjacency_list[row['Vertex1']].append((row['Vertex2'], row['edge_id'], row['edge_weight']))
    if not is_directed:
        adjacency_list[row['Vertex2']].append((row['Vertex1'], row['edge_id'], row['edge_weight']))

# Save the adjacency list to a file
with open('adjacency_list.txt', 'w') as f:
    for vertex, edges in adjacency_list.items():
        for edge in edges:
            f.write(f"{vertex}\t{edge[0]}\t{edge[1]}\t{edge[2]}\n")
