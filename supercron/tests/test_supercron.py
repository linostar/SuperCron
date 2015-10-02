#!/usr/bin/env python

import sys
import os
import unittest

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
		args = Namespace(Utils.list_to_dict("TEST__ls"))
		SuperCron.delete_job(args)

	def test_midnight(self):
		entry1 = b"@daily ls # SuperCron__TEST__ls"
		entry2  = b"0 0 * * * ls # SuperCron__TEST__ls"
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls", "midnight"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry1 in user_crontab or entry2 in user_crontab)

	def test_everyday(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} * * * ls # SuperCron__TEST__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls", "everyday"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_at_boot(self):
		entry = b"@reboot ls # SuperCron__TEST__ls"
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls", "at reboot"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_every_x_minutes(self):
		entry = b"*/5 * * * * ls # SuperCron__TEST__ls"
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls", "once every 5 minutes"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_every_x_hours(self):
		hour, minute = Utils.get_time_now()
		entry = "{} */2 * * * ls # SuperCron__TEST__ls".format(minute).encode()
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls", "once every 2 hours"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_every_x_days(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} */11 * * ls # SuperCron__TEST__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls", "once every 11 days"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_hour_minute_24h(self):
		entry = b"36 15 * * * ls # SuperCron__TEST__ls"
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls", "at 15:36"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_hour_minute_12h(self):
		entry = b"47 16 * * * ls # SuperCron__TEST__ls"
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls", "at 4:47 pm"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_day_month(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} 22 7 * ls # SuperCron__TEST__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls", "on 22/7"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_day_full_month(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} 14 3 * ls # SuperCron__TEST__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls", "14 march"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_mixed_datetime(self):
		entry = b"8 0 1 6 * ls # SuperCron__TEST__ls"
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls", "1/6 12:08 am"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_weekdays_single(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} * * 2 ls # SuperCron__TEST__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls", "on tuesdays"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_weekdays_multiple_non_consecutive(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} * * 1,3,5 ls # SuperCron__TEST__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls", "on mondays, wednesdays and fridays"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_weekdays_multiple_forward(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} * * 1-4 ls # SuperCron__TEST__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls", "from monday to thursday"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_weekdays_multiple_backward(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} * * 0,1,5,6 ls # SuperCron__TEST__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls", "from friday to monday"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_short_weekdays(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} * * 0,1,5,6 ls # SuperCron__TEST__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls", "from fri to mon"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_months_single(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} * 5 * ls # SuperCron__TEST__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls", "in May"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_months_multiple_non_consecutive(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} * 2,5,9 * ls # SuperCron__TEST__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls", "in May and September and February"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_months_multiple_forward(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} * 6-8 * ls # SuperCron__TEST__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls", "from June to August"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_months_multiple_backward(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} * 1,10,11,12 * ls # SuperCron__TEST__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls", "from October to January"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_short_months(self):
		hour, minute = Utils.get_time_now()
		entry = "{} {} * 1,10,11,12 * ls # SuperCron__TEST__ls".format(minute, hour).encode()
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls", "from oct to jan"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_mixed_weekday_time(self):
		entry = b"0 9 * * 1 ls # SuperCron__TEST__ls"
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls", "on monday 09:00"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_mixed_month_time(self):
		entry = b"55 12 * 8 * ls # SuperCron__TEST__ls"
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls", "in august at 12:55 pm"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_mixed_month_weekday_every_x_hours(self):
		hour, minute = Utils.get_time_now()
		entry = "{} */4 * 4 6 ls # SuperCron__TEST__ls".format(minute).encode()
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls", "every 4 hours on saturdays in april"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_mixed_month_multiple_weekday_multiple_every_x_days_midnight(self):
		entry = b"0 0 */2 10,12 1-5 ls # SuperCron__TEST__ls"
		args = Namespace(Utils.list_to_dict("TEST__ls", "ls",
			"midnight every 2 days from monday to friday in october and december"))
		SuperCron.add_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)


