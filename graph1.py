import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
import itertools
from matplotlib import colors as mcolors

# Esta función genera una matriz de adyacencia para un grafo con un número especificado de nodos. Cada nodo tiene una capacidad aleatoria entre 1 y 15, y cada par de nodos tiene una probabilidad del 30% de tener una arista entre ellos, con un peso aleatorio entre 1 y 15.
# La función devuelve la matriz de adyacencia y una lista de capacidades de nodos.
def generate_adjacency_matrix(nodes):
    adjacency_matrix = np.zeros((nodes, nodes))
    node_capacities = [random.randint(1,15) for _ in range(nodes)]

    for i in range(nodes):
        for j in range(i+1, nodes):
            if random.random() <= 0.3:
                adjacency_matrix[i][j] = adjacency_matrix[j][i] = random.randint(1,15)

    return adjacency_matrix, node_capacities
#Esta función toma una matriz de adyacencia y una lista de capacidades de nodos, y dibuja el grafo correspondiente. Cada nodo se colorea de manera única, y las capacidades de los nodos se muestran junto a los nodos.
def plot_graph_from_adjacency_matrix(adjacency_matrix, node_capacities):
    G = nx.Graph()

    for i in range(len(adjacency_matrix)):
        for j in range(i+1, len(adjacency_matrix)):
            if adjacency_matrix[i][j] != 0:
                G.add_edge(i, j, weight=adjacency_matrix[i][j])

    # Generar una lista de colores, uno para cada nodo
    all_colors = list(mcolors.CSS4_COLORS.keys())
    if len(adjacency_matrix) > len(all_colors):
        raise ValueError("Too many nodes for unique coloring")
    node_colors = all_colors[:len(adjacency_matrix)]

    pos = nx.spring_layout(G)
    # Agregar el parámetro node_color a nx.draw()
    nx.draw(G, pos, with_labels=True, node_color=node_colors)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Mostrar las capacidades de los nodos
    for i, capacity in enumerate(node_capacities):
        plt.text(pos[i][0], pos[i][1]+0.1, str(capacity), horizontalalignment='center')

    plt.show()
#sta función toma un grafo y una lista de demandas, y calcula todos los caminos posibles que pueden acomodar cada demanda. Para cada demanda, se calculan todos los caminos posibles desde el nodo fuente hasta el nodo objetivo, y se verifica si la suma de los pesos de las aristas en el camino es mayor o igual a la demanda. Si es así, la demanda es aceptada, y el peso del camino se suma al revenue total. La función imprime la demanda, el camino, el acceptance ratio y el revenue para cada demanda.

#La función devuelve una lista de tuplas, donde cada tupla contiene la demanda y el camino que la acomoda.
def calculate_all_possibilities_brute_force(graph, demands):
    total_demands = len(demands)
    accepted_demands = 0
    total_revenue = 0

    all_possibilities = []
    for demand in demands:
        for path in nx.all_simple_paths(graph, source=demand[0], target=demand[1]):
            path_edges = list(zip(path, path[1:]))
            path_weight = sum(graph[u][v]['weight'] for u, v in path_edges)
            if path_weight >= demand[2]:  # if the path can accommodate the demand
                accepted_demands += 1
                total_revenue += path_weight
                all_possibilities.append((demand, path))
                print(f'Demand: {demand}, Path: {path}, Acceptance Ratio: {accepted_demands/total_demands}, Revenue: {total_revenue}')

    return all_possibilities

#El código luego genera una matriz de adyacencia para un grafo con 20 nodos, convierte la matriz de adyacencia en un grafo de NetworkX, y calcula todos los caminos posibles para un conjunto de demandas.

# Finalmente, el código dibuja el grafo generado y muestra las capacidades de los nodos junto a los nodos.
# Assume that the demands are a list of tuples, where each tuple is (source, target, demand)
demands = [(0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5)]
all_possibilities = calculate_all_possibilities_brute_force(graph, demands)

# Generar una matriz de adyacencia para un gráfico con 5 nodos
N = 20
adjacency_matrix, node_capacities = generate_adjacency_matrix(N)
graph = nx.convert_matrix.from_numpy_array(adjacency_matrix)

# Asume que las demandas son una lista de enlaces
for possibility in all_possibilities:
    print(possibility)

# Dibujar el grafo
plot_graph_from_adjacency_matrix(adjacency_matrix, node_capacities)