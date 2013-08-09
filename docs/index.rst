.. gamma-speed documentation master file, created by
   sphinx-quickstart on Wed Jul 31 10:47:02 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to gamma-speed's documentation!
***************************************

The **gamma-speed** repository can be found `here <https://github.com/gammapy/gamma-speed>`_. 

gamma-speed_ is a project meant to profile and monitor ctools_ and gammalib_.

The motivation behind this project was that as new tools are being developed, the developer must see if the tools are working properly. A few different possibilities of monitoring these tools were considered. After a bit of online research, the conclusion was that given the limited time frame(8 weeks) the best solution would be to build Python based tools.

In order to monitor different system resources, the Python module :mod:`psutil` is being employed. For more details about how it works, see the psutil `website <http://code.google.com/p/psutil/>`_.

Different :mod:`psutil` functionalities are put together in monitor in order to get informaton about the system running a certain process. Monitor gathers this information and writes it to disk. After this, another python module will interpret the information coming from the output of monitor and plot the results.

A key point in this project was seeing how well ``gammalib`` and ``ctools`` parallelism obeys `Amdahl's Law <http://en.wikipedia.org/wiki/Amdahl%27s_law>`_. This law puts a limit on the maximum speed-up that can be obtained through parallelism and will be described in a later chapter.

In the end, a few conclusions were drawn about the parallel behaviour of these tools and an outline for future improvements to the project was drawn.
  

.. _ctools: http://cta.irap.omp.eu/ctools/
.. _gammalib: http://gammalib.sourceforge.net/
.. _gamma-speed: https://github.com/gammapy/gamma-speed/



Contents

.. toctree::
   :maxdepth: 1

   introduction/project-description
   introduction/amdahl
   introduction/cpu_info
   tutorial/install_stuff
   tutorial/tutorial
   results/results
   other/future
   other/link_collection

