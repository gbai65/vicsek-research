# Predicting Order-Disorder Phase Transitions with Machine Learning in the Vicsek Model

This is the project repository for the Predicting Order-Disorder Phase Transitions in the Vicsek Model project. In this repository, code for execution and supplementary documents are included in /code and /docs, respectively.

## Description

In this study, we use machine learning to classify and interpolate the phase structure of the Vicsek flocking model across the three-dimensional parameter space (η, ρ, v0). We construct a dataset of simulated parameter points and characterize each point using long-time dynamical observables. These observables are then used as inputs to a K-Means clustering procedure, which assigns each point to a disorder, order, or coexistence phase. Using these clustered labels, we train a neural network classifier to learn the mapping from model parameters to phase behavior, achieving a classification accuracy of 0.92. The resulting phase map resolves a narrow coexistence region separating the ordered and disordered phases and extends the inferred phase boundaries beyond the originally sampled simulation points. More broadly, this approach provides a systematic way to convert sparse simulation data into a global phase diagram for collective-motion models.

## Getting Started

The code in this project uses a number of machine learning libraries including, but not limited to, Scikit-Learn, PyTorch, NumPy, Matplotlib, etc. "module load ml" will install all necessary dependencies on the TJHSST Supercomputer Cluster.

### Executing program

In order to run the program, use the /code/runtime subsystem. The vicsek.cpp file contains code for the numbers-only C++ version of the simulation, and the bash files can be used to manipulate the execution of this program. The vicsek.py file contains Python code for the animated version of the simulation, which was used for visualization for an audience when presenting. The /code/"slurm runtime" folder is used for execution on the TJHSST Supercomputer Cluster with the Job Composer.
