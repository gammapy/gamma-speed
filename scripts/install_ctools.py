#!/usr/bin/env python
"""Install multiple versions of gammalib / ctools

Having multiple versions (different compilers / configure options / ...)
is necessary for benchmarking and tedious to do by hand on multiple machines.

This script will generate shell scripts that download / configure / build / install
multiple versions of gammalib and ctools in the current working directory.
"""
import subprocess
import os
import argparse
import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')


def create_installation(options):
    logging.info('Creating installation: {0}'.format(options['name']))

    GAMMALIB_URL = 'git@github.com:gammalib/gammalib.git'
    cmds = """
mkdir {name}
cd {name}
git clone {GAMMALIB_URL}"""


def create_all_installations():
    pass


if __name__ == '__main__':
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('infile', type=str,
                        help='Input FITS file name')
    args = parser.parse_args()
    args = vars(args)
    """
    create_all_environments()