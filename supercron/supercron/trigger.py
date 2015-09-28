from crontab import CronTab


class Trigger:
	"""class for storing, searching and applying triggers on jobs"""

	@staticmethod
	def check_triggering_jobs(job, trigger):
		cron = CronTab(user=True)
		if trigger == "enabled":
			pass
