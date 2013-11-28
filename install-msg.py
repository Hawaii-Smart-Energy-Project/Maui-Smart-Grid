#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MSG Install Script

This is an interface to the install process.

1. Create the distribution archive.
2. Extract the distribution.
3. Install the distribution.

Usage:

    python install-msg.py --sourcePath ${ROOT_PATH_TO_SOURCE}
    --installPathUser ${PATH_OF_USER_BASED_INSTALL}

The distribution archive is placed in ${ROOT_PATH_TO_SOURCE}/dist.

"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import subprocess
import argparse
import os
from msg_logger import MSGLogger


def processCommandLineArguments():
    global argParser, commandLineArgs
    argParser = argparse.ArgumentParser(description = '')
    argParser.add_argument('--sourcePath',
                           help = 'Path where the source code is located.',
                           required = True)
    argParser.add_argument('--installPathUser',
                           help = 'Path to be used for a user based install.',
                           required = True)

    commandLineArgs = argParser.parse_args()


def runCommand(cmd = None):
    if cmd is not None:
        try:
            subprocess.check_call(cmd, shell = True)
        except subprocess.CalledProcessError, e:
            logger.log("An exception occurred: %s" % e, 'error')


commandLineArgs = None
logger = MSGLogger(__name__)
processCommandLineArguments()

os.chdir(commandLineArgs.sourcePath)

print "%s" % os.getcwd()

archiveCmd = """python setup.py sdist"""
runCommand(archiveCmd)

installCmd = """python setup.py install --home=%s""" % commandLineArgs\
    .installPathUser
runCommand(installCmd)

print "\nInstallation of the MSG software to %s is complete." % \
      commandLineArgs.installPathUser
print "\nPlease add the following path, %s/lib/python, to your PYTHONPATH if " \
      "it " \
      "is not already there." % commandLineArgs.installPathUser
