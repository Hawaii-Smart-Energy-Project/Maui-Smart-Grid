#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from mecomapper import MECOMapper
from mecoconfig import MECOConfiger

class TestMECOMapper(unittest.TestCase) :
    """Unit tests for MECO Mapper.
    """

    def setUp(self) :
        self.m = MECOMapper()
        self.testColumns = self.m.dbColsMeterData.values()
        self.testLabels = self.m.dbColsMeterData.keys()
        self.testTableName = 'MeterData'
        self.config = MECOConfiger()

    def testMECOMapperCanBeInited(self) :
        localMapper = MECOMapper()
        self.assertIsInstance(self.m, type(localMapper))

    def testMappingReturnsAListWithMembersMoreThanZero(self) :
        self.assertTrue(len(self.testColumns) > 0)

    def test_fkey_mappings(self) :
        """Verify fkey mappings for tables.
        """

        print "test_fkey_mappings:"
        errors = 0
        fkeys = {'RegisterData' : 'meter_data_id'}

        for t in self.config.insertTables :
            try :
                print self.m.dbColumnsForTable(t)['_fkey']
                if self.m.dbColumnsForTable(t)['_fkey'] != fkeys[t] :
                    errors += 1
            except :
                # table doesnt have an fkey
                pass
        self.assertLess(errors, 1)

    # @todo finish writing
    def testMappingIsValidForMeterData(self) :
        """Compare columns that are mapped for given data labels.
        """

        # given labels from the source data, map them to db column names
        srcDataLabels = ('MacID', 'MeterName', 'UtilDeviceID')

if __name__ == '__main__' :
    unittest.main()
