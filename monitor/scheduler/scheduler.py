import time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger


# very simple cron scheduler
class Scheduler:
    def __init__(self, strategy, cron):
        self.strategy = strategy
        self.scheduler = BlockingScheduler()
        self.cron = cron

    def _func(self):
        self.strategy.run()

    def start(self):
        self.scheduler.add_job(self._func, CronTrigger.from_crontab(self.cron))
        self.scheduler.start()

    def stop(self):
        self.scheduler.shutdown(wait=False)
