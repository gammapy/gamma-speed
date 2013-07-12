#!/usr/bin/env python
import argparse
import multiprocessing
import os
import pandas as pd
import time
# TODO: import monitor.py through a relative path?
import src.monitor as mt
import glob

def parse_ctobssim_time(time_s):
    sec = time_s.split('.')[0]
    mic = time_s.split('.')[1]
    time_f = time.mktime(time.strptime(sec, '%Y-%m-%dT%H:%M:%S')) + float('0.' + mic)
    return time_f
    
def parse_log(logname):
    file = open(logname, 'r')
    content = filter(lambda t:'gammaspeed' in t, file.readlines())
    log_frame = pd.DataFrame(columns=['TIME', 'EVENT'])
    for c in content:
        time = c.split()[0]; 
        event = c.split()[1:]; 
        s = pd.Series(index=['TIME', 'EVENT'], data=[parse_ctobssim_time(time), event])
        log_frame = log_frame.append(s, ignore_index=True)
    return log_frame

def parse_extension(logext, outname):
    log = pd.DataFrame(columns=['TIME', 'EVENT'])

    for filename in glob.glob(logext):
        log = log.append(parse_log(filename), ignore_index=True)
    log.to_csv(outname)   
        
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-mt', '--maxthreads', default=multiprocessing.cpu_count(),
                        type=int, help='Maximum number of threads for the measurement')
    parser.add_argument('-l', '--loop', default=True, type=bool,
                        help='if more than one processors is specified, choose wether to\\'
                        + 'loop until the number of maxthreads has been reached\\'
                        + 'or use that number of threads from the start')
    parser.add_argument('-ca', '--ctobsargs', default='', type=str,
                        help="Arguments that should be passed to run_multi_ctobssim." 
                         "For more details, see the help of run_multi_ctobssim")
    
    args = parser.parse_args()
    
    if(args.loop):
        for nthrd in xrange(int(args.maxthreads)):
            ctobs_monitor = mt.monitor("./run_multi_ctobssim.py" + args.ctobsargs, nthrd + 1)
            ctobs_monitor.monitor("monitor_CPUs=" + str(nthrd + 1) + ".csv", 0.1)
            parse_extension('*.log', 'ctobssim_' + str(nthrd + 1) + 'CPUs.csv')
    else:
        ctobs_monitor = mt.monitor("./run_multi_ctobssim.py " + args.ctobsargs, args.maxthreads)
        ctobs_monitor.monitor("monitor_CPUs=" + str(args.maxthreads) + ".csv", 0.1)
        parse_extension('*.log', 'ctobssim_' + str(args.maxthreads) + 'CPUs.csv')

if __name__ == '__main__':
    main()
