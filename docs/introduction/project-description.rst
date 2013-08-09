Project description
*******************

-  Student: Andrei Cristian Ignat
-  Supervisor: Dr. Christoph Deil
-  Time: June 10, 2013 to August 9, 2013 (9 weeks)
-  Place: MPIK Heidelberg, H.E.S.S. group of Prof. Werner Hofmann

Abstract
========

Astronomical gamma-ray data analysis can be very CPU and / or I/O
intensive. The purpose of this 9-week, first year physics student
project is to time and profile typical data analysis tasks with a focus
on the speedups that can be obtained for the `maximum
likelihood <https://en.wikipedia.org/wiki/Maximum_likelihood>`_ fitting
step by using multiple CPU cores.

Introduction / Overview / Links
===============================

This is basically an introduction and link collection for Andrei. The
project description is in the next section.

-  To get an overview of gamma-ray astronomy science, read one of the
   review articles listed
   `here <http://tevcat.uchicago.edu/reviews.html>`_.
-  We will analyse data from two types of instruments:
-  `Fermi <http://fermi.gsfc.nasa.gov>`_ is a satellite observing in the
   GeV energy range. It's data and software (the Fermi Science tools)
   are publicly available
   `here <http://fermi.gsfc.nasa.gov/ssc/data/>`_.
