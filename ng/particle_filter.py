import random

import generators as gu
import likelihoods as lk
import sampler as fs
import numpy as np

class ParticleFilter:
    def __init__(self, particles, prior, outlier = 2):
        self.data = []        
        self.bitwise_data = [0]*gu.RANGE_MAX
        self.particles = np.array(particles)
        self.weights = [1./len(self.particles)] * len(self.particles)
        self.prior = prior
        self.outlier_penalty = outlier

    def update(self, data_point):
        self.data.append(data_point)
        self.bitwise_data[data_point-1] = 1

    def resample(self):
        likelihoods = lk.compute_likelihoods(self.particles, 
                                             self.bitwise_data,
                                             self.outlier_penalty)
        self.weights = likelihoods/sum(likelihoods)
        n = len(self.particles)
        bins = np.cumsum(self.weights)
        self.particles = self.particles[np.digitize(
                np.random.random_sample(n), bins)]
        self.weights[:] = 1./n

    def rejuvenate(self):
        likelihoods = lk.compute_likelihoods(self.particles, 
                                             self.bitwise_data,
                                             self.outlier_penalty)
        self.weights = likelihoods/sum(likelihoods)
        new_samples = fs.rejuvenate_all_arguments(self.particles, self.data)
        new_likelihoods = lk.compute_likelihoods(new_samples, 
                                                 self.bitwise_data,
                                                 self.outlier_penalty)

        priors = np.array([fs.compute_pcfg_prob(p, self.prior) 
                           for p in self.particles])
        new_priors = np.array([fs.compute_pcfg_prob(p, self.prior) 
                               for p in new_samples])
        r = ( new_likelihoods / likelihoods ) * ( priors / new_priors )
        a = np.random.random_sample(len(self.particles))
        self.particles = np.choose(a < r, [self.particles, new_samples])
