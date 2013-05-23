#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

from mecodbread import MECODBReader
import pylab
import matplotlib.pyplot as plt
import matplotlib.dates


class MECOPlotting(object):
    """
    """

    def __init__(self):
        """
        Constructor.
        """

        self.reader = MECODBReader()

    def plotReadingAndMeterCounts(self):
        dates, readingCounts, meterCounts = self.reader.readingAndMeterCounts()

        newDates = matplotlib.dates.date2num(dates)

        plt.xticks(rotation = 'vertical')
        plt.xlabel('Date')
        plt.ylabel('Counts')

        plt.plot_date(newDates, readingCounts, 'yo:', aa = True,
                      label = 'Readings/Meter')
        plt.plot_date(newDates, meterCounts, 'ro:', aa = True, label = 'Meters')

        plt.legend(loc = 'best')
        plt.title('Readings/Meter, and Meter, Count per Day')

        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(18.5, 10.5)

        pylab.savefig('ReadingAndMeterCounts.png', dpi = 150)


plotter = MECOPlotting()
plotter.plotReadingAndMeterCounts()



