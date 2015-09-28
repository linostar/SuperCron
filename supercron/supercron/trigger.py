import re
import codecs
import subprocess as sp

from crontab import CronTab, CronItem


class TCronTab(CronTab):
	"""class for extending CronTab with triggers"""

	PREFIX = "SuperCron__"
	
	def __init__(self, user=None, tab=None, tabfile=None, log=None):
		super(TCronTab, self).__init__(user, tab, tabfile, log)

	def pipeOpen(self, cmd, *args, **flags):
		l = tuple(cmd.split(' '))
		for (k,v) in flags.items():
			if v is not None:
				l += len(k)==1 and ("-%s" % (k,), str(v)) or ("--%s=%s" % (k,v),)
		l += tuple(args)
		return sp.Popen(tuple(a for a in l if a), stdout=sp.PIPE, stderr=sp.PIPE)

	def find_comment(self, comment):
		return super(TCronTab, self).find_comment(self.PREFIX + comment)

	def new(self, command="", comment="", user=None):
		if not user and self.user is False:
			raise ValueError("User is required for system crontabs.")
		item = TCronItem(command=command, comment=self.PREFIX + comment, user=user, cron=self)
		self.crons.append(item)
		self.lines.append(item)
		return item

	def read(self, filename=None):
		self.crons = []
		self.lines = []
		lines = []
		if self.intab is not None:
			lines = self.intab.split('\n')
		elif filename:
			self.filen = filename
			with codecs.open(filename, 'r', encoding='utf-8') as fhl:
				lines = fhl.readlines()
		elif self.user:
			(out, err) = self.pipeOpen("crontab", l='', **self.user_opt).communicate()
			if err and 'no crontab for' in str(err):
				pass
			elif err:
				raise IOError("Read crontab %s: %s" % (self.user, err))
			lines = out.decode('utf-8').split("\n")
		for line in lines:
			cron = TCronItem(line, cron=self)
			if cron.is_valid():
				self.crons.append(cron)
				self.lines.append(cron)
			else:
				self.lines.append(line.replace('\n', ''))

	def check_triggering_jobs(self, job, trigger):
		cron = CronTab(user=True)
		if trigger == "enabled":
			pass


class TCronItem(CronItem):
	"""class for extending CronItem with triggers"""

	PREFIX = "SuperCron__"
	SEPARATOR = "%"

	def __init__(self, line=None, command='', comment='', user=None, cron=None):
		super(TCronItem, self).__init__(line, command, comment, user, cron)

	def is_superjob(self):
		return self.comment.startswith(self.PREFIX)

	def get_name(self):
		if self.is_superjob():
			sep = self.comment.find(self.SEPARATOR)
			if sep == -1:
				return self.comment[len(self.PREFIX):]
			return self.comment[len(self.PREFIX):sep]
		else:
			# not a SuperCron job
			return self.comment

	def set_name(self, name):
		if self.is_superjob():
			sep = self.comment.find(self.SEPARATOR)
			if sep == -1 or sep == len(self.comment) - 1:
				self.comment = self.PREFIX + name
			else:
				self.comment = self.PREFIX + name + self.SEPARATOR + self.comment[sep+1:]
		elif self.comment:
			# this is not a SuperCron job, so don't edit
			pass
		else:
			self.comment = name

	def parse_trigger(self, string):
		matched = re.match(r"(on|off|toggle)\s+if\s+(.+)\s*==\s*(enabled|disabled|added|removed)",
			string.strip(), re.IGNORECASE)
		if matched:
			trigger = [matched.group(1).lower(), matched.group(2), matched.group(3).lower()]
			return trigger

	def get_trigger(self):
		if self.is_superjob():
			sep = self.comment.find(self.SEPARATOR)
			if sep not in (-1, 0, len(self.comment)-1):
				return self.comment[sep+1:].split(":")

	def set_trigger(self, trigger):
		if self.is_superjob():
			trigger_string = ":".join(trigger)
			sep = self.comment.find(self.SEPARATOR)
			if sep == -1:
				self.comment += self.SEPARATOR + trigger_string
			else:
				self.comment = self.comment[:sep] + self.SEPARATOR + trigger_string
		else:
			# do nothing for non-superjobs
			pass
