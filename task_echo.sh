#/bin/bash

echo "i am in $(hostname)"
echo "my machine id is $SLURM_PROCID"
echo "slurm gpu is $SLURM_STEP_GPUS"