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


def graph_from_adjacency_matrix(adjacency_matrix):
    G = nx.DiGraph()
    for i in range(len(adjacency_matrix)):
        for j in range(i+1, len(adjacency_matrix)):
            if adjacency_matrix[i][j] != 0:
                capacity=adjacency_matrix[i][j]
                G.add_edge(i, j, capacity=capacity, weight=capacity)
                G.add_edge(j, i, capacity=capacity, weight=capacity)
    return G 

def find_path(G, start_node, end_node, cost):
    # Modify demand in node start_node
    try:
        G.nodes[start_node]['demand'] = cost
        G.nodes[end_node]['demand'] = -cost
        flowCost, flowDict = nx.network_simplex(G)
        return flowCost, flowDict
    except nx.NetworkXUnfeasible:
        print("Demand Rejected.")
        return None
    
def update_graph(G, path):
    for nodeA, connections in path.items():
        for dest, cost in connections.items():
            if cost > 0:
                G[nodeA][dest]['capacity'] -= cost
                print(f"Reducing capacity from {nodeA} to {dest} by {cost}.")
    return G
            
    
if __name__ == "__main__":
    N = random.randint(10, 20)
    N = 10
    adjacency_matrix = generate_adjacency_matrix(N)
    graph = graph_from_adjacency_matrix(adjacency_matrix)
    pos = nx.spring_layout(graph)
    # Crear una nueva figura para el grafo original
    plt.figure()
    nx.draw(graph, pos, with_labels=True)
    plt.title("Original Graph")
    labels = nx.get_edge_attributes(graph, 'capacity')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.plot()
    
    nodeA = random.randint(0,N)
    nodeB = random.randint(0,N)
    nodeA = 1
    nodeB = 2
    data_flow = 5
    cost, path = find_path(graph, nodeA, nodeB, data_flow)
    updated_graph = update_graph(graph, path)



    # Crear una nueva figura para el grafo actualizado
    plt.figure()
    nx.draw(updated_graph, pos, with_labels=True)
    plt.title("Updated Graph")
    updated_labels = nx.get_edge_attributes(updated_graph, 'capacity')
    nx.draw_networkx_edge_labels(updated_graph, pos, edge_labels=updated_labels)
    plt.show()
    
