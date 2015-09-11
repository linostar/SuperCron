#!/usr/bin/env python

import sys

from crontab import CronTab


class HelpMessage(Exception):
	pass


class FullHelpMessage(Exception):
	pass


class NotEnoughArguments(Exception):
	pass


class Color:
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'


def parse_arguments():
	"""parse the arguments coming from running the script"""
	try:
		if len(sys.argv) == 1:
			raise HelpMessage
		if len(sys.argv) == 2:
			if sys.argv[1] == "-h" or sys.argv[1] == "--help":
				raise FullHelpMessage
			else:
				raise NotEnoughArguments
		if len(sys.argv) == 3:
			if sys.argv[1] == "-d":
				delete_job(sys.argv[2])
		if len(sys.argv) >= 4:
			return sys.argv[1], " ".join(sys.argv[2:])
		else:
			raise NotEnoughArguments
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

def parse_repetition(repeat):
	return repeat


if __name__ == "__main__":
	name, command, repeat = parse_arguments()
	add_job(name, command, parse_repetition(repeat))
	sys.exit(0)
