# -*- coding: utf-8 -*-
""" Main Click methods """

import configparser
import logging
import pathlib
import signal
import sys
import threading
from functools import partial
from time import sleep

import click

from tilty import tilt_device
from tilty.exceptions import ConfigurationFileNotFoundException
from tilty.tilty import LOGGER, emit, parse_config

CONFIG = configparser.ConfigParser()


def terminate_process(device, signal_number, frame):  # noqa  # pylint: disable=unused-argument
    """ handle SIGTERM """
    device.stop()
    sys.exit()


def scan_and_emit(device, emitters):
    """ method that does the needful
    """
    LOGGER.debug('Starting device scan')
    tilt_data = device.scan_for_tilt_data()
    if tilt_data:
        LOGGER.debug('tilt data retrieved')
        click.echo(tilt_data)
        emit(emitters=emitters, tilt_data=tilt_data)
    else:
        LOGGER.debug('No tilt data')


def scan_and_emit_thread(device, config, keep_running=False):
    """ method that calls the needful
    """
    emitters = parse_config(config)
    click.echo('Scanning for Tilt data...')
    scan_and_emit(device, emitters)
    while keep_running:
        LOGGER.debug('Scanning for Tilt data...')
        scan_and_emit(device, emitters)
        sleep_time = int(CONFIG['general'].get('sleep_interval', 1))
        LOGGER.debug('Sleeping for %s....', sleep_time)
        sleep(sleep_time)


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
    file = pathlib.Path(config_file)
    if not file.exists():
        raise ConfigurationFileNotFoundException()

    CONFIG.read(config_file)

    logging_level = 'INFO'
    try:
        logging_level = CONFIG['general'].get('logging_level', 'INFO')
    except KeyError:
        pass
    LOGGER.setLevel(logging.getLevelName(logging_level))

    device = tilt_device.TiltDevice()
    signal.signal(signal.SIGINT, partial(terminate_process, device))
    device.start()
    threading.Thread(
        target=scan_and_emit_thread,
        name='tilty_daemon',
        args=(device, CONFIG, keep_running)
    ).start()
    if keep_running:
        while True:
            pass
