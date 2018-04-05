import logging
import subprocess

import click
import coloredlogs


FORMAT = '[%(name)s] %(levelname)s:%(message)s'
FORMATTER = logging.Formatter(fmt=FORMAT)


def get_logger(name='default', level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(fmt=FORMATTER)
        logger.addHandler(handler)

    coloredlogs.install(level=level, logger=logger, fmt=FORMAT)

    return logger


def _warn(message):
    click.secho(message, fg='red')


def _note(message):
    click.secho(message, fg='green')


def _info(message):
    click.secho(message, fg='yellow')
