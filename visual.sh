#!/bin/bash
#SBATCH --account=def-guibault
#SBATCH --gres=gpu:1              # Number of GPUs (per node)
#SBATCH --mem=32G                # memory (per node)
#SBATCH --time=0-00:10            # time (DD-HH:MM)
python visual.py --np 2048 #name of your program
