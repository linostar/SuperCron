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
			if not check_other_args("delete", args):
				raise CantUseOptWithOthers
			delete_job(args.name)
			sys.exit(0)
		if args.enable:
			if not check_other_args("enable", args):
				raise CantUseOptWithOthers
			enable_job(args.name, True)
			sys.exit(0)
		if args.disable:
			if not check_other_args("disable", args):
				raise CantUseOptWithOthers
			enable_job(args.name, False)
			sys.exit(0)
		if args.repetition and args.command:
			return args.name, args.command, args.repetition
		else:
			raise NotEnoughArguments
	except CantUseOptWithOthers:
		print("Options '--delete', '--disable' and '--enable' cannot be used with any other options.")
		sys.exit(1)
	except NotEnoughArguments:
		print("Error: not enough (or invalid) arguments. Type 'supercron --help' for help.")
		sys.exit(1)

def check_other_args(wanted, args):
	for arg in args.__dict__:
		if arg != wanted and arg != "name" and args.__dict__[arg]:
			return False
	return True

def get_time_now():
	hour = datetime.now().hour
	minute = datetime.now().minute
	return hour, minute

def enable_job(name, enable_it):
	cron = CronTab(user=True)
	for job in cron.find_comment(name):
		job.enable(enable_it)
	if enable_it:
		action = "enabled"
	else:
		action = "disabled"
	cron.write_to_user(user=True)
	print("Jobs named '{}' have been {}.".format(name, action))

def add_job(name, command, repeat):
	"""add the job to crontab"""
	if not repeat:
		print("Error: invalid repetition clause.")
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
	if "dow_every" in repeat:
		job.dow.every(repeat['dow_every'])
	if "dow_on" in repeat:
		job.dow.on(*repeat['dow_on'])
	if "dow_during" in repeat:
		job.dow.during(*repeat['dow_during'])
	if "month_every" in repeat:
		job.month.every(repeat['month_every'])
	if "month_on" in repeat:
		job.month.on(repeat['month_on'])
	job.enable()
	cron.write_to_user(user=True)
	print("Jobs named '{}' have been successfully added.".format(name))

def delete_job(name):
	"""delete the specified job from user's crontab"""
	cron = CronTab(user=True)
	cron.remove_all(comment=name)
	cron.write_to_user(user=True)
	print("Jobs named '{}' have been deleted.".format(name))

def expand_repetition(repetition):
	for short_day in SHORT_DAYS.keys():
		repetition = re.sub("\b{}\b".format(short_day), SHORT_DAYS[short_day], repetition)
	for short_month in SHORT_MONTHS.keys():
		repetition = re.sub("\b{}\b".format(short_month), SHORT_MONTHS[short_month], repetition)
	return repetition

def parse_repetition(repetition):
	repeat = {}
	repetition = expand_repetition(repetition.lower())
	matched = re.search(r"(once\s+)?every\s+(\d+)\s+minute(s)?(\.)?", repetition)
	if matched:
		if int(matched.group(2)) > 0 and int(matched.group(2)) < 60:
			repeat['min_every'] = int(matched.group(2))
		else:
			print("Error: invalid value '{}'. Expected 1-59 for minutes.")
			sys.exit(1)
	matched = re.search(r"(once\s+)?every\s+(\d+)\s+hour(s)?(\.)?", repetition)
	if matched:
		if int(matched.group(2)) > 0 and int(matched.group(2)) < 24:
			repeat['hour_every'] = int(matched.group(2))
		else:
			print("Error: invalid value '{}'. Expected 1-23 for hours.")
			sys.exit(1)
	matched = re.search(r"(once\s+)?every\s+(\d+)\s+day(s)?(\.)?", repetition)
	if matched:
		if int(matched.group(2)) > 0 and int(matched.group(2)) < 460:
			repeat['day_every'] = int(matched.group(2))
		else:
			print("Error: invalid value '{}'. Expected 1-31 for days.")
			sys.exit(1)
	matched = re.search(r"(on\s+)?(\d+):(\d+)(\s+(am|pm))?", repetition)
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
			print("Error: invalid value for hour and/or minute.")
			sys.exit(1)
	matched = re.finditer(r"(on\s+)(monday|tuesday|wednesday|thursday|friday|saturday|sunday)s?", repetition)
	weekdays = []
	for match in matched:
		weekdays.append(DAYS[match.group(2)])
	if weekdays:
		repeat['dow_on'] = weekdays
	matched = re.search(r"(from\s+)(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\s+to\s+" +
		r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", repetition)
	if matched:
		weekdays = []
		weekdays.append(DAYS[matched.group(2)])
		weekdays.append(DAYS[matched.group(3)])
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
	# check if minute and hour fields are empty
	hour, minute = get_time_now()
	if not ("min_on" in repeat or "min_every" in repeat):
		repeat['min_on'] = minute
	if not ("hour_on" in repeat or "hour_every" in repeat):
		repeat['hour_on'] = hour
	return repeat


if __name__ == "__main__":
	name, command, repetition = parse_arguments()
	add_job(name, command[0], parse_repetition(repetition[0]))
	sys.exit(0)
