#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup script for MSG Data Processing and Operations.

Additional file-based inclusions can be found in MANIFEST.in.

The distribution archive is created as a source distribution,
http://docs.python.org/2/distutils/sourcedist.html, using

    python setup.py sdist

Installation is performed using

    python setup.py install [--prefix=${LIBRARY_PATH} --exec-prefix=${BIN_PATH]

where the path arguments within the square brackets are optional.
"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

from distutils.core import setup

setup(name = 'Maui-Smart-Grid', version = '1.0.0',
      description = 'Data Processing and Data Operations for the Maui Smart '
                    'Grid Project.',
      long_description = 'The University of Hawaii at Manoa was tasked with '
                         'maintaining a data repository for use by analysts '
                         'for the Maui Smart Grid (http://www.mauismartgrid'
                         '.com) energy sustainability project through the '
                         'Hawaii Natural Energy Institute (http://www.hnei'
                         '.hawaii.edu). This software provides the data '
                         'processing and operational resources necessary to '
                         'accomplish this task. Source data arrives in '
                         'multiple formats including XML, tab-separated '
                         'values, and comma-separated values. Issues for this'
                         ' project are tracked at the Hawaii Smart Energy '
                         'Project YouTRACK instance ('
                         'http://smart-energy-project.myjetbrains'
                         '.com/youtrack/rest/agile).',
      author = 'Daniel Zhang (張道博)',
      author_email = 'See https://github.com/dz1111',
      url = 'https://github.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid',
      license = 'https://raw.github'
                '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD'
                '-LICENSE.txt', platforms = 'OS X, Linux',

      package_dir = {'': 'src'},

      py_modules = [
                    'filelock',
                    'meco_data_autoloader',
                    'meco_db_delete',
                    'meco_db_insert',
                    'meco_db_read',
                    'meco_dupe_check',
                    'meco_fk',
                    'meco_mapper',
                    'meco_plotting',
                    'meco_pv_readings_in_nonpv_mlh_notifier',
                    'meco_xml_parser',
                    'msg_aggregated_data',
                    'msg_configer',
                    'msg_data_aggregator',
                    'msg_data_verifier.py',
                    'msg_db_connector',
                    'msg_db_exporter',
                    'msg_db_util',
                    'msg_file_util',
                    'msg_logger',
                    'msg_math_util',
                    'msg_noaa_weather_data_dupe_checker',
                    'msg_noaa_weather_data_inserter',
                    'msg_noaa_weather_data_parser',
                    'msg_noaa_weather_data_util',
                    'msg_notifier',
                    'msg_time_util'
      ],

      scripts = [
                 'src/autoloadNewMECOData.py',
                 'src/exportDBsToCloud.py',
                 'src/insertCompressedNOAAWeatherData.py',
                 'src/insertMECOEnergyData.py',
                 'src/insertSingleMECOEnergyDataFile.py',
                 'src/retrieveNOAAWeatherData.py',
                 'src/static-data-insert/insertCleanSCADAVoltageAndTapData.py',
                 'src/static-data-insert/insertLocationRecords.py',
                 'src/static-data-insert/insertMECOMeterLocationHistoryData.py',
                 'src/static-data-insert/insertMeterRecords.py',
                 'src/static-data-insert/insertNRELIrradianceData.py',
                 'src/static-data-insert/insertPowerMeterEvents.py',
                 'src/static-data-insert/insertSCADAWeatherData.py'
      ])
