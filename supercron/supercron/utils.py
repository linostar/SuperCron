from datetime import datetime
from subprocess import Popen, PIPE

class Utils:
	"""class that contains different utilities functions"""

	DEBUG = True
	FORBIDDEN_NAMES = ("@all", "@supercron")

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
	def debug_print(string, force_print=False):
		if Utils.DEBUG or force_print:
			print(string)

	@staticmethod
	def get_time_now():
		"""get current time"""
		hour = datetime.now().hour
		minute = datetime.now().minute
		return hour, minute

	@staticmethod
	def list_to_dict(name, command="", repetition=""):
		args_dict = {}
		args_dict['name'] = name
		args_dict['command'] = [command]
		args_dict['repetition'] = [repetition]
		return args_dict

	@staticmethod
	def get_crontab():
		p = Popen(["crontab", "-l"], stdout=PIPE, stderr=PIPE)
		crontab_out, crontab_err = p.communicate()
		return crontab_out

	@staticmethod
	def check_job_name(name):
		if name not in Utils.FORBIDDEN_NAMES:
			return True
