#!/usr/bin/env python

from matplotlib.ticker import FormatStrFormatter
import argparse
import matplotlib.pyplot as plt
import multiprocessing
import pandas as pd
from matplotlib.ticker import MaxNLocator

def speedUp(nCores, inPref, outPref):
    cores = [i + 1 for i in range(nCores)]
    times = pd.Series(index=cores)
    for i in xrange(int(nCores)):
        filename = inPref + "_CPUs=" + str(i + 1) + "_.csv"
        df = pd.read_csv(filename)
        # time spent for the whole process
        times[i + 1] = df['TIME'].iget(-1) - df['TIME'].iget(0)
        
    
    speed = pd.Series(data=times[1] / times, index=cores)
    
    eff = speed / cores
    
    speedfig = plt.figure(1)
    axes = plt.subplot(211)
    speedP = speed.plot(color='g', marker='.', ls='-', ms=15.0, mec='r')
    plt.ylabel('Speed-up factor (relative)')
    plt.xlabel('Number of cores')
    plt.title('Speed-up for ctobssim')
    axes.set_xlim(left=0, right=nCores + 1)
    axes.set_ylim(bottom=0)
    xa = axes.get_xaxis()
    xa.set_major_locator(MaxNLocator(integer=True))

    
    axes = plt.subplot(212)
    eff.plot(color='r', marker='.', ls='-', ms=15.0, mec='g')
    plt.ylabel('Efficiency (relative)')
    plt.xlabel('Number of cores')
    plt.title('Efficiency for ctobssim')
    axes.set_xlim(left=0, right=nCores + 1)
    axes.set_ylim(bottom=0, top=1.2)
    xa = axes.get_xaxis()
    xa.set_major_locator(MaxNLocator(integer=True))
    
    
    s = pd.read_csv('temp.csv')
    speedfig.subplots_adjust(hspace=.5)
    pltName = 'plots/' + outPref + str(float(s['values'][3]) - float(s['values'][2])) + '_' + s['values'][11] + '_' + s['values'][12] + '.png'
    
    speedfig.suptitle('Observation time:' + str(float(s['values'][3]) - float(s['values'][2])) + ' seconds; ' + s['values'][11] + ' runs; Machine: ' + s['values'][12])
        
    plt.savefig(pltName)
    
#     plt.show()
    
#     import IPython; IPython.embed()
        


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--infile', default='monitor',
                        help='Input file name - prefix')
    parser.add_argument('-nc', '--ncores', default=multiprocessing.cpu_count(),
                        help='Number of cores and implicitly of csv files')
    parser.add_argument('-o', '--outfile', default='SpeedEff',
                        help='Outfile prefix')
    
    args = parser.parse_args()
    speedUp(nCores=args.ncores, inPref=args.infile, outPref=args.outfile)

if __name__ == '__main__':
    main()