class TestJobs(unittest.TestCase):
	"""class that tests supercron for job actions"""

	def setUp(self):
		Utils.DEBUG = False
		args = Namespace(Utils.list_to_dict("TEST__pwd", "pwd", "10:10"))
		SuperCron.add_job(args)

	def tearDown(self):
		args = Namespace(Utils.list_to_dict("TEST__pwd"))
		SuperCron.delete_job(args)

	def test_disable_job(self):
		entry = b"# 10 10 * * * pwd # SuperCron__TEST__pwd"
		args = Namespace(Utils.list_to_dict("TEST__pwd"))
		SuperCron.disable_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_enable_job(self):
		entry = b"10 10 * * * pwd # SuperCron__TEST__pwd"
		dis_entry = b"# " + entry
		args = Namespace(Utils.list_to_dict("TEST__pwd"))
		SuperCron.disable_job(args)
		SuperCron.enable_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab and dis_entry not in user_crontab)

	def test_rename_job(self):
		entry1 = b"10 10 * * * pwd # SuperCron__TEST__pwd"
		entry2 = b"10 10 * * * pwd # SuperCron__TEST__ls"
		args = Namespace({"old_name": "TEST__pwd", "new_name": "TEST__ls"})
		SuperCron.rename_job(args)
		user_crontab = Utils.get_crontab()
		rename_check = entry1 not in user_crontab and entry2 in user_crontab
		args = Namespace({"old_name": "TEST__ls", "new_name": "TEST__pwd"})
		SuperCron.rename_job(args)
		self.assertTrue(rename_check)

	def test_delete_job(self):
		entry = b"10 10 * * * pwd # SuperCron__TEST__pwd"
		args = Namespace(Utils.list_to_dict("TEST__pwd"))
		SuperCron.delete_job(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry not in user_crontab)

	@unittest.skip("Skipped because it will clear all user SuperCron jobs")
	def test_clear_jobs(self):
		entry = b"10 10 * * * pwd # SuperCron__TEST__pwd"
		args = Namespace({"force": True})
		SuperCron.clear_jobs(args)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry not in user_crontab)

	def test_search_job_zero(self):
		entry = b"10 10 * * * pwd # SuperCron__TEST__pwd"
		args = Namespace(Utils.list_to_dict("TEST__pwd"))
		SuperCron.delete_job(args)
		self.assertTrue(SuperCron.search_job(args) != -1)

	def test_search_job_one(self):
		entry = b"10 10 * * * pwd # SuperCron__TEST__pwd"
		args = Namespace(Utils.list_to_dict("TEST__pwd"))
		self.assertTrue(SuperCron.search_job(args) != -1)

	def test_search_job_supercron(self):
		entry = b"10 10 * * * pwd # SuperCron__TEST__pwd"
		args = Namespace(Utils.list_to_dict("@supercron"))
		self.assertTrue(SuperCron.search_job(args) != -1)

	def test_search_job_all(self):
		entry = b"10 10 * * * pwd # SuperCron__TEST__pwd"
		args = Namespace(Utils.list_to_dict("@all"))
		self.assertTrue(SuperCron.search_job(args) != -1)


