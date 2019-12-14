# -*- coding: utf-8 -*-
""" Main Click methods """

import logging
from time import sleep

import click

from tilty import tilt_device

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


@click.command()
@click.option(
    '--keep-running',
    '-r',
    is_flag=True,
    help="Keep running until SIGTERM",
)
def run(keep_running):
    """ main cli entrypoint
    """
    click.echo('Scanning for Tilt data...')
    t = tilt_device.TiltDevice()
    t.start()
    if keep_running:
        while True:
            tilt_data = t.scan_for_tilt_data()
            if tilt_data:
                click.echo(tilt_data)
            sleep(10)
    else:
        tilt_data = t.scan_for_tilt_data()
        if tilt_data:
            click.echo(tilt_data)
