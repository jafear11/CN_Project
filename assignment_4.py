import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from network import Network
from main import shortest_path_brute

if __name__ == "__main__":    
    network = Network(8, "Assignment_4/assignment4_matrix.npy")
    demands = pd.read_csv('Assignment_4/assignment4_demands.csv')
    network.draw()
    plt.savefig(f"Assignment_4/network.png")
    
    accepted = 0
    cost_revenue = []
    for index, row in demands.iterrows():
        nodeA = row['NodeA']
        nodeB = row['NodeB']
        cost = row['Cost']
        duration = row['Duration']
        shortest_path = shortest_path_brute(network.graph, nodeA, nodeB, cost)
        
        if shortest_path:
            network.accept_demand(duration, shortest_path, cost)
            accepted += 1
            cost_revenue.append(1/len(shortest_path))
        else:
            network.accept_demand(0, None, cost)
            cost_revenue.append(1)
        network.update_network()
        network.draw()
        plt.savefig(f"Assignment_4/iteration_{index}.png")
    
    print(f"Accepted demands: {accepted}")
    print(f"Rejected demands: {len(demands) - accepted}")
    print(f"Acceptance ratio: {accepted/len(demands)}")
    print(f"Average cost/revenue: {np.mean(cost_revenue)}")
    




