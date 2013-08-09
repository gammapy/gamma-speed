Tutorial
********
In this short tutorial, a typical example of how to run the ``monitor`` is shown. After the measurement is over, a typical usage of the ``MonitorPlot`` class is described.

Assuming that you have added the ``scripts/src`` folder to your ``PYTHONPATH``, you can now import the ``monitor`` and ``monitor_plot`` modules inside Python scripts. This is what we will also do.

.. note::
   Except for the pieces of code where **Amdahl's Law** is required, none of the following examples require that the source code be modified to include logging statements that tell monitor how much time the process is spending in executing serial and parallel code.
   
Monitoring
==========
Start a new Python script called ``monitor_process_name`` and add::
    
    import monitor as mt
    
to the import list of the script. 

Now, in order to be able to run and monitor the process, you will need to instantiate a new ``Monitor`` object. This is done by simply calling::
    
    process_monitor = mt.Monitor("<process>", number_of_threads)
    
This object will now start the command you have passed to it and run it on ``number_of_threads`` threads. In order to actually gather information about the resources that the process is using, you need to call the ``monitor`` like this::

    process_monitor.monitor("monitor_CPUs_" + str(number_of_threads) + ".csv", 0.1)
            
The arguments passed to the ``monitor`` method dictate the name of the ``outfile`` and the ``cpuinterval`` or frequency with which the measurements should take place.      
            
.. note::
   If you have added logging statements to the ``ctools`` source code, you may also call the following method::
    
        process_monitor.parse_extension(logext='*.log', outname='process_CPUs_' + str(nthrd + 1) + '.csv', time_shift=TIME_ZONE_SHIFT)
   
   in order to select your logging statements and save them to separate outfiles.
   
Plotting
========
Plotting your results is a task for the ``MonitorPlot`` class. First, import the Python module containing it with::

    import monitor_plot as mtp
    
Now, you will need to instantiate a ``MonitorPlot`` object from this class. This is easily done by calling::

    my_plotter = mtp.MonitorPlot(args.infile, args.nrcsv, " function name")
    
This will tell the plotter what type of pattern the ``.csv`` filenames follow and also how many ``.csv`` files it should read.

The ``my_plotter`` object can now call methods that produce different plots. You may want to produce separate plots for CPU, RAM, disk READ and disk WRITE or you might to plot all these values on a single figure. These can be accomplished by calling::

    #For separate plots
    my_plotter.CPU_plot('CPU.png')
    my_plotter.MEM_plot('MEM.png')
    my_plotter.IO_speed_plot('io_write.png')
    my_plotter.IO_read('io_read.png')
    
    #For a all the plots in a single figure
    my_plotter.mplot(outfile='all_plots.png', figtitle='Resource utilization for process')

The second thing that the ``my_plotter`` object can do is plot the measured speedup from executing the process on multiple cores. In order to do this, it needs to know the time needed to execute the process on a single core and then the execution times on multicore machines. There are three different kinds of plots that can be obtained, namely

* a bar plot with the execution time versus number of cores - using the function ``times_bar``
* the speedup versus number of cores - using the function ``speed_plot`` 
* the efficiency of the process versus number of cores - using the function ``eff_plot``

The values that are used for these plots are obtained from the start and end times read from the normal output of monitoring. Again, you can choose to have all these plots separately or together in one figure. In order to produce the plots, call::
    
    # first read the values from the monitor output
    times = pd.Series(index=cores)
            
    for i in xrange(my_plotter.ncsv):
            df = my_plotter.read_monitor_log(i)
            # time spent for the whole process
            times[i + 1] = df['TIME'].iget(-1) - df['TIME'].iget(0)
        
    # for separate plots
    my_plotter.times_bar('time_bar_plot.png', ax=None, speed_frame=times)
    my_plotter.speed_plot('speed_up_plot.png', ax=None, speed_frame=times, amdahl_frame=None)
    my_plotter.eff_plot('eff_up_plot.png', ax=None, speed_frame=times, amdahl_frame=None)
    
    # for all the plots in one figure
    my_plotter.splot(figtitle='Speedup analysis for process', outfile='splot.png', speed_frame=times, amdahl_frame=None)
    
Amdahl's Law
------------
A functionality of plotting is that you can choose to add the speedup values predicted by Amdahl's Law to the plots. For this, you have to know how much time is spend executing the parallel code of the process ``parallel_time[P]``, where P is the number of cores used. In code, this would look like::

    amd = pd.Series(index=cores)
    parallel_loop = pd.Series(index=cores)
        
    for i in xrange(my_plotter.ncsv):
        df = my_plotter.read_monitor_log(i)
        start_time = df.at[0, 'TIME'] 
        aux = select_lines('secondary_log_CPUs_' + str(i + 1) + '.csv',
            start_time,
            ['gammaspeed:parallel_start',
             'gammaspeed:parallel_end'])
        parallel_time[i + 1] = aux[1] - aux[0]
        
    parallel_time_init = parallel_loop[1]
    
    for i in xrange(my_plotter.ncsv):
        amd[i + 1] = times[1] / (times[1] - parallel_time_init + parallel_time_init / (i + 1))
        
where ``'secondary_log_CPUs_' + str(i + 1) + '.csv'`` is the ``.csv`` file that contains the two timestamps for ``gammaspeed:parallel_start`` and ``gammaspeed:parallel_start``, i.e. how much time was spent in the execution of the parallel portion of the code. Addind these values to the previous plot is done by simply adding the ``amd`` Series as an argument when calling the ``splot`` function::

    # for separate plots
    my_plotter.speed_plot('speed_up_plot.png', ax=None, speed_frame=times, amdahl_frame=amd)
    my_plotter.eff_plot('eff_up_plot.png', ax=None, speed_frame=times, amdahl_frame=amd)
    
    # for all the plots in one figure
    my_plotter.splot(figtitle='Speedup analysis for process', outfile='splot.png', speed_frame=times, amdahl_frame=amd)
    
