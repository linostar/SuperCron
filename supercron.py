#!/usr/bin/env python

import sys
import re
import argparse

from crontab import CronTab


class HelpMessage(Exception):
	pass


class FullHelpMessage(Exception):
	pass


class NotEnoughArguments(Exception):
	pass


class CantUseDeleteWithOthers(Exception):
	pass


class Color:
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'


def parse_arguments():
	"""parse the arguments coming from running the script"""
	try:
		parser = argparse.ArgumentParser(description='A utility that translates intelligent schedule commands to crontab entries')
		parser.add_argument('-r', '--repetition', nargs='+', help='repetition clause')
		parser.add_argument('-c', '--command', nargs=1,
			help='command to be executed by the job (should be enclosed by quotes if it contains spaces)')
		parser.add_argument('-d', '--delete', action='store_true', help='name of the job')
		parser.add_argument('name', nargs='+', help='name of the job')
		args = parser.parse_args()
		if args.delete and (args.repetition or args.command):
			raise CantUseDeleteWithOthers
		if args.delete:
			delete_job(args.name)
			sys.exit(0)
		if args.repetition and args.command:
			return args.command, args.repetition
		else:
			raise NotEnoughArguments
	except CantUseDeleteWithOthers:
		print("Option '--delete' cannot be used with any other options.")
		sys.exit(1)
	except HelpMessage:
		print("{}Usage:{} supercron <job name> <command> <time or repetition>"
			.format(Color.BOLD, Color.END))
		print("")
		print("Type 'supercron -h' or 'supercron --help' for detailed information and examples.")
		sys.exit(0)
	except FullHelpMessage:
		print(("{}SuperCron{} is utility that allows you to enter intelligent schedule commands that" +
			" will be translated into crontab entries.").format(Color.BOLD, Color.END))
		print("")
		print("{}Usage:{}\n\tTo add a job:\t\tsupercron <job name> <command> <time or repetition>"
			.format(Color.BOLD, Color.END))
		print("\tTo delete a job:\tsupercron -d <job name>")
		sys.exit(0)
	except NotEnoughArguments:
		print("Error: not enough (or invalid) arguments. Type 'supercon --help' for help.")
		sys.exit(1)

def add_job(name, command, repeat):
	"""add the job to crontab"""
	cron = CronTab(user=True)
	job = cron.new(command=command, comment=name)
	if "min_every" in repeat:
		job.minute.every(repeat['min_every'])
	if "min_on" in repeat:
		job.minute.during(repeat['min_on'])
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
		job.month.during(repeat['month_on'])
	job.enable()
	cron.write_to_user(user=True)

def delete_job(name):
	"""delete the specified job from user's crontab"""
	cron = CronTab(user=True)
	cron.remove_all(comment=name)
	print("Job '{}' has been deleted.")

def parse_repetition(repetition):
	repeat = {}
	repetition = repetition.lower()
	matched = re.search(r"^once every (\d+) minute(s)?(\.)?$", repetition)
	if matched:
		repeat['min_every'] = int(matched.group(1))
	return repeat


if __name__ == "__main__":
	name, command, repetition = parse_arguments()
	add_job(name, command, parse_repetition(repetition))
	sys.exit(0)
