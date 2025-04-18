from Perturbation import Perturbation
from Graph import Graph
from file_exporter import export
import shutil
import os
from constants import METRIC_STEP_SIZE

class Simulation():
    """
    Simulates the perturbation process on multiple copies of a graph.
    
    Attributes:
    -----------
    graphs : list
        List of graph copies on which perturbations will be performed.
    perturbations : list
        List of perturbation instances associated with each graph copy.
    metric_evolution : list
        List of metric evolutions for each perturbation.
    """

    def __init__(self, rng,
                 graph: Graph,
                 k: int,
                 task_id: int,
                 simulation_type: str,
                 chosen_df: str,
                 threatened_habitats:str,
                 habitat: str = None, 
                 save_nodes: bool = False) -> None:
        """
        Initializes the Simulation with graph copies and perturbations.
        
        Parameters:
        -----------
        graph : Graph
            The graph on which perturbations will be simulated.
        k : int
            The number of graph copies and perturbations.
        """
        self.task_id = task_id
        self.simulation_type = simulation_type
        self.chosen_df = chosen_df
        self.habitat = habitat
        # self.threatened_habitats = threatened_habitats
        if self.simulation_type == 'threatened_habitats':
            self.threatened_habitats = threatened_habitats
        else:
            self.threatened_habitats = None
        self.graphs = self._create_graph_copies(graph, k)
        self.perturbations = self._create_perturbations(rng, k, save_nodes)
        self.rng = rng

    def _create_graph_copies(self, graph: Graph, k: int) -> list:
        """
        Creates k copies of the provided graph.
        
        Parameters:
        -----------
        graph : Graph
            The graph to be copied.
        k : int
            The number of copies to create.
        
        Returns:
        --------
        list
            A list of graph copies.
        """
        return [graph.copy() for _ in range(k)]

    def _create_perturbations(self, rng, k: int, save_nodes: bool) -> list:
        """
        Creates k perturbations for the graph copies.
        
        Parameters:
        -----------
        k : int
            The number of perturbations to create.
        
        Returns:
        --------
        list
            A list of Perturbation instances.
        """
        return [Perturbation(i, self.graphs[i], save_nodes, METRIC_STEP_SIZE, rng) for i in range(k)]

    def run(self) -> None:
        """
        Runs the simulation 
        """
        print(">>> simulation started")

        #remove_results_dir()

        [
            self._run_perturbation(perturbation)
            for perturbation in self.perturbations
        ]

        print(
            ">>> the simulation has successfully concluded, all perturbations are saved in the results directory"
        )

    def _run_perturbation(self, perturbation: Perturbation) -> dict:
        """
        Helper method to run a single perturbation.
        
        Parameters:
        -----------
        perturbation : Perturbation
            The perturbation instance to run.
        
        Returns:
        --------
        dict
            The metric evolution for the perturbation.
        """
        perturbation.run()
        metrics_evolution = perturbation.get_metric_evolution()
        export_directory = f'results/{self.simulation_type}/{self.chosen_df}'
        if self.simulation_type == 'threatened_habitats':
            # Convert the list of threatened_habitats to a string with the first two letters of each element
            threatened_habitats_str = "".join(word[:2] for word in self.threatened_habitats)
            # Include the count as a prefix to the string
            threatened_habitats_count = len(self.threatened_habitats)
            export_directory = os.path.join(export_directory, f'{threatened_habitats_count}_{threatened_habitats_str}')
            # Include self.threatened_habitat in the directory structure
            #export_directory = os.path.join(export_directory, self.threatened_habitats)
        
        if self.habitat != "None":
            export_directory = os.path.join(export_directory, self.habitat)
            
        export(metrics_evolution, 
               f'perturbation_{self.task_id}', directory=export_directory)
        #print(f'Habitat: {self.habitat}')
        return metrics_evolution

def remove_results_dir() -> None:
    directory_path = "results"
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
