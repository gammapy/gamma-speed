#!/usr/bin/env python

"""Automatically Monitor CPU, memory and disk I/O for a given process.

Example: ./monitor.py "ls -lh"
"""
import argparse
import pandas as pd
import psutil
import subprocess
import time
import multiprocessing
import os
 
class monitor:
    def __init__(self, cmd, nthreads):
        self.process = psutil.Popen(cmd, stdout=subprocess.PIPE)
        self.df = pd.DataFrame(columns=['CPU_USAGE', 'MEM_USAGE', 'IO_READ_COUNTS', 'IO_WRITE_COUNTS', 'IO_WRITE_BYTES', 'PROCESS_NAME', 'TIME'])
        self.name = self.process.name
        self.threads = nthreads 
    
    def monitor(self, outfile, cpuinterval):
        """Execute a given command (cmd is a string)
        and write usage to outfile"""
        os.environ["OMP_NUM_THREADS"] = str(self.threads)
        # The following thread stops when the initial one has come to a halt.
        while self.process.poll() == None:
            try:
                s = pd.Series([self.process.get_cpu_percent(interval=float(cpuinterval)), self.process.get_memory_info()[1],
                               self.process.get_io_counters ()[0], self.process.get_io_counters ()[1], self.process.get_io_counters ()[3], self.name, time.time()],
                              index=['CPU_USAGE', 'MEM_USAGE', 'IO_READ_COUNTS', 'IO_WRITE_COUNTS', 'IO_WRITE_BYTES', 'PROCESS_NAME', 'TIME'])
                self.df = self.df.append(s, ignore_index=True)
            except psutil.AccessDenied:
                print 'Process is over'
        # write the values into a csv file        
        self.df.to_csv(outfile)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-o', '--outfile', default='monitor',
                        help='Output file name')
    parser.add_argument('-mt', '--maxthreads', default=multiprocessing.cpu_count(), 
                        help='Maximum number of threads for the measurement')
    parser.add_argument('-ti', '--timeinterval', default=0.1,
                        help='The sampling interval at which the CPU measurements should take place')
    parser.add_argument('cmd', nargs='+',
                        help='Command to execute')
    parser.add_argument('-fn', '--function', default='',
                        help='If a ctools function that generates a .log file' + 
                        'is being monitored, it should be mentioned here\\ Ex. -fn=ctobssim')
    parser.add_argument('-l', '--loop', default=False, type=bool,
                        help='if more than one processors is specified, choose wether to\\'
                        + 'loop until the number of maxthreads has been reached\\'
                        + 'or use that number of threads from the start')
    
    args = parser.parse_args()
    
    if(args.loop):
        for nthrd in xrange(int(args.maxthreads)):
            my_monitor = monitor(args.cmd, nthrd+1)
            my_monitor.monitor(outfile=args.outfile + "_CPUs=" + str(nthrd+1) + ".csv", 
                               cpuinterval=args.timeinterval)
    else:
        my_monitor = monitor(args.cmd, args.maxthreads)
        my_monitor.monitor(outfile=args.outfile + "_CPUs=" + str(args.maxthreads) + ".csv",
                           cpuinterval=args.timeinterval)

if __name__ == '__main__':
    main()
