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

	def test_day_month(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} {} 22 7 * ls # ls".format(minute, hour).encode()
		SuperCron.add_job("ls", "ls", "on 22/7")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_mixed_datetime(self):
		entry = b"8 0 1 6 * ls # ls"
		SuperCron.add_job("ls", "ls", "1/6 12:08 am")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_weekdays_single(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} {} * * 2 ls # ls".format(minute, hour).encode()
		SuperCron.add_job("ls", "ls", "on tuesdays")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_weekdays_multiple_non_consecutive(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} {} * * 1,3,5 ls # ls".format(minute, hour).encode()
		SuperCron.add_job("ls", "ls", "on mondays, wednesdays and fridays")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_weekdays_multiple_forward(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} {} * * 1-4 ls # ls".format(minute, hour).encode()
		SuperCron.add_job("ls", "ls", "from monday to thursday")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_weekdays_multiple_backward(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} {} * * 0,1,5,6 ls # ls".format(minute, hour).encode()
		SuperCron.add_job("ls", "ls", "from friday to monday")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_short_weekdays(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} {} * * 0,1,5,6 ls # ls".format(minute, hour).encode()
		SuperCron.add_job("ls", "ls", "from fri to mon")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_months_single(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} {} * 5 * ls # ls".format(minute, hour).encode()
		SuperCron.add_job("ls", "ls", "in May")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_months_multiple_non_consecutive(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} {} * 2,5,9 * ls # ls".format(minute, hour).encode()
		SuperCron.add_job("ls", "ls", "in May and September and February")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_months_multiple_forward(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} {} * 6-8 * ls # ls".format(minute, hour).encode()
		SuperCron.add_job("ls", "ls", "from June to August")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_months_multiple_backward(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} {} * 1,10,11,12 * ls # ls".format(minute, hour).encode()
		SuperCron.add_job("ls", "ls", "from October to January")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_short_months(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} {} * 1,10,11,12 * ls # ls".format(minute, hour).encode()
		SuperCron.add_job("ls", "ls", "from oct to jan")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)


if __name__ == "__main__":
	unittest.main()
