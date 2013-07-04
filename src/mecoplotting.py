#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

from mecodbread import MECODBReader
import matplotlib

matplotlib.use('Agg')
import pylab
import matplotlib.pyplot as plt
import matplotlib.dates
from mecoconfig import MECOConfiger
import time

# Set TEST_SCRIPT to True to run plotting as a script.
TEST_SCRIPT = False


class MECOPlotting(object):
    """
    Provides plotting services to MECO data processing.
    """

    def __init__(self, testing = False):
        """
        Constructor.

        :param testing: Use testing mode if True.
        """

        self.reader = MECODBReader(testing)
        self.configer = MECOConfiger()
        self.dpi = 300


    def plotReadingAndMeterCounts(self, databaseName = None):
        """
        Create a plot of reading and meter counts.
        Save the plot to local storage.

        :param databaseName: Name of the database being used to generate the
        plot.
        """

        matplotlib.pyplot.ioff()

        dates, readingCounts, meterCounts = self.reader.readingAndMeterCounts()

        newDates = matplotlib.dates.date2num(dates)

        plt.xticks(rotation = 'vertical')
        plt.xlabel('Date')
        plt.ylabel('Counts')

        plt.plot_date(newDates, readingCounts, 'yo:', aa = True,
                      label = 'Readings/Meter')
        plt.plot_date(newDates, meterCounts, 'ro:', aa = True, label = 'Meters')

        plt.legend(loc = 'best')
        localtime = time.asctime(time.localtime(time.time()))

        databaseMsg = ''
        if databaseName:
            databaseMsg = " for Database %s" % databaseName

        plt.title(
            'Reading Count per Meter and Meter Count by Day%s'
            '\nCreated on %s' %
            (databaseMsg, localtime))

        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(18.5, 11.5)

        ax = fig.add_subplot(1, 1, 1)
        ax.set_axisbelow(True)
        ax.grid(b = True, which = 'major', color = '#dddddd', linestyle = '-')

        plotPath = self.configer.configOptionValue("Data Paths", "plot_path")
        pylab.savefig('%s/ReadingAndMeterCounts.png' % plotPath, dpi = self.dpi)


if TEST_SCRIPT:
    plotter = MECOPlotting()
    plotter.plotReadingAndMeterCounts(plotter.reader.dbName)

