from Graph import Graph
from collections import defaultdict
from constants import METRIC_STEP_SIZE, PRINT_SIZE, EXEMPT_TERMS


class Perturbation():
    """
    Represents a perturbation process on a graph. Nodes are removed from the graph 
    until it's empty, and metrics are updated at each step.
    
    Attributes:
    -----------
    graph : Graph
        The graph on which perturbations will be performed.
    """

    def __init__(self, task_id: int, graph: Graph, save_nodes: bool, metric_step_size: METRIC_STEP_SIZE, rng) -> None:
        """
        Initializes the Perturbation with a graph and optional settings.
        
        Parameters:
        -----------
        id : int
            Identifier for the perturbation.
        graph : Graph
            The graph on which perturbations will be performed.
        save_nodes : bool, optional
            Flag to track nodes during perturbations. Not intended for simulations. Default is False.
        metric_step_size : int, optional
            The step size for computing metrics. Default is 50.
        """
        
        self.task_id = task_id
        self.graph = graph
        self.metric_evolution = {}
        self.save_nodes = save_nodes
        self.node_evolution = {'removal_type': [], 'node': []}
        self.metric_step_size = metric_step_size
        self.rng=rng

    def run(self) -> None:
        """
        Executes the perturbation process on the graph. At each step:
        1. Metrics are computed for the first node and then every n nodes.
        2. A node is selected for removal.
        3. The chosen node and any dependent nodes are removed from the graph.
        
        If the `save_nodes` flag is enabled, the nodes removed during each perturbation step are recorded.
        Progress updates are printed for every 1000 nodes removed.
        """
        # Print a message indicating the perturbation process has started
        print(">>> perturbation", self.task_id, "started")

        # Initialize a counter to keep track of nodes removed
        node_count = 0

        # define current_nodes
        # Continue the process until the graph is empty
        # while self.graph.size() > 0:

        #while self.graph.size() >= FEEDING_GROUPS:
        while any(node not in EXEMPT_TERMS for node in self.graph.nx_graph.nodes):

            # Compute metrics for the first node and every n nodes
            if node_count == 0 or node_count % self.metric_step_size == 0:
                computed_metrics = self.graph.compute_metrics()
            else:
                computed_metrics = {}

            # Choose a node for removal
            node = self.graph.choose_node()
            # Update the metric evolution
            self._update_metric_evolution(computed_metrics)
            # Remove the chosen node and its dependents from the graph
            dependents = self.graph.remove_node_and_dependents(node)

            # If saving nodes is enabled, record node removal information
            if self.save_nodes:
                # Append "primary" to the removal type list
                self.node_evolution['removal_type'].append("primary")
                # Append the chosen node to the node list
                self.node_evolution['node'].append(node)
                # If there are dependents, append "secondary" for each and add them to the node list
                if len(dependents) > 0:
                    self.node_evolution['removal_type'].extend(["secondary"] *
                                                               len(dependents))
                    self.node_evolution['node'].extend(
                        dependent_node for dependent_node in dependents)

            # Print progress updates for every 1000 nodes removed
            if self.graph.size() % PRINT_SIZE == 0:
                print("id:", self.task_id, "-> size:", self.graph.size())

            # Increment the node count
            node_count += 1

            # get new node list for the next iteration
            # current_nodes = list(self.graph.nodes())

    def _update_metric_evolution(self, computed_metrics: dict) -> None:
        """
        Updates the metric evolution dictionary with the computed metrics.
        
        Parameters:
        -----------
        computed_metrics : dict
            The metrics computed at the current step.
        """
        for key, value in computed_metrics.items():
            self.metric_evolution.setdefault(key, []).append(value)

    def get_metric_evolution(self) -> dict:
        """
        Returns the metric evolution dictionary.

        Returns:
        --------
        dict
            The metric evolution.
        """
        #TO DO: if save_nodes=T, dictionary not transposed! it's fine, we don't need the save infos at the moment
        if self.save_nodes:
            return {
                'metric_evolution': self.metric_evolution,
                'node_evolution': {
                    'node': self.node_evolution['node'],
                    'removal_type': self.node_evolution['removal_type']
                }
            }
        else:
            #print("Metric Evolution Data:", self.metric_evolution)  # Add this line for debugging
            return self.metric_evolution
