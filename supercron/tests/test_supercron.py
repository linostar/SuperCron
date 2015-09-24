#!/usr/bin/env python

import sys
import os
import unittest
from subprocess import Popen, PIPE


ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(ROOT_DIR)

from supercron.supercron import SuperCron


class TestRepetitions(unittest.TestCase):
	"""class that tests supercron for repetition parsing"""

	def setUp(self):
		SuperCron.DEBUG = False

	def tearDown(self):
		SuperCron.delete_job("ls")

	def get_crontab(self):
		p = Popen(["crontab", "-l"], stdout=PIPE, stderr=PIPE)
		crontab_out, crontab_err = p.communicate()
		return crontab_out

	def test_midnight(self):
		entry1 = b"@daily ls # SuperCron__ls"
		entry2  = b"0 0 * * * ls # SuperCron__ls"
		SuperCron.add_job("ls", "ls", "midnight")
		user_crontab = self.get_crontab()
		self.assertTrue(entry1 in user_crontab or entry2 in user_crontab)

	def test_at_boot(self):
		entry = b"@reboot ls # SuperCron__ls"
		SuperCron.add_job("ls", "ls", "at reboot")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_every_x_minutes(self):
		entry = b"*/5 * * * * ls # SuperCron__ls"
		SuperCron.add_job("ls", "ls", "once every 5 minutes")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_every_x_hours(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} */2 * * * ls # SuperCron__ls".format(minute).encode()
		SuperCron.add_job("ls", "ls", "once every 2 hours")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_every_x_days(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} {} */11 * * ls # SuperCron__ls".format(minute, hour).encode()
		SuperCron.add_job("ls", "ls", "once every 11 days")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_hour_minute_24h(self):
		entry = b"36 15 * * * ls # SuperCron__ls"
		SuperCron.add_job("ls", "ls", "on 15:36")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_hour_minute_12h(self):
		entry = b"47 16 * * * ls # SuperCron__ls"
		SuperCron.add_job("ls", "ls", "on 4:47 pm")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_day_month(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} {} 22 7 * ls # SuperCron__ls".format(minute, hour).encode()
		SuperCron.add_job("ls", "ls", "on 22/7")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_mixed_datetime(self):
		entry = b"8 0 1 6 * ls # SuperCron__ls"
		SuperCron.add_job("ls", "ls", "1/6 12:08 am")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_weekdays_single(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} {} * * 2 ls # SuperCron__ls".format(minute, hour).encode()
		SuperCron.add_job("ls", "ls", "on tuesdays")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_weekdays_multiple_non_consecutive(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} {} * * 1,3,5 ls # SuperCron__ls".format(minute, hour).encode()
		SuperCron.add_job("ls", "ls", "on mondays, wednesdays and fridays")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_weekdays_multiple_forward(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} {} * * 1-4 ls # SuperCron__ls".format(minute, hour).encode()
		SuperCron.add_job("ls", "ls", "from monday to thursday")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_weekdays_multiple_backward(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} {} * * 0,1,5,6 ls # SuperCron__ls".format(minute, hour).encode()
		SuperCron.add_job("ls", "ls", "from friday to monday")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_short_weekdays(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} {} * * 0,1,5,6 ls # SuperCron__ls".format(minute, hour).encode()
		SuperCron.add_job("ls", "ls", "from fri to mon")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_months_single(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} {} * 5 * ls # SuperCron__ls".format(minute, hour).encode()
		SuperCron.add_job("ls", "ls", "in May")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_months_multiple_non_consecutive(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} {} * 2,5,9 * ls # SuperCron__ls".format(minute, hour).encode()
		SuperCron.add_job("ls", "ls", "in May and September and February")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_months_multiple_forward(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} {} * 6-8 * ls # SuperCron__ls".format(minute, hour).encode()
		SuperCron.add_job("ls", "ls", "from June to August")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_months_multiple_backward(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} {} * 1,10,11,12 * ls # SuperCron__ls".format(minute, hour).encode()
		SuperCron.add_job("ls", "ls", "from October to January")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_short_months(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} {} * 1,10,11,12 * ls # SuperCron__ls".format(minute, hour).encode()
		SuperCron.add_job("ls", "ls", "from oct to jan")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_mixed_weekday_time(self):
		entry = b"0 9 * * 1 ls # SuperCron__ls"
		SuperCron.add_job("ls", "ls", "on monday 09:00")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_mixed_month_time(self):
		entry = b"55 12 * 8 * ls # SuperCron__ls"
		SuperCron.add_job("ls", "ls", "in august at 12:55 pm")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_mixed_month_weekday_every_x_hours(self):
		hour, minute = SuperCron.get_time_now()
		entry = "{} */4 * 4 6 ls # SuperCron__ls".format(minute).encode()
		SuperCron.add_job("ls", "ls", "every 4 hours on saturdays in april")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_mixed_month_multiple_weekday_multiple_every_x_days_midnight(self):
		entry = b"0 0 */2 10,12 1-5 ls # SuperCron__ls"
		SuperCron.add_job("ls", "ls", "midnight every 2 days from monday to friday in october and december")
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)


class TestJobs(unittest.TestCase):
	"""class that tests supercron for job actions"""

	def setUp(self):
		SuperCron.DEBUG = False
		SuperCron.add_job("pwd", "pwd", "midnight")

	def tearDown(self):
		SuperCron.delete_job("pwd")

	def test_disable_job(self):
		SuperCron.enable_job("pwd", False)

	def test_enable_job(self):
		SuperCron.enable_job("pwd", True)


if __name__ == "__main__":
	unittest.main()
