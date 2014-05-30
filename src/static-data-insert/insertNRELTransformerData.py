#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module inserts transformer data into the database from NREL tab-separated 
data files for the distribution transformers that NREL metered in 2012 and
2013. Meters ST530 and ST534 are commercial model TPYT, while  15502, 10745 and
13976, residential meters of model SPDT. It walks the directory tree from the 
working directory to get all CSV file paths, and parses them as it goes. This
module requires a correctly configured instance of the Maui Smart Grid software
in the runtime environment.

Usage:
Run script from a working directory that contains files and folders that have
the NREL transformer data. And type:

insertNRELTransformerData.py [--email] [--testing]
"""

__author__ = 'David Wilkie'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import csv
import sys
import subprocess
import shutil
import os
from os.path import join
from msg_db_connector import MSGDBConnector
from msg_db_util import MSGDBUtil
from msg_notifier import MSGNotifier
from msg_configer import MSGConfiger
from msg_logger import MSGLogger
import argparse

commandLineArgs = None
logger = MSGLogger(__name__, 'debug')

def processCommandLineArguments():
    global argParser, commandLineArgs, filename
    argParser = argparse.ArgumentParser(
        description = 'Perform insertion of NREL Transformer data contained '
                      'in the wprking directory into the meco_v3 database.')
    argParser.add_argument('--email', action = 'store_true', default = False,
                           help = 'Send email notification if this flag is '
                                  'specified.')
    argParser.add_argument('--testing', action = 'store_true', default = False,
                           help = 'If this flag is on, '
                                  'insert data to the testing database as '
                                  'specified in the local configuration file.')
    commandLineArgs = argParser.parse_args()

def getDeviceNameFromFileName(name):
    """Parses the filename and returns device name, or false if not found."""
    if '10754' in name:
        return '10754'
    elif '13976' in name:
        return '13976'
    elif '15502' in name:
        return '15502'
    elif 'ST530' in name:
        return 'ST530'
    elif 'ST534' in name:
        return 'ST534'
    else:
        return False

if __name__ == '__main__':

    processCommandLineArguments()

    success = True
    anyFailure = False
    connector = MSGDBConnector(testing = commandLineArgs.testing)
    conn = connector.connectDB()
    cur = conn.cursor()
    dbUtil = MSGDBUtil()
    notifier = MSGNotifier()
    msgBody = ''
    configer = MSGConfiger()

    if commandLineArgs.testing:
        dbName = configer.configOptionValue("Database", "testing_db_name")
    else:
        dbName = "meco_v3"

    for root, dirs, files in os.walk(os.getcwd()):
        # For each file in the list of found files.
        for name in files:
            nameAndPath = join(root, name)
            if not '.csv' in name.lower(): # Skip all non-CSV files.
                continue
            msg = ("Loading NREL xformer data in file %s to database %s.\n" % (
                nameAndPath, dbName))
            sys.stderr.write(msg)
            msgBody += msg

            data = []
            lineCnt = 0

            with open(nameAndPath, "rU") as csvFile:
                for line in csv.reader(csvFile, delimiter = ","):
                    if lineCnt == 0: # Check the type of transformer.
                        if '15502' in name or '13976' in name \
                        or '10754' in name:
                            cols = ["timestamp", "quality", "v1_phasor_magnitude",\
                                    "v1_phase_angle", "v2_phasor_magnitude", \
                                    "v2_phase_angle", "v12_phasor_magnitude", \
                                    "v12_phase_angle", "i1_phasor_magnitude", \
                                    "i1_phase_angle", "i2_phasor_magnitude", \
                                    "i2_phase_angle", "in_phasor_magnitude", \
                                    "in_phase_angle", "frequency", "v1_rms", \
                                    "v2_rms", "v12_rms", "i1_rms", "i2_rms", \
                                    "in_rms", "apparent_power_magnitude_s", \
                                    "real_power_p", "reactive_power_q", \
                                    "power_factor", "meter_internal_temperature", \
                                    "transformer_housing_temperature", \
                                    "device_name"]
                            table = "dw.\"TransformerDataNREL\""

                        if 'ST534' in name or 'ST530' in name:
                            cols = ["timestamp", "quality", \
                                "va_phasor_magnitude", "va_phasor_angle", \
                                "vb_phasor_magnitude", "vb_phasor_angle", \
                                "vc_phasor_magnitude", "vc_phasor_angle",\
                                "ia_phasor_magnitude", "ia_phasor_angle", \
                                "ib_phasor_magnitude", "ib_phasor_angle", \
                                "ic_phasor_magnitude", "ic_phasor_angle", \
                                "frequency", "va_rms", "vb_rms", "vc_rms", \
                                "ia_rms", "ib_rms", "ic_rms", \
                                "apparent_power_magnitude_s", \
                                "phase_a_apparent_power_magnitude_s", \
                                "phase_b_apparent_power_magnitude_s", \
                                "phase_c_apparent_power_magnitude_s", \
                                "real_power_p", "phase_a_real_power_p", \
                                "phase_b_real_power_p", "phase_c_real_power_p",\
                                "reactive_power_q", "phase_a_reactive_power_q",\
                                "phase_b_reactive_power_q", \
                                "phase_c_reactive_power_q", "power_factor", \
                                "meter_internal_temperature", \
                                "transformer_housing_temperature", \
                                "device_name"]
                            table = "dw.\"TransformerDataNRELST\""

                    if lineCnt != 0: # Skip header.
                        data = line[0:len(cols)] # Overshoot to get last column.

                        for i in range(0, len(cols) - 1):
                            if len(data[i]) == 0 or data[i] == 'nil':
                                data[i] = 'NULL'
                            else:
                                # Escape single quotes with double single quotes in
                                # PostgreSQL.
                                data[i] = data[i].replace("'", "\'\'")
                                data[i] = "'" + data[i] + "'"

                        data = data + ["'" + getDeviceNameFromFileName(name) + "'"]

                        sql = """INSERT INTO %s (%s) VALUES (%s)""" % (
                            table, ','.join(cols), ','.join(data))
                        success = dbUtil.executeSQL(cur, sql)
                        if not success:
                            anyFailure = True

                    lineCnt += 1

            conn.commit()
            msg = ("Processed %s lines.\n" % lineCnt)
            lineCnt = 0
            sys.stderr.write(msg)
            msgBody += msg

    if not anyFailure:
        msg = "Finished inserting NREL transformer records.\n"
        sys.stderr.write(msg)
        msgBody += msg
    else:
        msg = "NREL transformer data records were NOT successfully loaded.\n"
        sys.stderr.write(msg)
        msgBody += msg

    if commandLineArgs.email:
        notifier.sendNotificationEmail(msgBody, testing = commandLineArgs.testing)
