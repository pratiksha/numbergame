import numpy as np

EPSILON = 0.00000000000000001

def compute_likelihoods(hypotheses, data, outlier_penalty = 2):
    likelihoods = []
    for h in hypotheses:
        inconsistencies = np.where(np.bitwise_xor(
                np.bitwise_and(h.bitwise, data), data) == 1)[0]
        hyp_len = len(np.nonzero(h.bitwise)[0])
        if hyp_len == 0:
            likelihoods.append(EPSILON)
            continue
        if len(inconsistencies) == 0:
            likelihoods.append(1./hyp_len)
        else:
            likelihoods.append(np.exp(
                    -outlier_penalty * float(len(inconsistencies)))*(1./(hyp_len)))
    return np.array(likelihoods)
