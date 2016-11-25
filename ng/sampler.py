import math

import numpy as np
import generators as gu

from numpy.random import random_sample

def pcfg_prob_helper(particle, prior):
    assert(not isinstance(particle, gu.Root))
    
    if isinstance(particle, gu.Operator):
        # every operator has two ways of ordering the operands
        # return probability of choosing the operands
        res = math.log( 
            math.exp( 
                sum([(pcfg_prob_helper(o, prior) +                     # probability of operands' subtrees
                      math.log(prior[particle.__class__][o.__class__])) # prior probability of operand
                     for o in particle.operands])) * 2 )                # ordering
        return res
    else: # is Generator
        # return probability of choosing the arguments
        res = math.log(particle.probability)
        return res

def compute_pcfg_prob(particle, prior):
    # root is special case, need to incorporate probability of choosing root operator
    return math.exp(
        math.log(prior[gu.Root][particle.__class__]) + 
        pcfg_prob_helper(particle, prior))

# http://stackoverflow.com/a/11373929
def weighted_values(values, probabilities, size):
    bins = np.cumsum(probabilities)
    return values[np.digitize(random_sample(size), bins)]

def precompute_samples(n, prior):
    return {
        gu.And : [weighted_values(
                np.array(prior[gu.And].keys()), 
                np.array(prior[gu.And].values()), n), 0],
        gu.Or : [weighted_values(
                np.array(prior[gu.Or].keys()), 
                np.array(prior[gu.Or].values()), n), 0],
        }    

def rejuvenate_arguments(f, data=None):
    '''
    Resample just the arguments of the function
    '''
    if isinstance(f, gu.Operator):
        f.operands = [rejuvenate_arguments(o, data) for o in f.operands] 
        return f
    else: # is Generator -- resample arguments
        return f.sample(data)

def rejuvenate_all_arguments(samples, data=None):
    return [rejuvenate_arguments(s, data) for s in samples]

def generate_samples(n, prior, data=None):
    root_samples = weighted_values(np.array(prior[gu.Root].keys()), 
                                   np.array(prior[gu.Root].values()), n)

    # Precompute some samples
    category_samples = precompute_samples(n*100, prior)
    
    def instantiate(s):
        if issubclass(s, gu.Operator):
            operands = []
            for i in range(s.noperands):
                idx = category_samples[s][1]
                operands.append(category_samples[s][0][idx])
                category_samples[s][1] += 1
            for j, o in enumerate(operands):
                operands[j] = instantiate(o)
            return s(*operands)
        else:
            return s.sample(data)

    # Instantiate all the samples
    return [instantiate(s) for s in root_samples]
