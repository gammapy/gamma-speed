#!/usr/bin/env python

"""
This script ilustrates the short comings of monitor.py

In this case of python parallel processing, the parallelization consists in the 
fact that the multiprocessing module launches a new process for each active cpu.

However, since monitor.py attaches itself to a single pid and not to the children
of that process as well, it will not detect what the children are doing, resulting
in zero measured activity even though this script is using 100% of each available 
CPU for the duration of 5 seconds  
"""

import multiprocessing
import time

def run():
    start = time.time()
    while int(time.time()-start) < 5:
        1+1;

if __name__=="__main__":
    for i in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=run)
        p.start()