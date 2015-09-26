#!/usr/bin/env python

import sys
import os
import unittest
from subprocess import Popen, PIPE


ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(ROOT_DIR)

from supercron.supercron import SuperCron
from supercron.utils import Utils
from supercron.namespace import Namespace


class TestRepetitions(unittest.TestCase):
	"""class that tests supercron for repetition parsing"""

	def setUp(self):
		Utils.DEBUG = False

	def tearDown(self):
		args = Namespace(Utils.list_to_dict("ls"))
		SuperCron.delete_job(args)

	def get_crontab(self):
		p = Popen(["crontab", "-l"], stdout=PIPE, stderr=PIPE)
		crontab_out, crontab_err = p.communicate()
		return crontab_out

	def test_midnight(self):
		entry1 = b"@daily ls # SuperCron__ls"
		entry2  = b"0 0 * * * ls # SuperCron__ls"
		args = Namespace(Utils.list_to_dict("ls", "ls", "midnight"))
		SuperCron.add_job(args)
		user_crontab = self.get_crontab()
		self.assertTrue(entry1 in user_crontab or entry2 in user_crontab)

	def test_everyday(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} * * * ls # SuperCron__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("ls", "ls", "everyday"))
		SuperCron.add_job(args)
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_at_boot(self):
		entry = b"@reboot ls # SuperCron__ls"
		args = Namespace(Utils.list_to_dict("ls", "ls", "at reboot"))
		SuperCron.add_job(args)
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_every_x_minutes(self):
		entry = b"*/5 * * * * ls # SuperCron__ls"
		args = Namespace(Utils.list_to_dict("ls", "ls", "once every 5 minutes"))
		SuperCron.add_job(args)
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_every_x_hours(self):
		hour, minute = Utils.get_time_now()
		entry = "{} */2 * * * ls # SuperCron__ls".format(minute).encode()
		args = Namespace(Utils.list_to_dict("ls", "ls", "once every 2 hours"))
		SuperCron.add_job(args)
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_every_x_days(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} */11 * * ls # SuperCron__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("ls", "ls", "once every 11 days"))
		SuperCron.add_job(args)
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_hour_minute_24h(self):
		entry = b"36 15 * * * ls # SuperCron__ls"
		args = Namespace(Utils.list_to_dict("ls", "ls", "at 15:36"))
		SuperCron.add_job(args)
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_hour_minute_12h(self):
		entry = b"47 16 * * * ls # SuperCron__ls"
		args = Namespace(Utils.list_to_dict("ls", "ls", "at 4:47 pm"))
		SuperCron.add_job(args)
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_day_month(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} 22 7 * ls # SuperCron__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("ls", "ls", "on 22/7"))
		SuperCron.add_job(args)
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_mixed_datetime(self):
		entry = b"8 0 1 6 * ls # SuperCron__ls"
		args = Namespace(Utils.list_to_dict("ls", "ls", "1/6 12:08 am"))
		SuperCron.add_job(args)
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_weekdays_single(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} * * 2 ls # SuperCron__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("ls", "ls", "on tuesdays"))
		SuperCron.add_job(args)
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_weekdays_multiple_non_consecutive(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} * * 1,3,5 ls # SuperCron__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("ls", "ls", "on mondays, wednesdays and fridays"))
		SuperCron.add_job(args)
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_weekdays_multiple_forward(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} * * 1-4 ls # SuperCron__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("ls", "ls", "from monday to thursday"))
		SuperCron.add_job(args)
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_weekdays_multiple_backward(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} * * 0,1,5,6 ls # SuperCron__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("ls", "ls", "from friday to monday"))
		SuperCron.add_job(args)
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_short_weekdays(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} * * 0,1,5,6 ls # SuperCron__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("ls", "ls", "from fri to mon"))
		SuperCron.add_job(args)
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_months_single(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} * 5 * ls # SuperCron__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("ls", "ls", "in May"))
		SuperCron.add_job(args)
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_months_multiple_non_consecutive(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} * 2,5,9 * ls # SuperCron__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("ls", "ls", "in May and September and February"))
		SuperCron.add_job(args)
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_months_multiple_forward(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} * 6-8 * ls # SuperCron__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("ls", "ls", "from June to August"))
		SuperCron.add_job(args)
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_months_multiple_backward(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} * 1,10,11,12 * ls # SuperCron__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("ls", "ls", "from October to January"))
		SuperCron.add_job(args)
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_short_months(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} * 1,10,11,12 * ls # SuperCron__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("ls", "ls", "from oct to jan"))
		SuperCron.add_job(args)
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_mixed_weekday_time(self):
		entry = b"0 9 * * 1 ls # SuperCron__ls"
		args = Namespace(Utils.list_to_dict("ls", "ls", "on monday 09:00"))
		SuperCron.add_job(args)
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_mixed_month_time(self):
		entry = b"55 12 * 8 * ls # SuperCron__ls"
		args = Namespace(Utils.list_to_dict("ls", "ls", "in august at 12:55 pm"))
		SuperCron.add_job(args)
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_mixed_month_weekday_every_x_hours(self):
		hour, minute = Utils.get_time_now()
		entry = "{} */4 * 4 6 ls # SuperCron__ls".format(minute).encode()
		args = Namespace(Utils.list_to_dict("ls", "ls", "every 4 hours on saturdays in april"))
		SuperCron.add_job(args)
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_mixed_month_multiple_weekday_multiple_every_x_days_midnight(self):
		entry = b"0 0 */2 10,12 1-5 ls # SuperCron__ls"
		args = Namespace(Utils.list_to_dict("ls", "ls",
			"midnight every 2 days from monday to friday in october and december"))
		SuperCron.add_job(args)
		user_crontab = self.get_crontab()
		self.assertTrue(entry in user_crontab)


class TestJobs(unittest.TestCase):
	"""class that tests supercron for job actions"""

	def setUp(self):
		Utils.DEBUG = False
		args = Namespace(Utils.list_to_dict("pwd", "pwd", "midnight"))
		SuperCron.add_job(args)

	def tearDown(self):
		args = Namespace(Utils.list_to_dict("pwd"))
		SuperCron.delete_job(args)

	def test_disable_job(self):
		args = Namespace(Utils.list_to_dict("pwd"))
		SuperCron.disable_job(args)

	def test_enable_job(self):
		args = Namespace(Utils.list_to_dict("pwd"))
		SuperCron.enable_job(args)

	def test_delete_job(self):
		args = Namespace(Utils.list_to_dict("pwd"))
		SuperCron.delete_job(args)

	def test_clear_jobs(self):
		args = Namespace()
		SuperCron.clear_jobs(args, True)


if __name__ == "__main__":
	unittest.main()
