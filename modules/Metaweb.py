import pandas as pd
import numpy as np
import networkx as nx
from enum import Enum
from constants import BOOTSTRAP_SIZE, SOURCE_COL, TARGET_COL, ALL_SPECIES_AND_FOOD_GROUPS

class MetawebProcessor:
    """
    Utility class for adding and removing nodes from the given metaweb.
    The rules for doing so are based on information stored in the datasets passed to the MetawebProcessor.
    """

    def __init__(self, rng, edge_df=None):
        self.rng = rng
        self.edge_df = edge_df
        self.node_attributes = pd.read_csv(ALL_SPECIES_AND_FOOD_GROUPS)

    def bootstrap_samples(self, edge_df: pd.DataFrame, rng=None, frac=BOOTSTRAP_SIZE) -> pd.DataFrame:
        # Create a directed graph from the edge DataFrame
        self.edge_df = edge_df.sort_values(by=[SOURCE_COL, TARGET_COL])
        S = nx.from_pandas_edgelist(self.edge_df, source=SOURCE_COL, target=TARGET_COL, create_using=nx.DiGraph())
        S = nx.reverse(S)

        def classify_trophic_categories(graph):
            # Initialize dictionaries to hold species by trophic level
            trophic_categories = {"Basal": [], "Primary": [], "Secondary": [], "Omnivores": []}
            
            basal_species = [node for node in graph.nodes() if graph.in_degree(node) == 0]
            trophic_categories["Basal"] = basal_species

            all_species = set(graph.nodes())
            non_basal_species = all_species - set(basal_species)
            
            for node in non_basal_species:
                predecessors = set(graph.predecessors(node))
                
                if predecessors.issubset(basal_species):
                    # Primary consumers feed exclusively on Basal species
                    trophic_categories["Primary"].append(node)
                elif not predecessors.isdisjoint(basal_species) and not predecessors.issubset(basal_species):
                    # Omnivores consume both Basal and non-Basal
                    trophic_categories["Omnivores"].append(node)
                else:
                    # Secondary consumers feed exclusively on non-Basal species
                    trophic_categories["Secondary"].append(node)
            
            trophic_categories["Primary"] += trophic_categories["Omnivores"]
            trophic_categories["Secondary"] += trophic_categories["Omnivores"]
                      
            for category, species_list in trophic_categories.items():
                trophic_categories[category] = sorted(species_list)
            
            return trophic_categories
        
        
        def connect_upstream(graph, downstream_nodes, upstream_category, upstream_frac):
            # Initialize a set to keep track of the selected upstream nodes.
            selected_upstream = set()

            # Iterate over each downstream node provided in the list.
            for downstream_node in downstream_nodes:
                # Generate a list of potential connections by checking each successor of the downstream node.
                # Ensure this list is sorted to maintain consistent order. Filter out any nodes that are already selected
                # or not in the specified trophic category or the omnivores category.
                potential_connections = sorted([
                    neighbor for neighbor in sorted(graph.successors(downstream_node))
                    if (neighbor in trophic_categories[upstream_category] or neighbor in trophic_categories["Omnivores"]) and
                    neighbor not in selected_upstream
                ])

                # If there are any potential connections left and the desired fraction of upstream nodes has not been reached,
                # select one randomly and add it to the set of selected upstream nodes.
                if potential_connections and len(selected_upstream) < upstream_frac:
                    selected_node = self.rng.choice(potential_connections)
                    selected_upstream.add(selected_node)

            # After trying to select nodes directly connected to the downstream nodes,
            # calculate if more nodes are needed to meet the desired fraction (upstream_frac).
            additional_needed = upstream_frac - len(selected_upstream)
            
            # If additional nodes are needed,
            if additional_needed > 0:
                # Determine which nodes are available for selection by removing the already selected nodes
                # from the set of all nodes in the specified trophic category. Sort this list to ensure consistent order.
                available_upstream = sorted(list(set(trophic_categories[upstream_category]) - selected_upstream))
                
                # If there are available nodes left for selection,
                if available_upstream:
                    # Select the needed number of additional nodes randomly without replacement.
                    # This ensures no duplicates and adheres to the specified fraction.
                    # Note: Adjust this line if self.rng.choice does not support 'size' and 'replace' arguments.
                    additional_selected = self.rng.choice(available_upstream, size=min(additional_needed, len(available_upstream)), replace=False)
                    # Update the set of selected nodes with the additional selections.
                    selected_upstream.update(additional_selected)

            # Return the final list of selected upstream nodes.
            return list(selected_upstream)



        
        trophic_categories = classify_trophic_categories(S)

        bas_frac = int(frac * len(trophic_categories['Basal']))
        
        prim_frac = int(frac * len(trophic_categories['Primary']))-int(frac * len(trophic_categories['Omnivores']))
        top_frac = int(frac * len(trophic_categories['Secondary']))

        # Your existing code here
        sampled_basal = np.sort(self.rng.choice(trophic_categories['Basal'], bas_frac, replace=False))
        sampled_primary = np.sort(connect_upstream(S, sampled_basal, "Primary", prim_frac))
        sampled_secondary = np.sort(connect_upstream(S, sampled_primary, "Secondary", top_frac))

        # Convert numpy arrays to lists if not already lists
        sampled_secondary_list = sampled_secondary.tolist() if isinstance(sampled_secondary, np.ndarray) else sampled_secondary
        sampled_primary_list = sampled_primary.tolist() if isinstance(sampled_primary, np.ndarray) else sampled_primary
        sampled_basal_list = sampled_basal.tolist() if isinstance(sampled_basal, np.ndarray) else sampled_basal

        # Now concatenate the lists
        all_sampled_nodes = set(sampled_secondary_list + sampled_primary_list + sampled_basal_list)

        B = S.subgraph(all_sampled_nodes).copy()

        isolated_nodes = [node for node in B.nodes() if B.in_degree(node) == 0 and B.out_degree(node) == 0]
        all_sampled_nodes -= set(isolated_nodes)

        #we drop isolated_nodes from all_sampled_nodes
        # Create a new edge DataFrame from the sampled nodes
        self.edge_df = self.edge_df[(self.edge_df[SOURCE_COL].isin(all_sampled_nodes)) & (self.edge_df[TARGET_COL].isin(all_sampled_nodes))]

        return self.edge_df
    
    def subset_by_habitat(self, edge_df: pd.DataFrame, habitat: str) -> pd.DataFrame:
            # Filter nodes based on habitat
            nodes_in_habitat = self.node_attributes[self.node_attributes['Habitat'].str.contains(habitat, na=False)]['Taxon']
            
            # Filter the edges based on the nodes in the specified habitat
            self.edge_df = edge_df[(edge_df[SOURCE_COL].isin(nodes_in_habitat)) & (edge_df[TARGET_COL].isin(nodes_in_habitat))]
            
            return self.edge_df