-  Imaging atmospheric Cherenkov telescopes
   (`IACT <https://en.wikipedia.org/wiki/IACT>`_) arrays are
   ground-based and observe in the TeV energy range. Currently there are
   three telescope arrays in operation
   (`HESS <http://www.mpi-hd.mpg.de/hfm/HESS/>`_,
   `MAGIC <http://magic.mppmu.mpg.de>`_,
   `VERITAS <http://veritas.sao.arizona.edu>`_ and one in preparation:
   `CTA <https://www.cta-observatory.org>`_. No data is publicly
   available, so we'll probably use simulated HESS or CTA data sets.
-  Fermi GeV data analysis and IACT TeV data analysis are pretty
   different.
-  Fermi has a very large field of view (about 10% of the whole sky at
   any time) and is continuously observing the sky. It has detected
   about 2000 point-like sources (see the `2FGL
   catalog <http://fermi.gsfc.nasa.gov/ssc/data/access/lat/2yr_catalog/>`_)
   and it's main background for source detection is Galactic diffuse
   gamma-ray emission (see `this
   paper <http://adsabs.harvard.edu/abs/2012arXiv1202.4039T>`_).
-  IACTs have a small field of view (a few degrees across) and the data
   consists of pointed observations (called "runs") on sky positions
   near suspected source positions. About 150 TeV sources have been
   detected so far (see `TeVCat <http://tevcat.uchicago.edu>`_) and the
   main background is from charged cosmic ray particles (see `Berge
   (2007) <http://adsabs.harvard.edu/abs/2007A%26A...466.1219B>`_). A
   good introduction to TeV astronomy and analysis methods is `de
   Naurois (2012) <http://inspirehep.net/record/1122589>`_.
-  Nevertheless the last analysis step of modeling / fitting the data is
   very similar for Fermi and IACTs.
-  The data either consists of unbinned event lists (energy, RA, DEC) or
   binned count cubes (events filled into energy-RA-DEC bins) from some
   small region of the sky, the so-called "region of interest (ROI)",
   which for Fermi typically is a circle with radius 10 to 20 deg.
-  The other input into the fit is observation exposure (computed from
   the instrument effective area and exposure time) and instrument
   resolution information. The spatial resolution is given by the
   so-called `point spread function
   (PSF) <http://en.wikipedia.org/wiki/Point_spread_function>`_, the
   energy resolution is given by a matrix, see e.g. the Fermi LAT
   instrument response functions (IRFs)
   `here <http://fermi.gsfc.nasa.gov/ssc/data/analysis/documentation/Cicerone/Cicerone_LAT_IRFs/IRF_overview.html>`_.
-  The model consists of a background model plus a number of sources,
   each with a spatial and spectral model with free parameters (see
   Sections 7.5.1 and 7.6.1 in `de Naurois
   (2012) <http://inspirehep.net/record/1122589>`_).
-  The model is then fit to the data taking the exposure and instrument
   resolution into account in a likelihood fit (see description for
   Fermi
   `here <http://fermi.gsfc.nasa.gov/ssc/data/analysis/documentation/Cicerone/Cicerone_Likelihood/Fitting_Models.html>`_
   or `here <https://github.com/kialio/fermi-summer-school>`_ and
   Chapter 7 in `de Naurois
   (2012) <http://inspirehep.net/record/1122589>`_ for IACTs).
   Unfortunately I'm not aware of a short and simple intro to likelihood
   fitting for beginners, maybe you can read
   `this <http://cxc.cfa.harvard.edu/sherpa/references/papers/statistics.pdf>`_
   or `this <http://cxc.harvard.edu/contrib/sherpa/scipy11/>`_ or do
   some of the tutorial from
   `Sherpa <http://cxc.cfa.harvard.edu/sherpa/>`_ or
   `iminuit <http://iminuit.github.io/iminuit/>`_ or
   `probfit <http://iminuit.github.io/probfit/>`_ or
   `RooFit <http://root.cern.ch/drupal/content/roofit>`_ or the
   `python4astronomer's Sherpa fitting
   tutorial <http://python4astronomers.github.io/fitting/fitting.html>`_.
   Understanding the steps involved in computing the likelihood function
   (a.k.a. "cost function" for "fit statistic") for a given set of model
   parameters will be the hardest part of this project, but it is
   probably necessary to a certain degree to understand where (numerical
   integration or convolution or model evaluation or computation of
   derivatives or summation over events / bins or ...) the CPU time is
   spent when profiling the analysis.
-  We will be using the following software:
-  The main focus will be on
   `gammalib <http://gammalib.sourceforge.net>`_ and
   `ctools <http://cta.irap.omp.eu/ctools/>`_ and specifically the
   `ctlike <http://cta.irap.omp.eu/ctools/doc/ctlike.html>`_ tool. The
   ctools can analyze Fermi data and, to a certain degree, HESS and CTA
   data analysis. They use `OpenMP <http://www.openmp.org/>`_ to run
   faster on multi-core machines.
-  We might compare the ctlike speed against
   `gtlike <http://fermi.gsfc.nasa.gov/ssc/data/analysis/scitools/help/gtlike.txt>`_
   in the Fermi science tools (can only use one core as far as I know).
-  If we also look at other steps like exposure computation or diffuse
   response or TS map computation, we might also look at
   `gtapps\_mp <https://github.com/kialio/gtapps_mp>`_, which uses
   Python
   `multiprocessing <http://docs.python.org/2.7/library/multiprocessing.html>`_
   to use multiple CPU cores.
-  If there is time, we might look at the speed of the HESS analysis
   program [HAP], which is a HESS internal analysis software.
-  If there is time, we might look at the speed of morphology fits with
   `Sherpa <http://cxc.cfa.harvard.edu/sherpa/>`_, which also uses
   Python multiprocessing to achieve speed-ups for certain steps
   (parameter error computation) as described
   `here <http://cxc.cfa.harvard.edu/sherpa/threads/multicore/>`_.

Project plan
============

We have nine weeks ... it's very hard to predict how fast results are
obtained ... so I reserved week 6 to continue with the main project or
to do one of the side projects and there are two weeks at the end to
write up the report and finish up loose ends.

-  Week 1: Learn some gamma-ray astrophysics (see references above)
-  Week 2: Learn some gamma-ray data analysis methods (see references
   above)
-  Week 3: Define and produce test data sets (one Galactic and one
   extra-galactic; one Fermi and one HESS)
-  Week 4: Run and time analyses with ctools on at least two machines
   and measure the speedup with the number of cores.
-  Week 5: Profile the analyses to find out where the CPU time is spent.
   Possibly try different compilers (gcc, clang, icc) and optimiser
   flags.
-  Week 6: Continue main project or if there is time do one of these
   things: time HAP, gt\_apps\_mp or Sherpa (see above) or some of the
   other ctools tasks (see `here <http://cta.irap.omp.eu/ctools/>`_).
   Looking at CPU usage, memory usage and disk I/O would also be
   interesting to get a rough overview of what the analyses are doing
   (e.g. ctselect speed is probably disk I/O speed limited)
-  Week 7: Write up report
-  Week 8: Iterate project report (e.g. clearer description or
   double-check results or add additional plots or ...)

The project report and notes and scripts in the
https://github.com/gammapy/gamma-speed/ repo are the product of your
project. It should be a starting point for further work on HESS, Fermi,
CTA data analysis speed by others in the future. Detailed descriptions
of which tools you tried to time and profile (and possibly measure
memory usage and disk I/O) and which are useful and which aren't and how
to use them is helpful.

The most useful thing would be an automatic script that measures certain
aspects of ctools performance for typical analysis scenarios that can
easily be re-run to try out speed improvements and prevent performance
regressions, but this level of automation is most likely not possible in
the given time. Just to get the idea I have in mind here, have a look at
the `PyPy speed center <http://speed.pypy.org>`_ or the `pandas
benchmark <http://pandas.pydata.org/pandas-docs/vbench/vb_groupby.html>`_
as measured by `vbench <https://github.com/pydata/vbench>`_

Further references
==================

Here's some more useful references for tools you might use:

-  Learn git: `basic
   tutorial <http://pcottle.github.io/learnGitBranching/>`_, `advanced
   tutorial <http://gitimmersion.com/>`_
-  Learn Python astro basics: https://astropy4mpik.readthedocs.org/ and
   http://python4astronomers.github.io
-  Profiling tool:
   `KCachegind <http://kcachegrind.sourceforge.net/html/Home.html>`_


