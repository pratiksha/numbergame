import ng.sampler as fs

from ng.particle_filter import ParticleFilter
from operator import itemgetter

def postprocess_frequencies(particles):
    end = {}
    for p, w in particles:
        if p in end.keys():
            end[p] += 1
        else:
            end[p] = 1
    return end

def run_filter(data, nparticles, rejuvenation, prior, outlier = 2, outfile=None):
    pfilter = ParticleFilter(fs.generate_samples(nparticles, prior), prior, outlier)

    stepwise_predictions = []
    for i, d in enumerate(data):
        pfilter.update(d)
        for j in range(rejuvenation):
            pfilter.rejuvenate()
        for r in range(1):
            pfilter.resample()
        grouped = postprocess_frequencies(zip(pfilter.particles, 
                                              pfilter.weights))
        stepwise_predictions.append(sorted(grouped.items(), key=itemgetter(1),
                                           reverse=True))

    return stepwise_predictions

def run_batch(data, nparticles, rejuvenation, prior, outlier = 2, resample=20, outfile=None):
    pfilter = ParticleFilter(fs.generate_samples(nparticles, prior), prior, outlier)

    stepwise_predictions = []
    
    for i, d in enumerate(data):
        pfilter.update(d)
        pfilter.resample()
    for j in range(rejuvenation):
        pfilter.rejuvenate()
        pfilter.resample()
    grouped = postprocess_frequencies(zip(pfilter.particles, 
                                          pfilter.weights))
    stepwise_predictions.append(sorted(grouped.items(), key=itemgetter(1),
                                       reverse=True))

    return stepwise_predictions

'''
particles is a list of particles to initialize with
'''
def run_with_initial_particles(data, particles, rejuvenation,
                               prior, outlier = 2, resample=20, outfile=None):

    pfilter = ParticleFilter(particles, prior, outlier)

    stepwise_predictions = []
    
    for i, d in enumerate(data):
        pfilter.update(d)
    for j in range(rejuvenation):
        pfilter.rejuvenate()
        pfilter.resample()
    grouped = postprocess_frequencies(zip(pfilter.particles, 
                                          pfilter.weights))
    stepwise_predictions.append(sorted(grouped.items(), key=itemgetter(1),
                                       reverse=True))

    return stepwise_predictions

