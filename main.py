# coding=utf-8
import logging
import os
from voter import voter
from alert import ali_sms_alert, level
from monitor.scheduler.scheduler import Scheduler
from monitor.strategy.simple_strategy import SimpleStrategy

BANNER = r"""
                                                 _
   ___ ___  ___ _ __ ___   ___  ___  __   _____ | |_ ___ _ __
  / __/ _ \/ __| '_ ` _ \ / _ \/ __| \ \ / / _ \| __/ _ \ '__|
 | (_| (_) \__ \ | | | | | (_) \__ \  \ V / (_) | ||  __/ |
  \___\___/|___/_| |_| |_|\___/|___/   \_/ \___/ \__\___|_|
"""

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"),
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT
    )

log = logging.getLogger(__name__)


def main():
    log.info(BANNER)
    log.info("start autovoter")
    from config import CONFIG
    strategy = SimpleStrategy(CONFIG)
    cron = CONFIG["scheduler"]["cron"]
    scheduler = Scheduler(strategy, cron)
    scheduler.start()

if __name__ == "__main__":
    main()
