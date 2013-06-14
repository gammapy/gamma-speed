import subprocess
import numpy as np

def time_first(n_data, n_threads, task):
    n_data = int(n_data)
    cmd = './first {n_data} {n_threads} {task}'.format(**locals())
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output = process.communicate()[0]
    time = float(output.strip().split()[-1])
    return time

def run_parameter_study():
    n_data_list = 10 ** np.arange(3, 7)
    n_threads_list = range(1, 5)
    for n_data in n_data_list:
        for n_threads in n_threads_list:
            t = time_first(n_data, n_threads, 'sum')
            print n_data, n_threads, t

if __name__ == '__main__':
    run_parameter_study()