#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MSG Install Script

This script is useful for updating an existing MSG software installation from an
active development code base (the most recent source code base).

This is an interface to the install process that automates the following
operations.

1. Create the distribution archive.
2. Extract the distribution archive.
2. Install the distribution from extracted archive.

Usage:

    python install-msg.py --sourcePath ${ROOT_PATH_TO_SOURCE}
    --installPathUser ${BASE_PATH_OF_USER_BASED_INSTALL}

The distribution archive is placed in ${ROOT_PATH_TO_SOURCE}/dist.

Important Note:
*****************************************************************************
The software is installed to path given by the base path to a directory named
after the software including its version number. For example, if the user
install path is  given as ~/software the software will be installed to
~/software/Maui-Smart-Grid-1.x.x where 1.x.x represents the appropriate
version number.
*****************************************************************************

The external dependencies, documented at

    https://github.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid
    #installation-and-updating

should be satisfied using a suitable method such as installation through pip.
"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import subprocess
import argparse
import os
import tarfile


def processCommandLineArguments():
    global argParser, COMMAND_LINE_ARGS
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
        except subprocess.CalledProcessError as error:
            print "Exception occurred while calling the process to run a " \
                  "command: %s" % error


def softwareInstallName():
    cmd = "python %s/setup.py --name" % COMMAND_LINE_ARGS.sourcePath
    try:
        softwareName = subprocess.check_output(cmd, shell = True)
    except subprocess.CalledProcessError as error:
        print "An exception occurred while calling the process to get the " \
              "software install name: %s" % error
    return softwareName.strip()


def softwareVersion():
    """
    There may be issues with retrieving the version number this way when
    dependencies are defined in __init.py__.
    """

    cmd = "python %s/setup.py --version" % COMMAND_LINE_ARGS.sourcePath
    try:
        softwareVersion = subprocess.check_output(cmd, shell = True)
    except subprocess.CalledProcessError as error:
        print "An exception occurred while calling the process to get the " \
              "software version: %s" % error
    return softwareVersion.strip()


COMMAND_LINE_ARGS = None
processCommandLineArguments()

os.chdir(COMMAND_LINE_ARGS.sourcePath)

archiveCmd = """python setup.py sdist"""
runCommand(archiveCmd)

PROJECT_NAME = softwareInstallName()
VERSION = softwareVersion()

print "Current working directory is %s." % os.getcwd()
print "\nPerforming scripted install of %s-%s." % (PROJECT_NAME, VERSION)

# Extract the distribution archive into the dist directory.
os.chdir('%s/dist' % COMMAND_LINE_ARGS.sourcePath)
print
print "Current working directory is %s." % os.getcwd()
t = tarfile.open(name = '%s/dist/%s-%s.tar.gz' % (
    COMMAND_LINE_ARGS.sourcePath, PROJECT_NAME, VERSION))

t.extractall()

# Change the working directory to the extracted archive path.
print "Performing install."
os.chdir('%s/dist/%s-%s' % (COMMAND_LINE_ARGS.sourcePath, PROJECT_NAME, VERSION ))
print "Current working directory is %s." % os.getcwd()

# Install the software.
installCmd = """python setup.py install --home=%s/%s-%s""" % (
    COMMAND_LINE_ARGS.installPathUser, PROJECT_NAME, VERSION)
runCommand(installCmd)

print "\nInstallation of the MSG software to %s is complete." % \
      COMMAND_LINE_ARGS.installPathUser
print "\nPlease add the path, %s/lib/python, to your PYTHONPATH if it is not " \
      "already there." % COMMAND_LINE_ARGS.installPathUser
