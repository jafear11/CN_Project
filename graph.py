import numpy as np
import random
import matplotlib.pyplot as plt
import networkx as nx
import time
from network import Network

                
def shortest_path_brute(G, start_node, end_node, cost):
    try:
        paths = list(nx.all_simple_paths(G, start_node, end_node))
        valid_paths = []
        for path in paths:
            weights = [G[u][v].get('weight', 1) for u, v in zip(path[:-1], path[1:])]
            if all(weight >= cost for weight in weights):
                total_cost = sum(weights)
                valid_paths.append((total_cost, path))
        if not valid_paths:
            print("Demand rejected: no capacity.")
            return None
        valid_paths.sort()
        
        print(f"Shortest path from node {start_node} and {end_node}: {valid_paths[0][1]}")
        print(f"Total cost: {valid_paths[0][0]}")
        print(f"Cost/Revenue: {valid_paths[0][0] / ((len(valid_paths[0][1]) - 1)*cost)}")
        print(f"Number of hops: {len(valid_paths[0][1]) - 1}")
        return valid_paths[0][1]
    
    except nx.NetworkXNoPath:
        print("Demand rejected: destination unreachable.")
        return None

if __name__ == "__main__":
    
    network = Network(random.randint(10, 15))
    while True:
        nodeA = random.randint(0,network.nodes-1)
        nodeB = random.randint(0,network.nodes-1)
        cost = random.randint(1, 5)
        shortest_path = shortest_path_brute(network.graph, nodeA, nodeB, cost)
        if shortest_path:
            duration = random.randint(1, 5)
            network.accept_demand(duration, shortest_path, cost)
            
        network.update_network()
        time.sleep(1)
        

