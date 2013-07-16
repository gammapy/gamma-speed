#!/usr/bin/env python
import argparse
import multiprocessing
import src.monitor as mt
TIME_ZONE_SHIFT = 7200  # the ctobssim log messages correspond to 
                        # Greenwich Mean Time and python makes the 
                        # measurements for the current time zone - 
                        # in this case, CET -> 7200 s shift

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-mt', '--maxthreads', default=multiprocessing.cpu_count(),
                        type=int, help='Maximum number of threads for the measurement')
    parser.add_argument('-l', '--loop', default=True, type=bool,
                        help='if more than one processors is specified, choose wether to\\'
                        + 'loop until the number of maxthreads has been reached\\'
                        + 'or use that number of threads from the start')
    parser.add_argument('-ca', '--ctlikesargs', default='', type=str,
                        help="Arguments that should be passed to run_multi_ctobssim." 
                         "For more details, see the help of run_multi_ctobssim")
    
    args = parser.parse_args()
    
    if(args.loop):
        for nthrd in xrange(int(args.maxthreads)):
            ctlike_monitor = mt.monitor("./run_multi_ctlike.py" + args.ctlikesargs, nthrd + 1)
            ctlike_monitor.monitor("monitor_CPUs=" + str(nthrd + 1) + ".csv", 0.1)
            ctlike_monitor.parse_extension(logext='*.log', outname='ctlike_CPUs=' + str(nthrd+1) + '.csv', time_shift=TIME_ZONE_SHIFT)
    else:
        ctlike_monitor = mt.monitor("./run_multi_ctlike.py" + args.ctlikeargs, args.maxthreads)
        ctlike_monitor.monitor("monitor_CPUs=" + str(args.maxthreads) + ".csv", 0.1)
        ctlike_monitor.parse_extension(str("*.log"), outname='ctlike_CPUs=' + str(args.maxthreads) + '.csv', time_shift=TIME_ZONE_SHIFT)

if __name__ == '__main__':
    main()
