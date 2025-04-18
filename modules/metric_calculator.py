import networkx as nx
from enum import Enum
#import community as community_louvain #only if calculating modularity
from statistics import mean

class Metrics(Enum):
    """
    Enumeration of available graph metrics.
    """
    GRAPH_SIZE = "graph_size"
    #LINKS = "link_size"
    # AVG_IN_DEGREE = "avg_in_degree"
    # AVG_OUT_DEGREE = "avg_out_degree"
    #AVG_TOTAL_DEGREE = "avg_total_degree"
    #NUMBER_OF_WCCS = "number_of_wccs"
    #NUMBER_OF_SCCS = "number_of_sccs"
    MAX_WCC_SIZE = "largest_wcc_size"
    #MAX_SCC_SIZE = "largest_scc_size"
    #WCC_AVG_DIAMETER = "wcc_diameter"
    #SCC_AVG_DIAMETER = "scc_diameter"
    #MODULARITY = "modularity"
    #CONNECTANCE = "density"
    #GCC = "clustering_coefficient"
    #BAS = "fraction_of_basal_species"
    #TOP = "fraction_of_top_species"
    #INT = "fraction_of_intermediate_species"
    #OMNI = "degree_of_omnivory"
    #GEN = "mean_generality"
    #VUL = "mean_vulnerability"



