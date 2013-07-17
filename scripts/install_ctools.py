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
import pandas as pd
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')


class installer:
    def __init__(self, options):
        self.options = options

    def __call__(self):
        self.create_environment()
        self.install_gammalib()
        self.install_ctools()
        
    def create_environment(self):
        logging.info('Creating installation: {0}'.format(self.options['name']))
    
        name = self.options['name']
        
        GAMMALIB_URL = self.options['gamma_url']
        CTOOLS_URL = self.options['ctools_url']
        
        # Create the install commands and execute them
        try:
            down = "mkdir {0}; cd {0}; git clone {1}; git clone {2}; mkdir install".format(name, GAMMALIB_URL, CTOOLS_URL)
            proc = subprocess.Popen(args=down, shell=True, stdout=subprocess.PIPE)
            proc.wait()
            self.options['install_path'] = os.path.abspath(name + '/install')
            logging.info("software successfuly downloaded")
        except:
            logging.error("something went wrong")
            exit()
            
    def install_gammalib(self):
        logging.info("Entered GAMMALIB install")
    
        folder_name = self.options['name'] + '/gammalib/'
        
        # account for the possibility of having to install a certain branch
        if self.options['branch'] != None:
            branch_me_baby = 'git checkout ' + self.options['branch'] + "; "
        else:
            branch_me_baby = ''
            
        goto_branch = "cd " + folder_name + "; " + branch_me_baby
        
        gen_config_install = './autogen.sh; ' + './configure --prefix=' + self.options['install_path'] + '; make; make install'
        try:
            proc = subprocess.Popen(args=goto_branch + gen_config_install, stdout=subprocess.PIPE, shell=True)
            proc.wait()
            logging.info("GAMMALIB install finished")
        except:
            logging.error("GAMMALIB install failed")
            exit()
    
    def install_ctools(self):
        logging.info("Entered CTOOLS install")
    
        folder_name = self.options['name'] + '/ctools/'
        
        # account for the possibility of having to install a certain branch
        if self.options['branch'] != None:
            branch_me_baby = 'git checkout ' + self.options['branch'] + "; "
        else:
            branch_me_baby = ''
            
        goto_branch = "cd " + folder_name + "; " + branch_me_baby
        
        gen_config_install = './autogen.sh; ' + './configure --prefix=' + self.options['install_path'] + '; make; make install'
        try:
            proc = subprocess.Popen(args = goto_branch + gen_config_install, stdout=subprocess.PIPE, shell=True)
            proc.wait()
            logging.info("CTOOLS install finished")
        except:
            logging.error("CTOOLS install failed")
            exit()
    
def general_install():
    GAMMALIB_URL = 'git@github.com:gammalib/gammalib.git'
    CTOOLS_URL = 'git@github.com:ctools/ctools.git'
    NAME = 'general_install'
    BRANCH = None
    INSTALL_PATH = None
    
    options = pd.Series(data=[GAMMALIB_URL, CTOOLS_URL, NAME, BRANCH, INSTALL_PATH],
                        index=['gamma_url', 'ctools_url', 'name', 'branch', 'install_path'], dtype=str)
    
    gen_installer = installer(options)
    gen_installer()
    
def logging_install():
    GAMMALIB_URL = 'git@github.com:ignatndr/gammalib.git'
    CTOOLS_URL = 'git@github.com:ignatndr/ctools.git'
    NAME = 'extralog_install'
    BRANCH = 'gammaspeed_extra_log'
    INSTALL_PATH = None
    
    options = pd.Series(data=[GAMMALIB_URL, CTOOLS_URL, NAME, BRANCH, INSTALL_PATH],
                        index=['gamma_url', 'ctools_url', 'name', 'branch', 'install_path'], dtype=str)
    
    log_installer = installer(options)
    log_installer()
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-log', type=bool, default=False,
                        help='Choose whether to install the extra_log version of ctools and gammalib')
    
    parser.add_argument('-gen', type=bool, default=False,
                        help='Choose whether to install the general version of ctools and gammalib')
    
    args = parser.parse_args()
    if args.log:
        logging_install()
        
    if args.gen:
        general_install()

