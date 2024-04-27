
import numpy as np
import random
import matplotlib.pyplot as plt
import networkx as nx

def generate_adjacency_matrix(nodes):
    adjacency_matrix = np.zeros((nodes, nodes))

    for i in range(nodes):
        for j in range(i+1, nodes):
            if random.random() <= 0.3:
                adjacency_matrix[i][j] = adjacency_matrix[j][i] = random.randint(1,15)

    return adjacency_matrix

def plot_graph_from_adjacency_matrix(adjacency_matrix):
    G = nx.Graph()

    for i in range(len(adjacency_matrix)):
        for j in range(i+1, len(adjacency_matrix)):
            if adjacency_matrix[i][j] != 0:
                G.add_edge(i, j, weight=adjacency_matrix[i][j])

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.show()    
# Generar una matriz de adyacencia para un gráfico con 5 nodos
N = 20
adjacency_matrix = generate_adjacency_matrix(N)
plot_graph_from_adjacency_matrix(adjacency_matrix)