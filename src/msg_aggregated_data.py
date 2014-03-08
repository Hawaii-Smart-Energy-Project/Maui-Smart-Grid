#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'


class MSGAggregatedData(object):
    """
    Data type representing aggregated data.
    """

    def __init__(self, columns = None, data = None):
        """
        Constructor.
        """

        if not columns:
            raise(Exception, 'Columns not provided.')
        if not data:
            raise(Exception, 'Data not provided.')
        self.columns = columns
        self.data = data
