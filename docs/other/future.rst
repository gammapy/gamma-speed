Future directions
*****************

Measuring FITS I/O
==================

Goal
----

Measure the FITS I/O speed for CTA format event lists and compare to
`ROOT <http://root.cern.ch/>`_ and `HDF5 <http://www.hdfgroup.org/HDF5/>`_.

For FITS look at the speed of:

* `CFITSIO <http://heasarc.gsfc.nasa.gov/fitsio/>`_
* `CFITSIO Python wrapper <https://pypi.python.org/pypi/fitsio/>`_
* `astropy.io.fits <https://astropy.readthedocs.org/en/latest/io/fits/index.html>`_
* `astropy.io.table <https://astropy.readthedocs.org/en/latest/table/index.html>`_
* `GammaLib <http://gammalib.sourceforge.net>`_ (e.g. write with `ctobssim` and read / write with `ctselect`)

Methods
-------

Define test datasets of different sizes (1 MB to 10 GB with ~ 10 values and log spacing).

Do operations so that I/O speed dominates execution time:

* Event selection using box cuts
* Histogram or simply sum data

These days memory is pretty large (10 GB to 100 GB are typical), maybe we should also measure
memory to CPU I/O bound operations?

Some references
---------------

* http://www.hdfgroup.org/HDF5/RD100-2002/HDF5_Performance.pdf
* http://heasarc.gsfc.nasa.gov/fitsio/c/c_user/node119.html
* http://adsabs.harvard.edu/abs/2009CoPhC.180.2499A
* http://adsabs.harvard.edu/abs/2011JPhCS.331c2010A
