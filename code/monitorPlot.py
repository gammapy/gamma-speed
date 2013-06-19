#!/usr/bin/env python
"""
Plotting tool for Monitor CPU, memory and disk I/O for a given process.

Example: ./monitor.py "ls -lh"

"""
import argparse
import matplotlib.pyplot as plt
import pandas as pd

def monitorPlot(infile):
        # write the values into a csv file        
        df = pd.read_csv(infile)
        
        name = df.at[1, 'PROCESS_NAME']
        fig = plt.figure(1)
     
        plt.subplot(211)
        df['CPU_USAGE'].plot()
        plt.ylabel('CPU (%)')
        plt.title('CPU usage for ' + name)
         
        plt.subplot(212)
        df['MEM_USAGE'].plot()
        plt.ylabel('RAM usage (bytes)')
        plt.title('Memory usage for ' + name)
     
        fig = plt.figure(2)
        plt.subplot(311)
        df['IO_READ_COUNTS'].plot()
        plt.ylabel('IO Read (counts)')
        plt.title('IO Read counts for ' + name)
 
        plt.subplot(312)
        df['IO_WRITE_COUNTS'].plot()
        plt.ylabel('IO Write (counts)')
        plt.title('IO write counts for ' + name)
        
        plt.subplot(313)
        df['IO_WRITE_BYTES'].plot()
        plt.ylabel('IO Write (bytes)')
        plt.title('Bytes written by ' + name)
     
        fig.subplots_adjust(hspace=.5)
     
        plt.show()
    
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--infile', default='monitor.csv',
                        help='Input file name')
    
    args = parser.parse_args()
    monitorPlot(infile=args.infile)
    

if __name__ == '__main__':
    main()

