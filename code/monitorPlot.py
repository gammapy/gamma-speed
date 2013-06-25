#!/usr/bin/env python
import argparse
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FormatStrFormatter
import multiprocessing

def monitorPlot(infile,nfiles):
        # read the values into a csv file        
        fig=plt.figure(1)
        for i in xrange(nfiles):
            df = pd.read_csv(infile+"_CPUs="+str(i+1)+"_.csv")
            name = df.at[1, 'PROCESS_NAME']
        
        
            df['IO_WRITE_BYTES']=df['IO_WRITE_BYTES'].diff()/df['TIME'].diff()/int(1e6)
            df['MEM_USAGE']=df['MEM_USAGE']/int(1e6)
        
            df['TIME']=df['TIME']-df.at[0,'TIME']
        
            plt.subplot(311)
            df.plot(x='TIME',y='CPU_USAGE')
            plt.ylabel('CPU (%)')
            plt.title('CPU usage for ' + name)
            plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.2f s'))
        
            plt.subplot(312)
            df.plot(x='TIME',y='MEM_USAGE')
            plt.ylabel('RAM usage (MB)')
            plt.title('Memory usage for ' + name)
            plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.2f s'))
#         fig = plt.figure(2)
#         plt.subplot(311)
#         df['IO_READ_COUNTS'].plot()
#         plt.ylabel('IO Read (counts)')
#         plt.title('IO Read counts for ' + name)
#  
#         plt.subplot(312)
#         df['IO_WRITE_COUNTS'].plot()
#         plt.ylabel('IO Write (counts)')
#         plt.title('IO write counts for ' + name)     
            plt.subplot(313)
            df.plot(x='TIME',y='IO_WRITE_BYTES')
            plt.ylabel('IO Write (MB/s)')
            plt.title('Write rate ' + name)
            plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.2f s'))

        fig.subplots_adjust(hspace=.5)
     
        plt.show()
    
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--infile', default='monitor',
                        help='Input file name - prefix')
    parser.add_argument('-n', '--nrcsv', default=multiprocessing.cpu_count(),
                        help='Number of csv files')
    
    args = parser.parse_args()
    monitorPlot(infile=args.infile,nfiles=args.nrcsv)
    

if __name__ == '__main__':
    main()