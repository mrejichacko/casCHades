from abc import ABC, abstractmethod
import networkx as nx
import pandas as pd
from constants import ALL_SPECIES_AND_FOOD_GROUPS
from constants import EXEMPT_TERMS
from enum import Enum
import numpy as np


class AttackStrategy(ABC):
    """
    Abstract base class for attack or perturbation strategies on a graph.
    Derived classes should define methods to categorize or select nodes in the graph 
    based on specific criteria or configurations.
    """

    @abstractmethod
    def setup_attack_strategy(self, nx_graph: nx.DiGraph) -> None:
        """
        Abstract method to setup the attack strategy for the given graph.
        
        Parameters:
        -----------
        nx_graph : nx.DiGraph
            The directed graph for which the attack strategy is to be set up.
        """
        pass

    @abstractmethod
    def choose_node(self, nx_graph: nx.DiGraph, rng) -> str:
        pass

    def notify_nodes(self, nodes: set) -> None:
        """
        Notifies the attack strategy about nodes that have been removed from the graph. 
        The attack strategy can then adjust its internal state accordingly, if required. 
        For example, the Sequential strategy would remove these nodes from its list of 
        sorted nodes, ensuring they are not selected for perturbation in future steps.

        Note:
        - The default behavior in the base class (AttackStrategy) is to do nothing (pass).
        - The Sequential strategy overrides this method to provide custom behavior.

        Parameters:
        -----------
        nodes : set
            A set of nodes that have been removed from the graph.
        """
        pass


class Random(AttackStrategy):
    """
    Represents a random attack strategy on the graph.
    Nodes are chosen randomly for perturbation.
    """
    def __init__(self, exempt_terms: set = EXEMPT_TERMS, rng=None):
        self.exempt_terms = exempt_terms
        self.rng=rng     

    def setup_attack_strategy(self, nx_graph: nx.DiGraph) -> None:
        """
        No setup required for the random strategy.
        """
        pass

    
    def choose_node(self, nx_graph: nx.DiGraph, rng) -> str:
        """
        Chooses a node randomly from the graph.
        
        Parameters:
        -----------
        nx_graph : nx.DiGraph
            The directed graph from which a node is to be chosen.
        
        Returns:
        --------
        str
            The chosen node.
        """

        eligible_nodes = [node for node in nx_graph.nodes() if node not in self.exempt_terms]

        if not eligible_nodes:
            print("No eligible nodes found. Exiting.")
            return None  # No eligible nodes left
        
        return self.rng.choice(eligible_nodes)

class Rare(AttackStrategy):
    def __init__(self, exempt_terms: set = EXEMPT_TERMS, rng=None):
        self.exempt_terms = exempt_terms
        self.species_df = pd.read_csv(ALL_SPECIES_AND_FOOD_GROUPS, usecols=['Taxon', 'Count'])
        self.rng = rng

    def setup_attack_strategy(self, nx_graph: nx.DiGraph) -> None:
        """
        No setup required for the random strategy.
        """
        pass

    def _update_probabilities(self, nx_graph: nx.DiGraph) -> None:
        # Filter to include only nodes in the graph and not exempt
        filtered_df = self.species_df[
            self.species_df['Taxon'].isin(nx_graph.nodes) & 
            ~self.species_df['Taxon'].isin(self.exempt_terms) &
            ~self.species_df['Count'].isna()
        ]

        # Calculate and normalize probabilities
        inverse_counts = 1 / filtered_df['Count']
        total_inverse_count = sum(inverse_counts)
        probabilities = inverse_counts / total_inverse_count

        # Assign probabilities to nodes in the graph
        for specie, prob in zip(filtered_df['Taxon'], probabilities):
            nx_graph.nodes[specie]['Count_p'] = prob

    def choose_node(self, nx_graph: nx.DiGraph, rng) -> str:
        # Ensure probabilities are up-to-date
        self._update_probabilities(nx_graph)

        # Get eligible nodes and their probabilities
        eligible_nodes = [(node, nx_graph.nodes[node]['Count_p']) for node in nx_graph.nodes 
                          if node not in self.exempt_terms and 'Count_p' in nx_graph.nodes[node]]

        if not eligible_nodes:
            print("No eligible nodes found. Exiting.")
            return None

        nodes, probabilities = zip(*eligible_nodes)
        return self.rng.choice(nodes, p=probabilities)

    def notify_nodes(self, removed_nodes: set) -> None:
        # This method might not be needed if _update_probabilities is called in choose_node
        pass


