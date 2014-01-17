#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'David Wilkie & Christian Damo'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github.com/Hawaii-Smart-Energy-Project/ \
			  Maui-Smart-Grid/master/BSD-LICENSE.txt'

"""
Usage:

	python insertCleanSCADAVoltageAndTapData.py
	
This script parses any CSV files in the working directory, which should all be
MECO SCADA data, and separates their columns severally into their own files--
one each for good, bad and raw data. The algorithm to determine whether the
data is good or not measures the sliding standard deviation and looks for
places where it falls below a threshold specified in the algorithm. Because
this function relies upon a mean (namely, of the sliding window) to calculate 
standard deviation, a few of the bad members may sneak into the "good" 
dataset. Davey was not extremely concerned about optimizing this out of the 
algorithm because the number of these cases was a very small fraction of a 
percent of the total data. Still, it bears mention. Currently, the script is 
written to create files for the Wailea transformer voltages, irradiance 
data, and circuits 1517 and 1518.

Running time is a couple of minutes.
"""

import csv
import sys
import subprocess
import datetime
import os
import math
from msg_db_connector import MSGDBConnector
from msg_db_util import MSGDBUtil

def getCleanName(name):
	"""
	A convenience function for naming the output files.

	:param name: A name of the target file.
	:returns: The name suffixed with "_clean" and the file extension.
	"""

	name = name.split(".")
	name = name[0] + "_clean." + name[1]
	return name

def getTimestamp(datetimeStr):
	"""
	A convenience function to parse a string into a Python datetime object.

	:param datetimeStr: A string containing a date and time, e.g.: Sun Sep 01 2013 24:00:00.000 GMT-1000
	:returns: The corresponding datetime.datetime object
	"""

	# We're parsing the string into a list of the days, minutes, etc.
	guava = datetimeStr.split(".")
	guava1 = guava[0].split(" ")
	month = guava1[1]
	day = guava1[2]
	year = guava1[3]
	time = guava1[4].split(":")
	# The raw data calls the 0 hour 24, rather than 0
	if time[0] == "24":
		time[0] = 0
	hour = time[0]
	minute = time[1]
	second = time[2]

	if month.lower() == "jan":
		month = 1
	elif month.lower() == "feb":
		month = 2
	elif month.lower() == "mar":
		month = 3
	elif month.lower() == "apr":
		month = 4
	elif month.lower() == "may":
		month = 5
	elif month.lower() == "jun":
		month = 6
	elif month.lower() == "jul":
		month = 7
	elif month.lower() == "aug":
		month = 8
	elif month.lower() == "sep":
		month = 9
	elif month.lower() == "oct":
		month = 10
	elif month.lower() == "nov":
		month =11 
	elif month.lower() == "dec":
		month =12 

	# We can finally make a Python datetime object, now
	timestamp = datetime.datetime(int(year), month, int(day), int(hour),
								  int(minute), int(second))
	return timestamp

def getColumnNumber(header, desiredValue):
	"""
	Return the "column number" (that is, list index) of a string, if it is
	found in the list.

	:param header: The header line of a CSV header, formatted as a list.
	:param desiredValue: A string containing the name of the column sought
	:returns: The column number corresponding to the desired value
	"""

	i = 0
	for item in header:
		if desiredValue not in item:
			i = i + 1
		else:
			return i

