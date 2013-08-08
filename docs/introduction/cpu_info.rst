CPU Infos
*********

This is a short summary description of the machines used for this study.

Andrei's Asus G51J
------------------

-  Processor: Intel Core i5 430M (`Intel
   Info <http://ark.intel.com/products/43537/>`_)
-  Cache: L2: 3072 kB
-  Memory: 2 x 2 GB DDR3 @ 1067MHz
-  Graphics: NVIDIA GeForce GTS 360M 1024MB (can be used with CUDA)
-  Storage: Momentus ST9500420AS
-  OS: Ubuntu 12.10(quantal) 64bit

Andrei's Desktop machine
------------------------

-  Processor: 3.0 GHz Intel Core 2 Duo E8400(2 cores)
-  Cache: L2: 6 MB
-  Memory: 1 GB DDR3 @ 1066 MHz + 2 GB DDR3 @ 1066 MHz
-  Graphics: Intel Graphics Media Accelerator 950
-  Storage: Seagate ST1000DM003-9YN162 1TB
-  OS: Ubuntu 12.04(precise) 64bit

New MPIK cluster machine
------------------------

-  Name: ``lfc301``
-  Processor: 2 x Intel(R) Xeon(R) CPU E5-2660 0 @ 2.20GHz = 16 cores
   (`Intel Info <http://ark.intel.com/products/64584/>`_)
-  check: 2.2 GHz E5 2660 -> Turboboost 2.8 GHz if only some cores are
   used
-  Cache: 20 MB
-  Memory: 132 GB
-  Storage: Lustre file system
-  OS: Scientific Linux 6

Old MPIK cluster machine
------------------------

-  Name: ``lfc292``
-  Processor: 2 CPU x Intel(R) Xeon(R) CPU E5450 @ 3.00GHz = 8 cores
   (`Intel
   Info <http://ark.intel.com/products/33083/Intel-Xeon-Processor-E5450-12M-Cache-3_00-GHz-1333-MHz-FSB>`_)
-  check: 3 GHz
-  Cache: 6 MB
-  Memory: 16 GB
-  Storage: Lustre file system
-  OS: Scientific Linux 6

Christoph's Macbook Pro Retina
------------------------------

-  Processor: 2.6 GHz Intel Core i7-3720QM (4 core) (`Intel
   Info <http://ark.intel.com/products/64891>`_)
-  Cache: L2: 256 KB per core, L3: 6 MB
-  Memory: 2 x 8 GB = 16 GB 1600 MHz DDR3
-  Graphics: NVIDIA GeForce GT 650M 1024 MB (can be used with CUDA)
-  Storage: APPLE SSD SM512E
-  OS: OS X 10.8.4

Howto
=====

Here are some notes on how to find out more about a given machine:

-  ``cat /proc/cpuinfo``
-  ``df -h``
-  ``sudo dmidecode --type 17`` for RAM information
-  Get CPU Info on a Mac: ``sysctl -n machdep.cpu.brand_string``

.. note::
   The results presented later were obtained from the new MPIK cluster machine ``lfc301``.