class Common(AttackStrategy):
    def __init__(self, exempt_terms: set = EXEMPT_TERMS, rng=None):
        self.exempt_terms = exempt_terms
        self.species_df = pd.read_csv(ALL_SPECIES_AND_FOOD_GROUPS, usecols=['Taxon', 'Count'])
        self.rng = rng

    def setup_attack_strategy(self, nx_graph: nx.DiGraph) -> None:
        """
        No setup required for the random strategy.
        """
        pass

    def _update_probabilities(self, nx_graph: nx.DiGraph) -> None:
        # Filter to include only nodes in the graph and not exempt
        filtered_df = self.species_df[
            self.species_df['Taxon'].isin(nx_graph.nodes) & 
            ~self.species_df['Taxon'].isin(self.exempt_terms) &
            ~self.species_df['Count'].isna()
        ]

        # Directly use the counts as probabilities
        total_count = sum(filtered_df['Count'])
        probabilities = filtered_df['Count'] / total_count

        # Assign probabilities to nodes in the graph
        for specie, prob in zip(filtered_df['Taxon'], probabilities):
            nx_graph.nodes[specie]['Count_p'] = prob


    def choose_node(self, nx_graph: nx.DiGraph, rng) -> str:
        # Ensure probabilities are up-to-date
        self._update_probabilities(nx_graph)

        # Get eligible nodes and their probabilities
        eligible_nodes = [(node, nx_graph.nodes[node]['Count_p']) for node in nx_graph.nodes 
                          if node not in self.exempt_terms and 'Count_p' in nx_graph.nodes[node]]
        
        # TO DO: When EXEMPT_TERMS are set to zero, they can be removed but they don't have Counts so there's an error. So only run these if either EXEMPT terms are excluded, OR make a metaweb without the feeding guilds at all

        if not eligible_nodes:
            print("No eligible nodes found. Exiting.")
            return None

        nodes, probabilities = zip(*eligible_nodes)
        return self.rng.choice(nodes, p=probabilities)

    def notify_nodes(self, removed_nodes: set) -> None:
        # This method might not be needed if _update_probabilities is called in choose_node
        pass

