import numpy as np
import random
import matplotlib.pyplot as plt
import networkx as nx
from network import Network
from tqdm import tqdm
import argparse

                
def shortest_path_brute(G, start_node, end_node, resources):
    try:
        paths = list(nx.all_simple_paths(G, start_node, end_node))
        valid_paths = []
        for path in paths:
            weights = [G[u][v].get('weight', 1) for u, v in zip(path[:-1], path[1:])]
            if all(weight >= resources for weight in weights):
                valid_paths.append((len(path), path))
        if not valid_paths:
            return None
        valid_paths.sort()
        return valid_paths[0][1]
    except nx.NetworkXNoPath:
        """ print("Demand rejected: destination unreachable.") """
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This is the main executable for the project. The configuration parameters are listed below.')
    parser.add_argument('--N', default = 15, type=int, help='Number of nodes')
    parser.add_argument('--demands', default = 100, type=int, help='Number of demands')
    parser.add_argument('--duration', default = 3, type=int, help='Average duration')
    parser.add_argument('--resources', type=int, default = 3, help='Average amount of resources')
    parser.add_argument('--matrix', type=str, default = None, help='Matrix file')
    parser.add_argument('--sim', type=bool, default = False, help='True to run several experiments.')
    args = parser.parse_args()
    
    if args.matrix:
        network = Network(args.N, matrix = args.matrix)
    else:
        network = Network(args.N)
    
    for i in tqdm(range(args.demands)):
        nodeA = random.randint(0,network.nodes-1)
        nodeB = random.randint(0,network.nodes-1)
        while nodeA == nodeB:
            nodeB = random.randint(0,network.nodes-1)
        resources = random.randint(args.resources - 2, args.resources + 2)
        shortest_path = shortest_path_brute(network.graph, nodeA, nodeB, resources)
        if shortest_path:
            duration = random.randint(args.duration - 2 , args.duration + 2)
            network.accept_demand(duration, shortest_path, resources)
        else:
            # For experimentation
            network.accept_demand(0, None, resources)
        network.update_network()

    network.save_experiment(args.sim)
    
    if args.sim:
        with open("simulation.csv", "a") as f:
            f.write(f"{args.resources},{args.duration},{network.acceptance_ratio}\n")
        