def getColumns():
	"""
	Return a dictionary mapping column names to their index in the CSV
	header.

	:returns: The dictionary of columns.
	"""

	columns = {}
	# The order of the columns corresponding to data we want is subject to 
	# change without notice, so we have this function to account for possible 
	# changes. Note that the names of the columns are assumed not to change.
	columns['timestampCol'] = getColumnNumber(header, 'local datetime') 
	columns['ampA1517Col'] = getColumnNumber(header, 'WAILEA/CB/1517/AMPA')
	columns['ampB1517Col'] = getColumnNumber(header, 'WAILEA/CB/1517/AMPB')
	columns['ampC1517Col'] = getColumnNumber(header, 'WAILEA/CB/1517/AMPC')
	columns['mvar1517Col'] = getColumnNumber(header, 'WAILEA/CB/1517/MVAR')
	columns['mw1517Col'] = getColumnNumber(header, 'WAILEA/CB/1517/MW')
	columns['ampA1518Col'] = getColumnNumber(header, 'WAILEA/CB/1518/AMPA')
	columns['ampB1518Col'] = getColumnNumber(header, 'WAILEA/CB/1518/AMPB')
	columns['ampC1518Col'] = getColumnNumber(header, 'WAILEA/CB/1518/AMPC')
	columns['mvar1518Col'] = getColumnNumber(header, 'WAILEA/CB/1518/MVAR')
	columns['mw1518Col'] = getColumnNumber(header, 'WAILEA/CB/1518/MW')
	columns['transformerVltACol'] = getColumnNumber(header, 
									'WAILEA/XFMR/TSF4/VLTA')
	columns['transformerVltBCol'] = getColumnNumber(header, 
									'WAILEA/XFMR/TSF4/VLTB')
	columns['transformerVltCCol'] = getColumnNumber(header, 
									'WAILEA/XFMR/TSF4/VLTC')
	columns['transformerVoltCol'] = getColumnNumber(header, 
									'WAILEA/XFMR/TSF4/VOLT')

	# The following columns aren't in all of the CSV files.
	if 'WAILEA/WX/MET_SOLAR/KW' in header:
		columns['irradianceCol'] = getColumnNumber(header, \
								   'WAILEA/WX/MET_SOLAR/KW')
	elif 'WAILEA/WX/MET_SOLAR/VAL' in header:
		columns['irradianceCol'] = getColumnNumber(header, \
								   'WAILEA/WX/MET_SOLAR/VAL')

	if 'WAILEA/XFMR/TSF4/TAP' in header:
		columns['tapCol'] = getColumnNumber(header, 'WAILEA/XFMR/TSF4/TAP')

	if 'KIHEI/WX/MET_AIR_TEMP/DEGF' in header:
		columns['temperatureCol'] = getColumnNumber(header, \
									'KIHEI/WX/MET_AIR_TEMP/DEGF')

	if 'KIHEI/WX/MET_REL_HUMID/PCT' in header:
		columns['humidityCol'] = getColumnNumber(header, \
								 'KIHEI/WX/MET_REL_HUMID/PCT')

	return columns

def slidingStandardDeviationCalc(avg, var, x_0, x_n, windowSize):
	"""
	Return the variance and standard deviation based on the previous variance.

	:param avg: The average value of the items in the window x[0]..x[n-1]
	:param var: The variance of the items in the window x[0]..x[n-1]
	:param x_0: The item of the window to be counted out of the rolling 
				standard deviation
	:param x_n: The item of the window to be counted into the rolling standard 
				deviation
	:param windowSize: The number of items in the calculation.
	:returns: newVar: The new variance, ie. of x[1]..x[n]; and newStdDev: The
			  new standard deviation of same, ie. sqrt(newVar)
	"""

	newAvg = avg + (x_n - x_0) / windowSize
	newVar = var + (x_n - newAvg + x_0 - avg) * (x_n - x_0) / (windowSize - 1)
	# I've read that very small values can give a slightly negative std. dev. 
	# due to floating point arithmetic, leading to a negative square root.
	# Thus, we round it to 0. Not ideal but it prevents a crash case.
	if newVar < 0:
		newVar = 0

	newStdDev = math.sqrt(newVar)
	return newVar, newStdDev

def calculateOnlineVariance(data):
	"""
	Returns the variance of the given list.

	:param data: A list of numbers to be measured (ie. the window)
	:returns: The variance of the data. 
	"""

	n, mean, M2 = 0, 0, 0

	for x in data:
		n = n + 1
		delta = x - mean
		mean = mean + delta/n
		M2 = M2 + delta*(x-mean)

	variance = M2/(n-1)
	return variance

