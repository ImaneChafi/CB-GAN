#!/bin/bash
#SBATCH --account=def-guibault
#SBATCH --gres=gpu:1              # Number of GPUs (per node)
#SBATCH --mem=32G               # memory (per node)
#SBATCH --time=0-00:20            # time (DD-HH:MM)
cd metrics/CD_EMD
cd emd_ && python setup.py build_ext --inplace && cd ..
cd cd && python setup.py build_ext --inplace && cd ..

pwd
cd ..
cd ..

pwd

python train.py --choice preps_miccai --np 2048 --max_epoch 300 #name of your program
