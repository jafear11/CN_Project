import numpy as np
import random
import matplotlib.pyplot as plt
import networkx as nx
import time
from network import Network
from tqdm import tqdm
import argparse

                
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
            return None
        valid_paths.sort()
        
        """ print(f"Shortest path from node {start_node} and {end_node}: {valid_paths[0][1]}")
        print(f"Total cost: {valid_paths[0][0]}")
        print(f"Cost/Revenue: {valid_paths[0][0] / ((len(valid_paths[0][1]) - 1)*cost)}")
        print(f"Number of hops: {len(valid_paths[0][1]) - 1}") """
        return valid_paths[0][1]
    
    except nx.NetworkXNoPath:
        """ print("Demand rejected: destination unreachable.") """
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Hola hello.')
    parser.add_argument('--N', default = 15, type=int, help='Number of nodes')
    parser.add_argument('--demands', default = 100, type=int, help='Number of demands')
    parser.add_argument('--duration', default = 3, type=int, help='Average dyration')
    parser.add_argument('--cost', type=int, default = 3, help='Average cost')
    parser.add_argument('--matrix', type=str, default = None, help='Matrix file')
    args = parser.parse_args()
    
    if args.matrix:
        network = Network(args.N, matrix = args.matrix)
    else:
        network = Network(args.N)
    
    for i in tqdm(range(args.demands)):
        nodeA = random.randint(0,network.nodes-1)
        nodeB = random.randint(0,network.nodes-1)
        cost = random.randint(args.cost - 2, args.cost + 2)
        shortest_path = shortest_path_brute(network.graph, nodeA, nodeB, cost)
        if shortest_path:
            duration = random.randint(args.duration - 2 , args.duration + 2)
            network.accept_demand(duration, shortest_path, cost)
        else:
            # For experimentation
            network.accept_demand(0, None, cost)
        network.update_network()

    network.save_experiment()


