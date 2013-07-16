#!/usr/bin/env python
"""Run ctlike for multiple observations."""
import argparse
import ctools
import pandas as pd
import platform
import multiprocessing

def ctlike_unbinned(selected_events_name, IRF, CALDB, outfile):
    """
    Copied and modified from ctools/test/test_python.py
    """
    # Perform maximum likelihood fitting
    like = ctools.ctlike()
    like.logFileOpen()
    like["infile"].filename(selected_events_name)
    like["srcmdl"].filename('$CTOOLS/share/models/crab.xml')
    like["outmdl"].filename(outfile)
    like["caldb"].string(CALDB)
    like["irf"].string(IRF)
    like.execute()

def ctlike_binned(events_name, cntmap_name, emin, emax, enumbins, nxpix, nypix, binsz, ra, dec, IRF, CALDB, outfile):
    """
    Copied and modified from ctools/examples/make_binned_analysis.py
    """
    # Bin the events first
        # Bin events into counts map
    bin = ctools.ctbin()
    bin.logFileOpen()  # We need this to explicitely open the log file in Python mode
    bin["evfile"].filename(events_name)
    bin["outfile"].filename(cntmap_name)
    bin["emin"].real(emin)
    bin["emax"].real(emax)
    bin["enumbins"].integer(enumbins)
    bin["nxpix"].integer(nxpix)
    bin["nypix"].integer(nypix)
    bin["binsz"].real(binsz)
    bin["coordsys"].string('GAL')
    bin["xref"].real(ra)
    bin["yref"].real(dec)
    bin["proj"].string('CAR')
    bin.execute()

    # Perform maximum likelihood fitting
    like = ctools.ctlike()
    like.logFileOpen()
    like["infile"].filename(cntmap_name)
    like["srcmdl"].filename('$CTOOLS/share/models/crab.xml')
    like["outmdl"].filename(outfile)
    like["caldb"].string(CALDB)
    like["irf"].string(IRF)
    like.execute()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, add_help=True)
    
    
    parser.add_argument("-infile", type=str, help="name of file containing the events/list of event files", default="sim_events.xml")
    parser.add_argument("-irf", type=str, help="name of the file containing the Instrument Response Function", default="cta_dummy_irf")
    parser.add_argument("-caldb", type=str, help="path to calibration database", default="$GAMMALIB/share/caldb/cta")
    parser.add_argument("-outfile", type=str, help="name of outfile", default='fit_results.xml')
    parser.add_argument("-binfile", type=str, help="name of file containing ctbin output", default='bin_results.xml')
    parser.add_argument("-binned", type=bool, help="do binned or unbinned analysis", default=False)

    args = parser.parse_args()
    
    if args.binned:
        ctlike_binned(args.infile, args.binfile, 0.1, 100.0, 20,200, 200, 0.02, 83.63, 22.01, args.irf, args.caldb, args.outfile)
    else:
        ctlike_unbinned(args.infile, args.irf, args.caldb, args.outfile)