def voltageStandardDeviationAlgorithm(reader, filename, unit, columnNumber, 
									  timestampColumnNumber):     
	"""     
	Uses a sliding window to measure the standard deviation, notifies the user 
	via the console when the std. dev. falls beneath a threshold indicating 
	the meter readings are unchanging for a given minimum number of seconds.

	:param reader: A CSV reader.
	:param filename: Name of the output file to be created.
	:param unit: The item of the CSV to be analyzed.
	:param columnNumber: The column # of the item.
	:param timestampColumnNumber: The column # of the timestamp.
	"""

	MIN_TIME = 300
	windowSize = 20
	THRESHOLD = 0.00001
	i, avg, variance, rollingStdDev = 0, 0, 0, 0
	window = []
	event = False
	beginString = ""
	begin = None
	blankRowSequence = False

	# We're gonna sort everything into two files.
	badDataFile = file(filename, 'w+')
	badDataWriter = csv.writer(badDataFile)
	rows = []
	header = ["timestamp", unit]
	badDataWriter.writerow(header)

	# Jettison the header line.
	columnName = reader.next()[columnNumber]

	# We still need to initialize the window and related variables.
	while i < windowSize:
		i += 1
		row = reader.next()
		# In case we encounter a blank row (although this should've been 
		# cleaned up before this function was called).
		if row[columnNumber] == '':
			i -= 1
			continue
		window.append(float(row[columnNumber]))

	avg = reduce(lambda x, y: x + y, window) / len(window)
	variance = calculateOnlineVariance(window)
	cumulativeStdDev = math.sqrt(variance)

	for row in reader:
		vlt = float(row[columnNumber])
		timestamp = getTimestamp(row[timestampColumnNumber])
		newRow = [row[timestampColumnNumber], row[columnNumber]]
		avg = reduce(lambda x, y: x + y, window) / len(window)
		variance, rollingStdDev = slidingStandardDeviationCalc(avg, 
								  variance, window[0], vlt, len(window))
		# Drop the first item and slide the window forward.
		del window[0]
		window.append(vlt)

		# This logic is for marking and printing when an event occurs, as well
		# as keeping a list of the rows that may or may not be in the set of
		# good data and writing the new files.
		if event and rollingStdDev > THRESHOLD:
			rows.append(newRow)

			if (timestamp - begin).total_seconds() > MIN_TIME:
				print "Standard deviation for", str(columnName), "fell to", \
					  THRESHOLD, "or lower for the following duration:"
				print "\tBegin:\t", beginString[4:-13], "\n\tEnd:\t", \
					  row[timestampColumnNumber][4:-13]
				badDataWriter.writerows(rows)

			rows = []
			event = False
		
		elif not event and rollingStdDev <= THRESHOLD:
			rows.append(newRow)
			event = True
			begin = timestamp
			beginString = row[timestampColumnNumber]
		
		elif event: 
			rows.append(newRow)

	# CASE: We reach the end of the file but any of the flags are still set,
	# which means we should print a note of that:
	if event:
		print "Reached end of file with the flag set."
		print "Begin:\t" + beginString

		if (timestamp - begin).total_seconds() > MIN_TIME:
			badDataWriter.writerows(rows)

	print "\nStandardDeviationAlgorithm's run for", unit, "is complete.\n"

def writeNullsIntoCsv(badDataCsv, originalCsv, newFile, columnNumber, timestampColumnNumber):
	"""
	Given the output of voltageStandardDeviationAlgorithm file and the file 
	from which it was derived, write NULL values into the field (indicated by 
	columnNumber) where timestamps from each file correspond.

	:param badDataCsv: The CSV file containing rows to be removed.
	:param originalCsv: The CSV file from which to remove the rows.
	:param newFile: The output file.
	:param columnNumber: The column to be overwritten.
	:param timestampColumnNumber: The column # of the timestamp.
	"""
	
	print "Overwriting bad data from", badDataCsv.name, "w/ blank (null) values."
	original_reader = csv.reader(originalCsv)
	badDataReader = csv.reader(badDataCsv)
	newFileWriter = csv.writer(newFile)
	# Write the header to thw new file and index over the header from the other input file.
	newFileWriter.writerow(original_reader.next())
	badDataReader.next()
	
	for badDataRow in badDataReader:
		originalRow = original_reader.next()
		originalTimestamp = getTimestamp(originalRow[timestampColumnNumber])
		badDataTimestamp = getTimestamp(badDataRow[0])
	
		while (originalTimestamp - badDataTimestamp).total_seconds() < 0:
			newFileWriter.writerow(originalRow)
			originalRow = original_reader.next()
			originalTimestamp = getTimestamp(originalRow[timestampColumnNumber])
	
		if (originalTimestamp - badDataTimestamp).total_seconds() == 0:
			originalRow[columnNumber] = "NULL"
	
		if (originalTimestamp - badDataTimestamp).total_seconds() > 0:
			print "ERROR: total_seconds > 0"
			print (originalTimestamp - badDataTimestamp).total_seconds()
			print "Original ts:", originalTimestamp
			print "Bad data ts:", badDataTimestamp
			return
	
		newFileWriter.writerow(originalRow)
	
	for remainingRow in original_reader:
		newFileWriter.writerow(remainingRow)

