#!/usr/bin/env python
"""Generate large event list and do file I/O to test monitoring.

TODO: develop this into a command line tool for testing
"""
import argparse
import os


def gamma_save(file_size):
    import gammalib

    # Set filename
    filename = "data.fits"

    fits = gammalib.GFits(filename, True)

    # multiply by 1000 to get MB filesize
    nrows = file_size * 1024
    # one column contains a string that is 1kb
    col9 = gammalib.GFitsTableStringCol("STRING", nrows, 1024)
    for i in range(nrows):
        col9[i] = str(i * 100)
    tbl_ascii = gammalib.GFitsAsciiTable()
    tbl_ascii.append_column(col9)
    fits.append(tbl_ascii)

    fits.save(clobber=False)
    fits.close()


def gamma_saveto(file_size):
    import gammalib

    # Set filename
    filename = "data.fits"

    fits = gammalib.GFits(filename, True)

    # multiply by 1000 to get MB filesize
    nrows = file_size * 1024
    # one column contains a string that is 1kb
    col9 = gammalib.GFitsTableStringCol("STRING", nrows, 1024)
    for i in range(nrows):
        col9[i] = str(i * 100)
    tbl_ascii = gammalib.GFitsAsciiTable()
    tbl_ascii.append_column(col9)
    fits.append(tbl_ascii)

    fits.saveto("copy.fits")


def fits_gen(file_size):
    # Alternative: Write random data to FITS file via astropy.io.fits
    import numpy as np
    from astropy.io import fits
    # Generate np.zeros() data.
    # NOTE: one could use random data instead,
    # but the generation process(that uses CPU) is not important.
    data = np.zeros(file_size * 1024 ** 2 / 8)
    fits.writeto('data.fits', data=data, clobber=True)


def fits_copy(file_size):
    fits_gen(file_size)
    d = open('data.fits', 'r')
    c = open('copy1.fits', 'w')
    c.write(d.read())
    d.close()
    c.close()

# Other alternative:
# Generate GFits directly (not via GCTAEventList) ... see
# $GAMMALIB/test/test_GFits.py as an example.


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-iot', '--iotype', default='gamma_save',
                        choices=['fits_gen', 'fits_copy', 
                                 'gamma_save', 'gamma_saveto'],
                        help='choose the type of io that you want to make')
    parser.add_argument('-s', '--size', default=1000,
                        help='size in MB of the file you want to make')

    args = parser.parse_args()
    func_list = {
        'fits_gen': fits_gen,
        'fits_copy': fits_copy,
        'gamma_save': gamma_save,
        'gamma_saveto': gamma_saveto}
    func_list[args.iotype](int(args.size))
    # Remove test files
    try:
        os.remove('data.fits')
        os.remove('copy.fits')
    except:
        pass

if __name__ == '__main__':
    main()
