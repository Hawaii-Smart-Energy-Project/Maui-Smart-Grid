#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

class MECOFKDeterminer(object) :
    """Determine foreign key values and maintain storage of primary key values
    to be used as foreign key values.
    """

    def __init__(self) :
        """Constructor
        """

        self.pkValforCol = {'meter_data_id':None,
                            'register_data_id':None,
                            'register_read_id':None,
                            'tier_id':None,
                            'register_id':None,
                            'interval_read_data_id':None,
                            'interval_id':None,
                            'reading_id':None,
                            'event_data_id':None,
                            'event_id':None
        }
