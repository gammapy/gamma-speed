Amdahl's Law
************
Theory
======
...states that, given *P* cores, the speed up for that number of cores is *S(P)*

.. math::

        S(P) = \frac{t_{total}(1)}{t_{total}(P)} = \frac{t_{serial} + t_{parallel}}{t_{serial}+\frac{t_{parallel}}{P}}

with :math:`t_{total}` the total runtime, :math:`t_{serial}` the time needed to run the serial part of the code and :math:`t_{parallel}` the time needed to run the parallel part of the code.

Under this formulation, the maximum speedup, as :math:`P\rightarrow\infty` is

.. math::

    S_{max} = \frac{t_{total}}{t_{serial}} = 1 + \frac{t_{parallel}}{t_{serial}}


Applying the law
================
* the output of ``monitor`` for 1 CPU contains the total runtime i.e. :math:`t_{serial}+t_{parallel}(1)`

* log statements have been added to the source code such that the parallel runtime :math:`t_{parallel}(P)` is recorded for *P* CPU's

Thus, you obtain the predicted speed up :math:`S_p(P)` and the observed speedup :math:`S_o(P)`

.. math::
    
    S_p (P) = \frac{t_{serial} + t_{parallel}(1)}{t_{serial} + \frac{t_{parallel}(1)}{P}} \qquad S_o(P) = \frac{t_{serial} + t_{parallel}(1)}{t_{serial} + t_{parallel}(P)}

From these, one can derive the efficiency for *P* cores as

.. math::
    
    E_p(P)=\frac{S_p(P)}{P}  \qquad\qquad\qquad E_o(P)=\frac{S_o(P)}{P}


External resources

`Wikipedia <http://en.wikipedia.org/wiki/Amdahl's_law‎>`_

`Reevaluating Amdahl's Law and Gustafson's Law <http://spartan.cis.temple.edu/shi/public_html/docs/amdahl/amdahl.html>`_
