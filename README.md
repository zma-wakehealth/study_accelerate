# Purpose
Figure out how to submit accelerate job and other general jobs on the demon cluster which uses slurm.

# Most important bit
srun will run the script ntasks times. For accelerate, I need to run the accelerate launch on each node, so using ntasks-per-node=1 solves all the problems.

# Experiments
1. request 3 nodes on defq: output_exp1.txt; this use --gpus=3, --partition=defq
2. request 2 gpus on the gpu partition, but on 1 node demon120: output_exp2.txt; this use --gpus=2, --partition=gpu, --nodelist=demon120
3. request 2 gpus on the gpu partition, but on 1 node demon121: output_exp2.txt; this use --gpus=2, --partition=gpu, --nodelist=demon121
4. request 2 gpus on the gpu partition, but on 2 nodes: output_exp3.txt;

When running on gpu partition, let's pretend users are already running on some gpus by calling an interactive mode on both demon120 and demon121. Then do sbatch on another terminal, ssh into the node and make sure the sbatch jobs are not running on occupied gpus by the itneractive mode.

It is interesting to see that 

