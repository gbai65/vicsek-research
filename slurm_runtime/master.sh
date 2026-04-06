#!/bin/bash
#SBATCH -n 1
#SBATCH --job-name=master.sh
#SBATCH --array=1-5
#SBATCH --time=7-00:00:00
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --partition=compute

chmod +x runVicsek.sh
chmod +x runtime
./runVicsek.sh