def trimBlankLines(inputFile, columns, timestampColumnNumber):
	"""
	Given an input CSV file, scan through the rows for lines with blank 
	values for the columns, whatever they may be, and elide those (and only
	those) from the output file.

	:param inputFile: A CSV file
	:param columns: A list of column indices to be checked for blank entries. 
	:param timestampColumnNumber: The column # of the timestamp.
	:returns: The output file containing no blank lines.
	"""

	reader = csv.reader(inputFile)
	outputFile_name = getCleanName(inputFile.name)
	outputFile = open(outputFile_name, "w+")
	writer = csv.writer(outputFile)
	blankRowSequence = False

	# When finding a sequence of rows with blank voltage values, we find its
	# beginning and end, and print the findings to std i/o.
	for row in reader:
		allColumnsBlank = True

		for column in columns:
			if row[column] != '':
				allColumnsBlank = False
				break

		if not allColumnsBlank:
			writer.writerow(row)

			if blankRowSequence:
				blankRowSequence = False
				print "Sequence of blank rows found:\n\tBegin:\t", \
					startBlankRowSequence[4:-13],"\n\tEnd:\t", \
					row[timestampColumnNumber][4:-13]

		elif not blankRowSequence:
			startBlankRowSequence = row[timestampColumnNumber]
			blankRowSequence = True

	return outputFile

def writeSeparateFiles(reader, columns):
	"""
	Writes files separately for addition to the database tables.

	:param reader: A CSV reader.
	:param columns: A dictionary mapping column names to their indices.
	"""

	irradianceFileName = 'irradianceOutput.csv'
	circuitFileName = 'circuitOutput.csv'
	transformerFileName = 'transformerOutput.csv'
	outputIrradianceFile = open(irradianceFileName, 'wb')
	outputCircuitFile = open(circuitFileName, 'wb')
	outputTransformerFile = open(transformerFileName, 'wb')
	writerIrradiance = csv.writer(outputIrradianceFile)
	writerCircuit = csv.writer(outputCircuitFile)
	writerTransformer = csv.writer(outputTransformerFile)
	i, j = 0, 0
	stinkers = []
	tapDataPresent, weatherDataPresent = True, True

	# Not all the CSV files had tap or weather data, so we check for it and set
	# things up if found.
	try:
		columns['tapCol']
	except KeyError:
		tapDataPresent = False

	try:
		columns['humidityCol']
	except KeyError:
		weatherDataPresent = False

	if tapDataPresent:
		outputTapDataFile = open('tapOutput.csv', 'wb')
		writerTapData = csv.writer(outputTapDataFile)
		newRowTapData = ['timestamp', 'tap_setting', 
						'substation', 'transformer']
		writerTapData.writerow(newRowTapData)

	if weatherDataPresent:
		outputWeatherDataFile = open('weatherOutput.csv', 'wb')
		writerWeatherData = csv.writer(outputWeatherDataFile)
		newRowWeatherData = ['timestamp', 'met_air_temp_degf', 
							 'met_rel_humid_pct']
		writerWeatherData.writerow(newRowWeatherData)

	# Build the csv header rows and write them.
	newRowIrradiance = ['sensor_id', 'irradiance_w_per_m2', 'timestamp']
	newRowCircuit = ['circuit','timestamp','amp_a' ,'amp_b' , 'amp_c' , 
					 'mvar' ,'mw']
	newRowTransformer = ['transformer', 'timestamp', 'vlt_a', 'vlt_b',
						 'vlt_c','volt']
	writerIrradiance.writerow(newRowIrradiance)
	writerCircuit.writerow(newRowCircuit)
	writerTransformer.writerow(newRowTransformer)
	reader.next()

	for row in reader:
		j += 1
		try:
			timestamp = getTimestamp(row[columns['timestampCol']])
			newRowCircuit1517 = ['1517', timestamp, 
					row[columns['ampA1517Col']], row[columns['ampB1517Col']],
					row[columns['ampC1517Col']], row[columns['mvar1517Col']], 
					row[columns['mw1517Col']]]
			newRowCircuit1518 = ['1518', timestamp, 
					row[columns['ampA1518Col']], row[columns['ampB1518Col']],
					row[columns['ampC1518Col']], row[columns['mvar1518Col']], 
					row[columns['mw1518Col']]]
			newRowTransformer = ['wailea', timestamp, 
					row[columns['transformerVltACol']], 
					row[columns['transformerVltBCol']],	
					row[columns['transformerVltCCol']], 
					row[columns['transformerVoltCol']]]
			newRowIrradiance = ['4', row[columns['irradianceCol']], timestamp]
			writerCircuit.writerow(newRowCircuit1517)
			writerCircuit.writerow(newRowCircuit1518)
			writerTransformer.writerow(newRowTransformer)
			writerIrradiance.writerow(newRowIrradiance)

			if tapDataPresent:
				newRowTapData = [timestamp, row[columns['tapCol']], 
								 'wailea', '4']
				writerTapData.writerow(newRowTapData)
			if weatherDataPresent:
				newRowWeatherData = [timestamp, row[columns['temperatureCol']],
									 row[columns['humidityCol']]]
				writerWeatherData.writerow(newRowWeatherData)

		except IndexError:
			i += 1
			stinkers.append(row)
			continue

	if i > 0:
		print 'Raised IndexError exception', i, 'times in', j, 'lines copied '\
			  'during generation of the split files. This (these) bad row(s) '\
			  'raised exceptions:'

		for stinker in stinkers:
			print stinker

