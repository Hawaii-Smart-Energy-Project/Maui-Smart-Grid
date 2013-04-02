#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Insert Location Records into the database from a tab-separated data file.

Usage:
insertLocationRecords.py ${FILENAME}

"""

__author__ = 'Daniel Zhang (張道博)'

import csv
import sys
from mecodbconnect import MECODBConnector
from mecodbutils import MECODBUtil

filename = sys.argv[1]

success = True
anyFailure = False
connector = MECODBConnector()
conn = connector.connectDB()
cur = conn.cursor()
dbutil = MECODBUtil()

print "Loading data in file %s" % (filename)

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

            print line
            data = line[0:38]

            print
            for i in range(0, 38):
                if len(data[i]) == 0:
                    data[i] = 'NULL'
                else:
                    data[i] = "'" + data[i] + "'"
            print ','.join(data)

            print
            sql = """INSERT INTO "LocationRecords" (%s) VALUES (%s)""" % (
                ','.join(cols), ','.join(data))
            print "sql = %s" % sql

            print

            print len(cols)
            print len(data)

            success = dbutil.executeSQL(cur, sql)
            if not success:
                anyFailure = True

        lineCnt += 1

conn.commit()

if not anyFailure:
    print "Finished inserting location records."
else:
    print "Location records were NOT successfully loaded."