class MetricCalculator():
    """
    Utility class to compute various metrics for directed graphs.
    
    Attributes:
    -----------
    METRICS : list of str
        List of metric method names available in this class.
    """
    
    METRICS = [metric.value for metric in Metrics]
    
    def compute_metrics(self, graph: nx.DiGraph) -> dict:
        """
        Computes all the metrics listed in METRICS for the provided graph.
        
        Parameters:
        -----------
        graph : nx.DiGraph
            The graph for which metrics are to be calculated.
        
        Returns:
        --------
        dict
            Dictionary with metric names as keys and computed values as associated values.
        """
        metric_results = {}
        DECIMAL_POS = 5  # decimal precision
        
        for metric in self.METRICS:
            metric_function = getattr(self, metric)
            metric_results[metric] = round(metric_function(graph), DECIMAL_POS)  
        
        return metric_results
    

    def graph_size(self, graph:nx.DiGraph) -> int:
        return len(graph)
    
    def link_size (self, graph:nx.DiGraph) -> int:
        return graph.number_of_edges()
    
    #IMPORTANT TO NOTE THAT THIS IS NOT A DIRECTED GRAPH
    def modularity(self, graph: nx.DiGraph) -> float:
        def calculate_modularity_louvain(graph: nx.DiGraph):
            # Convert the directed graph to an undirected graph
            undirected_graph = graph.to_undirected()

             # Early return if the graph has no edges
            if undirected_graph.number_of_edges() == 0:
                return 0.0

            # Detect communities using the Louvain method
            partition = community_louvain.best_partition(undirected_graph)

            # Calculate modularity
            modularity = community_louvain.modularity(partition, undirected_graph)
            return modularity

        return calculate_modularity_louvain(graph)
        
    def scc_diameter(self, graph:nx.DiGraph) -> float:
        scc_list = list(nx.strongly_connected_components(graph))
        if not scc_list:
            return float('nan')  # No SCCs

        diameters = []
        for scc in scc_list:
            subgraph = graph.subgraph(scc)
            if subgraph.number_of_nodes() > 1:
                diameters.append(nx.diameter(subgraph))

        if not diameters:
            return float('nan')  # No diameters calculated

        return sum(diameters) / len(diameters)

    def wcc_diameter(self, graph: nx.DiGraph) -> float:
        wcc_list = list(nx.weakly_connected_components(graph))
        if not wcc_list:
            return float('nan')  # No WCCs

        diameters = []
        for wcc in wcc_list:
            subgraph = graph.subgraph(wcc).to_undirected()  # Convert to undirected for WCC
            if subgraph.number_of_nodes() > 1:
                diameters.append(nx.diameter(subgraph))

        if not diameters:
            return float('nan')  # No diameters calculated

        return sum(diameters) / len(diameters)

        

    def avg_in_degree(self, graph: nx.DiGraph) -> float:
        return sum(dict(graph.in_degree()).values()) / len(graph)
    
    
    def avg_out_degree(self, graph: nx.DiGraph) -> float:
        return sum(dict(graph.out_degree()).values()) / len(graph)
    
    
    def avg_total_degree(self, graph: nx.DiGraph) -> float:
        return sum(dict(graph.degree()).values()) / len(graph)

    
    def density(self, graph: nx.DiGraph) -> float: #connectance
        n = len(graph) 
        if n < 2:
            return 0  # or some other value to indicate the graph is too small
        return nx.density(graph)
    

    def largest_wcc_size(self, graph: nx.DiGraph) -> float:
        return len(max(list(nx.weakly_connected_components(graph))))

    
    def largest_scc_size(self, graph: nx.DiGraph) -> float:
        return len(max(list(nx.strongly_connected_components(graph))))
    

    def number_of_wccs(self, graph: nx.DiGraph) -> float:
        return len(list(nx.weakly_connected_components(graph)))
    
    
    def number_of_sccs(self, graph: nx.DiGraph) -> float:
        return len(list(nx.strongly_connected_components(graph)))   
      
    
    def avg_betweenness(self, graph: nx.DiGraph) -> float:
        return sum(dict(nx.betweenness_centrality(graph, normalized=False)).values())
    

    def avg_in_closeness(self, graph: nx.DiGraph) -> float:
        return sum(dict(nx.closeness_centrality(graph, normalized=False)).values())
    

    def avg_shortest_path_lssc(self, graph: nx.DiGraph) -> float:
        lscc = max(nx.strongly_connected_components(graph), key=len)
        subgraph = graph.subgraph(lscc)
        return nx.average_shortest_path_length(subgraph)
    
    def avg_shortest_path_all_scc(self, graph: nx.DiGraph) -> float:
        scc_list = list(nx.strongly_connected_components(graph))
        if not scc_list:
            return float('nan')  # Return NaN if there are no SCCs

        avg_path_lengths = []
        for scc in scc_list:
            subgraph = graph.subgraph(scc)
            # Only calculate if the subgraph has more than one node
            if subgraph.number_of_nodes() > 1:
                avg_path_lengths.append(nx.average_shortest_path_length(subgraph))

        if not avg_path_lengths:
            return float('nan')  # Return NaN if no path lengths were calculated

        return sum(avg_path_lengths) / len(avg_path_lengths)


    def avg_shortest_path_all_wcc(self, graph: nx.DiGraph) -> float:
        wcc_list = list(nx.weakly_connected_components(graph))
        if not wcc_list:
            return float('nan')  # Return NaN if there are no WCCs

        avg_path_lengths = []
        for wcc in wcc_list:
            subgraph = graph.subgraph(wcc).to_undirected() # Convert to undirected for WCC
            # Only calculate if the subgraph has more than one node
            if subgraph.number_of_nodes() > 1:
                avg_path_lengths.append(nx.average_shortest_path_length(subgraph))

        if not avg_path_lengths:
            return float('nan')  # Return NaN if no path lengths were calculated

        return sum(avg_path_lengths) / len(avg_path_lengths)



    def avg_trophic_level(self, graph: nx.DiGraph) -> float:
        return sum(dict(nx.trophic_levels(graph)).values()) / len(graph)
    
   
    def clustering_coefficient(self, graph: nx.DiGraph) -> float:
        return nx.average_clustering(graph, count_zeros=True)
    
    def fraction_of_basal_species(self, graph: nx.DiGraph) -> float:
        """Calculate the fraction of basal species in a directed graph."""
        basal_species = [node for node in graph if graph.in_degree(node) == 0 and graph.out_degree(node) > 0]
        return len(basal_species) / graph.number_of_nodes()

    def fraction_of_top_species(self, graph: nx.DiGraph) -> float:
        """Calculate the fraction of top species in a directed graph."""
        top_species = [node for node in graph if graph.out_degree(node) == 0 and graph.in_degree(node) > 0]
        return len(top_species) / graph.number_of_nodes()

    def fraction_of_intermediate_species(self, graph: nx.DiGraph) -> float:
        """Calculate the fraction of intermediate species in a directed graph.
        
        Intermediate species are defined as any species that are not basal or top species.
        """
        basal_species = [node for node in graph if graph.in_degree(node) == 0 and graph.out_degree(node) > 0]
        top_species = [node for node in graph if graph.out_degree(node) == 0 and graph.in_degree(node) > 0]
        # Intermediate species are now any node not in basal or top categories
        intermediate_species = [node for node in graph if node not in basal_species + top_species]
        
        return len(intermediate_species) / graph.number_of_nodes()

    
    def degree_of_omnivory(self, graph: nx.DiGraph) -> float:
        basal_species = set(node for node in graph if graph.in_degree(node) == 0)
        non_basal_species = set(graph.nodes) - basal_species
        
        omnivores = []
        for node in non_basal_species:
            # Check if the node feeds on at least one basal and one non-basal node
            prey = set(graph.predecessors(node))  # Nodes from which there's an incoming edge to 'node'
            if prey & basal_species and prey & non_basal_species:
                omnivores.append(node)
        
        # Calculate the fraction of omnivores that are not basal
        return len(omnivores) / len(non_basal_species) if non_basal_species else 0


    def mean_generality(self, graph: nx.DiGraph) -> float:
        """
        Calculate the mean generality of species in the network.
        Generality is defined as the average number of prey per predator.
        """
        generalities = [graph.out_degree(node) for node in graph if graph.out_degree(node) > 0]
        return mean(generalities) if generalities else 0

    def mean_vulnerability(self, graph: nx.DiGraph) -> float:
        """
        Calculate the mean vulnerability of species in the network.
        Vulnerability is defined as the average number of predators per prey.
        """
        vulnerabilities = [graph.in_degree(node) for node in graph if graph.in_degree(node) > 0]
        return mean(vulnerabilities) if vulnerabilities else 0

