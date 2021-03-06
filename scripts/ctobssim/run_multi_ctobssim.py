#!/usr/bin/env python
"""Run ctobssim with multiple observations to see if OpenMP kicks in."""
import argparse
import gammalib
import ctools
import pandas as pd
import platform
import multiprocessing


def set(RA=83.63, DEC=22.01, tstart=0.0, duration=1800.0, deadc=0.95,
        emin=0.1, emax=100.0, rad=5.0,
        irf="cta_dummy_irf", caldb="$GAMMALIB/share/caldb/cta"):
    """
    Create one CTA observation

    Copied from ctools/scripts/obsutils.py and modified a bit.
    """
    # Allocate CTA observation
    obs = gammalib.GCTAObservation()

    # Set pointing direction
    pntdir = gammalib.GSkyDir()
    pntdir.radec_deg(RA, DEC)

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


def run_multi_ctobssim(RA, DEC, TSTART, DURATION,
                       DEADC, EMIN, EMAX, RAD, IRF, CALDB, outfile, nobs):
    """TODO: document what it does"""

    observations = gammalib.GObservations()

    # Automatically generate a number of nobs
    for i in xrange(nobs):
        obs = set(RA, DEC, TSTART, DURATION, DEADC, EMIN, EMAX,
                  RAD, IRF, CALDB)
        obs.id(str(i))
        observations.append(obs)

    observations.models('$CTOOLS/share/models/crab.xml')

    ctobssim = ctools.ctobssim(observations)
    ctobssim.logFileOpen()
    ctobssim['outfile'].filename(outfile)

    ctobssim.execute()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, add_help=True)

    parser.add_argument("-RA", type=float,
                        help="right ascension",
                        default=86.63)
    parser.add_argument("-DEC", type=float,
                        help="declination",
                        default=22.01)
    parser.add_argument("-tstart", type=float,
                        help="the time at which the observation starts",
                        default=0.0)
    parser.add_argument("-dur", type=float,
                        help="duration of the observation",
                        default=3000.0)
    parser.add_argument("-deadc", type=float,
                        help="deadtime correction factor",
                        default=0.95)
    parser.add_argument("-emin", type=float,
                        help="minimum energy in TeV",
                        default=0.1)
    parser.add_argument("-emax", type=float,
                        help="maximum energy in TeV",
                        default=100.0)
    parser.add_argument("-rad", type=float,
                        help=" ",
                        default=5.0)
    parser.add_argument("-irf", type=str,
                        help="name of the file containing the " +
                        "Instrument Response Function",
                        default="cta_dummy_irf")
    parser.add_argument("-caldb", type=str,
                        help="path to calibration database",
                        default="$GAMMALIB/share/caldb/cta")
    parser.add_argument("-outfile", type=str,
                        help="name of outfile",
                        default='sim_events.xml')
    parser.add_argument("-nobs", type=int,
                        help="number of observations to be generated",
                        default=multiprocessing.cpu_count())

    args = parser.parse_args()

    run_multi_ctobssim(
        args.RA,
        args.DEC,
        args.tstart,
        args.dur,
        args.deadc,
        args.emin,
        args.emax,
        args.rad,
        args.irf,
        args.caldb,
        args.outfile,
        args.nobs)
