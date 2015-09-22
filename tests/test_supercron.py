#!/usr/bin/env python

import sys
import os
import unittest
from subprocess import Popen, PIPE


ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(ROOT_DIR)

from supercron import SuperCron


class RunTests(unittest.TestCase):
	"""class that tests supercron for behavior correctness"""

	def setUp(self):
		SuperCron.DEBUG = False

	def tearDown(self):
		SuperCron.delete_job("ls")

	def get_crontab(self):
		p = Popen(["crontab", "-l"], stdout=PIPE, stderr=PIPE)
		crontab_out, crontab_err = p.communicate()
		return crontab_out

	def test_midnight(self):
		entry1 = b"@daily ls # ls"
		entry2  = b"0 0 * * * ls # ls"
		SuperCron.add_job("ls", "ls", "midnight")
		user_crontab = self.get_crontab()
		self.assertTrue(entry1 in user_crontab or entry2 in user_crontab)

	def test_every_x_minutes(self):
		entry = b"*/5 * * * * ls # ls"
		SuperCron.add_job("ls", "ls", "once every 5 minutes")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_every_x_hours(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} */2 * * * ls # ls".format(minute).encode()
		SuperCron.add_job("ls", "ls", "once every 2 hours")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_every_x_days(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} {} */11 * * ls # ls".format(minute, hour).encode()
		SuperCron.add_job("ls", "ls", "once every 11 days")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_hour_minute_24h(self):
		entry = b"36 15 * * * ls # ls"
		SuperCron.add_job("ls", "ls", "on 15:36")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_hour_minute_12h(self):
		entry = b"47 16 * * * ls # ls"
		SuperCron.add_job("ls", "ls", "on 4:47 pm")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)


if __name__ == "__main__":
	unittest.main()
