#!/usr/bin/env python
"""Run ctobssim with multiple observations to see if OpenMP kicks in."""
import argparse
import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')
import gammalib
import ctools


def set(RA=83.63, DEC=22.01, tstart=0.0, duration=1800.0, deadc=0.95,
        emin=0.1, emax=100.0, rad=5.0,
        irf="cta_dummy_irf", caldb="$GAMMALIB/share/caldb/cta"):
    """Create one CTA observation

    Copied from ctools/scripts/obsutils.py and modified a bit.
    """
    # Allocate CTA observation
    obs = gammalib.GCTAObservation()

    # Set pointing direction
    pntdir = gammalib.GSkyDir()
    pntdir.radec_deg(RA, DEC)
    # import IPython; IPython.embed(); 1/0
    pnt = gammalib.GCTAPointing()
    pnt.dir(pntdir)
    obs.pointing(pnt)

    # Set ROI
    roi = gammalib.GCTARoi()
    instdir = gammalib.GCTAInstDir()
    instdir.dir(pntdir)
    roi.centre(instdir)
    roi.radius(rad)

    # Set GTI
    gti = gammalib.GGti()
    start = gammalib.GTime(tstart)
    stop = gammalib.GTime(tstart + duration)
    gti.append(start, stop)

    # Set energy boundaries
    ebounds = gammalib.GEbounds()
    e_min = gammalib.GEnergy()
    e_max = gammalib.GEnergy()
    e_min.TeV(emin)
    e_max.TeV(emax)
    ebounds.append(e_min, e_max)

    # Allocate event list
    events = gammalib.GCTAEventList()
    events.roi(roi)
    events.gti(gti)
    events.ebounds(ebounds)
    obs.events(events)

    # Set instrument response
    obs.response(irf, caldb)

    # Set ontime, livetime, and deadtime correction factor
    obs.ontime(duration)
    obs.livetime(duration * deadc)
    obs.deadc(deadc)

    # Return observation
    return obs


def run_multi_ctobssim(obstime=1e5):
    """TODO: document what it does"""
    obs1 = set(duration=int(obstime))
    obs2 = set(duration=int(obstime))
    observations = gammalib.GObservations()
    obs1.id('1')
    obs2.id('2')
    observations.append(obs1)
    observations.append(obs2)
    observations.models('$CTOOLS/share/models/crab.xml')

    ctobssim = ctools.ctobssim(observations)
    ctobssim.logFileOpen()
    ctobssim['outfile'].filename('sim_events.xml')

    ctobssim.execute()
    ctobssim.save()

if __name__ == '__main__':
    # TODO: set obstime, n_obs, write_outfiles, ... via command line arguments
    parser = argparse.ArgumentParser(description=__doc__)
    # parser.add_argument('outfile', type=str,
    #                    help='Output XML file name')
    args = parser.parse_args()
    args = vars(args)

    run_multi_ctobssim()
