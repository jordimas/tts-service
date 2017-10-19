# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import unittest
import os
import datetime
from usage import Usage

class UsageTest(Usage):

    datetime = None

    def _get_time_now(self):
        return self.datetime

    def _set_time_now(self, value):
        self.datetime = value

class TestUsage(unittest.TestCase):

    def setUp(self):
        filename = Usage().FILE
        if os.path.exists(filename):
            os.remove(filename)

    def readLog(self):
        with open(Usage().FILE, "r") as temp:
            return temp.readlines()

    def test_log_one(self):
        usage = UsageTest()
        usage.rotate = False
        usage._set_time_now(datetime.datetime(2016, 10, 5))
        usage.log()
        lines = self.readLog()

        self.assertEqual(len(lines), 1)
        self.assertEqual('2016-10-05 00:00:00\n', lines[0])

    def test_log_two(self):
        usage = UsageTest()
        usage.rotate = False
        usage._set_time_now(datetime.datetime(2016, 10, 5))
        usage.log()
        usage._set_time_now(datetime.datetime(2016, 10, 6))
        usage.log()
        lines = self.readLog()

        self.assertEqual(2, len(lines))
        self.assertEqual('2016-10-05 00:00:00\n', lines[0])
        self.assertEqual('2016-10-06 00:00:00\n', lines[1])

    def test_get_stats_none(self):
        usage = UsageTest()
        usage.rotate = False
        usage._set_time_now(datetime.datetime(2016, 10, 5))
        usage.log()
        usage._set_time_now(datetime.datetime(2016, 10, 6))
        usage.log()

        count = usage.get_stats(datetime.datetime(2016, 10, 1))
        self.assertEqual('0', count)

    def test_get_stats_one(self):
        date = datetime.datetime(2016, 10, 5)
        usage = UsageTest()
        usage.rotate = False
        usage._set_time_now(date)
        usage.log()
        usage._set_time_now(datetime.datetime(2016, 10, 6))
        usage.log()

        count = usage.get_stats(date)
        self.assertEqual('1', count)

    def test_rotate_one_out(self):
        usage = UsageTest()
        usage.rotate = False
        usage._set_time_now(datetime.datetime(2016, 10, 1))
        usage.log()
        usage._set_time_now(datetime.datetime(2016, 10, 2))
        usage.log()

        usage.rotate = True
        usage._set_time_now(datetime.datetime(2016, 10, 9))
        usage.log()
        lines = self.readLog()

        self.assertEqual(2, len(lines))
        self.assertEqual('2016-10-02 00:00:00\n', lines[0])
        self.assertEqual('2016-10-09 00:00:00\n', lines[1])


if __name__ == '__main__':
    unittest.main()
