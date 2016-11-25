import sys

import numpy as np

from csv import writer
from matplotlib import pyplot as plt

from run_filter import run_filter, run_batch
from priors.uniform_prior import priors
    
def plot_runs(runs, num, nparticles):
    ax = plt.subplot(14, 1, num)
    ylabel = str(nparticles)
    plt.bar([i+1 for i in range(len(runs))], runs, align='center')
    ax.set_xlim((1, len(runs)))
    ax.yaxis.set_ticks(np.arange(0, np.amax(runs), np.amax(runs)/2))
    plt.ylabel(ylabel, rotation='horizontal')

def write_normalized_runs(runs, outfile):
    maxval = np.amax(runs)
    norm_runs = runs/maxval
    runwriter = writer(outfile, delimiter=',')
    runwriter.writerow(norm_runs)

def plot_order_effects(outdir):
    seqs = [[30, 33, 24, 21, 36, 31, 39], [30, 31, 33, 24, 21, 36, 39]]
    particles=[30, 50, 70, 90, 110, 130]
    rsteps = [2]
    nruns = 200

    plt.figure()
    
    for r in rsteps:
        print 'rstep', r
        all_data = np.zeros((len(seqs), len(seqs[0]),
                            len(particles), 100))
        for k, seq in enumerate(seqs):
            print 'seq', k
            for p, nparticles in enumerate(particles):
                print 'particles', nparticles
                for i in range(nruns):
                    stepwise_totals = run_filter(seq, nparticles, r, priors)
                    for s, step_total in enumerate(stepwise_totals):
                        for hyp, count in step_total[:1]: # take the MAP hypothesis #
                            all_data[k, s, p] = np.add(all_data[k, s, p], 
                                                       hyp.bitwise)

        ## filename format: seqnum_rejuvenation.step.csv ##
        for step in range(len(seqs[0])):
            particle_runs = all_data[:,step]
            fig = plt.figure()
            fig.suptitle(', '.join([str(d) for d in seq[:step+1]]))

            for k2 in range(len(seqs)):
                for p, num in enumerate(particles):
                    plot_runs(particle_runs[k2, p], 
                              (p+1) + (k2*len(particles)), num)
                f = open(outdir + '/' + 
                         str(k2) + '_' + str(r) + 'r.' + 
                         str(step) + '.csv', 'wb')
                for run in particle_runs[k2]:
                    write_normalized_runs(run, f)
                f.close()

            print "saving figure...", step, r, particle_runs
            plt.savefig(outdir + '/' + 
                        str(r) + 'r.' + str(step) + 
                        '.png', bbox_inches='tight')
            plt.close()

def main():
    outdir = sys.argv[1]
    plot_order_effects(outdir)

if __name__=="__main__":
    main()
