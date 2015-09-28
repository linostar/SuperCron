import re

try:
	from utils import Utils
except ImportError:
	from supercron.utils import Utils


class Repetition:
	"""class for parsing repetition clauses"""

	@staticmethod
	def expand_repetition(repetition):
		"""expand short day/month names to full day/month names"""
		for short_day in Utils.SHORT_DAYS.keys():
			repetition = re.sub(r"\b{}\b".format(short_day), Utils.SHORT_DAYS[short_day], repetition)
		for short_month in Utils.SHORT_MONTHS.keys():
			repetition = re.sub(r"\b{}\b".format(short_month), Utils.SHORT_MONTHS[short_month], repetition)
		return repetition

	@staticmethod
	def parse_repetition(repetition):
		"""parse and convert different types of repetition clauses"""
		repeat = {}
		repetition = Repetition.expand_repetition(repetition.lower())
		# check for repetition clauses like: "every reboot"
		matched = re.search(r"(at|every)\s+(boot|reboot)", repetition)
		if matched:
			repeat['reboot'] = True
		# check for repetition clauses like: "once every 21 minutes"
		matched = re.search(r"(once\s+)?every\s+(\d+\s+)?minute(s)?", repetition)
		if matched:
			if not matched.group(2):
				repeat['min_every'] = 1
			elif int(matched.group(2)) > 0 and int(matched.group(2)) < 60:
				repeat['min_every'] = int(matched.group(2))
			else:
				Utils.debug_print("Error: invalid value '{}'. Expected 1-59 for minutes.")
				sys.exit(1)
		# check for repetition clauses like: "once every 3 hours"
		matched = re.search(r"(once\s+)?every\s+(\d+\s+)?hour(s)?", repetition)
		if matched:
			if not matched.group(2):
				repeat['hour_every'] = 1
			elif int(matched.group(2)) > 0 and int(matched.group(2)) < 24:
				repeat['hour_every'] = int(matched.group(2))
			else:
				Utils.debug_print("Error: invalid value '{}'. Expected 1-23 for hours.")
				sys.exit(1)
		# check for repetition clauses like: "once every 11 days"
		matched = re.search(r"(once\s+)?every\s+(\d+\s+)?day(s)?", repetition)
		if matched:
			if not matched.group(2):
				repeat['day_every'] = 1
			elif int(matched.group(2)) > 0 and int(matched.group(2)) < 460:
				repeat['day_every'] = int(matched.group(2))
			else:
				Utils.debug_print("Error: invalid value '{}'. Expected 1-31 for days.")
				sys.exit(1)
		# check for repetition clauses like: "once every 3 months"
		matched = re.search(r"(once\s+)?every\s+(\d+\s+)?month(s)?", repetition)
		if matched:
			if not matched.group(2):
				repeat['month_every'] = 1
			elif int(matched.group(2)) > 0 and int(matched.group(2)) < 13:
				repeat['month_every'] = int(matched.group(2))
			else:
				Utils.debug_print("Error: invalid value '{}'. Expected 1-12 for months.")
				sys.exit(1)
		# check for repetition clause: "everyday"
		matched = re.match(r"\b(everyday|anyday)\b", repetition)
		if matched:
			repeat['day_every'] = 1
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
				Utils.debug_print("Error: invalid value for hour and/or minute.")
				sys.exit(1)
		# check for repetition clauses like: "19/05"
		matched = re.search(r"(on\s*)?\b(\d{1,2})[/-](\d{1,2})\b", repetition)
		if matched:
			day = int(matched.group(2))
			month = int(matched.group(3))
			if month > 12 or month < 1:
				Utils.debug_print("Error: invalid value for month (expected value: 1-12).")
				sys.exit(1)
			if month == 2 and (day > 29 or day < 1):
				Utils.debug_print("Error: invalid value for day (expected value: 1-29).")
				sys.exit(1)
			if month in (4, 6, 9, 11) and (day > 30 or day < 1):
				Utils.debug_print("Error: invalid value for day (expected value: 1-30).")
				sys.exit(1)
			if day > 31 or day < 1:
				Utils.debug_print("Error: invalid value for day (expected value: 1-31).")
				sys.exit(1)
			else:
				repeat['day_on'] = day
				repeat['month_on'] = [month]
		# check for repetition clauses like: "on monday"
		m_repetition = repetition.replace(" and ", " on ").replace(",and ", " on ").replace(",", " on ")
		matched = re.finditer(r"(on\s+)(monday|tuesday|wednesday|thursday|friday|saturday|sunday)s?", m_repetition)
		weekdays = []
		for match in matched:
			weekdays.append(Utils.DAYS[match.group(2)])
		if weekdays:
			repeat['dow_on'] = weekdays
		# check for repetition clauses like: "from monday to friday"
		matched = re.search(r"(from\s+)(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\s+to\s+" +
			r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", repetition)
		if matched:
			weekdays = []
			weekdays.append(Utils.DAYS[matched.group(2)])
			weekdays.append(Utils.DAYS[matched.group(3)])
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
			matched_months.append(Utils.MONTHS[match.group(2)])
		if matched_months:
			repeat['month_on'] = matched_months
		# check for repetition clauses like: "from june to august"
		matched = re.search(r"(from\s+)(january|february|march|april|may|june|july|august|september|october|november|december)" +
			r"\s+to\s+(january|february|march|april|may|june|july|august|september|october|november|december)", repetition)
		if matched:
			matched_months = []
			matched_months.append(Utils.MONTHS[matched.group(2)])
			matched_months.append(Utils.MONTHS[matched.group(3)])
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
			hour, minute = Utils.get_time_now()
			if not ("min_on" in repeat or "min_every" in repeat):
				repeat['min_on'] = minute
			if not ("hour_on" in repeat or "hour_every" in repeat or "min_every" in repeat):
				repeat['hour_on'] = hour
		return repeat
