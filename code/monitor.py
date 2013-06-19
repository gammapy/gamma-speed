#!/usr/bin/env python
"""Monitor CPU, memory and disk I/O for a given process.

Example: ./monitor.py "ls -lh"
"""
import argparse
import pandas as pd
import psutil
import subprocess

def monitor(cmd, outfile):
        """Execute a given command (cmd is a string)
        and write usage to outfile"""
        process = psutil.Popen(cmd[0].split(), stdout=subprocess.PIPE)

        df = pd.DataFrame(columns=['CPU_USAGE', 'MEM_USAGE', 'IO_READ_COUNTS', 'IO_WRITE_COUNTS', 'IO_WRITE_BYTES', 'PROCESS_NAME'])
                
        name = process.name
        # The following thread stops when the initial one has come to a halt.
        while process.poll() == None:
            try:
                s = pd.Series([process.get_cpu_percent(interval=0.1), process.get_memory_info()[1], 
                               process.get_io_counters ()[0], process.get_io_counters ()[1], process.get_io_counters ()[3], name],
                              index=['CPU_USAGE', 'MEM_USAGE', 'IO_READ_COUNTS', 'IO_WRITE_COUNTS', 'IO_WRITE_BYTES', 'PROCESS_NAME'])
                df = df.append(s, ignore_index=True)
            except psutil.AccessDenied:
                print 'Process is over'
        # write the values into a csv file        
        df.to_csv(outfile)
   
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-o', '--outfile', default='monitor.csv',
                        help='Output file name')
    parser.add_argument('cmd', nargs='+',
                        help='Command to execute')

    args = parser.parse_args()
    monitor(cmd=args.cmd, outfile=args.outfile)
    

if __name__ == '__main__':
    main()
