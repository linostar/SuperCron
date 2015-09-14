#!/usr/bin/env python

import sys
import re
import argparse

from crontab import CronTab


class NotEnoughArguments(Exception):
	pass


class CantUseDeleteWithOthers(Exception):
	pass


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
		parser.add_argument("-d", "--delete", action="store_true",
			help="for deleteing a job (cannot be simultaneously used with other options)")
		parser.add_argument("name", help="name of the job")
		args = parser.parse_args()
		if args.delete and (args.repetition or args.command):
			raise CantUseDeleteWithOthers
		if args.delete:
			delete_job(args.name)
			sys.exit(0)
		if args.repetition and args.command:
			return args.name, args.command, args.repetition
		else:
			raise NotEnoughArguments
	except CantUseDeleteWithOthers:
		print("Option '--delete' cannot be used with any other options.")
		sys.exit(1)
	except NotEnoughArguments:
		print("Error: not enough (or invalid) arguments. Type 'supercron --help' for help.")
		sys.exit(1)

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
		job.dow.on(repeat['dow_on'])
	if "month_every" in repeat:
		job.month.every(repeat['month_every'])
	if "month_on" in repeat:
		job.month.on(repeat['month_on'])
	job.enable()
	cron.write_to_user(user=True)
	print("Job '{}' has been successfully added.".format(name))

def delete_job(name):
	"""delete the specified job from user's crontab"""
	cron = CronTab(user=True)
	cron.remove_all(comment=name)
	cron.write_to_user(user=True)
	print("Job '{}' has been deleted.".format(name))

def parse_repetition(repetition):
	repeat = {}
	repetition = repetition.lower()
	matched = re.search(r"(once )?every (\d+) minute(s)?(\.)?", repetition)
	if matched:
		if int(matched.group(2)) > 0 and int(matched.group(2)) < 60:
			repeat['min_every'] = int(matched.group(2))
		else:
			print("Error: invalid value '{}'. Expected 1-59 for minutes.")
			sys.exit(1)
	matched = re.search(r"(once )?every (\d+) hour(s)?(\.)?", repetition)
	if matched:
		if int(matched.group(2)) > 0 and int(matched.group(2)) < 24:
			repeat['hour_every'] = int(matched.group(2))
			repeat['min_on'] = 0
		else:
			print("Error: invalid value '{}'. Expected 1-23 for hours.")
			sys.exit(1)
	matched = re.search(r"(once )?every (\d+) day(s)?(\.)?", repetition)
	if matched:
		if int(matched.group(2)) > 0 and int(matched.group(2)) < 460:
			repeat['day_every'] = int(matched.group(2))
			repeat['min_on'] = 0
			repeat['hour_on'] = 0
		else:
			print("Error: invalid value '{}'. Expected 1-31 for days.")
			sys.exit(1)
	return repeat


if __name__ == "__main__":
	name, command, repetition = parse_arguments()
	add_job(name, command[0], parse_repetition(repetition[0]))
	sys.exit(0)
