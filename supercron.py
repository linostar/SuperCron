#!/usr/bin/env python

import sys
import re
import argparse
from datetime import datetime

from crontab import CronTab


class NotEnoughArguments(Exception):
	pass


class CantUseOptWithOthers(Exception):
	pass


class SuperCron:
	"""Main SuperCron class"""

	DEBUG = True

	DAYS = {
		"sunday": "0",
		"monday": "1",
		"tuesday": "2",
		"wednesday": "3",
		"thursday": "4",
		"friday": "5",
		"saturday": "6"
	}

	MONTHS = {
		"january": "1",
		"february": "2",
		"march": "3",
		"april": "4",
		"may": "5",
		"june": "6",
		"july": "7",
		"august": "8",
		"september": "9",
		"october": "10",
		"november": "11",
		"december": "12"
	}

	SHORT_DAYS = {key[:3]:key for key in DAYS.keys()}

	SHORT_MONTHS = {key[:3]:key for key in MONTHS.keys()}

	@staticmethod
	def debug_print(string):
		if SuperCron.DEBUG:
			print(string)

	@staticmethod
	def parse_arguments():
		"""parse the arguments coming from running the script"""
		try:
			parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
				description="A utility that translates intelligent schedule commands to crontab entries.",
				epilog="Examples:\n\tAdd a job:\tsupercron -c \"date +%j >> some_file\" -r \"every 1 hour\" log_dates" +
				"\n\tDelete a job:\tsupercron -d log_dates")
			parser.add_argument("-r", "--repetition", nargs=1,
				help="repetition clause (should be enclosed by quotes if it contains spaces)")
			parser.add_argument("-c", "--command", nargs=1,
				help="command to be executed by the job (should be enclosed by quotes if it contains spaces)")
			parser.add_argument("-d", "--delete", action="store_true", help="for deleteing a job")
			parser.add_argument("--enable", action="store_true", help="for enabling a job")
			parser.add_argument("--disable", action="store_true", help="for disabling a job")
			parser.add_argument("name", help="name of the job")
			args = parser.parse_args()
			if args.delete:
				if not SuperCron.check_other_args("delete", args):
					raise CantUseOptWithOthers
				SuperCron.delete_job(args.name)
				sys.exit(0)
			if args.enable:
				if not SuperCron.check_other_args("enable", args):
					raise CantUseOptWithOthers
				SuperCron.enable_job(args.name, True)
				sys.exit(0)
			if args.disable:
				if not SuperCron.check_other_args("disable", args):
					raise CantUseOptWithOthers
				SuperCron.enable_job(args.name, False)
				sys.exit(0)
			if args.repetition and args.command:
				return args.name, args.command, args.repetition
			else:
				raise NotEnoughArguments
		except CantUseOptWithOthers:
			SuperCron.debug_print("Options '--delete', '--disable' and '--enable' cannot be used with any other options.")
			sys.exit(1)
		except NotEnoughArguments:
			SuperCron.debug_print("Error: not enough (or invalid) arguments. Type 'supercron --help' for help.")
			sys.exit(1)

	@staticmethod
	def check_other_args(wanted, args):
		"""check that mutual exclusive options are alone"""
		for arg in args.__dict__:
			if arg != wanted and arg != "name" and args.__dict__[arg]:
				return False
		return True

	@staticmethod
	def get_time_now():
		"""get current time"""
		hour = datetime.now().hour
		minute = datetime.now().minute
		return hour, minute

	@staticmethod
	def enable_job(name, enable_it):
		"""enable or disable job(s) by their name"""
		cron = CronTab(user=True)
		for job in cron.find_comment(name):
			job.enable(enable_it)
		if enable_it:
			action = "enabled"
		else:
			action = "disabled"
		cron.write_to_user(user=True)
		SuperCron.debug_print("Jobs named '{}' have been {}.".format(name, action))

	@staticmethod
	def add_job(name, command, repeat):
		"""add the job to crontab"""
		repeat = SuperCron.parse_repetition(repeat)
		if not repeat:
			SuperCron.debug_print("Error: invalid repetition clause.")
			sys.exit(1)
		cron = CronTab(user=True)
		job = cron.new(command=command, comment=name)
		if "min_every" in repeat:
			job.minute.every(repeat['min_every'])
		if "min_on" in repeat:
			job.minute.on(repeat['min_on'])
		if "hour_every" in repeat:
			job.hour.every(repeat['hour_every'])
		if "hour_on" in repeat:
			job.hour.on(repeat['hour_on'])
		if "day_every" in repeat:
			job.day.every(repeat['day_every'])
		if "day_on" in repeat:
			job.day.on(repeat['day_on'])
		if "dow_on" in repeat:
			job.dow.on(*repeat['dow_on'])
		if "dow_during" in repeat:
			job.dow.during(*repeat['dow_during'])
		if "month_every" in repeat:
			job.month.every(repeat['month_every'])
		if "month_during" in repeat:
			job.month.during(*repeat['month_during'])
		if "month_on" in repeat:
			job.month.on(*repeat['month_on'])
		job.enable()
		cron.write_to_user(user=True)
		SuperCron.debug_print("Jobs named '{}' have been successfully added.".format(name))

	@staticmethod
	def delete_job(name):
		"""delete the specified job from user's crontab"""
		cron = CronTab(user=True)
		cron.remove_all(comment=name)
		cron.write_to_user(user=True)
		SuperCron.debug_print("Jobs named '{}' have been deleted.".format(name))

	@staticmethod
	def expand_repetition(repetition):
		"""expand short day/month names to full day/month names"""
		for short_day in SuperCron.SHORT_DAYS.keys():
			repetition = re.sub(r"\b{}\b".format(short_day), SuperCron.SHORT_DAYS[short_day], repetition)
		for short_month in SuperCron.SHORT_MONTHS.keys():
			repetition = re.sub(r"\b{}\b".format(short_month), SuperCron.SHORT_MONTHS[short_month], repetition)
		return repetition

	@staticmethod
	def parse_repetition(repetition):
		"""parse and convert different types of repetition clauses"""
		repeat = {}
		repetition = SuperCron.expand_repetition(repetition.lower())
		# check for repetition clauses like: "once every 21 minutes"
		matched = re.search(r"(once\s+)?every\s+(\d+\s+)?minute(s)?", repetition)
		if matched:
			if not matched.group(2):
				repeat['min_every'] = 1
			elif int(matched.group(2)) > 0 and int(matched.group(2)) < 60:
				repeat['min_every'] = int(matched.group(2))
			else:
				SuperCron.debug_print("Error: invalid value '{}'. Expected 1-59 for minutes.")
				sys.exit(1)
		# check for repetition clauses like: "once every 3 hours"
		matched = re.search(r"(once\s+)?every\s+(\d+\s+)?hour(s)?", repetition)
		if matched:
			if not matched.group(2):
				repeat['hour_every'] = 1
			elif int(matched.group(2)) > 0 and int(matched.group(2)) < 24:
				repeat['hour_every'] = int(matched.group(2))
			else:
				SuperCron.debug_print("Error: invalid value '{}'. Expected 1-23 for hours.")
				sys.exit(1)
		# check for repetition clauses like: "once every 11 days"
		matched = re.search(r"(once\s+)?every\s+(\d+\s+)?day(s)?", repetition)
		if matched:
			if not matched.group(2):
				repeat['day_every'] = 1
			elif int(matched.group(2)) > 0 and int(matched.group(2)) < 460:
				repeat['day_every'] = int(matched.group(2))
			else:
				SuperCron.debug_print("Error: invalid value '{}'. Expected 1-31 for days.")
				sys.exit(1)
		# check for repetition clauses like: "once every 3 months"
		matched = re.search(r"(once\s+)?every\s+(\d+\s+)?month(s)?", repetition)
		if matched:
			if not matched.group(2):
				repeat['month_every'] = 1
			elif int(matched.group(2)) > 0 and int(matched.group(2)) < 13:
				repeat['month_every'] = int(matched.group(2))
			else:
				SuperCron.debug_print("Error: invalid value '{}'. Expected 1-12 for months.")
				sys.exit(1)
		# check for repetition clause: "at midnight"
		matched = re.match(r"(at\s*)?\bmidnight\b", repetition)
		if matched:
			repeat['min_on'] = 0
			repeat['hour_on'] = 0
		# check for repetition clauses like: "10:32 am"
		matched = re.search(r"(on|at\s*)?\b(\d{1,2}):(\d{1,2})\b(\s*(am|pm))?", repetition)
		if matched:
			hour = int(matched.group(2))
			minute = int(matched.group(3))
			if matched.group(4):
				if matched.group(5) == "pm":
					if hour != 12:
						hour += 12
				else:
					if hour == 12:
						hour = 0
			if hour < 24 and minute < 59:
				repeat['min_on'] = minute
				repeat['hour_on'] = hour
			else:
				SuperCron.debug_print("Error: invalid value for hour and/or minute.")
				sys.exit(1)
		# check for repetition clauses like: "19/05"
		matched = re.search(r"(on\s*)?\b(\d{1,2})[/-](\d{1,2})\b", repetition)
		if matched:
			day = int(matched.group(2))
			month = int(matched.group(3))
			if month > 12 or month < 1:
				SuperCron.debug_print("Error: invalid value for month (expected value: 1-12).")
				sys.exit(1)
			if month == 2 and (day > 29 or day < 1):
				SuperCron.debug_print("Error: invalid value for day (expected value: 1-29).")
				sys.exit(1)
			if month in (4, 6, 9, 11) and (day > 30 or day < 1):
				SuperCron.debug_print("Error: invalid value for day (expected value: 1-30).")
				sys.exit(1)
			if day > 31 or day < 1:
				SuperCron.debug_print("Error: invalid value for day (expected value: 1-31).")
				sys.exit(1)
			else:
				repeat['day_on'] = day
				repeat['month_on'] = [month]
		# check for repetition clauses like: "on monday"
		m_repetition = repetition.replace(" and ", " on ").replace(",and ", " on ").replace(",", " on ")
		matched = re.finditer(r"(on\s+)(monday|tuesday|wednesday|thursday|friday|saturday|sunday)s?", m_repetition)
		weekdays = []
		for match in matched:
			weekdays.append(SuperCron.DAYS[match.group(2)])
		if weekdays:
			repeat['dow_on'] = weekdays
		# check for repetition clauses like: "from monday to friday"
		matched = re.search(r"(from\s+)(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\s+to\s+" +
			r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", repetition)
		if matched:
			weekdays = []
			weekdays.append(SuperCron.DAYS[matched.group(2)])
			weekdays.append(SuperCron.DAYS[matched.group(3)])
			if weekdays[0] < weekdays[1]:
				repeat['dow_during'] = weekdays
			else:
				dows = []
				i = int(weekdays[0])
				while i != int(weekdays[1]):
					dows.append(str(i))
					i = (i + 1) % 7
				dows.append(str(weekdays[1]))
				repeat['dow_on'] = dows
		# check for repetition clauses like: "on december"
		m_repetition = repetition.replace(" and ", " in ").replace(",and ", " in ").replace(",", "in ")
		matched = re.finditer(r"([oi]n\s+)(january|february|march|april|may|june|july|august|september|october|november|december)",
			m_repetition)
		matched_months = []
		for match in matched:
			matched_months.append(SuperCron.MONTHS[match.group(2)])
		if matched_months:
			repeat['month_on'] = matched_months
		# check for repetition clauses like: "from june to august"
		matched = re.search(r"(from\s+)(january|february|march|april|may|june|july|august|september|october|november|december)" +
			r"\s+to\s+(january|february|march|april|may|june|july|august|september|october|november|december)", repetition)
		if matched:
			matched_months = []
			matched_months.append(SuperCron.MONTHS[matched.group(2)])
			matched_months.append(SuperCron.MONTHS[matched.group(3)])
			if matched_months[0] < matched_months[1]:
				repeat['month_during'] = matched_months
			else:
				consec_months = []
				i = int(matched_months[0])
				while i != int(matched_months[1]):
					consec_months.append(str(i))
					i = (i % 12) + 1
				consec_months.append(str(matched_months[1]))
				repeat['month_on'] = consec_months
		# check if minute and hour fields are empty
		if repeat:
			hour, minute = SuperCron.get_time_now()
			if not ("min_on" in repeat or "min_every" in repeat):
				repeat['min_on'] = minute
			if not ("hour_on" in repeat or "hour_every" in repeat or "min_every" in repeat):
				repeat['hour_on'] = hour
		return repeat


if __name__ == "__main__":
	name, command, repetition = SuperCron.parse_arguments()
	SuperCron.add_job(name, command[0], repetition[0])
	sys.exit(0)
