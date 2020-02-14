# -*- coding: utf-8 -*-
""" InfluxDB emitter """
import json
import logging

from influxdb import InfluxDBClient

from tilty.common import safe_get_key

LOGGER = logging.getLogger()


class InfluxDB:  # pylint: disable=too-few-public-methods
    """ Class to represent the actual device """
    def __init__(self, config):
        """ Initializer

        Args:
            config: (dict) represents the configuration for the emitter
        """
        self.temperature_payload = config['temperature_payload']
        self.gravity_payload = config['gravity_payload']
        self.client = InfluxDBClient(
            config['url'],
            safe_get_key(config, 'port', 80),
            safe_get_key(config, 'user'),
            safe_get_key(config, 'password'),
            config['database']
        )

    def emit(self, **kwargs):  # pylint: disable=no-self-use,unused-argument
        """ Initializer

        Args:
        """
        LOGGER.info('[influxdb] posting temperature data')
        self.client.write_points([json.loads(self.temperature_payload)])
        LOGGER.info('[influxdb] posting gravity data')
        self.client.write_points([json.loads(self.gravity_payload)])