class ProcessingStrategy(Enum):
    """
    Stores different strategies that can be used to process the metaweb,
    before being used to create the graph.
    """

    USE_AS_IS = "USE_AS_IS"
    BOOTSTRAP = "BOOTSTRAP"
    HABITAT_SUBSETTING = "HABITAT_SUBSETTING"


class Metaweb:
    """
    Stores the metaweb and provides functionality for adding and removing links.
    The procedures for adding and removing links are implemented by the MetawebProcessor.
    """

    def __init__(self, csv: str, usecols: list) -> None:
        self.edges = pd.read_csv(csv, usecols=usecols)

    def get_edges(self) -> pd.DataFrame:
        return self.edges

    def setup(self, strategy: ProcessingStrategy, data_processor: MetawebProcessor, rng=None, habitat=None) -> None:
        if strategy == ProcessingStrategy.BOOTSTRAP:
            self._bootstrap_samples(data_processor, rng=rng)
        elif strategy == ProcessingStrategy.HABITAT_SUBSETTING and habitat is not None:
            self._subset_by_habitat(data_processor, habitat)
        else:
            # Default to using as is
            pass

    def _bootstrap_samples(self, data_processor: MetawebProcessor, rng=None):
        self.edges = data_processor.bootstrap_samples(self.edges, rng=rng)

    def _subset_by_habitat(self, data_processor: MetawebProcessor, habitat: str):
        self.edges = data_processor.subset_by_habitat(self.edges, habitat)
