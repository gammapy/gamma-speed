#/usr/bin/env python
"""Generate large event list and do file I/O to test monitoring.

TODO: develop this into a command line tool for testing
"""
import gammalib

# Simulate phase
events = gammalib.GCTAEventList()
n_events = int(1e3)
for _ in range(n_events):
	e = gammalib.GCTAEventAtom()
	events.append(e)

# Convert list to fits phase
fits = gammalib.GFits()
events.write(fits)


# Save fits to file phase
fits.saveto('/tmp/test_asdf.fits', True)


"""
Alternative: Write random data to FITS file via astropy.io.fits

import numpy as np
from astropy.io import fits
file_size = 1000 # in MB
# Generating random data is quite slow.
# I think you could use np.zeros() instead.
data = np.random.random(file_size * 1024 ** 2 / 8)
fits.writeto('data.fits', data=data, clobber=True)

Other alternative:
Generate GFits directly (not via GCTAEventList) ... see $GAMMALIB/test/test_GFits.py as an example.

"""