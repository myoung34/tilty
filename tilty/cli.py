# -*- coding: utf-8 -*-
""" Main Click methods """

import configparser
import logging
import signal
import sys
import threading
from functools import partial
from time import sleep

import click

from tilty import tilt_device
from tilty.tilty import emit

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

CONFIG = configparser.ConfigParser()


def terminate_process(device, signal_number, frame):  # noqa  # pylint: disable=unused-argument
    """ handle SIGTERM """
    device.stop()
    sys.exit()


def scan_and_emit(device, config):
    """ method that does the needful
    """
    tilt_data = device.scan_for_tilt_data()
    click.echo(tilt_data)
    emit(config=config, tilt_data=tilt_data)


def scan_and_emit_thread(device, config, keep_running=False):
    """ method that calls the needful
    """
    scan_and_emit(device, config)
    while keep_running:
        scan_and_emit(device, config)
        sleep(int(config['general']['sleep_interval']))


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
