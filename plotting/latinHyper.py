import numpy as np
from scipy.stats import qmc

def generateLHS(n_samples):
    sampler = qmc.LatinHypercube(d=3)
    sample = sampler.random(n=n_samples)
    
    l_bounds = [0, np.log10(0.1), np.log10(0.01)]
    u_bounds = [1, np.log10(2), np.log10(0.5)]

    sample_scaled = qmc.scale(sample, l_bounds, u_bounds)

    sample_scaled[:, 1] = 10**sample_scaled[:, 1]
    sample_scaled[:, 2] = 10**sample_scaled[:, 2]

    return sample_scaled

numSamples = 200
finalSamples = generateLHS(numSamples)

data = np.array(finalSamples)

np.savetxt('LHSpoints.txt', data, fmt='%.8f', delimiter=' ')