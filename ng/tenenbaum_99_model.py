import generators as gu
import sampler as fs

import numpy as np

def numbergame_likelihoods(hypotheses, data):
    likelihoods = []
    for h in hypotheses:
        inconsistencies = np.where(np.bitwise_xor(
                np.bitwise_and(h.bitwise, data), data) == 1)[0]
        hyp_len = len(np.nonzero(h.bitwise)[0])
        if hyp_len == 0:
            likelihoods.append(0)
            continue
        if len(inconsistencies) == 0:
            likelihoods.append(1./(hyp_len))
        else:
            likelihoods.append(0)
    return np.array(likelihoods)

class NumbergameModel:
    def __init__(self, data, particles, prior):
        self.data = data
        self.bitwise_data = [0]*gu.RANGE_MAX
        for d in self.data:
            self.bitwise_data[d-1] = 1
        self.particles = np.array(particles)
        self.prior = prior

        likelihoods = numbergame_likelihoods(self.particles, 
                                             self.bitwise_data)
        likelihoods = np.power(likelihoods, len(data))
        priors = np.array([fs.compute_pcfg_prob(p, self.prior) 
                           for p in self.particles])

        joint = np.exp(np.add(np.log(likelihoods), np.log(priors)))
        joint /= sum(joint)
        self.joint = joint
