import numpy as np
import random
import matplotlib.pyplot as plt
import networkx as nx

class Network:
    def __init__(self, nodes = 15, matrix = None):
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
            self.experiment_id = random.randint(0, 1000) 

            if matrix:
                self.adjacency_matrix = np.load(matrix)
                self.nodes = len(self.adjacency_matrix)
            else:
                self.adjacency_matrix = self.generate_adjacency_matrix(nodes)
                self.nodes = nodes
                np.save(f"Results/experiment_{self.experiment_id}_matrix.npy", self.adjacency_matrix)
                
            self.graph = self.graph_from_adjacency_matrix()
            self.backup = self.graph.copy()
            self.pos = nx.spring_layout(self.backup)
            self.demands = {}
            self.time = 0
            # For experimentation
            self.processed_demands = {} 
        
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
        if self.nodes > 10:
            plt.figure(figsize=(12, 12)) 
        else:
            plt.figure()
        nx.draw(self.graph, self.pos, with_labels=True)
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=labels)
        plt.plot()
        return None
    
    def accept_demand(self, duration, path, resources):
        """
        Accepts a demand by updating the graph's edge weights and storing the demand information in
        a tuple of (duration, path, resources).

        Args:
            path (list): The path representing the demand.
            resources (float): The resources associated with the demand.
            duration (float): The duration of the demand.

        Returns:
            None
        """
        if duration != 0:
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                if self.graph.has_edge(u, v):
                    self.graph[u][v]['weight'] -= resources

        # Tuple of duration, path, resources
        demand = (duration, path, resources)
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
        _, path, resources = demand
        if path:
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                if self.graph.has_edge(u, v):
                    self.graph[u][v]['weight'] += resources
                      
        self.processed_demands[time] = self.demands[time]
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
                duration, path, resources = self.demands[key]
                if duration >= 1:
                    self.demands[key] = (duration - 1, path, resources)
                else:
                    keys_to_delete.append(key)
            for key in keys_to_delete:
                self.release_demand(self.demands[key], key)
                
    def save_experiment(self, save = False):
        """
        Saves the experiment results to files.

        This method saves the experiment results as a plot and a CSV file.
        The plot is saved as a PNG file in the "Results" directory with the filename
        "experiment_{experiment_id}.png", where experiment_id is the ID of the current experiment.
        The CSV file is saved as "experiment_{experiment_id}_demands.csv" and contains the accepted demands
        with their corresponding time, duration, path, and required resources.
        
        """
        if not save:
            self.draw()
            plt.savefig(f"Results/experiment_{self.experiment_id}.png")      
        
            # Write accepted demands to a csv file
            with open(f"Results/experiment_{self.experiment_id}_demands.csv", "w") as f:
                f.write("Time,Duration,Path,Resources\n")
                for time, demand in self.processed_demands.items():
                    duration, path, resources = demand
                    f.write(f"{time},{duration},{path},{resources}\n")
                f.close()
        self.statistics(save)
        
        
    def statistics(self, save = False):
        revenue_costs = []
        hops = []
        rejected_demands = 0
        for (_, demand) in self.processed_demands.items():
            if demand[1] is None:
                revenue_costs.append(1)
                rejected_demands += 1
            else:
                revenue_costs.append(1/len(demand[1])) 
                hops.append(len(demand[1]))
        
        acceptance_ratio = (len(self.processed_demands) - rejected_demands) / len(self.processed_demands)
        self.acceptance_ratio = acceptance_ratio
        
        if not save:
            plt.clf()
            plt.figure(figsize=(10.6666666666, 8)) 
            plt.plot(revenue_costs, marker='o', color='blue')
            plt.ylabel('Revenue/Cost')
            plt.xlabel('Demand')
            plt.title('Revenue/Cost for each demand')
            plt.draw()
            plt.savefig(f"Results/experiment_{self.experiment_id}_revenue_cost.png")
        
            with open(f"Results/experiment_{self.experiment_id}_statistics.txt", "w") as f:
                f.write(f"""
Total number of demands: {len(self.processed_demands)}
Number of nodes: {self.nodes}
Number of rejected demands: {rejected_demands}
Acceptance ratio: {format(acceptance_ratio, '.2f')}
Average revenue/cost: {format(np.mean(revenue_costs), '.2f')}
Standard deviation revenue/cost: {format(np.std(revenue_costs), '.2f')}
Average number of hops: {format(np.mean(hops), '.2f')}
                        """)
                f.close() 
            print(f"Experiment {id} saved.")
       
        