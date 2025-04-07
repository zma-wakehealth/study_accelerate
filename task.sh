#/bin/bash

echo "i am in $(hostname)"
echo "my machine id is $SLURM_PROCID"

accelerate launch --config_file config_${SLURM_PROCID}.yaml test2.py