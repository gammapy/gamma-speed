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

    def CPU_plot(self, outfile, ax=None):
        if ax is None:
            ax=plt.gca()
            fig = plt.figure(2, figsize=(15.0, 15.0))
        
        if self.ncsv > 4:
            sel_vals = range(0, self.ncsv, self.ncsv/4)
            sel_vals.append(self.ncsv - 1)
        else:
            sel_vals = xrange(self.ncsv)
        
        for i in sel_vals:
            df = self.read_monitor_log(i)
            if i == 0:
                core_label = '1 core'
            else:
                core_label = str(i + 1) + ' cores'
            
            plt.plot(df['TIME'].values, df['CPU_USAGE'].values, label=core_label, hold=True, axes=ax)

        plt.ylabel('CPU (%)')
        plt.title('CPU usage for ' + self.procname)
        plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        plt.legend(loc=0, ncol=self.ncsv / 2)
        plt.xlabel('Time(s)')
        [x1, x2, y1, y2] = plt.axis()
        plt.axis((x1, x2, y1, y2 * 1.1))
        
        if outfile is not '':
            plt.savefig(outfile + ".png")
            plt.close()
            
    def MEM_plot(self, outfile, ax=None):
        if ax is None:
            ax=plt.gca()
            fig = plt.figure(3, figsize=(15.0, 15.0))
        
        if self.ncsv > 4:
            sel_vals = range(0, self.ncsv, self.ncsv/4)
            sel_vals.append(self.ncsv - 1)
        else:
            sel_vals = xrange(self.ncsv)
        
        for i in sel_vals:
            df = self.read_monitor_log(i)
            if i == 0:
                core_label = '1 core'
            else:
                core_label = str(i + 1) + ' cores'
            
            plt.plot(df['TIME'].values, df['MEM_USAGE'].values, label=core_label, hold=True, axes=ax)

        plt.ylabel('RAM usage (MB)')
        plt.title('Memory usage for ' + self.procname)
        plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        plt.legend(loc=0, ncol=self.ncsv / 2)
        plt.xlabel('Time(s)')
        [x1, x2, y1, y2] = plt.axis()
        plt.axis((x1, x2, y1, y2 * 1.1))
        
        if outfile is not '':
            plt.savefig(outfile + ".png")
            plt.close()

    def IO_cumulative_plot(self, outfile, ax=None):
        if ax is None:
            ax=plt.gca()
            fig = plt.figure(4, figsize=(15.0, 15.0))
        
        if self.ncsv > 4:
            sel_vals = range(0, self.ncsv, self.ncsv/4)
            sel_vals.append(self.ncsv - 1)
        else:
            sel_vals = xrange(self.ncsv)
        
        for i in sel_vals:
            df = self.read_monitor_log(i)
            if i == 0:
                core_label = '1 core'
            else:
                core_label = str(i + 1) + ' cores'
        
            df['IO_WRITE_BYTES'] = df['IO_WRITE_BYTES'] / int(1e6)
            plt.plot(df['TIME'].values, df['IO_WRITE_BYTES'].values, label=core_label, hold=True, axes=ax)

        plt.ylabel('IO Write (MB)')
        plt.title('Write sum for ' + self.procname)
        plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        plt.legend(loc=0, ncol=self.ncsv / 2)
        plt.xlabel('Time(s)')
        [x1, x2, y1, y2] = plt.axis()
        plt.axis((x1, x2, y1, y2 * 1.1))
            
        if outfile is not '':
            plt.savefig(outfile + ".png")
            plt.close()
               
    def IO_speed_plot(self, outfile, ax=None):
        if ax is None:
            ax=plt.gca()
            fig = plt.figure(5, figsize=(15.0, 15.0))
        
        if self.ncsv > 4:
            sel_vals = range(0, self.ncsv, self.ncsv/4)
            sel_vals.append(self.ncsv - 1)
        else:
            sel_vals = xrange(self.ncsv)
        
        for i in sel_vals:            
            df = self.read_monitor_log(i)
            if i == 0:
                core_label = '1 core'
            else:
                core_label = str(i + 1) + ' cores'
                
            df['IO_WRITE_BYTES'] = df['IO_WRITE_BYTES'].diff() / df['TIME'].diff() / int(1e6)
            plt.plot(df['TIME'].values, df['IO_WRITE_BYTES'].values, label=core_label, hold=True, axes=ax)

        plt.ylabel('IO Write (MB/s)')
        plt.title('Write rate for ' + self.procname)
        plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        plt.legend(loc=0, ncol=self.ncsv / 2)
        plt.xlabel('Time(s)')
        [x1, x2, y1, y2] = plt.axis()
        plt.axis((x1, x2, y1, y2 * 1.1))
            
        if outfile is not '':
            plt.savefig(outfile + ".png")
            plt.close()
    
    def IO_read(self, outfile, ax=None):
        if ax is None:
            ax=plt.gca()
            fig = plt.figure(5, figsize=(15.0, 15.0))
        
        if self.ncsv > 4:
            sel_vals = range(0, self.ncsv, self.ncsv/4)
            sel_vals.append(self.ncsv - 1)
        else:
            sel_vals = xrange(self.ncsv)
        
        for i in sel_vals:            
            df = self.read_monitor_log(i)
            if i == 0:
                core_label = '1 core'
            else:
                core_label = str(i + 1) + ' cores'
                
            df['IO_READ_BYTES'] = df['IO_READ_BYTES'].diff() / df['TIME'].diff() / int(1e6)
            plt.plot(df['TIME'].values, df['IO_READ_BYTES'].values, label=core_label, hold=True, axes=ax)

        plt.ylabel('I\O Read (MB/s)')
        plt.title('Read rate for ' + self.procname)
        plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        plt.legend(loc=0, ncol=self.ncsv / 2)
        plt.xlabel('Time(s)')
        [x1, x2, y1, y2] = plt.axis()
        plt.axis((x1, x2, y1, y2 * 1.1))
            
        if outfile is not '':
            plt.savefig(outfile + ".png")
            plt.close()
                 
    def times_bar(self, outfile='', ax=None, speed_frame=None):
        if ax is None:
            ax=plt.gca()
            fig = plt.figure(6, figsize=(5.0, 15.0))
        
        cores = [i + 1 for i in range(self.ncsv)]
            
        if speed_frame is None:
            times = pd.Series(index=cores)
            for i in xrange(int(self.ncsv)):
                df = self.read_monitor_log(i)
                # time spent for the whole process
                times[i + 1] = df['TIME'].iget(-1) - df['TIME'].iget(0)
        else:
            times = speed_frame
            
        times.plot(kind='bar', label = 'Execution time', axes=ax)
        plt.ylabel('Time(s)')
        plt.xlabel('Number of cores')
        plt.title('Execution time for' + self.procname)
        ax.set_xlim(left=0, right=self.ncsv + 1)
        ax.set_ylim(bottom=0)
        xa = ax.get_xaxis()
        [x1, x2, y1, y2] = plt.axis()
        plt.axis((x1, x2, y1, y2 * 1.1))
        plt.legend(loc=0)

        if outfile is not '':
            plt.savefig(outfile + '.png')
            plt.close()
        
    def speed_plot(self, outfile='', ax=None, speed_frame=None, amdahl_frame=None):
        if ax is None:
            ax=plt.gca()
            fig = plt.figure(7, figsize=(5.0, 15.0))
            
        if speed_frame is None:
            cores = [i + 1 for i in range(self.ncsv)]
            times = pd.Series(index=cores)
            for i in xrange(int(self.ncsv)):
                df = self.read_monitor_log(i)
                # time spent for the whole process
                times[i + 1] = df['TIME'].iget(-1) - df['TIME'].iget(0)

            speed = pd.Series(data=times[1] / times, index=cores)
        else:
            speed = speed_frame[1] / speed_frame
            
        speed.plot(color='g', marker='.', ls='-', ms=15.0, mec='r',label='Measured values')
        if amdahl_frame is not None:
            amdahl_frame.plot(color='b', ls='-', label='Amdahl\'s Law')
        plt.ylabel('Speed-up')
        plt.xlabel('Number of cores')
        plt.title('Speed-up for' + self.procname)
        ax.set_xlim(left=0, right=self.ncsv + 1)
        ax.set_ylim(bottom=0)
        xa = ax.get_xaxis()
        [x1, x2, y1, y2] = plt.axis()
        plt.axis((x1, x2, y1, y2 * 1.1))
        plt.legend(loc=0)
        
        if outfile is not '':
            plt.savefig(outfile + '.png')
            plt.close()
        
    def eff_plot(self, outfile='', ax=None, speed_frame=None, amdahl_frame=None):
        if ax is None:
            ax=plt.gca()
            fig = plt.figure(8, figsize=(5.0, 15.0))
            
        if speed_frame is None:
            cores = [i + 1 for i in range(self.ncsv)]
            times = pd.Series(index=cores)
            for i in xrange(int(self.ncsv)):
                df = self.read_monitor_log(i)
                # time spent for the whole process
                times[i + 1] = df['TIME'].iget(-1) - df['TIME'].iget(0)

            eff = pd.Series(data=times[1] / times, index=cores) / cores
        else:
            cores = [i + 1 for i in range(self.ncsv)]
            eff = speed_frame[1] / speed_frame / cores
            
        eff.plot(color='r', marker='.', ls='-', ms=15.0, mec='g', label='Measured values')
        
        if amdahl_frame is not None:
            amdahl_eff = amdahl_frame / cores
            amdahl_eff.plot(color='b', ls='-', label='Amdahl\'s Law')
        plt.ylabel('Efficiency')
        plt.xlabel('Number of cores')
        plt.title('Efficiency for' + self.procname)
        ax.set_xlim(left=0, right=self.ncsv + 1)
        ax.set_ylim(bottom=0)
        xa = ax.get_xaxis()
        [x1, x2, y1, y2] = plt.axis()
        plt.axis((x1, x2, y1, y2 * 1.1))
        plt.legend(loc=0)
        
        if outfile is not '':
            plt.savefig(outfile + '.png')
            plt.close()
        
    def mplot(self, outfile, figtitle):
        """
        function used to plot the data gathered by monitor.py
        if outfile is '' <empty>, then the function returns the plot 
        instance for further modifications
        """
        fig = plt.figure(1, figsize=(15.0, 15.0))
        
        sub1 = plt.subplot(411)
        self.CPU_plot('', sub1)
        
        sub2 = plt.subplot(412)
        self.MEM_plot('', sub2)

        sub3 = plt.subplot(413)
        self.IO_read('', sub3)

        sub4 = plt.subplot(414)
        self.IO_speed_plot('', sub4)
             
        fig.subplots_adjust(hspace=.5)
         
        fig.suptitle(figtitle)
        
        if outfile is not '':
            plt.savefig(outfile + ".png")
        else:
            return plt
        plt.close()
    
    def splot(self, figtitle, outfile='', speed_frame=None, amdahl_frame=None):
        """
        function used for plotting the speed up.
        If speed_frame is defined and contains other time values than the total ones,
        the default method for aquiring data is overriden and the new values are plotted instead.
        (int ncores, str out_pref, boolean save_plot, pandas.DataFrame speed_frame)
        """
        if speed_frame is None:
            cores = [i + 1 for i in range(self.ncsv)]
            times = pd.Series(index=cores)
            for i in xrange(int(self.ncsv)):
                df = self.read_monitor_log(i)
                # time spent for the whole process
                times[i+1] = df['TIME'].iget(-1) - df['TIME'].iget(0)
        else:
            times = speed_frame
        #plot style definitions
        speedfig = plt.figure(figsize=(15.0,15.0))
        sub1 = plt.subplot(311)
        self.times_bar('', ax=sub1, speed_frame=times)
        
        sub2 = plt.subplot(312)
        self.speed_plot('', sub2, times, amdahl_frame)
                
        sub3 = plt.subplot(313)
        self.eff_plot('', sub3, times, amdahl_frame)
        
        speedfig.subplots_adjust(hspace=.5)

        speedfig.suptitle(figtitle)
            
        if outfile is not '':
            plt.savefig(outfile + '.png')

        plt.close()

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
    my_mplot.splot('Machine: ' + platform.node(), 'plots/' + args.out_pref + '_' + args.function + '_' + platform.node() + 'speed_up', None, None)
    
if __name__ == '__main__':
    main()
