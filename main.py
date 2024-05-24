import numpy as np
import random
import matplotlib.pyplot as plt
import networkx as nx
from network import Network
from tqdm import tqdm
import argparse

                
def shortest_path_brute(G, start_node, end_node, resources):
    """
    Finds the shortest path in a graph G from start_node to end_node, considering only paths 
    where the weight of each edge is greater than or equal to the given resources. It does so by
    brute force (evaluating all possible paths from start_node to end_node and filtering out the
    invalid ones). If no valid path is found, it returns None.

    Parameters:
    - G (networkx.Graph): The graph in which to find the shortest path.
    - start_node: The starting node of the path.
    - end_node: The ending node of the path.
    - resources: The resources required by the demand.

    Returns:
    - list or None: The shortest path from start_node to end_node, or None if no valid path is found.
    """
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
    
    # If the network is not given, we create a random one
    if args.matrix:
        network = Network(args.N, matrix = args.matrix)
    else:
        network = Network(args.N)
    
    # Iterate through the number of demands, generating them randomly
    for i in tqdm(range(args.demands)):
        nodeA = random.randint(0,network.nodes-1)
        nodeB = random.randint(0,network.nodes-1)
        while nodeA == nodeB:
            # We don't want the same node for both start and end
            nodeB = random.randint(0,network.nodes-1)
        resources = random.randint(args.resources - 2, args.resources + 2)
        
        #Find the shortest path with minimum resources
        shortest_path = shortest_path_brute(network.graph, nodeA, nodeB, resources)
        
        # If it exists, we accept the demand else, we reject it.
        if shortest_path:
            duration = random.randint(args.duration - 2 , args.duration + 2)
            network.accept_demand(duration, shortest_path, resources)
        else:
            # For experimentation
            network.accept_demand(0, None, resources)
            
        # Time ticks and the network is updated
        network.update_network()

    network.save_experiment(args.sim)
    
    # When we do a more complex simualtion, each experiment is saved in a row of a csv file
    if args.sim:
        with open("simulation.csv", "a") as f:
            f.write(f"{args.resources},{args.duration},{network.acceptance_ratio}\n")
        


