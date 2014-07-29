#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

from enum import Enum


class MSGAggregationTypes(Enum):
    """
    Types for aggregation.
    """
    weather = 1
    egauge = 2
    circuit = 3
    irradiance = 4


class MSGNotificationHistoryTypes(Enum):
    """
    Types for the notification history.
    """
    msg_db_exporter = 1
    msg_data_aggregator = 2
    msg_export_summary = 3
