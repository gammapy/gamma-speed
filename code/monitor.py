#!/usr/bin/env python
"""Monitor CPU, memory and disk I/O for a given process.

Example: ./monitor.py "ls -lh"
"""
import argparse
import subprocess
import psutil

def monitor(cmd, outfile):
    """Execute a given command (cmd is a string)
    and write usage to outfile"""
    popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    #import IPython; IPython.embed()
    process = psutil.Process(popen.pid)

    while True:
        info = dict()
        info['cpu_usage'] = process.get_cpu_percent(interval=0.01)
        info['mem_usage'] = 42
        info['disk_io'] = 42
        print info
        # TODO: finish this script

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