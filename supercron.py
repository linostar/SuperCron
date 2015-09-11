#!/usr/bin/env python

import sys

from crontab import CronTab


class HelpMessage(Exception):
	pass

class FullHelpMessage(Exception):
	pass

class NotEnoughArguments(Exception):
	pass


def parse_arguments():
	try:
		if len(sys.argv) == 1:
			raise HelpMessage
		if len(sys.argv) == 2:
			if (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
				raise FullHelpMessage
			else:
				raise NotEnoughArguments
		else:
			return sys.argv[1], " ".join(sys.argv[2:])
	except HelpMessage:
		print("Usage: supercron <script to be excecuted> <time or repetition clause>")
		print("Type 'supercron -h' or 'supercron --help' for detailed information and examples.")
		sys.exit(0)
	except FullHelpMessage:
		print("SuperCron is utility that allows you to enter intelligent schedule commands that" +
			"will be translated into crontab entries.")
		print("Usage: supercron <script to be excecuted> <time or repetition clause>")
		sys.exit(0)
	except NotEnoughArguments:
		print("Error: not enough arguments. Type 'supercon --help' for help.")
		sys.exit(1)



if __name__ == "__main__":
	script, repeat = parse_arguments()
	sys.exit(0)
