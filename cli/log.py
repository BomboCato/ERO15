#
# cli/log.py
#

import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("Rich")


def info(msg: str) -> None:
    log.info(msg)

def warn(msg: str) -> None:
    log.warn(msg)

def error(msg: str) -> None:
    log.error(msg)
