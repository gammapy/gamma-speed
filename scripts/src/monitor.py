#!/usr/bin/env python

"""Automatically Monitor CPU, memory and disk I/O for a given process.

    Usage
    -----
    Monitor can be used to see how a certain process is using the system resources.
    The process has to take longer than the cpuinterval variable in the Monitor.monitor
    method. That is why an extremely simple usage, such as::
        ./monitor.py "ls -lh"
    will fail to yield accurate results. It is therefore recommended that monitor be run
    on longer processes. A good set of examples is given in the scripts/calibrate folder
     
"""
import argparse
import pandas as pd
import psutil
import subprocess
import time
import multiprocessing
import os
import glob
import logging
import shlex
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')
import sys

class Monitor(object):
    """Monitor RAM, CPU, and disk I/O for a given process

    Parameters
    ----------
    cmd : string
        The command that is to be monitored
    nthreads : string
        The number of threads that the process is supposed to run on

    .. note :: 
        the number of threads can only be set for a program that has
        been parallelized using *OpenMP* since this number is controlled 
        through the *OMP_NUM_THREADS* environment variable
        
        
    Methods
    -------
    monitor(outfile, cpuinterval)
        gathers information for a given command and writes the information to
        outfile
    parse_time(time_s, times_shift)
        parse the time format of GLog
    parse_log(logname, time_shift)
        select the log entries that contain the string 'gammaspeed' from the 
        file 'logname'
    parse_extension(logext, outname, time_shift)
        parse all the log files that have the name '*.logext', select entries
        with parse_log and write them to the file outname
    
    Examples
    --------
    1. Say you want to monitor the command "sleep 3" which does nothing but 
        take 3 seconds to run. What you would then have to do is run the 
        following from the command line::
            ./monitor.py --loop=True "sleep 3"
        This would then produce a number n(=number of CPUs available on the 
        machine) outfiles which contain the output of the measurements
    2. If you want to only monitor for a certain number of threads, say 3,
        then the command looks like::
            ./monitor.py --maxthreads=3 --loop=False "sleep 3"
        This would then have as output only one file namely::
            monitor_CPUs_3.csv
    3. (for gammalib and ctools) If you have added special log statements 
        inside the source code, you can interpret these log statements through 
        the option::
            ./monitor.py -log=True
    
    """
    
    def __init__(self, cmd, nthreads):
        self.threads = nthreads
        os.environ["OMP_NUM_THREADS"] = str(self.threads)
        self.process = psutil.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
        self.df = pd.DataFrame(
            columns=['CPU_USAGE',
                     'MEM_USAGE',
                     'IO_READ_BYTES',
                     'IO_WRITE_BYTES',
                     'PROCESS_NAME',
                     'TIME', 'NUM_THREADS'])
        self.name = self.process.name

    def monitor(self, outfile, cpuinterval):
        """Monitor a given command 
        
        Parameters
        ----------
        outfile : string
            The name of the file to which the observations should be written
        cpuinterval : float
            The frequency with which CPU, RAM and disk I/O should be sampled
            .. note :: 
                After running the calibration tests, the interval was set to
                0.1 seconds since this value gave the most accurate results
                For more details, see the Calibration section
        
        Usage
        -----
        A monitor object has to be initialized for the command that is to be 
        run. After the command has started running, the Monitor.monitor() 
        method will sample the resource utilization of that command at given 
        intervals.
        """
        
        # Remember start time for on screen display
        start = time.time()
        # While the process does not have an exit status i.e. process.poll() 
        # is None, monitor the process
        while self.process.poll() is None:
            try:
                # get the CPU value with a frequency of cpuinterval
                # this is a blocking operation i.e. it will wait for 
                # cpuinterval seconds before continuing the while loop
                CPU = self.process.get_cpu_percent(interval=float(cpuinterval))
                MEM = self.process.get_memory_info()[1]
                    
                # the get_io_counters() does not seem to work on Mac, so it 
                # has been surrounded in a try except loop
                try:
                    READ = self.process.get_io_counters()[2]
                    WRITE = self.process.get_io_counters()[3]
                except AttributeError:
                    READ = None
                    WRITE = None
                
                # get the process name
                NAME = self.name
                TIME = time.time()
                THREADS = self.process.get_num_threads()
                
                # write these values to an auxiliary pd.Series object that can
                # be appended to the main DataFrame later
                s = pd.Series(
                    data = [CPU, MEM, READ, WRITE, NAME, TIME, THREADS],
                    index=['CPU_USAGE', 'MEM_USAGE', 'IO_READ_BYTES', 'IO_WRITE_BYTES',
                            'PROCESS_NAME', 'TIME', 'NUM_THREADS'])

                # append the values of this measurement                
                self.df = self.df.append(s, ignore_index=True)
                # print the runtime on screen
                sys.stdout.write('\r')
                sys.stdout.write("Runtime ............................. " + "{:5.2f}".format(TIME-start) + " seconds")
                sys.stdout.flush()
    
            except psutil.AccessDenied:
                # the while loop exits when the process is over.
                # However, it might happen that the process finished inside 
                # the while loop. Once the process is dead, there is no
                # information available about it anymore and any method called
                # on the process will return psutil.AccessDenied as an error
                # This is how you know that the process is dead.
                sys.stdout.write('\n')
                sys.stdout.flush()
                logging.info('Process is over for ' + str(self.threads) + ' thread(s)')
                print self.df.describe()

        # write the values into a csv file
        self.df.to_csv(outfile, index=False)
        logging.info('Wrote file ' + outfile)
        
        sys.stdout.write('\n\n.................................................................................\n\n')
    
    def parse_time(self, time_s, time_shift):
        """parse the time for a GLog entry
        
        Parameters
        ----------
        time_s : string
            The GLog value for the timestamp
        time_shift : float
            The value of the time zone shift
            
        Usage
        -----
        Since the GLog class logs timestamps under the format
            2013-08-06T09:45:30.025850
        these need to be converted to seconds since the epoch for the monitor
        to be able to parse them
        """
        sec = time_s.split('.')[0]
        mic = time_s.split('.')[1]
        time_f = time.mktime(time.strptime(sec,'%Y-%m-%dT%H:%M:%S')) + float('0.' + mic) + float(time_shift)
        return time_f

    def parse_log(self, logname, time_shift):
        """select log entries of format gammaspeed:entry
        
        Parameters
        ----------
        logname : string
            The name of the log entry
        time_shift : float
            Value for time zone shift
            
        Usage
        -----
        This method is used to select all the entries that respect the format
            gammaspeed:SOMETHING_HAS_HAPPENED
        Such entries were for example added to gammalib and ctools in order 
        to delimitate the parallel portions of the code from the serial ones
        
        """
        file = open(logname, 'r')
        content = filter(lambda t: 'gammaspeed' in t, file.readlines())
        log_frame = pd.DataFrame(columns=['TIME', 'EVENT'])
        for c in content:
            time = c.split()[0]
            event = c.split()[2:]
            s = pd.Series(index=['TIME', 'EVENT'], 
                          data=[self.parse_time(time, time_shift), event])
            log_frame = log_frame.append(s, ignore_index=True)
        return log_frame

    def parse_extension(self, logext, outname, time_shift):
        """parse all the logfiles with extension logext
        
        Parameters
        ----------
        logext : string
            The extension of the log files 
        outname : string 
            The name of the file that is to be written to disk
        time_shift : 
            Value for time zone shift
            
        Usage
        -----
        This method is used to open all the log files that have the extension
        ``*.logext``, select from them the entries that correspond to 
        gammaspeed relevant events and writes these selected events to a new 
        file to disk. This new file will later be handled by monitor_plot.
        """
        log = pd.DataFrame(columns=['TIME', 'EVENT'])
        for filename in glob.glob(logext):
            log = log.append(
                self.parse_log(
                    filename,
                    time_shift),
                ignore_index=True)
        log.to_csv(outname)
        logging.info('Wrote file ' + outname)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-o', '--outfile', default='monitor',
                        help='Output file name')
    parser.add_argument(
        '-mt', '--maxthreads', default=multiprocessing.cpu_count(),
        help='Maximum number of threads for the measurement')
    parser.add_argument('-ti', '--timeinterval', default=0.1,
                        help='The sampling interval at which ' +
                        'the CPU measurements should take place')
    parser.add_argument('cmd', type=str,
                        help='Command to execute')
    parser.add_argument('-fn', '--function', default='',
                        help='If a ctools function that generates a log file' +
                        ' is being monitored, it should be mentioned here' +
                        'Ex. -fn=ctobssim')
    parser.add_argument('-l', '--loop', default=False, type=bool,
                        help='if more than one processors is specified,' +
                        ' choose wether to loop until the number of ' +
                        ' maxthreads has been reached or use that number' +
                        ' of threads from the start')

    args = parser.parse_args()

    if(args.loop):
        for nthrd in xrange(int(args.maxthreads)):
            my_monitor = Monitor(args.cmd, nthrd + 1)
            my_monitor.monitor(
                outfile=args.outfile + "_CPUs_" + str(nthrd + 1) + ".csv",
                cpuinterval=args.timeinterval)
    else:
        my_monitor = Monitor(args.cmd, args.maxthreads)
        my_monitor.monitor(
            outfile=args.outfile + "_CPUs_" + str(args.maxthreads) + ".csv",
            cpuinterval=args.timeinterval)

if __name__ == '__main__':
    main()
