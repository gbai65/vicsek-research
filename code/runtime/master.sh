#!/bin/bash
#SBATCH --job-name=vicsek
#SBATCH -n 5
#SBATCH --time=7-00:00:00
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --partition=compute

srun (runtime/runVicsek.sh)