def insertData(files, table, cols):
	"""
	Insert aggregated data generated by this script into a database table.

	:param files: A list of the filenames to be processed.
	:param table: The name of the table in the DB.
	:param cols: A list of the columns (as strings) in the table.
	:param testing: Specify whether to use test 
	"""
	connector = MSGDBConnector()
	conn = connector.connectDB()
	dbUtil = MSGDBUtil()
	cursor = conn.cursor()

	cnt = 0

	for file in files:

		with open(file, 'rb') as csvfile:
			myReader = csv.reader(csvfile, delimiter = ',')
			# Skip the header line.
			reader.next()
			for row in myReader:
				sql = """INSERT INTO "%s" (%s) VALUES (%s)""" % (
					table, ','.join(cols),
					','.join("'" + item.strip() + "'" for item in row))

				sql = sql.replace("'NULL'", 'NULL')

				dbUtil.executeSQL(cursor, sql)

				cnt += 1
				if cnt % 10000 == 0:
					conn.commit()

		conn.commit()
		cnt = 0

def insertDataCaller():
	"""Calls the insertData function a few times to insert info into the DB."""

	cols = ['transformer', 'timestamp', 'vlt_a', 'vlt_b', 'vlt_c', 'volt']
	insertData(['transformerOutput.csv'], 'TransformerData', cols)

	cols = ['circuit', 'timestamp', 'amp_a','amp_b', 'amp_c' , 'mvar', 'mw']
	insertData(['circuitOutput.csv'], 'CircuitData', cols)

	cols = ['sensor_id', 'timestamp', 'irradiance_w_per_m2']
	insertData(['irradianceOutput.csv'], 'IrradianceData', cols)

	cols = ['timestamp', 'tap_setting']
	insertData(['tapOutput.csv'], 'TapData', cols)

	cols = ['timestamp', 'met_air_temp_degf', 'met_rel_humid_pct']
	insertData(['weatherOutput.csv'], 'KiheiSCADATemperatureHumidity', cols)

#----------------#
# Body of script #
#----------------#

output = subprocess.Popen(['ls'],stdout = subprocess.PIPE, 
		 stderr = subprocess.STDOUT, shell = True).communicate()[0]
#split the string by lines
output = output.split('\n')
fileNames = []

