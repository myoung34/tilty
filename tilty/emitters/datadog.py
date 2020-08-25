# -*- coding: utf-8 -*-
""" DataDog emitter """
import logging

from datadog import initialize, statsd

from tilty.common import safe_get_key

LOGGER = logging.getLogger()


def __type__() -> str:
    return 'Datadog'


class Datadog:  # pylint: disable=too-few-public-methods
    """ Class to represent the actual device """
    def __init__(self, config: dict) -> None:
        """ Initializer

        Args:
            config: (dict) represents the configuration for the emitter
        """
        # [datadog]
        # host = 'host'
        # port = 'port'
        options = {
            'statsd_host': config['host'],
            'statsd_port': safe_get_key(config, 'port', 8125),
        }
        initialize(**options)

    def emit(self, tilt_data: dict) -> None:  # pylint:disable=no-self-use
        """ Initializer

        Args:
            tilt_data (dict): data returned from valid tilt device scan
        """
        LOGGER.info('[datadog] posting temperature data')
        tags = [f"color:{tilt_data['color']}"]
        if tilt_data['mac']:
            tags = [
                f"color:{tilt_data['color']}",
                f"mac:{tilt_data['mac']}",
            ]
        statsd.gauge(
            'tilty.temperature',
            tilt_data['temp'],
            tags=tags,
        )
        LOGGER.info('[datadog] posting gravity data')
        statsd.gauge(
            'tilty.gravity',
            tilt_data['gravity'],
            tags=tags,
        )
