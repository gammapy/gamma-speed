#!/usr/bin/env python
import argparse
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FormatStrFormatter
import multiprocessing

def monitorPlot(infile,nfiles,outpref):
        # read the values into a csv file        
        fig=plt.figure(1,figsize=(15.0, 10.0))
        for i in xrange(nfiles):
            filename = infile+"_CPUs="+str(i+1)+"_.csv"
            df = pd.read_csv(filename)
#             import IPython; IPython.embed()
            name = df.at[1, 'PROCESS_NAME']
            
            if i==0:
                theLabel='1 core'
            else:
                theLabel=str(i+1)+' cores'
        
            df['IO_WRITE_BYTES']=df['IO_WRITE_BYTES'].diff()/df['TIME'].diff()/int(1e6)
            df['MEM_USAGE']=df['MEM_USAGE']/int(1e6)
        
            df['TIME']=df['TIME']-df.at[    0,'TIME']
        
            plt.subplot(311)
            df.plot(x='TIME',y='CPU_USAGE', label=theLabel)
            plt.ylabel('CPU (%)')
            plt.title('CPU usage for ctobssim')
            plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            plt.legend(loc=0, ncol=nfiles/2)
            plt.xlabel('Time(s)')
            
            mem = plt.subplot(312)
            df.plot(x='TIME',y='MEM_USAGE',label=theLabel)
            plt.ylabel('RAM usage (MB)')
            plt.title('Memory usage for ctobssim')
            plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            plt.legend(loc=0, ncol=nfiles/2)
            plt.xlabel('Time(s)')
#         fig = plt.figure(2)
#         plt.subplot(311)
#         df['IO_READ_COUNTS'].plot()usage
#         plt.ylabel('IO Read (counts)')
#         plt.title('IO Read counts for ' + name)
#  
#         plt.subplot(312)
#         df['IO_WRITE_COUNTS'].plot()
#         plt.ylabel('IO Write (counts)')
#         plt.title('IO write counts for ' + name)     
            plt.subplot(313)
            iow = df.plot(x='TIME',y='IO_WRITE_BYTES',label=theLabel)
            plt.ylabel('IO Write (MB/s)')
            plt.title('Write rate for ctobssim')
            plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            plt.legend(loc=0, ncol=nfiles/2)
            plt.xlabel('Time(s)')
            
        s=pd.read_csv('temp.csv')
        
#         import IPython;IPython.embed()
            
        fig.subplots_adjust(hspace=.5)
        
        pltName = 'plots/'+outpref+str(float(s['values'][3])-float(s['values'][2]))+'sec_'+s['values'][11]+'obs_'+s['values'][12]+'.png'
        
        fig.suptitle('Observation time:'+str(float(s['values'][3])-float(s['values'][2]))+' seconds; '+s['values'][11]+' runs; Machine: '+s['values'][12])
        
        plt.savefig(pltName)
#         plt.show()
    
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--infile', default='monitor',
                        help='Input file name - prefix')
    parser.add_argument('-n', '--nrcsv', default=multiprocessing.cpu_count(),
                        help='Number of csv files')
    parser.add_argument('-o', '--outfile', default='',
                        help='Outfile prefix')
    
    args = parser.parse_args()
    monitorPlot(infile=args.infile,nfiles=args.nrcsv,outpref=args.outfile)
    

if __name__ == '__main__':
    main()