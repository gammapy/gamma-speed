#!/bin/bash

## This script automatically clones and installs one version of ctools and gammalib and ctools in the current directory.
## The usage is 
##      ./install_ctools.sh [SOURCE] [BRANCH]
##  where SOURCE can be either LOG -> git@github.com:ignatndr/gammalib git@github.com:ignatndr/ctools.git
##                          or NORMAL -> git@github.com:gammalib/gammalib.git git@github.com:ctools/ctools.git
##  and BRANCH is the optional git branch that should be installed
##  In the case no SOURCE is specified, nothing is done by the script. 

## For gammaspeed, execute the script under
##          ./install_ctools.sh LOG gammaspeed_extra_log

SOURCE=$1
BRANCH=$2

if [ "$SOURCE" = "LOG" ]; then
        #set up directory structure and download neccessary software
        mkdir extralog_install
        cd extralog_install
        git clone git@github.com:ignatndr/gammalib.git
        git clone git@github.com:ignatndr/ctools.git
        mkdir install
        INSTALL_DIR=$PWD/install

        #install gammalib
        cd gammalib
        if [ "$BRANCH" != NULL ];
            then 
                git checkout $BRANCH
        fi
        ./autogen.sh
        ./configure --prefix=$INSTALL_DIR
        make
        make install
        
        #install ctools
        cd ../ctools
        if [ "$BRANCH" != NULL ];
            then 
                git checkout BRANCH
        fi
        ./autogen.sh
        ./configure --prefix=INSTALL_DIR
        make
        make install
        
        #print further instructions
        echo 
        echo Files have been installed in 
        echo $INSTALL_DIR
        echo To use the gammalib and ctools version that you just installed, please
        echo run the following commands:
        echo    export GAMMALIB = $INSTALL_DIR
        echo    export CTOOLS = $INSTALL_DIR
        echo    source \$CTOOLS/bin/ctools-init.sh
        echo    source \$GAMMALIB/bin/gammalib-init.sh

fi;

if [ "$SOURCE" = "NORMAL" ]; then
        #set up directory structure and download neccessary software
        mkdir normal_install
        cd normal_install
        git@github.com:gammalib/gammalib.git
        git@github.com:ctools/ctools.git
        mkdir install
        INSTALL_DIR=$PWD/install
        
        #install gammalib
        cd gammalib
        if [ "$BRANCH" != NULL ];
            then 
                git checkout $BRANCH
        fi
        ./autogen.sh
        ./configure --prefix=$INSTALL_DIR
        make
        make install
        
        #install install ctools
        cd ../ctools
        if [ "$BRANCH" != NULL ];
            then 
                git checkout $BRANCH
        fi
        ./autogen.sh
        ./configure --prefix=$INSTALL_DIR
        make
        make install
        
        #print further instructions
        echo 
        echo Files have been installed in 
        echo $INSTALL_DIR
        echo To use the gammalib and ctools version that you just installed, please
        echo run the following commands:
        echo    export GAMMALIB = $INSTALL_DIR
        echo    export CTOOLS = $INSTALL_DIR
        echo    source \$CTOOLS/bin/ctools-init.sh
        echo    source \$GAMMALIB/bin/gammalib-init.sh
fi;
