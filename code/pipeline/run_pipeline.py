#! /usr/bin/env python
from ctools import *
from gammalib import *
import argparse
import multiprocessing
import pandas as pd
import time 

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
def pipeline_save(nevents):
    """
    Binned analysis pipeline - save intermediate results.
    
    This function implements an analysis pipeline that successively calls
    ctobssim, ctbin and ctlike by saving the intermediate results as FITS
    files on disk. This replicates the way how the analysis would be done
    in a ftools-like approach.
    """
    # Set script parameters
    model_name  = "${GAMMALIB}/share/models/crab.xml"
    events_name = "events.fits"
    cntmap_name = "cntmap.fits"
    result_name = "results.xml"
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

    # Initialise timing
    wall_seconds = 0.0
    cpu_seconds  = 0.0
    
    times=list()    
    events=list()
    # Simulate events
    # since we want more than one event, we will have to use a 
    # GObservations container for our event list
    observations = GObservations()

    times.append(time.time())
    events.append("gammaspeed_ctobssim_start")
    for i in xrange(nevents):
        obs = set()
        obs.id(str(i))
        observations.append(obs)

    observations.models('$CTOOLS/share/models/crab.xml')
    sim = ctobssim(observations)
    sim.logFileOpen()
    sim["outfile"].filename(events_name)
    sim.execute()
    
    times.append(time.time())
    events.append("gammaspeed_ctobssim_end")
    
    times.append(time.time())
    events.append("gammaspeed_ctbin_start")
    # Bin events into counts map
    bin = ctbin()
    bin.logFileOpen()  # We need this to explicitely open the log file in Python mode
    bin["evfile"].filename(events_name)
    bin["outfile"].filename(cntmap_name)
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
    bin.execute()
    times.append(time.time())
    events.append("gammaspeed_ctbin_end")
    
    times.append(time.time())
    events.append("gammaspeed_ctlike_start")
    # Perform maximum likelihood fitting
    like = ctlike()
    like.logFileOpen()  # We need this to explicitely open the log file in Python mode
    like["infile"].filename(cntmap_name)
    like["srcmdl"].filename(model_name)
    like["outmdl"].filename(result_name)
    like["caldb"].string(caldb)
    like["irf"].string(irf)
    like.execute()
    times.append(time.time())
    events.append("gammaspeed_ctlike_start")
    
    s=pd.Series(events, index=times)
    s.to_csv("pipeline_save_CPU=" + str(multiprocessing.cpu_count()) + ".csv")
    # Return
    return

def pipeline_in_memory(nevents):
    """copied from ctools/examples/make_binned_analysis"""
    
    # Set script parameters
    model_name = "${GAMMALIB}/share/models/crab.xml"
    caldb = "${GAMMALIB}/share/caldb/cta"
    irf = "cta_dummy_irf"
    ra = 83.63
    dec = 22.01
    rad_sim = 10.0
    tstart = 0.0
    tstop = 1800.0
    emin = 0.1
    emax = 100.0
    enumbins = 20
    nxpix = 200
    nypix = 200
    binsz = 0.02
    coordsys = "CEL"
    proj = "CAR"
    
    times=list()    
    events=list()
    # Simulate events
    # since we want more than one event, we will have to use a 
    # GObservations container for our event list
    observations = GObservations()

    times.append(time.time())
    events.append("gammaspeed_ctobssim_start")
    for i in xrange(nevents):
        obs = set()
        obs.id(str(i))
        observations.append(obs)

    observations.models('$CTOOLS/share/models/crab.xml')
    sim = ctobssim(observations)
    sim.logFileOpen()
    sim.run()
    
    times.append(time.time())
    events.append("gammaspeed_ctobssim_end")
    
    times.append(time.time())
    events.append("gammaspeed_ctbin_start")
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
    bin.logFileOpen()
    bin.run()
    times.append(time.time())
    events.append("gammaspeed_ctbin_end")
    
    times.append(time.time())
    events.append("gammaspeed_ctlike_start")
    # Perform maximum likelihood fitting
    like = ctlike(bin.obs())
    like.logFileOpen()
    like.run()
    times.append(time.time())
    events.append("gammaspeed_ctlike_end")
    
    s=pd.Series(events, index=times)
    s.to_csv("pipeline_in_memory_CPU=" + str(multiprocessing.cpu_count()) + ".csv")
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, add_help=True)
    
    parser.add_argument("-nobs", type=int, help="number of observations to be generated", default=multiprocessing.cpu_count())
    parser.add_argument("-type", type=str, help="type of pipeline to run", default='in_memory')

    args = parser.parse_args()
    
    if args.type is 'in_memory':
        pipeline_in_memory(args.nobs)
    else:
        pipeline_save(args.nobs)
