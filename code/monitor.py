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

def monitor(cmd, outfile, cpuinterval):
    """Execute a given command (cmd is a string)
    and write usage to outfile"""

    process = psutil.Popen(cmd[0].split(), stdout=subprocess.PIPE)
    df = pd.DataFrame(columns=['CPU_USAGE', 'MEM_USAGE', 'IO_READ_COUNTS', 'IO_WRITE_COUNTS', 'IO_WRITE_BYTES', 'PROCESS_NAME', 'TIME'])
    name = process.name     
    # The following thread stops when the initial one has come to a halt.
    while process.poll() == None:
        try:
            s = pd.Series([process.get_cpu_percent(interval=float(cpuinterval)), process.get_memory_info()[1],
                           process.get_io_counters ()[0], process.get_io_counters ()[1], process.get_io_counters ()[3], name, time.time()],
                          index=['CPU_USAGE', 'MEM_USAGE', 'IO_READ_COUNTS', 'IO_WRITE_COUNTS', 'IO_WRITE_BYTES', 'PROCESS_NAME', 'TIME'])
            df = df.append(s, ignore_index=True)
        except psutil.AccessDenied:
            print 'Process is over'

    # write the values into a csv file        
    df.to_csv(outfile)

def parse_ctobssim_time(time_s):
    sec = time_s.split('.')[0]
    mic = time_s.split('.')[1]
    time_f = time.mktime(time.strptime(sec, '%Y-%m-%dT%H:%M:%S')) + float('0.' + mic)
    return time_f
    
def parse_log(logname, outname):
    file = open(logname, 'r')
    content = filter(lambda t:'gammaspeed' in t, file.readlines())
    log_frame = pd.DataFrame(columns=['TIME', 'EVENT'])
    for c in content:
        time = c.split()[0]; 
        event = c.split()[2]; 
        s = pd.Series(index=['TIME', 'EVENT'], data=[parse_ctobssim_time(time), event])
        log_frame = log_frame.append(s, ignore_index=True)
    log_frame.to_csv(outname)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-o', '--outfile', default='monitor',
                        help='Output file name')
    parser.add_argument('-mt', '--maxthreads', default=multiprocessing.cpu_count(), type=int,
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
                        +'loop until the number of maxthreads has been reached\\'
                        +'or use that number of threads from the start')
    
    args = parser.parse_args()
    
    if(args.loop):
        for i in xrange(int(args.maxthreads)):
            os.environ["OMP_NUM_THREADS"] = str(i + 1)
            monitor(cmd=args.cmd, outfile=args.outfile + "_CPUs=" + str(i + 1) + ".csv", cpuinterval=args.timeinterval)
            if(args.function in ['ctobssim','ctlike']):
                parse_log(args.function + '.log', args.function + "_CPUs=" + str(i + 1) + ".csv")
    else:
            os.environ["OMP_NUM_THREADS"] = str(args.maxthreads)
            monitor(cmd=args.cmd, outfile=args.outfile + "_CPUs=" + str(args.maxthreads) + ".csv", cpuinterval=args.timeinterval)
            if(args.function in ['ctobssim','ctlike']):
                parse_log(args.function + '.log', args.function + "_CPUs=" + str(args.maxthreads) + ".csv")

if __name__ == '__main__':
    main()
