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

def monitor(cmd, outfile):
        """Execute a given command (cmd is a string)
        and write usage to outfile"""
        process = psutil.Popen(cmd[0].split(), stdout=subprocess.PIPE)

        df = pd.DataFrame(columns=['CPU_USAGE', 'MEM_USAGE', 'IO_READ_COUNTS', 'IO_WRITE_COUNTS', 'IO_WRITE_BYTES', 'PROCESS_NAME','TIME'])
                
        name = process.name
        # The following thread stops when the initial one has come to a halt.
        while process.poll() == None:
            try:
                s = pd.Series([process.get_cpu_percent(interval=0.1), process.get_memory_info()[1], 
                               process.get_io_counters ()[0], process.get_io_counters ()[1], process.get_io_counters ()[3], name,time.time()],
                              index=['CPU_USAGE', 'MEM_USAGE', 'IO_READ_COUNTS', 'IO_WRITE_COUNTS', 'IO_WRITE_BYTES', 'PROCESS_NAME','TIME'])
                df = df.append(s, ignore_index=True)
            except psutil.AccessDenied:
                print 'Process is over'
        # write the values into a csv file        
        df.to_csv(outfile)
   
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-o', '--outfile', default='monitor',
                        help='Output file name')
    parser.add_argument('-mt', '--maxthreads', default=multiprocessing.cpu_count(),
                        help='Maximum number of threads for the measurement')
    parser.add_argument('cmd', nargs='+',
                        help='Command to execute')

    args = parser.parse_args()
#     import IPython; IPython.embed()
    for i in xrange(args.maxthreads):
        os.environ["OMP_NUM_THREADS"]=str(i+1)
        monitor(cmd=args.cmd, outfile=args.outfile+"_CPUs="+str(i+1)+"_.csv")
    

if __name__ == '__main__':
    main()