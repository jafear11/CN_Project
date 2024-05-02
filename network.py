import numpy as np
import random
import matplotlib.pyplot as plt
import networkx as nx

class Network:
    def __init__(self, nodes = 15):
            """
            Initializes a Graph object.

            Parameters:
            - nodes (int): The number of nodes in the graph. Defaults to a random integer between 10 and 15.

            Attributes:
            - nodes (int): The number of nodes in the graph.
            - adjacency_matrix (list): The adjacency matrix representing the graph.
            - graph (list): The graph represented as a list of lists.
            - demands (dict): A dictionary to store demands.
            - time (int): The current time.
            """
            self.nodes = nodes
            self.adjacency_matrix = self.generate_adjacency_matrix(nodes)
            self.graph = self.graph_from_adjacency_matrix()
            self.demands = {}
            self.time = 0
        
    def generate_adjacency_matrix(self, nodes):
        """
        Generates an adjacency m
        Generates an adjacency matrix for a graph with the given number of nodes.

        Parameters:
        - nodes (int): The number of nodes in the graph.

        Returns:
        - adjacency_matrix (numpy.ndarray): The generated adjacency matrix.

        The adjacency matrix is a square matrix of size (nodes, nodes) where each element represents
        the weight of the edge between two nodes. If there is no edge between two nodes, the weight
        is set to 0. The weights are randomly assigned based on a probability of 0.3. If an edge is
        assigned, the weight is a random integer between 3 and 15. If a node has no outgoing edges,
        a random outgoing edge is added to ensure connectivity.

        Note: This method requires the numpy library to be imported.
        """
        adjacency_matrix = np.zeros((nodes, nodes))

        for i in range(nodes):
            for j in range(i+1, nodes):
                if random.random() <= 0.3:
                    adjacency_matrix[i][j] = adjacency_matrix[j][i] = random.randint(3,15)
            if np.sum(adjacency_matrix[i]) == 0:
                adjacency_matrix[i][random.randint(0, nodes-1)] = random.randint(3,15)
        return adjacency_matrix
    
    def graph_from_adjacency_matrix(self):
        """
        Creates a graph object from the given adjacency matrix.

        Returns:
        - G: A graph object representing the adjacency matrix.

        """
        G = nx.Graph()
        for i in range(len(self.adjacency_matrix)):
            for j in range(i+1, len(self.adjacency_matrix)):
                if self.adjacency_matrix[i][j] != 0:
                    G.add_edge(i, j, weight=self.adjacency_matrix[i][j]) 
        return G

    def draw(self):
        """
        Draws the graph using the spring layout algorithm and displays it.
        
        """
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True)
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)
        plt.plot()
        return None
    
    def accept_demand(self, duration, path, cost):
        """
        Accepts a demand by updating the graph's edge weights and storing the demand information in
        a tuple of (duration, path, cost).

        Args:
            path (list): The path representing the demand.
            cost (float): The cost associated with the demand.
            duration (float): The duration of the demand.

        Returns:
            None
        """
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            if self.graph.has_edge(u, v):
                self.graph[u][v]['weight'] -= cost

        # Tuple of duration, path, cost
        demand = (duration, path, cost)
        self.demands[self.time] = demand
    
    def release_demand(self, demand, time):
        """
        Increases the weight of edges in the graph based on the cost of a given demand, since the duration
        specified for that demand has expired.

        Parameters:
        - demand: A tuple containing the demand information. It should have the following structure:
                  (duration, path, cost)
        - time: The time at which the demand was accepted.

        Returns:
        None
        """
        _, path, cost = demand
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            if self.graph.has_edge(u, v):
                self.graph[u][v]['weight'] += cost
        del self.demands[time]
    
    def update_network(self):
            """
            Updates the network by decrementing the duration of active demands by 1.
            If a demand's duration reaches 1, it is released from the network. Also time
            passed is incremented by 1.
            """
            self.time += 1
            keys_to_delete = []
            for key in list(self.demands.keys()):
                duration, path, cost = self.demands[key]
                self.demands[key] = (duration - 1, path, cost)
                if duration == 1:
                    keys_to_delete.append(key)

            for key in keys_to_delete:
                self.release_demand(self.demands[key], key)