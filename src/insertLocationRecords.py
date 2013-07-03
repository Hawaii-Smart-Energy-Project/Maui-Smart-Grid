#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

"""
Insert Location Records into the database from a tab-separated data file.

Usage:
insertLocationRecords.py ${FILENAME}

"""

import csv
import sys
from mecodbconnect import MECODBConnector
from mecodbutils import MECODBUtil
from meconotifier import MECONotifier
from mecoconfig import MECOConfiger

filename = sys.argv[1]

success = True
anyFailure = False
connector = MECODBConnector()
conn = connector.connectDB()
cur = conn.cursor()
dbUtil = MECODBUtil()
notifier = MECONotifier()
msg = ''
msgBody = ''
configer = MECOConfiger()

dbName = configer.configOptionValue("Database", "db_name")

msg = ("Loading static location record data in file %s to database %s.\n" % (
filename, dbName))
sys.stderr.write(msg)
msgBody += msg

f = open(filename, "r")
reader = csv.reader(f)

# @todo verify column order

data = []
cols = ['load_device_type', 'load_action', 'device_util_id', 'device_serial_no',
        'device_status', 'device_operational_status', 'install_date',
        'remove_date', 'cust_account_no', 'cust_name', 'service_point_util_id',
        'service_type', 'meter_phase', 'cust_billing_cycle', 'location_code',
        'voltage_level', 'voltage_phase', 'service_pt_height',
        'service_pt_longitude', 'service_pt_latitude', 'device_pt_ratio',
        'device_ct_ratio', 'premise_util_id', 'premise_type',
        'premise_description', 'address1', 'address2', 'city', 'cross_street',
        'state', 'post_code', 'country', 'timezone', 'region_code',
        'map_page_no', 'map_coord', 'longitude', 'latitude']

lineCnt = 0

with open(filename) as tsv:
    for line in csv.reader(tsv, delimiter = "\t"):
        if lineCnt != 0:

            data = line[0:38]

            for i in range(0, 38):
                if len(data[i]) == 0:
                    data[i] = 'NULL'
                else:
                    data[i] = "'" + data[i] + "'"

            sql = """INSERT INTO "LocationRecords" (%s) VALUES (%s)""" % (
                ','.join(cols), ','.join(data))

            success = dbUtil.executeSQL(cur, sql)
            if not success:
                anyFailure = True

        lineCnt += 1

conn.commit()

msg = ("Processed %s lines.\n" % lineCnt)
sys.stderr.write(msg)
msgBody += msg

if not anyFailure:
    msg = "Finished inserting location records.\n"
    sys.stderr.write(msg)
    msgBody += msg
else:
    msg = "Location records were NOT successfully loaded.\n"
    sys.stderr.write(msg)
    msgBody += msg

notifier.sendNotificationEmail(msgBody)
