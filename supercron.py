#!/usr/bin/env python

import sys

from crontab import CronTab


class HelpMessage(Exception):
	pass

class NotEnoughArguments(Exception):
	pass


def parse_arguments():
	try:
		if len(sys.argv) == 1:
			raise HelpMessage
		if len(sys.argv) == 2:
			if (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
				raise HelpMessage
			else:
				raise NotEnoughArguments
		else:
			return sys.argv[1], " ".join(sys.argv[2:])
	except HelpMessage:
		print("Syntax: supercron <script to be excecuted> <time or repetition clause>")
		sys.exit(0)
	except NotEnoughArguments:
		print("Error: not enough arguments. Type 'supercon --help' for help.")
		sys.exit(1)



if __name__ == "__main__":
	script, repeat = parse_arguments()
	sys.exit(0)
