How to install the necessary software
*************************************
In order to be able to run ``monitor.py`` on your system, you are going to need to install a few dependencies.

Python dependecies
==================
First of all, you need at least **python 2.7** or later in order to be able to ``import argparse``.

After you have solved this issue, ``monitor.py`` is heavily based on the following packages:

* `psutil <http://code.google.com/p/psutil/>`_ - for obtaining information about the resources being used by the system;
* `pandas <http://pandas.pydata.org/>`_ - for saving the information obtained from psutil and the plotting it later on;
* `matplotlib <http://matplotlib.org/>`_ - for plotting the different results.

Usually this is only a matter of simply running ::

    pip install <PACKAGE_NAME>

Besides these basic requirement, in order to monitor ``ctools`` and ``gammalib`` you need to install them first :D

``ctools`` and ``gammalib``
===========================
In order to profile and benchmark ``ctools`` and ``gammalib``, one obviously needs to have installed these two pieces of software. In the monitoring process though, the need arose to insert logging statements in the source code. Therefore, a slightly modified version was used. This version can be found at

* `gammalib <https://github.com/ignatndr/gammalib>`_
* `ctools <https://github.com/ignatndr/ctools>`_

In order to make things easier though, there is a script that will automatically install these tools for you. This is a shell script that runs on Unix machines and assumes that you have already installed `github <https://github.com/>`_ on your machine. Running it is an extremely simple matter of going to the ``gamma-speed/scripts`` directory, copying ``install_ctools.sh`` to the directory in which you want to install ``ctools`` and ``gammalib`` and running it under the command::

    ./install_ctools.sh LOG gammaspeed_extra_log
    
.. note::
    If you want to install the normal version of ``gammalib`` and ``ctools``, you can run ``./install_ctools.sh NORMAL``. However, all the examples that will be presented from now on were run with the extra logging version of the ``gammalib`` and ``ctools``. If you still wish to install the normal version, you should be aware that in the following examples, whenever you see the option ``-log=True``, you should replace it with ``-log=False`` when executing python scripts from gamma-speed.

Logging in ``gammalib``
=======================
If you have installed the software using::

    ./install_ctools.sh LOG gammaspeed_extra_log
    
then you have the version that implements the following way of logging in ``gammalib``. If you want to add secondary log statements, just follow the method described below.

An extremely useful tools for logging comes from ``gammalib`` and is called GLog. This class provides the user a simple and easy to use log object. After importing the header for the logger class

``#include "GLog.hpp"``

one cam simply create a new logger object and start logging away!::

    GLog logtt;
    clobber = true;
    filename = "magicLog.log"
    logtt.open(filename, clobber);
    logtt.date(true);
    logtt << "logger: at your service" <<std::endl;
    logtt.close();

Of course, there are fancier options available from the GLog class such as different headers, formats, etc. For debugging purposes though, the little piece of code above will suffice.
    
Setting up your environment
===========================

After you have installed all these magnificent pieces of software, you still need to tell your machine that they are there. My reccomendation would be to add the following lines of code at the end of your ``.bashrc`` file. Obviously, you can export these variables everytime you want to monitor something or can build a separate script that contains these lines of code and run this script each time before starting to monitor.

1. In order to tell your machine that you have installed the monitor, you need to add the ``scripts/src`` directory to your ``PYTHONPATH``. This is done by calling::

    export PYTHONPATH=$PYTHONPATH:<path/to/gamma-speed>/gamma-speed/scripts/src

   Now, your system knows that there are Python modules that can be imported in the ``src`` directory.

2. If you want to monitor ``gammalib`` and ``ctools``, you need to tell your system that you have installed these two and where to look for them. This is done by running the following lines of code::

    export GAMMALIB = <INSTALL_DIR>
    export CTOOLS = <INSTALL_DIR>
    source $CTOOLS/bin/ctools-init.sh
    source $GAMMALIB/bin/gammalib-init.sh
    
   Now you can run the ``ctools`` tests that are in the ``gamma-speed`` repository.
   

