#!/usr/bin/env python

"""
Parse and plot the output of monitor.py

Example: ./monitor_plot.py --nrcsv=3 --outfile=performance --function=cp
will interpret the output of 3 .csv files and will make a plot with the name
    performance_cp.png in the directory plots/
"""
import argparse
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FormatStrFormatter
import multiprocessing
import numpy as np
import platform

class monitorplot:
    def __init__(self, infile, ncsv, procname):
        self.infile = infile
        self.ncsv = ncsv
        self.procname = procname
        
    def read_monitor_log(self, current_CPU_count):
        filename = self.infile + "_CPUs=" + str(current_CPU_count + 1) + ".csv"
        df = pd.read_csv(filename)
        name = df.at[1, 'PROCESS_NAME']
        df['MEM_USAGE'] = df['MEM_USAGE'] / int(1e6)
        df['TIME'] = df['TIME'] - df.at[0, 'TIME']
        return df
        
    def read_gammalib_log(self, current_CPU_count):     
       filename = self.procname + "_CPUs=" + str(current_CPU_count + 1) + ".csv"
       df = pd.read_csv(filename)
       return df

    def mplot(self, outfile, figtitle):
        """
        function used to plot the data gathered by monitor.py
        if outfile is '' <empty>, then the function returns the plot 
        instance for further modifications
        """
        fig = plt.figure(1, figsize=(15.0, 15.0))
        
        for i in xrange(self.ncsv):
            df = self.read_monitor_log(i)
            if i == 0:
                core_label = '1 core'
            else:
                core_label = str(i + 1) + ' cores'
     
            plt.subplot(411)
            df.plot(x='TIME', y='CPU_USAGE', label=core_label)
            plt.ylabel('CPU (%)')
            plt.title('CPU usage for ' + self.procname)
            plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            plt.legend(loc=0, ncol=self.ncsv / 2)
            plt.xlabel('Time(s)')
            [x1, x2, y1, y2] = plt.axis()
            plt.axis((x1, x2, y1, y2 * 1.1))
              
            mem = plt.subplot(412)
            df.plot(x='TIME', y='MEM_USAGE', label=core_label)
            plt.ylabel('RAM usage (MB)')
            plt.title('Memory usage for ' + self.procname)
            plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            plt.legend(loc=0, ncol=self.ncsv / 2)
            plt.xlabel('Time(s)')
            [x1, x2, y1, y2] = plt.axis()
            plt.axis((x1, x2, y1, y2 * 1.1))
             
            plt.subplot(413)
            df['IO_WRITE_BYTES'] = df['IO_WRITE_BYTES'] / int(1e6)
            iow = df.plot(x='TIME', y='IO_WRITE_BYTES', label=core_label)
            plt.ylabel('IO Write (MB)')
            plt.title('Write sum for ' + self.procname)
            plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            plt.legend(loc=0, ncol=self.ncsv / 2)
            plt.xlabel('Time(s)')
            [x1, x2, y1, y2] = plt.axis()
            plt.axis((x1, x2, y1, y2 * 1.1))
             
            df['IO_WRITE_BYTES'] = df['IO_WRITE_BYTES'].diff() / df['TIME'].diff()
            plt.subplot(414)
            iow = df.plot(x='TIME', y='IO_WRITE_BYTES', label=core_label)
            plt.ylabel('IO Write (MB/s)')
            plt.title('Write rate for ' + self.procname)
            plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            plt.legend(loc=0, ncol=self.ncsv / 2)
            plt.xlabel('Time(s)')
            [x1, x2, y1, y2] = plt.axis()
            plt.axis((x1, x2, y1, y2 * 1.1))
             
        fig.subplots_adjust(hspace=.5)
         
        fig.suptitle(figtitle)
        
        if outfile=='':
            return plt
        else:
            plt.savefig(outfile + ".png")

    def speed_up(self, ncores, figtitle, out_pref='', save_plot=True, speed_frame=None):
        """
        function used for plotting the speed up.
        If speed_frame is defined and contains other time values than the total ones,
        the default method for aquiring data is overriden and the new values are plotted instead.
        (int ncores, str out_pref, boolean save_plot, pandas.DataFrame speed_frame)
        """
        if speed_frame==None:
            cores = [i + 1 for i in range(ncores)]
            times = pd.Series(index=cores)
            for i in xrange(int(ncores)):
                df = self.read_gammalib_log(i)
                # time spent for the whole process
                times[i + 1] = df['TIME'].iget(-1) - df['TIME'].iget(0)
                
            speed = pd.Series(data=times[1] / times, index=cores)
            eff = speed / cores
        else:
            cores = [i + 1 for i in range(ncores)]
            speed = pd.Series(data=speed_frame[0] / speed_frame, index=cores)
            eff = speed / cores
            
        #plot style definitions
        speedfig = plt.figure()
        axes = plt.subplot(211)
        speedP = speed.plot(color='g', marker='.', ls='-', ms=15.0, mec='r')
        plt.ylabel('Speed-up factor (relative)')
        plt.xlabel('Number of cores')
        plt.title('Speed-up for ctobssim')
        axes.set_xlim(left=0, right=ncores + 1)
        axes.set_ylim(bottom=0)
        xa = axes.get_xaxis()
#         xa.set_major_locator(MaxNLocator(integer=True))
        
        
        axes = plt.subplot(212)
        eff.plot(color='r', marker='.', ls='-', ms=15.0, mec='g')
        plt.ylabel('Efficiency (relative)')
        plt.xlabel('Number of cores')
        plt.title('Efficiency for ctobssim')
        axes.set_xlim(left=0, right=ncores + 1)
        axes.set_ylim(bottom=0)
        xa = axes.get_xaxis()
#         xa.set_major_locator(MaxNLocator(integer=True))
        
        speedfig.subplots_adjust(hspace=.5)

        pltname='plots/' + out_pref + '_speed_up.png'
        speedfig.suptitle(figtitle)
            
        if save_plot:
            plt.savefig(pltname)
        else:
            return plt
        


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--infile', default='monitor',
                        help='Input file name - prefix')
    parser.add_argument('-n', '--nrcsv', default=multiprocessing.cpu_count(), type=int,
                        help='Number of csv files')
    parser.add_argument('-o', '--out_pref', default='',
                        help='Outfile prefix')
    parser.add_argument('-fn', '--function', default='',
                        help='If a ctools function has been monitored, it should be mentioned here\\ Ex. -fn=ctobssim')
    
    args = parser.parse_args()
    my_mplot = monitorplot(args.infile, args.nrcsv, args.function)
    my_mplot.mplot(outfile='plots/' + args.out_pref + '_' + args.function + '_' + platform.node(),
           figtitle='Machine: ' + platform.node())

if __name__ == '__main__':
    main()
