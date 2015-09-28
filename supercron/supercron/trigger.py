from crontab import CronTab, CronItem


class TCronTab(CronTab):
	"""class for extending CronTab with triggers"""

	PREFIX = "SuperCron__"

	def __init__(self, user=None, tab=None, tabfile=None, log=None):
		super(TCronTab, self).__init__(user, tab, tabfile, log)

	def find_comment(self, comment):
		return super(TCronTab, self).find_comment(PREFIX + comment)

	def new(self, command="", comment="", user=None):
		if not user and self.user is False:
			raise ValueError("User is required for system crontabs.")
		item = TCronItem(command=command, comment=self.PREFIX + comment, user=user, cron=self)
		self.crons.append(item)
		self.lines.append(item)
		return item

	def check_triggering_jobs(self, job, trigger):
		cron = CronTab(user=True)
		if trigger == "enabled":
			pass


class TCronItem(CronItem):
	"""class for extending CronItem with triggers"""

	PREFIX = "SuperCron__"

	def __init__(self, line=None, command='', comment='', user=None, cron=None):
		super(TCronItem, self).__init__(line, command, comment, user, cron)

	def get_name(self):
		if self.comment.startswith(self.PREFIX):
			sep = self.comment.find("%")
			if sep == -1:
				return self.comment
			return self.comment[:sep].rstrip()
		else:
			# not a SuperCron job
			return self.comment

	def set_name(self, name):
		if if self.comment.startswith(self.PREFIX):
			sep = self.comment.find("%")
			if sep == -1 or sep == len(self.comment) - 1:
				self.comment = name
			else:
				self.comment = name + " %" + self.comment[sep+1:]
		elif self.comment:
			# this is not a SuperCron job, so don't edit
			pass
		else:
			self.comment = name
