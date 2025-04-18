import argparse
import itertools
import os
import sys
import numpy as np

sys.path.append('modules')
print(sys.path)
import constants
from Graph import Graph
from Metaweb import Metaweb, MetawebProcessor, ProcessingStrategy
from attack_strategy import ThreatenedHabitats, Random, Rare, Common
from Simulation import Simulation
from file_exporter import export
import Perturbation

def run_simulation(parameters, task_id):
    print(f'Starting simulation with parameters: {parameters}') 
    adjusted_seed = parameters['ID'] % 1000
    #adjusted_seed = 1
    print(f"Using seed: {adjusted_seed}")

    # Initialize a numpy random generator with the adjusted seed
    rng = np.random.default_rng(adjusted_seed)
    
    # Perturbation.FEEDING_GROUPS = constants.FEEDING_GROUPS_MAPPING[
    #     parameters['CHOSEN_DF']]
    food_web = constants.FOOD_WEB_MAPPING[parameters['CHOSEN_DF']]
    metaweb = Metaweb(food_web,
                      usecols=[constants.SOURCE_COL, constants.TARGET_COL])

    if parameters['type'] == 'random_simulation':
        #adjusted_seed = parameters['ID'] % 1000
        #print(f"Using seed: {adjusted_seed}")
        #random.seed(adjusted_seed)
        #np.random.seed(adjusted_seed)
        #random.seed(parameters['ID'])  # for reproducibility purpose
        attack_strategy = Random(constants.EXEMPT_TERMS, rng=rng)

    elif parameters['type'] == 'threatened_habitats':
        #adjusted_seed = parameters['ID'] % 1000
        #print(f"Using seed: {adjusted_seed}")
        #random.seed(adjusted_seed)
        #np.random.seed(adjusted_seed)
        #random.seed(parameters['ID'])
        #np.random.seed(parameters['ID'])  # for reproducibility purpose
        threatened_habitats = parameters['THREATENED_HABITATS']
        attack_strategy = ThreatenedHabitats(threatened_habitats, rng=rng)
    
    elif parameters['type'] == 'rare':
        #adjusted_seed = parameters['ID'] % 1000
        #print(f"Using seed: {adjusted_seed}")
        #random.seed(adjusted_seed)
        #np.random.seed(adjusted_seed)
        #random.seed(parameters['ID'])  # for reproducibility purpose
        attack_strategy = Rare(constants.EXEMPT_TERMS, rng=rng)

    elif parameters['type'] == 'common':
        #adjusted_seed = parameters['ID'] % 1000
        #print(f"Using seed: {adjusted_seed}")
        #random.seed(adjusted_seed)
        #np.random.seed(adjusted_seed)
        #random.seed(parameters['ID'])  # for reproducibility purpose
        attack_strategy = Common(constants.EXEMPT_TERMS, rng=rng)

    else:
        raise NotImplementedError(
            f'Simulation type \"{parameters["type"]}\" not implemented yet')
        exit

    metaweb_processor = MetawebProcessor(rng=rng)

    metaweb.setup(strategy=ProcessingStrategy.USE_AS_IS,  # Adjust strategy here to US_AS_IS or BOOTSTRAP
                  data_processor=metaweb_processor,
                  rng=rng,
                  habitat=parameters.get('HABITAT', None))  # if not for habitat subsetting, it will just run without the paramet
    edge_df = metaweb.get_edges()

    graph = Graph(attack_strategy,
                  edge_df,
                  source=constants.SOURCE_COL,
                  target=constants.TARGET_COL,
                  rng=rng)
    graph.setup_attack_strategy()
    simulation = Simulation(rng,
                            graph, 
                            k=1,
                            task_id=int(task_id),
                            simulation_type=parameters['type'],
                            chosen_df=parameters['CHOSEN_DF'],
                            habitat=parameters['HABITAT'],
                            threatened_habitats=parameters['THREATENED_HABITATS'],
                            save_nodes=False)
    simulation.run()


def product_dict(**kwargs):
    keys = kwargs.keys()
    for instance in itertools.product(*kwargs.values()):
        yield dict(zip(keys, instance))

script_params = [
    {
        'type': ['random_simulation'],
        'CHOSEN_DF': [
            'EA_Alpines', 'cscf_EA_Alpines', 
            'EA_Lowlands', 'cscf_EA_Lowlands',
            'JU_Alpines', 'cscf_JU_Alpines', 
            'JU_Lowlands', 'cscf_JU_Lowlands',
            'MP_Alpines', 'cscf_MP_Alpines', 
            'MP_Lowlands', 'cscf_MP_Lowlands',
            'NA_Alpines', 'cscf_NA_Alpines', 
            'NA_Lowlands', 'cscf_NA_Lowlands',
            'SA_Alpines', 'cscf_SA_Alpines', 
            'SA_Lowlands', 'cscf_SA_Lowlands',
            'WA_Alpines', 'cscf_WA_Alpines', 
            'WA_Lowlands', 'cscf_WA_Lowlands'
        ],
        'THREATENED_HABITATS': ['None'],
        'HABITAT': ['None'],
        'ID': list(range(1000))
    },
    {
        'type': ['threatened_habitats'],
        'CHOSEN_DF': [
            'EA_Alpines', 'EA_Lowlands', 'JU_Alpines', 'JU_Lowlands',
            'MP_Alpines', 'MP_Lowlands', 'NA_Alpines', 'NA_Lowlands',
            'SA_Alpines', 'SA_Lowlands', 'WA_Alpines', 'WA_Lowlands'
        ],
        'THREATENED_HABITATS': [
            ['Grassland'], ['Wetland'], ['Cropland'], ['Water'], ['Forest']
        ],
        'HABITAT': ['None'],
        'ID': list(range(1000))
    },
    {
        'type': ['rare'], 
        'CHOSEN_DF': [
            'cscf_EA_Alpines', 'cscf_EA_Lowlands', 'cscf_JU_Alpines', 'cscf_JU_Lowlands',
            'cscf_MP_Alpines', 'cscf_MP_Lowlands', 'cscf_NA_Alpines', 'cscf_NA_Lowlands',
            'cscf_SA_Alpines', 'cscf_SA_Lowlands', 'cscf_WA_Alpines', 'cscf_WA_Lowlands'
        ],
        'THREATENED_HABITATS': ['None'],
        'HABITAT': ['None'],
        'ID': list(range(1000))
    },
    {
        'type': ['common'], 
        'CHOSEN_DF': [
            'cscf_EA_Alpines', 'cscf_EA_Lowlands', 'cscf_JU_Alpines', 'cscf_JU_Lowlands',
            'cscf_MP_Alpines', 'cscf_MP_Lowlands', 'cscf_NA_Alpines', 'cscf_NA_Lowlands',
            'cscf_SA_Alpines', 'cscf_SA_Lowlands', 'cscf_WA_Alpines', 'cscf_WA_Lowlands'
        ],
        'THREATENED_HABITATS': ['None'],
        'HABITAT': ['None'],
        'ID': list(range(1000))
    }
]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--task_id', type=int)
    args = parser.parse_args()
    task_id = args.task_id
    parameter_combinations = list(
        itertools.chain.from_iterable([
            list(product_dict(**script_params[i]))
            for i in range(len(script_params))
        ]))
    print(len(parameter_combinations))
    run_simulation(parameter_combinations[task_id], task_id)
