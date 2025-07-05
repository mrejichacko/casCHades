# Analyses of Regional Food Web Robustness under Habitat Loss

### This repository reproduces the simulations from:
### Reji Chacko, M., Albouy, C., Altermatt, F. et al. Species loss in key habitats accelerates regional food web disruption. <i>Commun Biol</i> 8, 988 (2025). https://doi.org/10.1038/s42003-025-08396-y


## 🌟 **Objective**

The primary objective of this project is to:
- Apply various attack strategies to simulate perturbations.
- Extract results for analysis.

## 📚 **Modules Overview**

### 1. `constants.py`
- Houses constants and configurations used throughout the project.

### 2. `attack_strategy.py`
- Defines various attack strategies for perturbing the graph.
- Includes strategies used in the study, such as: RANDOM, THREATENED_HABITATS, RARE and COMMON
- An additional strategy is provided: SEQUENTIAL, where species can be removed according to their position in the food web

### 3. `metaweb.py`
- The `Metaweb` class resides here, responsible for data acquisition and preprocessing.
- We use USE_AS_IS to use the regional food webs, as they are.
- BOOTSTRAPPING is an alternative option, in which random subsets of the regional food web are created, but has not been used in the study
- HABITAT_SUBSETTING is an alternative option, in which the regional multi-habitats are subset to each habitat type, but this has also in the end not used in the study

### 4. `Graph.py`
- This module represents the food web using a directed graph.
- Provides utilities for graph manipulation and metric computation.

### 5. `metric_calculator.py`
- Contains the MetricCalculator class responsible for computing various metrics on the graph.
- For the study, we focused on graph size and the number of WCC, but other metrics can also be calculated

### 6. `Perturbation.py`
- Represents a perturbation process on a graph where nodes are removed, and metrics are updated at each step.

### 7. `Simulation.py`
- The core simulation module that uses different attack strategies on the graph and computes metrics.

### 8. `file_exporter.py`
- This module simply facilitates the naming and saving of result files to the right location.

## 🔍 **Running the Simulations**

### 9. `simulation.py`
- Script to create all combinations of parameters and run simulations
- See the script_params to find which ID (from 0:107999) corresponds to which simulation. For example, simulations 0-999 represent the 1000 simulations of the random scenario, in the EA_Alpines dataset (Eastern Central Alps montane region).

### 10. `run_simulations.sh`
- To run all simulations on a cluster, for example, you will just need to pull the repository and run "sbatch run_simulations.sh" (adjusted for your cluster, of course)
- To run a single simulation, just run "python3 robustness_analysis/simulation.py -i n", replacing n with the number of the simulation ID you wish to run

### Notes

- If you are accessing this folder through git, note that the food webs are too large to upload, please find them here: DOI: 10.16904/envidat.642
- First, copy the food webs into the data/foodwebs folder from Envidat repositories: 02_analyses\data\foodwebs\f75a975
- Second, copy the checklist of species into the data/node_lists from the Envidat repository here: 02_analyses\data\taxa_list.csv
- If you are accessing this folder through the Envidate repository, please note the constants script will need an update of the folder paths reading to the right folders. e.g. 02_analyses\data\foodwebs\f75a975 to data/foodwebs. Please note that they have been kept separate as the simulations scripts are optimised to run on a remote cluster, while the analyses scripts are optimised to run locally.
