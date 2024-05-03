import time  # Cambia la importación para evitar conflictos con la función time
import numpy as np
import random
import matplotlib.pyplot as plt
import networkx as nx
start_time = time.time()

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
        return None, None
    
def update_graph(G, path):
    for nodeA, connections in path.items():
        for dest, cost in connections.items():
            if cost > 0:
                G[nodeA][dest]['capacity'] -= cost
                print(f"Reducing capacity from {nodeA} to {dest} by {cost}.")
    return G
            
def plot_assignment_results(assignments, costs):
    plt.figure(figsize=(10, 6))
    plt.barh(range(len(assignments)), costs, color='skyblue')
    plt.xlabel('Cost or Acceptance Ratio')
    plt.ylabel('Allocations')
    plt.title('Cost or Acceptance Ratio of each Allocation')
    for i, cost in enumerate(costs):
        plt.text(cost, i, str(cost), va='center')
    plt.yticks(range(len(assignments)), assignments)
    plt.tight_layout()
    plt.show()

    
def plot_acceptance_ratio(acceptance_ratios):
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(acceptance_ratios)), acceptance_ratios, marker='o', color='green')
    plt.xlabel('Time Interval')
    plt.ylabel('Acceptance Ratio')
    plt.title('Acceptance Ratio Over Time')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_demand_acceptance_over_time(demands_accepted):
    times = list(demands_accepted.keys())
    demands = [len(demands_accepted[time]) for time in times]
    plt.figure(figsize=(10, 6))
    plt.plot(times, demands, marker='o', color='orange')
    plt.xlabel('Time')
    plt.ylabel('Number of Accepted Demands')
    plt.title('Acceptance of Demands over Time')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
def plot_link_capacity(graph):
    plt.figure(figsize=(10, 6))
    
    # Calcula la capacidad restante de cada enlace y normaliza los valores para el ancho de las flechas
    edge_widths = [1 - graph.edges[edge]['capacity'] / graph.edges[edge]['weight'] for edge in graph.edges]
    edge_labels = nx.get_edge_attributes(graph, 'capacity')
    pos = nx.spring_layout(graph)  # Asigna un layout al grafo
    
    # Dibuja el grafo con anchos de flecha proporcionales a la capacidad restante
    nx.draw(graph, with_labels=True, node_color='skyblue', node_size=500, edge_color='gray', width=edge_widths, pos=pos)
    nx.draw_networkx_edge_labels(graph, pos=pos, edge_labels=edge_labels)
    plt.title('Link Capacity After Demand Allocation')  # Título agregado
    plt.show()

def dijkstra(graph, source, target):
    return nx.dijkstra_path(graph, source, target)

def a_star(graph, source, target):
    return nx.astar_path(graph, source, target)

def bellman_ford(graph, source, target):
    return nx.bellman_ford_path(graph, source, target)

# Comparación de los algoritmos
def calculate_accepted_demands(algorithm, G, demands):
    accepted_demands = 0
    for demand in demands:
        duration, path, cost = demand
        # Usamos una copia del gráfico para no modificar el gráfico original
        G_copy = G.copy()
        try:
            # Intentamos aceptar la demanda
            nx.accept_demand(G_copy, duration, path, cost)
            # Si la demanda fue aceptada sin lanzar una excepción, incrementamos el contador
            accepted_demands += 1
        except Exception:
            # Si la demanda no pudo ser aceptada, simplemente continuamos con la siguiente demanda
            continue
    return accepted_demands

def calculate_accepted_demands(algorithm, G, demands):
    accepted_demands = 0
    for demand in demands:
        duration, path, cost = demand
        G_copy = G.copy()
        try:
            algorithm(G_copy, duration, path, cost)
            accepted_demands += 1
        except Exception:
            continue
    return accepted_demands

def compare_algorithms(G, source, target, demands):
    total_demands = len(demands)
    algorithms = [nx.dijkstra_path, nx.astar_path, nx.bellman_ford_path]
    algorithm_names = ['Dijkstra', 'A*', 'Bellman-Ford']
    acceptance_ratios = []

    duration = 10
    for algorithm in algorithms:
        accepted_demands = calculate_accepted_demands(algorithm, G, demands)
        acceptance_ratio = accepted_demands / total_demands
        acceptance_ratios.append(acceptance_ratio)

        print(f"{algorithm.__name__} Acceptance Ratio: {acceptance_ratio}")

    plt.figure(figsize=(10, 6))
    plt.bar(algorithm_names, acceptance_ratios, color=['blue', 'green', 'red'])
    plt.xlabel('Algorithm')
    plt.ylabel('Acceptance Ratio')
    plt.title('Comparison of Path Finding Algorithms')
    plt.ylim(0, 1)
    plt.show()
    
if __name__ == "__main__":
    
    N = random.randint(10, 20)
    N = 10  # Estableces N en 10, no necesitas la primera asignación de random.randint(10, 20)
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
    
    # Seleccionar nodos de origen y destino
    nodes = list(graph.nodes)
    nodeA = random.choice(nodes)  # Selección aleatoria de un nodo de la lista de nodos
    nodeB = random.choice(nodes)  # Selección aleatoria de otro nodo de la lista de nodos
    data_flow = 5
    demands = [(random.randint(1, 10), random.choice(nodes), random.choice(nodes)) for _ in range(10)]

    compare_algorithms(graph, nodeA, nodeB, demands)
    # Encontrar el camino
    cost, path = find_path(graph, nodeA, nodeB, data_flow)
    
    # Verificar si se encontró un camino válido
    if cost is not None and path is not None:
        updated_graph = update_graph(graph, path)
        
                
        # Crear una nueva figura para el grafo actualizado
        plt.figure()
        nx.draw(updated_graph, pos, with_labels=True)
        plt.title("Updated Graph")
        updated_labels = nx.get_edge_attributes(updated_graph, 'capacity')
        nx.draw_networkx_edge_labels(updated_graph, pos, edge_labels=updated_labels)
        plt.show()
        
        
        plot_link_capacity(updated_graph)
        
        # Calcula el costo o ratio de aceptación de cada asignación
        assignments = ["Demand1", "Demand2", "Demand3"]  # Ejemplo de nombres de asignaciones
        costs = [random.randint(1, 10) for _ in range(len(assignments))]  # Ejemplo de costos aleatorios
        plot_assignment_results(assignments, costs)
        
        # Calcula y grafica la ratio de aceptación a lo largo del tiempo
        acceptance_ratios = [random.uniform(0, 1) for _ in range(10)]  # Ejemplo de ratios de aceptación aleatorios
        plot_acceptance_ratio(acceptance_ratios)
        
        # Calcula y grafica la aceptación de demandas a lo largo del tiempo
        demands_accepted = {0: [1, 2, 3], 1: [4, 5], 2: [6], 3: [7, 8, 9]}  # Ejemplo de datos de demandas aceptadas
        plot_demand_acceptance_over_time(demands_accepted)
        
        #plot_link_capacity(updated_graph)
        
        plt.show()
        

        
        
    else:
        print("No se encontró un camino válido para la demanda especificada.")

