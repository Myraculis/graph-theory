import networkx as nx
import matplotlib.pyplot as plt

def create_graph(edges):
    G = nx.Graph()
    G.add_edges_from(edges)
    return G

def draw_graph(G):
    pos = nx.spring_layout(G)  # positions for all nodes
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, edge_color='gray')
    plt.show()

# Example: Define a set of edges
edges = [(1, 2), (1, 3), (1,4), (2, 4), (3, 4), (4, 5)]

# Create and draw the graph
G = create_graph(edges)
draw_graph(G)