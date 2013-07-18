#! /usr/bin/env python
from ctools import *
from gammalib import *
from math import *
import os
import glob
import sys

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

def pipeline():
    """copied from ctools/examples/make_binned_analysis"""
    """
    Binned analysis pipeline - keep intermediate results in memory.
    
    This function implements an analysis pipeline that successively calls
    ctobssim, ctbin and ctlike without saving the intermediate results as
    FITS files on disk. All data are hold in memory.
    
    At the end, results are plotted (if matplotlib is installed)
    """
    # Set script parameters
    model_name  = "${GAMMALIB}/share/models/crab.xml"
    caldb       = "${GAMMALIB}/share/caldb/cta"
    irf         = "cta_dummy_irf"
    ra          =   83.63
    dec         =   22.01
    rad_sim     =   10.0
    tstart      =    0.0
    tstop       = 1800.0
    emin        =    0.1
    emax        =  100.0
    enumbins    =   20
    nxpix       =  200
    nypix       =  200
    binsz       =    0.02
    coordsys    = "CEL"
    proj        = "CAR"

    # Simulate events
    sim = ctobssim()
    sim["infile"].filename(model_name)
    sim["caldb"].string(caldb)
    sim["irf"].string(irf)
    sim["ra"].real(ra)
    sim["dec"].real(dec)
    sim["rad"].real(rad_sim)
    sim["tmin"].real(tstart)
    sim["tmax"].real(tstop)
    sim["emin"].real(emin)
    sim["emax"].real(emax)
    sim.run()
    sys.stdout.write("Simulated events ("+str(sim.celapse())+" CPU seconds)\n")

    # Bin events into counts map
    bin = ctbin(sim.obs())
    bin["emin"].real(emin)
    bin["emax"].real(emax)
    bin["enumbins"].integer(enumbins)
    bin["nxpix"].integer(nxpix)
    bin["nypix"].integer(nypix)
    bin["binsz"].real(binsz)
    bin["coordsys"].string(coordsys)
    bin["xref"].real(ra)
    bin["yref"].real(dec)
    bin["proj"].string(proj)
    bin.run()
    sys.stdout.write("Binned events into counts map ("+str(bin.celapse())+" CPU seconds)\n")

    # Update timing
    wall_seconds += bin.telapse()
    cpu_seconds  += bin.celapse()

    # Perform maximum likelihood fitting
    like = ctlike(bin.obs())
    like.run()
    sys.stdout.write("Maximum likelihood fitting ("+str(like.celapse())+" CPU seconds)\n")

    # Update timing
    wall_seconds += like.telapse()
    cpu_seconds  += like.celapse()
        
    # Show total times
    sys.stdout.write("Total wall time elapsed: "+str(wall_seconds)+" seconds\n")
    sys.stdout.write("Total CPU time used ...: "+str(cpu_seconds)+" seconds\n")

    # Show model fitting results
    #sys.stdout.write(like.obs().models()+"\n")

    # Plot counts
    if has_matplotlib:
        plot_counts(bin.obs())
    else:
        sys.stdout.write("Matplotlib is not (correctly) installed on your system. No counts spectra are shown.\n")
    
    # Return
    return