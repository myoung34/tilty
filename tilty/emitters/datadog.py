# -*- coding: utf-8 -*-
""" DataDog emitter """
import logging

from datadog import initialize, statsd

from tilty.common import safe_get_key

LOGGER = logging.getLogger()


class Datadog:  # pylint: disable=too-few-public-methods
    """ Class to represent the actual device """
    def __init__(self, config):
        """ Initializer

        Args:
            config: (dict) represents the configuration for the emitter
        """
        self.temperature = config['temperature']
        self.gravity = config['gravity']
        self.color = config['color']
        options = {
            'statsd_host': config['host'],
            'statsd_port': safe_get_key(config, 'port', 8125),
        }
        initialize(**options)

    def emit(self, **kwargs):  # pylint: disable=no-self-use,unused-argument
        """ Initializer

        Args:
        """
        LOGGER.info('[datadog] posting temperature data')
        statsd.gauge(
            'tilty.temperature',
            self.temperature,
            tags=[f"color:{self.color}"]
        )
        LOGGER.info('[datadog] posting gravity data')
        statsd.gauge(
            'tilty.gravity',
            self.gravity,
            tags=[f"color:{self.color}"]
        )
