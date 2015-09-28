#!/usr/bin/env python

import sys
import argparse

try:
	from namespace import Namespace
	from utils import Utils
	from repetition_parsing import Repetition
	from trigger import TCronTab
except ImportError:
	from supercron.namespace import Namespace
	from supercron.utils import Utils
	from supercron.repetition_parsing import Repetition
	from supercron.trigger import TCronTab


class SuperCron:
	"""Main SuperCron class"""

	VERSION = "0.3.0"
	TOBEDELETED = "SuperCron__TOBEDELETED"

	@staticmethod
	def parse_arguments():
		"""parse the arguments coming from running the script"""
		parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
			description="A utility that translates intelligent schedule commands to crontab entries.",
			epilog="Examples:\n\tAdd a job:\tsupercron add -c \"date +%j\" -r \"every 2 days\" log_dates" +
			"\n\tRename a job:\tsupercron rename log_dates log_all_dates" +
			"\n\tDelete a job:\tsupercron delete log_dates" +
			"\n\tEnable a job:\tsupercron enable log_dates" +
			"\n\tDisable a job:\tsupercron disable log_dates" +
			"\n\tSearch jobs:\tsupercron search log_dates" +
			"\n\tClear all jobs:\tsupercron clear")
		parser.add_argument("-V", "--version", action="version", version="SuperCron v{}".format(
			SuperCron.VERSION), help="display version number and exit")
		# Add subparsers
		subparsers = parser.add_subparsers(title="Subcommands", help="Subcommand help")
		parser_add = subparsers.add_parser("add", help="for adding a job",
			description="For adding a job to user's crontab.")
		parser_rename = subparsers.add_parser("rename", help="for renaming a job",
			description="For renaming a SuperCron job in user's crontab.")
		parser_delete = subparsers.add_parser("delete", help="for deleting a job",
			description="For deleting a SuperCron job from user's crontab.")
		parser_enable = subparsers.add_parser("enable", help="for enabling a job",
			description="For enabling a SuperCron job in user's crontab.")
		parser_disable = subparsers.add_parser("disable", help="for disabling a job",
			description="For disabling a SuperCron job in user's crontab.")
		parser_search = subparsers.add_parser("search", help="for searching for a job by name",
			formatter_class=argparse.RawDescriptionHelpFormatter,
			description="For listing SuperCron jobs that match the exact name supplied.\n" +
			"Special cases of the value of 'name':\n" +
			"  - '@supercon' (without quotes): list all SuperCron jobs in user's crontab\n" +
			"  - '@all' (without quotes): list all user's crontab entries")
		parser_clear = subparsers.add_parser("clear", help="for clearing all SuperCron's jobs",
			description="For clearing all SuperCron jobs from user's crontab.")
		# subcommand 'add' arguments
		parser_add.add_argument("-r", "--repetition", nargs=1, required=True,
			help="repetition clause (should be enclosed by quotes if it contains spaces)")
		parser_add.add_argument("-c", "--command", nargs=1, required=True,
			help="command to be executed by the job (should be enclosed by quotes if it contains spaces)")
		parser_add.add_argument("-q", "--quiet", action="store_true", help="do not print any output or error messages")
		parser_add.add_argument("name", help="name of the job")
		parser_add.set_defaults(func=SuperCron.add_job)
		# subcommand 'rename' arguments
		parser_rename.add_argument("-q", "--quiet", action="store_true", help="do not print any output or error messages")
		parser_rename.add_argument("old_name", help="old name of the job")
		parser_rename.add_argument("new_name", help="new name of the job")
		parser_rename.set_defaults(func=SuperCron.rename_job)
		# subcommand 'delete' arguments
		parser_delete.add_argument("-q", "--quiet", action="store_true", help="do not print any output or error messages")
		parser_delete.add_argument("name", help="name of the job")
		parser_delete.set_defaults(func=SuperCron.delete_job)
		# subcommand 'enable' arguments
		parser_enable.add_argument("-q", "--quiet", action="store_true", help="do not print any output or error messages")
		parser_enable.add_argument("name", help="name of the job")
		parser_enable.set_defaults(func=SuperCron.enable_job)
		# subcommand 'disable' arguments
		parser_disable.add_argument("-q", "--quiet", action="store_true", help="do not print any output or error messages")
		parser_disable.add_argument("name", help="name of the job")
		parser_disable.set_defaults(func=SuperCron.disable_job)
		# subcommand 'search' arguments
		parser_search.add_argument("name", help="name of the job")
		parser_search.set_defaults(func=SuperCron.search_job)
		# subcommand 'clear' arguments
		parser_clear.add_argument("-q", "--quiet", action="store_true", help="do not print any output or error messages")
		parser_clear.add_argument("-f", "--force", action="store_true", help="do not ask for confirmation before clearing")
		parser_clear.set_defaults(func=SuperCron.clear_jobs)
		# parse all args
		args = parser.parse_args()
		args.func(args)

	@staticmethod
	def _generic_enable_job(name, enable_it, quiet=None):
		"""enable or disable job(s) by their name"""
		if quiet != None:
			Utils.DEBUG = not quiet
		count = 0
		cron = TCronTab(user=True)
		for job in cron:
			if job.get_name() == name and job.is_enabled() != enable_it:
				job.enable(enable_it)
				count += 1
		if enable_it:
			action = "enabled"
		else:
			action = "disabled"
		cron.write_to_user(user=True)
		if count == 1:
			Utils.debug_print("1 job named '{}' has been {}.".format(name, action))
		else:
			Utils.debug_print("{} jobs named '{}' have been {}.".format(count, name, action))

	@staticmethod
	def enable_job(args):
		if "quiet" in args:
			SuperCron._generic_enable_job(str(args.name), True, args.quiet)
		else:
			SuperCron._generic_enable_job(str(args.name), True)

	@staticmethod
	def disable_job(args):
		if "quiet" in args:
			SuperCron._generic_enable_job(str(args.name), False, args.quiet)
		else:
			SuperCron._generic_enable_job(str(args.name), False)

	@staticmethod
	def add_job(args):
		"""add the job to crontab"""
		if "quiet" in args:
			Utils.DEBUG = not args.quiet
		name = str(args.name)
		if Utils.check_job_name(name) == -1:
			Utils.debug_print("Error: job name cannot be '{}'.".format(name))
			sys.exit(1)
		if Utils.check_job_name(name) == -2:
			Utils.debug_print("Error: job name cannot contain a '%' symbol.")
			sys.exit(1)
		command = str(args.command[0])
		repetition = str(args.repetition[0])
		repeat = Repetition.parse_repetition(repetition)
		if not repeat:
			Utils.debug_print("Error: invalid repetition sentence: '{}'."
				.format(repetition))
			sys.exit(1)
		cron = TCronTab(user=True)
		job = cron.new(command=command, comment=name)
		if "reboot" in repeat:
			job.every_reboot()
		else:
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
		Utils.debug_print("Jobs named '{}' have been successfully added.".format(name))

	@staticmethod
	def rename_job(args):
		"""rename a job in user's crontab"""
		if "quiet" in args:
			Utils.DEBUG = not args.quiet
		count = 0
		old_name = str(args.old_name)
		new_name = str(args.new_name)
		if Utils.check_job_name(new_name) == -1:
			Utils.debug_print("Error: job name cannot be '{}'.".format(name))
			sys.exit(1)
		if Utils.check_job_name(new_name) == -2:
			Utils.debug_print("Error: job name cannot contain a '%' symbol.")
			sys.exit(1)
		cron = TCronTab(user=True)
		for job in cron:
			if job.get_name() == old_name:
				job.set_name(new_name)
				count += 1
		cron.write_to_user(user=True)
		if count == 0:
			Utils.debug_print("Error: job '{}' does not exist.".format(old_name))
		elif count == 1:
			Utils.debug_print("1 job has been renamed from '{}' to '{}'."
				.format(old_name, new_name))
		else:
			Utils.debug_print("{} jobs have been renamed from '{}' to '{}'."
				.format(count, old_name, new_name))

	@staticmethod
	def delete_job(args):
		"""delete the specified job from user's crontab"""
		if "quiet" in args:
			Utils.DEBUG = not args.quiet
		name = str(args.name)
		count = 0
		cron = TCronTab(user=True)
		for job in cron:
			if job.get_name() == name:
				cron.remove(job)
				count += 1
		cron.write_to_user(user=True)
		if count == 1:
			Utils.debug_print("1 job named '{}' has been deleted.".format(name))
		else:
			Utils.debug_print("{} jobs named '{}' have been deleted.".format(count, name))

	@staticmethod
	def clear_jobs(args):
		if "quiet" in args:
			Utils.DEBUG = not args.quiet
		if "force" in args and args.force:
			SuperCron._generic_clear_jobs(args, not Utils.DEBUG)
			return
		Utils.debug_print("Note: this will not affect crontab entries not added by SuperCron.")
		confirm_clear = raw_input("Are you sure you want to clear all of your SuperCron jobs? [y/n]: ")
		if confirm_clear == "y":
			SuperCron._generic_clear_jobs(args, args.quiet)
		else:
			Utils.debug_print("Cancelled.")

	@staticmethod
	def _generic_clear_jobs(args, quiet):
		Utils.DEBUG = not quiet
		count = 0
		cron = TCronTab(user=True)
		for job in cron:
			if job.is_superjob():
				job.comment = SuperCron.TOBEDELETED
				count += 1
		cron.remove_all(comment=SuperCron.TOBEDELETED)
		cron.write_to_user(user=True)
		if count == 1:
			Utils.debug_print("1 job has been removed from your crontab.")
		else:
			Utils.debug_print("{} jobs have been removed from your crontab.".format(count))

	@staticmethod
	def search_job(args):
		"""That moment when you have to rely on a function to look for a job"""
		try:
			count = 0
			name = str(args.name)
			job_list = []
			cron = TCronTab(user=True)
			if name == "@all":
				for job in cron:
					job_name = job.get_name()
					enabled = "YES" if job.is_enabled() else "NO"
					job_list.append([job_name, enabled, str(job.slices), job.command])
			elif name == "@supercron":
				for job in cron:
					if job.is_superjob():
						job_name = job.get_name()
						enabled = "YES" if job.is_enabled() else "NO"
						job_list.append([job_name, enabled, str(job.slices), job.command])
			else:
				jobs = cron.find_comment(name)
				for job in jobs:
					enabled = "YES" if job.is_enabled() else "NO"
					job_list.append([name, enabled, str(job.slices), job.command])
			if job_list:
				col_widths = []
				col_titles = ["Name", "Enabled", "Repetition", "Command"]
				for i in range(0, 4):
					col_widths.append(max(max(len(n[i]) for n in job_list) + 2, len(col_titles[i]) + 2))
				Utils.debug_print("".join(word.ljust(col_widths[i]) for word, i in zip(col_titles, range(0, 4))))
				Utils.debug_print("-" * (sum(col_widths) - 2))
				for job_item in job_list:
					Utils.debug_print("".join(word.ljust(col_widths[i]) for word, i in zip(job_item, range(0, 4))))
					count += 1
			else:
				Utils.debug_print("Zero search results.")
			return count
		except:
			# in case of any error, so the unittests can detect it
			return -1

	@staticmethod
	def interactive_mode():
		try:
			action_list = ("add", "rename", "delete", "enable", "disable", "search", "clear")
			Utils.debug_print("SuperCron (interactive mode)")
			Utils.debug_print("")
			action = raw_input("Action [add/rename/delete/enable/disable/search/clear]: ")
			action = str(action.lower().strip())
			if action not in action_list:
				Utils.debug_print("Error: action '{}' not recognized.".format(action))
				sys.exit(1)
			args = Namespace()
			if action == "clear":
				Utils.debug_print("")
				SuperCron.clear_jobs(args)
				return
			if action == "rename":
				args.old_name = raw_input("Job old name: ")
				args.new_name = raw_input("Job new name: ")
				Utils.debug_print("")
				SuperCron.rename_job(args)
				return
			args.name = raw_input("Job name: ")
			if action == "add":
				args.command = [raw_input("Command to be executed: ")]
				args.repetition = [raw_input("Repetition sentence: ")]
				Utils.debug_print("")
				SuperCron.add_job(args)
			elif action == "delete":
				Utils.debug_print("")
				SuperCron.delete_job(args)
			elif action == "enable":
				Utils.debug_print("")
				SuperCron.enable_job(args)
			elif action == "disable":
				Utils.debug_print("")
				SuperCron.disable_job(args)
			elif action == "search":
				Utils.debug_print("")
				SuperCron.search_job(args)
		except KeyboardInterrupt:
			Utils.debug_print("\nCancelled.")


def main():
	if len(sys.argv) == 1:
		SuperCron.interactive_mode()
	else:
		SuperCron.parse_arguments()
	sys.exit(0)

if __name__ == "__main__":
	main()