for line in output:
	line = line.split(' ')
	#for each element find the file name of the files in that folder with the
	#extension *.txt
	for element in line:
		if '.csv' in element and '~' not in element and '_clean' \
		not in element and 'output' not in element:
			#if you found a valid filename, put it in a list
			fileNames.append(element)

# for each file in the list of found files
for filename in fileNames:
	#let the user know you're working on it
	print 'Working on ' + filename
	reader = csv.reader(open(filename,'r'))
	header = reader.next()
	columns = getColumns()

	# Here's where we call our algorithm to scan for lines found in the data
	# where all the 'items to scan for' are blank. If a line of the CSV is 
	# missing output for all members in the tuple, it will be deleted in the 
	# trimBlankLines() routine.
	itemsToScanFor = (columns['transformerVltACol'], 
		 		 	  columns['transformerVltBCol'], 
		 		 	  columns['transformerVltCCol'])
	inputFile = open(filename, 'r')

	trimmedFile = trimBlankLines(inputFile, itemsToScanFor,
								 columns['timestampCol'])
	trimmedFilename = trimmedFile.name

	with open(trimmedFilename, 'r') as trimmedFile:
		reader = csv.reader(trimmedFile)
		voltageStandardDeviationAlgorithm(reader, 'wailea_voltage_a.csv', 
			'voltage', columns['transformerVltACol'], columns['timestampCol'])
	with open(trimmedFilename, 'r') as trimmedFile:
		reader = csv.reader(trimmedFile)
		voltageStandardDeviationAlgorithm(reader, 'wailea_voltage_b.csv', 
			'voltage', columns['transformerVltBCol'], columns['timestampCol'])
	with open(trimmedFilename, 'r') as trimmedFile:
		reader = csv.reader(trimmedFile)
		voltageStandardDeviationAlgorithm(reader, 'wailea_voltage_c.csv', 
			'voltage', columns['transformerVltCCol'], columns['timestampCol'])

	# And finally we overwrite places the CSV file where we had bad data with 
	# null values. Yes, this could be broken out into a function...
	trimmedFile = open(trimmedFilename, 'r')
	newFile = open('output.csv', 'w+')
	badDataFile = open('wailea_voltage_a.csv', 'r')
	writeNullsIntoCsv(badDataFile, trimmedFile, newFile, 
		columns['transformerVltACol'], columns['timestampCol'])
	subprocess.call(['rm', '-f', badDataFile.name])
	subprocess.call(['mv', newFile.name, trimmedFile.name])
	trimmedFile.close()
	newFile.close()
	badDataFile.close()

	trimmedFile = open(trimmedFilename, 'r')
	newFile = open('output.csv', 'w+')
	badDataFile = open('wailea_voltage_b.csv', 'r')
	writeNullsIntoCsv(badDataFile, trimmedFile, newFile, \
					  columns['transformerVltBCol'], columns['timestampCol'])
	subprocess.call(['rm', '-f', badDataFile.name])
	subprocess.call(['mv', newFile.name, trimmedFile.name])
	trimmedFile.close()
	newFile.close()
	badDataFile.close()

	trimmedFile = open(trimmedFilename, 'r')
	newFile = open('output.csv', 'w+')
	badDataFile = open('wailea_voltage_c.csv', 'r')
	writeNullsIntoCsv(badDataFile, trimmedFile, newFile, 
		columns['transformerVltCCol'], columns['timestampCol'])
	subprocess.call(['rm', '-f', badDataFile.name])
	subprocess.call(['mv', newFile.name, trimmedFile.name])
	trimmedFile.close()
	newFile.close()
	badDataFile.close()

	trimmedFile = open(trimmedFilename, 'r')
	reader = csv.reader(trimmedFile)
	writeSeparateFiles(reader, columns)
	insertDataCaller()

	newFile.close()
	trimmedFile.close()
	badDataFile.close()
	subprocess.call(['rm', '-f', filename])
	subprocess.call(['rm', '-f', 'circuitOutput.csv'])
	subprocess.call(['rm', '-f', 'transformerOutput.csv'])
	subprocess.call(['rm', '-f', 'tapOutput.csv'])
	subprocess.call(['rm', '-f', 'irradianceOutput.csv'])
	subprocess.call(['rm', '-f', 'weatherOutput.csv'])

