# -*- coding: utf-8 -*-
""" Main Click methods """

import configparser
import logging
from time import sleep

import click

from tilty import tilt_device
from tilty.tilty import emit

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

CONFIG = configparser.ConfigParser()


@click.command()
@click.option(
    '--keep-running',
    '-r',
    is_flag=True,
    help="Keep running until SIGTERM",
)
@click.option(
    '--config-file',
    '-c',
    default='config.ini',
    help="configuration file path",
)
def run(
    keep_running,
    config_file='config.ini',
):
    """ main cli entrypoint
    """
    CONFIG.read(config_file)
    click.echo('Scanning for Tilt data...')
    t = tilt_device.TiltDevice()
    t.start()
    if keep_running:
        while True:
            tilt_data = t.scan_for_tilt_data()
            emit(config=CONFIG, tilt_data=tilt_data)
            sleep(int(CONFIG['general']['sleep_interval']))
    else:
        tilt_data = t.scan_for_tilt_data()
        click.echo(tilt_data)
        emit(config=CONFIG, tilt_data=tilt_data)
