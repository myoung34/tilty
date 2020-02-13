# -*- coding: utf-8 -*-
""" InfluxDB emitter """
import requests


class InfluxDB:  # pylint: disable=too-few-public-methods
    """ Class to represent the actual device """
    def __init__(self, config):
        """ Initializer

        Args:
            config: (dict) represents the configuration for the emitter
        """
        self.url = config['url']
        self.database = config['database']
        self.temperature_payload = config['temperature_payload']
        self.gravity_payload = config['gravity_payload']

    def emit(self, **kwargs):  # pylint: disable=no-self-use,unused-argument
        """ Initializer

        Args:
        """
        requests.post(
            url=self.url,
            params=(('db', 'mydb')),
            data=self.temperature_payload,
        )
        requests.post(
            url=self.url,
            params=(('db', 'mydb')),
            data=self.gravity_payload,
        )
