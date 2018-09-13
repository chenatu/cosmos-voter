import yaml
import logging

log = logging.getLogger(__name__)


with open("config.yaml", "rb") as stream:
    log.info("load config from config.yaml")
    CONFIG = yaml.load(stream)
