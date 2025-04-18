import networkx as nx
import pandas as pd
from metric_calculator import MetricCalculator
from attack_strategy import AttackStrategy
import copy


class Graph():
    """
    Represents a directed graph with methods to perform various operations like 
    node removal, metric calculation, and more.
    
    Attributes:
    -----------
    nx_graph : NetworkX.DiGraph
        The underlying directed graph representation using NetworkX.
    metrics_calculator : MetricCalculator
        Utility to compute various metrics on the graph.
    metrics_trend : dict
        Stores the trends of metrics computed over operations on the graph.
    """

    def __init__(self, attack_strategy: AttackStrategy, edge_df: pd.DataFrame, source: str, target: str, rng) -> None:
        self.attack_strategy = attack_strategy
        self.metric_calculator = MetricCalculator()
        self.nx_graph = self.load_data(edge_df, source, target)
        self.rng = rng


   
    def load_data(self, edge_df: pd.DataFrame, source: str, target: str) -> nx.DiGraph:
        g = nx.from_pandas_edgelist(edge_df, source=source, target=target, create_using=nx.DiGraph())
        return nx.reverse(g)
    

    def setup_attack_strategy(self) -> None:
        self.attack_strategy.setup_attack_strategy(self.nx_graph)
    
    
    def size(self) -> int:
        return len(self.nx_graph)
    

    def copy(self) -> object:
        return copy.deepcopy(self)


    def compute_metrics(self) -> None:
        return self.metric_calculator.compute_metrics(self.nx_graph)
    

    def choose_node(self) -> str:
        return self.attack_strategy.choose_node(self.nx_graph, self.rng)
    
        
    def remove_node_and_dependents(self, node: str) -> list:
        """
        Removes the specified node from the graph and also removes any dependent nodes 
        that might be affected by this removal (like isolated nodes).
        
        Parameters:
        -----------
        node : str
            The node to be removed.
        
        Returns:
        -----------
        removed_neighbors: list
            The dependent nodes which have been removed.
        """
        k_level_neighbors = set(self.nx_graph.successors(node))
        self.nx_graph.remove_node(node)

        removed_neighbors = set()

        # Explore neighbors level after level
        while len(k_level_neighbors) > 0:

            new_level_neighbors = set()
            removed_neighbors = set()

            # In the worst case the check must be done |k_level_neighbors| times
            for i in range(len(k_level_neighbors)):
                change_flag = False  # flag indicating if any nodes were removed in this loop

                for neighbor in set(k_level_neighbors):  # TODO: check scenario of copying set and without
                    
                    # A node is removed if it does not have any inward edge, if it's isolated, or if it's an isolated self-loop
                    if self.nx_graph.in_degree(neighbor) == 0 or self.nx_graph.degree(neighbor) == 0 or (self.nx_graph.in_degree(neighbor) == 1 and self.nx_graph.has_edge(neighbor, neighbor)):
                        new_level_neighbors.update(set(self.nx_graph.successors(neighbor)))
                        k_level_neighbors.remove(neighbor)
                        removed_neighbors.add(neighbor)
                        self.nx_graph.remove_node(neighbor)

                        change_flag = True
                
                if not change_flag:
                    break

            k_level_neighbors = new_level_neighbors - removed_neighbors

            self._notify_nodes(removed_neighbors)

        return list(removed_neighbors)
        

    def _notify_nodes(self, removed_neighbors: set) -> None: 
        self.attack_strategy.notify_nodes(removed_neighbors)
                