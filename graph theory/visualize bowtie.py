import networkx as nx
import matplotlib.pyplot as plt

# Create a bowtie graph
G = nx.Graph()

# Add edges to form two triangles with a shared vertex
edges = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 2)]
G.add_edges_from(edges)

# Draw the graph
plt.figure(figsize=(6, 6))

# Define the positions of the nodes for a clear visual representation
pos = {0: (-1, 0), 1: (0, 1), 2: (0, 0), 3: (0, -1), 4: (1, 0)}

# Draw the graph with custom positions
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=800, font_size=12, font_weight='bold', edge_color='gray')

plt.title("Bowtie Graph")
plt.show()
