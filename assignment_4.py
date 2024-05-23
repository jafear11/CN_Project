import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from network import Network
from main import shortest_path_brute
import imageio.v2 as imageio
import os

if __name__ == "__main__":    
    network = Network(8, "Assignment_4/assignment4_matrix.npy")
    demands = pd.read_csv('Assignment_4/assignment4_demands.csv')
    network.draw()
    plt.savefig(f"Assignment_4/network.png")
    
    accepted = 0
    revenue_cost = []
    for index, row in demands.iterrows():
        nodeA = row['NodeA']
        nodeB = row['NodeB']
        resources = row['Resources']
        duration = row['Duration']
        shortest_path = shortest_path_brute(network.graph, nodeA, nodeB, resources)
        print("Nodes: ", nodeA, " - " , nodeB, f"  |  Resource demand: {resources}" )
        if shortest_path:
            print(f"    Chosen path: {shortest_path} \n")
        else:
            print("     Chosen path: Demand rejected \n")
        if shortest_path:
            network.accept_demand(duration, shortest_path, resources)
            accepted += 1
            revenue_cost.append(1/len(shortest_path))
        else:
            network.accept_demand(0, None, resources)
            revenue_cost.append(1)
        network.update_network()
        network.draw()
        plt.savefig(f"Assignment_4/iteration_{index}.png")
    
    print(f"Accepted demands: {accepted}")
    print(f"Rejected demands: {len(demands) - accepted}")
    print(f"Acceptance ratio: {accepted/len(demands)}")
    print(f"Average revenue/cost: {np.mean(revenue_cost)}")
    
    images = []
    
    for i in range(10):
        filename = os.path.join('Assignment_4', f'iteration_{i}.png')
        images.append(imageio.imread(filename))
    
    imageio.mimsave('Assignment_4/video.mp4', images, fps=1)

    for i in range(10):
        os.remove(f'Assignment_4/iteration_{i}.png')




