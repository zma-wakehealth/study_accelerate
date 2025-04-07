#!/bin/bash
#SBATCH --time=00:20:00
#SBATCH --job-name=XYZ
#SBATCH --gpus=2                                # this is the simplest form, too many params make the defq complain about
                                                # "Requested node configuration is not available"   
                                                # ideally we would like to put --ntasks-per-node=1 here    
#SBATCH --partition=gpu
#SBATCH --output=output_exp4_echo.txt
#SBATCH --nodelist=demon120,demon121

#SBATCH --nodes=2                               # this is for testing purpose only
#SBATCH --gpus-per-node=1                       # same here

module load cuda-toolkit
source ~/.nlp/bin/activate

echo "Node numbers: $SLURM_NNODES"
echo "GPU numbers: $SLURM_GPUS"
echo "node list: $SLURM_JOB_NODELIST"
echo "number of tasks: $SLURM_NTASKS"           # this will be empty, need to set it in srun

# get the config file for each node
python prepare_config.py

# use ntasks-per-node to make sure only 1 task is run on each node
srun --ntasks-per-node=1 bash task_echo.sh