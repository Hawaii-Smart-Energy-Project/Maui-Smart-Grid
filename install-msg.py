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
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import subprocess
import argparse
import os
import tarfile

COMMAND_LINE_ARGS = None

def processCommandLineArguments():
    global argParser, COMMAND_LINE_ARGS
    argParser = argparse.ArgumentParser(description = '')
    argParser.add_argument('--sourcePath',
                           help = 'Path where the source code is located.',
                           required = True)
    argParser.add_argument('--installPathUser',
                           help = 'Path to be used for a user based install.',
                           required = True)

    COMMAND_LINE_ARGS = argParser.parse_args()


def runCommand(cmd = None):
    """
    Run a system command.
    :param cmd: String of command to run.
    :return: None.
    """
    if cmd is not None:
        try:
            subprocess.check_call(cmd, shell = True)
        except subprocess.CalledProcessError as error:
            print "Exception occurred while calling the process to run a " \
                  "command: {}".format(error)


def softwareInstallName():
    """
    Provide the software install name.
    :returns: String for name of software.
    """
    softwareName = ''
    cmd = "python {}/setup.py --name".format(COMMAND_LINE_ARGS.sourcePath)
    try:
        softwareName = subprocess.check_output(cmd, shell = True)
    except subprocess.CalledProcessError as error:
        print "An exception occurred while calling the process to get the " \
              "software install name: {}".format(error)
    return softwareName.strip()


def softwareVersion():
    """
    There may be issues with retrieving the version number this way when
    dependencies are defined in __init.py__.
    """
    softwareVersion = ''
    cmd = "python {}/setup.py --version".format(COMMAND_LINE_ARGS.sourcePath)
    try:
        softwareVersion = subprocess.check_output(cmd, shell = True)
    except subprocess.CalledProcessError as error:
        print "An exception occurred while calling the process to get the " \
              "software version: {}".format(error)
    return softwareVersion.strip()


processCommandLineArguments()

os.chdir(COMMAND_LINE_ARGS.sourcePath)

archiveCmd = "python setup.py sdist"
runCommand(archiveCmd)

PROJECT_NAME = softwareInstallName()
VERSION = softwareVersion()

print "Current working directory is {}.".format(os.getcwd())
print "\nPerforming scripted install of {}-{}.".format(PROJECT_NAME, VERSION)

# Extract the distribution archive into the dist directory.
os.chdir('{}/dist'.format(COMMAND_LINE_ARGS.sourcePath))
print
print "Current working directory is {}.".format(os.getcwd())
t = tarfile.open(
    name = '{}/dist/{}-{}.tar.gz'.format(COMMAND_LINE_ARGS.sourcePath,
                                         PROJECT_NAME, VERSION))

t.extractall()

# Change the working directory to the extracted archive path.
print "Performing install."
os.chdir(
    '{}/dist/{}-{}'.format(COMMAND_LINE_ARGS.sourcePath, PROJECT_NAME, VERSION))
print "Current working directory is {}.".format(os.getcwd())

# Install the software.
installCmd = """python setup.py install --home={}/{}-{}""".format(
    COMMAND_LINE_ARGS.installPathUser, PROJECT_NAME, VERSION)
runCommand(installCmd)

print "\nInstallation of the MSG software to {} is complete.".format(
    COMMAND_LINE_ARGS.installPathUser)
print "\nPlease add the path, {}/lib/python, to your PYTHONPATH if it is not already there.".format(
    COMMAND_LINE_ARGS.installPathUser)