class ThreatenedHabitats(AttackStrategy):
    """
    Represents an attack strategy based on threatened habitats.
    Nodes (species) residing in threatened habitats are chosen based on their respective probabilities.
    """

    def __init__(self, threatened_habitats: list, min_probability: int = 0.1, exempt_terms: set = EXEMPT_TERMS, rng=None):
        """
        Initializes the ThreatenedHabitats attack strategy.

        Parameters:
        -----------
        threatened_habitats : list
            List of habitats that are considered threatened.
        min_probability : int, optional
            Minimum probability for a habitat to be chosen. Default is 0.05.
        """
        self.threatened_habitats = threatened_habitats
        self.min_probability = min_probability
        self.buckets = {}
        self.exempt_terms = exempt_terms
        self.rng = rng

    def setup_attack_strategy(self, nx_graph: nx.DiGraph) -> dict:

        species_df = pd.read_csv(ALL_SPECIES_AND_FOOD_GROUPS, usecols=['Taxon', 'Habitat'])
        self._set_habitats(nx_graph, species_df)

        # Step 1: Attach proportion to nodes and add to proportion to set of proportions
        proportions = set()
        for node, data in nx_graph.nodes(data=True):
            habitats = [habitat.strip() for habitat in data.get('Habitat', [])]  # Stripping whitespaces
            
            threatened_count = sum(1 for habitat in habitats if habitat in self.threatened_habitats)
            proportion = threatened_count / len(habitats) if habitats else 0.0
            nx_graph.nodes[node]["Bucket"] = str(proportion)

            proportions.add(proportion)

        # Step 2: Create buckets dictionary to return
        buckets = {}
        for prop in proportions:
            buckets[str(prop)] = prop

        # Step 3: Retrieve smallest proportion
        min_proportion = min(buckets.values())

        # Step 4: Compute x using the smallest proportion
        # first dynamically recalculate min_probability
        # Calculate the number of species in the graph
        num_species = nx_graph.number_of_nodes()

        # Compute min_probability using the background extinction rate and the number of species
        self.min_probability = self.min_probability / 1_000_000 * num_species
        #print(num_species)
        #print(self.min_probability)

        n = len(proportions)
        s = sum(proportions)
        x = self.min_probability*s / (1 - self.min_probability*n) - min_proportion * (1 - self.min_probability*n)

        # Step 5: Compute denominator for normalizing to probability
        proportions.discard(100) # remove fake proportion before computing
        denominator = sum(proportion + x for proportion in proportions)

        # Step 5: Update proportions
        buckets = {bucket: (prop + x) / denominator for bucket, prop in buckets.items()}

        # Step 6: Set buckets
        self.buckets = buckets


    def _set_habitats(self, nx_graph: nx.DiGraph, species_df: pd.DataFrame) -> None:

        for _, row in species_df.iterrows():
            specie = row['Taxon']
            habitat_list = row['Habitat'].split(";")
            
            if specie in list(nx_graph.nodes).copy():
                nx_graph.nodes[specie]['Habitat'] = habitat_list



    def choose_node(self, nx_graph: nx.DiGraph, rng) -> str:
        chosen_bucket = self._choose_bucket()
        eligible_nodes = [node for node, data in nx_graph.nodes(data=True) if data.get('Bucket') == chosen_bucket and node not in self.exempt_terms]
        
        if not eligible_nodes:
            print(f"No nodes found for bucket {chosen_bucket}. Removing bucket.")
            del self.buckets[chosen_bucket]  # Remove the bucket from the dictionary
            
            # Normalize the remaining probabilities
            total_probability = sum(self.buckets.values())
            for key in self.buckets:
                self.buckets[key] /= total_probability

            return self.choose_node(nx_graph, rng)  # Recursively choose another node
        return self.rng.choice(eligible_nodes)

    
    def _choose_bucket(self) -> str:
        buckets = list(self.buckets.keys())
        probabilities = list(self.buckets.values())
        return self.rng.choice(buckets, p=probabilities)


class Sequential(AttackStrategy):
    """
    Represents a sequential attack strategy on the graph.
    Nodes are chosen based on a specific metric, in decreasing order of their values.
    """

    class SortBy(Enum):
        """
        Enumeration for the different metrics based on which nodes can be sorted.
        """
        DEGREE = nx.degree_centrality
        IN_DEGREE = nx.in_degree_centrality
        OUT_DEGREE = nx.out_degree_centrality
        CLOSENESS = nx.closeness_centrality
        BETWEENNESS = nx.betweenness_centrality
        EDGE_BETWEENNESS = nx.edge_betweenness_centrality
        TROPHIC_LEVELS = nx.trophic_levels

    def __init__(self, metric: SortBy) -> None:
        self.metric = metric
        self.sorted_nodes = []


    def setup_attack_strategy(self, nx_graph: nx.DiGraph) -> None:
        metric_values = self.metric(nx_graph)
        self.sorted_nodes = sorted(metric_values, key=metric_values.get, reverse=True)


    def choose_node(self, nx_graph: nx.DiGraph) -> str:
        return self.sorted_nodes.pop(0)
    

    def notify_nodes(self, nodes: set) -> None:
        """
        Takes out secondary removals from the sorted list of nodes.
        """
        self.sorted_nodes = [node for node in self.sorted_nodes if node not in nodes]


