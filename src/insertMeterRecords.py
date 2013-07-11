#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

"""
Static Meter Record Loading.

Insert Meter Records into the database from a tab-separated data file.

Usage:
insertMeterRecords.py ${FILENAME}

"""

import csv
import sys
from mecodbconnect import MECODBConnector
from mecodbutils import MECODBUtil
from meconotifier import MSGNotifier
from mecoconfig import MECOConfiger

filename = sys.argv[1]

configer = MECOConfiger()
connector = MECODBConnector()
conn = connector.connectDB()
cur = conn.cursor()
dbUtil = MECODBUtil()
notifier = MSGNotifier()
msgBody = ''
msg = ''

dbName = configer.configOptionValue("Database", "db_name")

msg = ("Loading static meter record data in file %s to database %s.\n" % (
filename, dbName))
sys.stderr.write(msg)
msgBody += msg

f = open(filename, "r")
reader = csv.reader(f)

data = []
cols = ['type', 'action', 'did_sub_type', 'device_util_id', 'device_serial_no',
        'device_status', 'device_operational_status', 'device_name',
        'device_description', 'device_mfg', 'device_mfg_date',
        'device_mfg_model', 'device_sw_ver_no', 'device_sw_rev_no',
        'device_sw_patch_no', 'device_sw_config', 'device_hw_ver_no',
        'device_hw_rev_no', 'device_hw_patch_no', 'device_hw_config',
        'meter_form_type', 'meter_base_type', 'max_amp_class', 'rollover_point',
        'volt_type', 'nic_mac_address', 'nic_serial_no', 'nic_rf_channel',
        'nic_network_identifier', 'nic_model', 'nic_sw_ver_no', 'nic_sw_rev_no',
        'nic_sw_patch_no', 'nic_released_date', 'nic_sw_config',
        'nic_hw_ver_no', 'nic_hw_rev_no', 'nic_hw_patch_no', 'nic_hw_config',
        'master_password', 'reader_password', 'cust_password', 'meter_mode',
        'timezone_region', 'battery_mfg_name', 'battery_model_no',
        'battery_serial_no', 'battery_mfg_date', 'battery_exp_date',
        'battery_installed_date', 'battery_lot_no', 'battery_last_tested_date',
        'price_program', 'catalog_number', 'program_seal', 'meter_program_id',
        'device_attribute_1', 'device_attribute_2', 'device_attribute_3',
        'device_attribute_4', 'device_attribute_5', 'nic_attribute_1',
        'nic_attribute_2', 'nic_attribute_3', 'nic_attribute_4',
        'nic_attribute_5']

lineCnt = 0

with open(filename) as tsv:
    for line in csv.reader(tsv, delimiter = "\t"):
        if lineCnt != 0:

            data = line[0:66]

            for i in range(0, 66):

                if len(data[i]) == 0:
                    data[i] = 'NULL'
                else:
                    data[i] = "'" + data[i] + "'"

            sql = """INSERT INTO "MeterRecords" (%s) VALUES (%s)""" % (
                ','.join(cols), ','.join(data))

            dbUtil.executeSQL(cur, sql)

        lineCnt += 1

conn.commit()

msg = ("Processed %s lines.\n" % lineCnt)
sys.stderr.write(msg)
msgBody += msg

notifier.sendNotificationEmail(msgBody)