class TestTriggers(unittest.TestCase):
	"""class for testing triggers"""

	def setUp(self):
		Utils.DEBUG = False
		args = Namespace(Utils.list_to_dict("TEST__echo1", "echo 1 > /dev/null", "11:11"))
		SuperCron.add_job(args)
		args = Namespace(Utils.list_to_dict("TEST__echo2", "echo 2 > /dev/null", "12:12"))
		SuperCron.add_job(args)

	def tearDown(self):
		args = Namespace(Utils.list_to_dict("TEST__echo1"))
		SuperCron.delete_job(args)
		args = Namespace(Utils.list_to_dict("TEST__echo2"))
		SuperCron.delete_job(args)

	def test_trigger_on_if_enabled(self):
		entry1 = b"11 11 * * * echo 1 > /dev/null # SuperCron__TEST__echo1%on:TEST__echo2:enabled"
		entry2 = b"# 11 11 * * * echo 1 > /dev/null # SuperCron__TEST__echo1%on:TEST__echo2:enabled"
		args1 = Namespace({"name": "TEST__echo1"})
		SuperCron.disable_job(args1)
		args1 = Namespace({"name": "TEST__echo2"})
		SuperCron.disable_job(args1)
		args2 = Namespace({"name": "TEST__echo1", "trigger": ["on if TEST__echo2 is enabled"]})
		SuperCron.trigger_job(args2)
		SuperCron.enable_job(args1)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry1 in user_crontab and not entry2 in user_crontab)

	def test_trigger_on_if_disabled(self):
		entry1 = b"11 11 * * * echo 1 > /dev/null # SuperCron__TEST__echo1%on:TEST__echo2:disabled"
		entry2 = b"# 11 11 * * * echo 1 > /dev/null # SuperCron__TEST__echo1%on:TEST__echo2:disabled"
		args1 = Namespace({"name": "TEST__echo1"})
		SuperCron.disable_job(args1)
		args2 = Namespace({"name": "TEST__echo1", "trigger": ["on if TEST__echo2 is disabled"]})
		SuperCron.trigger_job(args2)
		args1 = Namespace({"name": "TEST__echo2"})
		SuperCron.disable_job(args1)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry1 in user_crontab and not entry2 in user_crontab)

	def test_trigger_on_if_added(self):
		entry1 = b"11 11 * * * echo 1 > /dev/null # SuperCron__TEST__echo1%on:TEST__echo2:added"
		entry2 = b"# 11 11 * * * echo 1 > /dev/null # SuperCron__TEST__echo1%on:TEST__echo2:added"
		args1 = Namespace({"name": "TEST__echo1"})
		SuperCron.disable_job(args1)
		args1 = Namespace({"name": "TEST__echo2"})
		SuperCron.delete_job(args1)
		args2 = Namespace({"name": "TEST__echo1", "trigger": ["on if TEST__echo2 is added"]})
		SuperCron.trigger_job(args2)
		args1 = Namespace(Utils.list_to_dict("TEST__echo2", "echo 2 > /dev/null", "12:12"))
		SuperCron.add_job(args1)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry1 in user_crontab and not entry2 in user_crontab)

	def test_trigger_on_if_deleted(self):
		entry1 = b"11 11 * * * echo 1 > /dev/null # SuperCron__TEST__echo1%on:TEST__echo2:deleted"
		entry2 = b"# 11 11 * * * echo 1 > /dev/null # SuperCron__TEST__echo1%on:TEST__echo2:deleted"
		args1 = Namespace({"name": "TEST__echo1"})
		SuperCron.disable_job(args1)
		args2 = Namespace({"name": "TEST__echo1", "trigger": ["on if TEST__echo2 is deleted"]})
		SuperCron.trigger_job(args2)
		args1 = Namespace({"name": "TEST__echo2"})
		SuperCron.delete_job(args1)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry1 in user_crontab and not entry2 in user_crontab)

	def test_trigger_off_if_enabled(self):
		entry = b"# 11 11 * * * echo 1 > /dev/null # SuperCron__TEST__echo1%off:TEST__echo2:enabled"
		args1 = Namespace({"name": "TEST__echo2"})
		SuperCron.disable_job(args1)
		args2 = Namespace({"name": "TEST__echo1", "trigger": ["off if TEST__echo2 is enabled"]})
		SuperCron.trigger_job(args2)
		SuperCron.enable_job(args1)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_trigger_off_if_disabled(self):
		entry = b"# 11 11 * * * echo 1 > /dev/null # SuperCron__TEST__echo1%off:TEST__echo2:disabled"
		args2 = Namespace({"name": "TEST__echo1", "trigger": ["off if TEST__echo2 is disabled"]})
		SuperCron.trigger_job(args2)
		args1 = Namespace({"name": "TEST__echo2"})
		SuperCron.disable_job(args1)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_trigger_off_if_added(self):
		entry = b"# 11 11 * * * echo 1 > /dev/null # SuperCron__TEST__echo1%off:TEST__echo2:added"
		args1 = Namespace({"name": "TEST__echo2"})
		SuperCron.delete_job(args1)
		args2 = Namespace({"name": "TEST__echo1", "trigger": ["off if TEST__echo2 is added"]})
		SuperCron.trigger_job(args2)
		args1 = Namespace(Utils.list_to_dict("TEST__echo2", "echo 2 > /dev/null", "12:12"))
		SuperCron.add_job(args1)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_trigger_off_if_deleted(self):
		entry = b"# 11 11 * * * echo 1 > /dev/null # SuperCron__TEST__echo1%off:TEST__echo2:deleted"
		args2 = Namespace({"name": "TEST__echo1", "trigger": ["off if TEST__echo2 is deleted"]})
		SuperCron.trigger_job(args2)
		args1 = Namespace({"name": "TEST__echo2"})
		SuperCron.delete_job(args1)
		user_crontab = Utils.get_crontab()
		self.assertTrue(entry in user_crontab)

	def test_trigger_addition_removal(self):
		entry1 = b"11 11 * * * echo 1 > /dev/null # SuperCron__TEST__echo1"
		entry2 = b"11 11 * * * echo 1 > /dev/null # SuperCron__TEST__echo1%off:TEST__echo2:deleted"
		args2 = Namespace({"name": "TEST__echo1", "trigger": ["off if TEST__echo2 is deleted"]})
		SuperCron.trigger_job(args2)
		user_crontab = Utils.get_crontab()
		test1 = entry2 in user_crontab
		args2 = Namespace({"name": "TEST__echo1", "trigger": ["none"]})
		SuperCron.trigger_job(args2)
		user_crontab = Utils.get_crontab()
		test2 = entry1 in user_crontab and not entry2 in user_crontab
		self.assertTrue(test1 and test2)


def main():
	unittest.main()

if __name__ == "__main__":
	main()
