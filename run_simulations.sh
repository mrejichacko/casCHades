#!/bin/bash

#SBATCH -A es_pelli
#SBATCH -J casCHades
#SBATCH --time=00-24:00:00
#SBATCH --output=log/log_full_fg_removed/simul_%A.out
#SBATCH --error=log/log_full_fg_removed/simul_%A.error
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=8G
#SBATCH --array=0-107  # Adjust the array size accordingly, 0-215 for habitats alone

module load stack 
module load gcc/12.2.0 python/3.11.6

# Calculate the total number of simulations
total_simulations=108000  # n simulations per task, starting from ID 0

# Calculate the number of simulations per task
simulations_per_task=1000

# Calculate the start ID for the current job array task
start_id=$((SLURM_ARRAY_TASK_ID * simulations_per_task))
end_id=$((start_id + simulations_per_task - 1))

# Loop through each task
for ((sim_id=start_id; sim_id<=end_id; sim_id++))
do
    python robustness_analysis/simulation.py -i $sim_id
done