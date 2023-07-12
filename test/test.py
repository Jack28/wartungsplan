#!/usr/bin/env python
# encoding: utf-8

###############################################################################
#                                                                             #
# Test suite Wartungspläne CLI Tool                                           #
#                                                                             #
# test.py                                                                     #
###############################################################################
#                                                                             #
# Copyright (C) 2016-2022 science + computing ag                              #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation, either version 3 of the License, or (at       #
# your option) any later version.                                             #
#                                                                             #
# This program is distributed in the hope that it will be useful, but         #
# WITHOUT ANY WARRANTY; without even the implied warranty of                  #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU           #
# General Public License for more details.                                    #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
#                                                                             #
###############################################################################

""" Test suite for a tool than opens recurring tickets """

import unittest
import tempfile
import os
import sys
import logging
import icalendar

# Add Wartungsplan to PYTHONPATH
TESTSDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(TESTSDIR))

from src import Wartungsplan


class DummyBackend:
    def __init__(self, _):
        pass

    def act(self, events, __):
        return len(events)


class TestWartungsplan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ Set up common test case resources. """
        cls.tests_data_dir = os.path.join(TESTSDIR, "test-data")
        cls.b = DummyBackend(None)

    def test_one_event_with_empty_subject(self):
        p = os.path.join(self.tests_data_dir, "Empty-Event-2023-05-01.ics")
        with open(p, encoding='utf-8') as c:
            cal = icalendar.Calendar.from_ical(c.read())
            wp = Wartungsplan.Wartungsplan("2023-05-01", "2023-05-02", cal, self.b)
            self.assertEqual(wp.act(), 1)
            wp = Wartungsplan.Wartungsplan("2023-05-02", "2023-05-03", cal, self.b)
            self.assertEqual(wp.act(), 0)

    def test_every_second_tuesday(self):
        p = os.path.join(self.tests_data_dir, "Every2ndTuesday-2023-05-02.ics")
        with open(p, encoding='utf-8') as c:
            cal = icalendar.Calendar.from_ical(c.read())
            wp = Wartungsplan.Wartungsplan("2023-05-02", "2023-05-03", cal, self.b)
            self.assertEqual(wp.act(), 1)
            wp = Wartungsplan.Wartungsplan("2023-05-02", "2023-06-06", cal, self.b)
            self.assertEqual(wp.act(), 2)

    def test_every_day_with_html(self):
        p = os.path.join(self.tests_data_dir, "EveryDayWithHeavyHTML.ics")
        with open(p, encoding='utf-8') as c:
            cal = icalendar.Calendar.from_ical(c.read())
            wp = Wartungsplan.Wartungsplan("2023-05-05", "2023-05-06", cal, self.b)
            self.assertEqual(wp.act(), 1)
            wp = Wartungsplan.Wartungsplan("2023-06-01", "2023-07-01", cal, self.b)
            self.assertEqual(wp.act(), 30)

    def test_bangkok_timezone(self):
        p = os.path.join(self.tests_data_dir, "TimezoneBangkok3rdOr4th-05-2023.ics")
        with open(p, encoding='utf-8') as c:
            cal = icalendar.Calendar.from_ical(c.read())
            wp = Wartungsplan.Wartungsplan("2023-05-03", None, cal, self.b)
            self.assertEqual(wp.act(), 1)
            wp = Wartungsplan.Wartungsplan("2023-05-04", None, cal, self.b)
            self.assertEqual(wp.act(), 0)


if __name__ == '__main__':
    logging.disable(logging.ERROR)

    unittest.main()