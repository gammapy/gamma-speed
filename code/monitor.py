#!/usr/bin/env python
"""Monitor CPU, memory and disk I/O for a given process.

Example: ./monitor.py "ls -lh"
"""
import argparse
import subprocess
from subprocess import PIPE
import psutil
import csv
import matplotlib.pyplot as plt

def monitor(cmd, outfile):
    	"""Execute a given command (cmd is a string)
    	and write usage to outfile"""
    	process = psutil.Popen(cmd[0].split(), stdout=subprocess.PIPE)
    	info = dict(disk_io=[],cpu_usage=[],mem_usage=[],name=process.name)
    
	#The following thread stops when the initial one has come to a halt.
    	while process.poll()==None:
		try:
			info['disk_io'].append(process.get_io_counters ())
			info['cpu_usage'].append(process.get_cpu_percent(interval=0.0001))
            		info['mem_usage'].append(process.get_memory_info())
        	except psutil.AccessDenied:
			print 'Process is over'
	
    
    	#write the values into a casv file	    
    	writer = csv.writer(open(outfile, 'wb'))    
	for key, value in info.items():
   		writer.writerow([key, value])
   	
    	#import IPython; IPython.embed()
    	fig=plt.figure(1)
	
	plt.subplot(411)
	plt.plot(info['cpu_usage'])
    	plt.ylabel('CPU (%)')
    	plt.title('CPU usage for ' + info['name'])
    	
	plt.subplot(412)
	plt.plot(info['mem_usage'][0])
	plt.ylabel('Memory (bytes)')
	plt.title('Memory usage for' + info['name'])
	
	plt.subplot(413)
	plt.plot(info['disk_io'][3])
	plt.ylabel('Read (bytes)')
	plt.title('Bytes read by' + info['name'])

	plt.subplot(414)
        plt.plot(info['disk_io'][4])
        plt.ylabel('Write (bytes)')
        plt.title('Bytes written by' + info['name'])
	
	fig.subplots_adjust(hspace=.5)
	
	plt.show()
    
    
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
