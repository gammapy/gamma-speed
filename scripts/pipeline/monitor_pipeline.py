#!/usr/bin/env python
import argparse
import multiprocessing
import monitor as mt
import shutil
TIME_ZONE_SHIFT = 7200  # the ctobssim log messages correspond to
                        # Greenwich Mean Time and python makes the
                        # measurements for the current time zone -
                        # in this case, CET -> 7200 s shift


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-mt', '--maxthreads', default=multiprocessing.cpu_count(),
        type=int, help='Maximum number of threads for the measurement')
    parser.add_argument('-l', '--loop', default=True, type=bool,
                        help='if more than one processors is specified, ' +
                        'choose wether to loop until the number of ' +
                        'maxthreads has been reached or use that number' +
                        ' of threads from the start')
    parser.add_argument('-pa', '--pipeargs', default='', type=str,
                        help="Arguments that should be passed to " +
                        "run_multi_ctobssim. For more details, see the " +
                        "help of run_multi_ctobssim")
    parser.add_argument('-log', default=False, type=bool,
                        help='if gammaspeed logging statements have been ' +
                        'added to ctools and gammalib, this option should ' +
                        ' be set to True')

    args = parser.parse_args()

    if args.loop:
        for nthrd in xrange(int(args.maxthreads)):
            pipe_monitor = mt.Monitor("./run_pipeline.py" + args.pipeargs, nthrd + 1)
            pipe_monitor.monitor("monitor_CPUs_" + str(nthrd + 1) + ".csv", 0.1)
            if args.log:
                try:
                    pipe_monitor.parse_extension(
                        logext='*.log',
                        outname='pipeline_CPUs_' + str(nthrd + 1) + '.csv',
                        time_shift=TIME_ZONE_SHIFT)
                    shutil.copy2('ctlike.log','original_ctlike_CPUs_'+str(nthrd+1)+'.log')
                    shutil.copy2('ctobssim.log','original_ctobssim_CPUs_'+str(nthrd+1)+'.log')
                    shutil.copy2('ctbin.log','original_ctbin_CPUs_'+str(nthrd+1)+'.log')
                except ValueError:
                    print 'no log file(s) found'
    else:
        pipe_monitor = mt.Monitor("./run_pipeline.py" + args.pipeargs, args.maxthreads)
        pipe_monitor.monitor("monitor_CPUs_" + str(args.maxthreads) + ".csv", 0.1)
        if args.log:
            try:
                pipe_monitor.parse_extension(
                    logext='*.log',
                    outname='pipeline_CPUs_' + str(args.maxthreads) + '.csv',
                    time_shift=TIME_ZONE_SHIFT)
            except ValueError:
                print 'no log file(s) found'

if __name__ == '__main__':
    main()
