# -*- coding: utf-8 -*-
""" InfluxDB emitter """
import json
import logging

from influxdb import InfluxDBClient
from jinja2 import Template

from tilty.common import safe_get_key

LOGGER = logging.getLogger()


def __type__() -> str:
    return 'InfluxDB'


class InfluxDB:  # pylint: disable=too-few-public-methods
    """ Class to represent the actual device """
    def __init__(self, config: dict) -> None:
        """ Initializer

        Args:
            config: (dict) represents the configuration for the emitter
        """
        # [influxdb]
        # url = www.foo.com
        # port = 80
        # database = tilty
        # gravity_payload_template = {"measurement": "gravity", "tags": {"color": "{{ color }}"}, "fields": {"value": {{ gravity }}}}  # noqa  # pylint: disable=line-too-long
        # temperature_payload_template = {"measurement": "temperature", "tags": {"color": "{{ color }}"}, "fields": {"value": {{ temp }}}}  # noqa  # pylint: disable=line-too-long
        self.gravity_template = Template(config['gravity_payload_template'])  # noqa
        self.temperature_template = Template(config['temperature_payload_template'])  # noqa
        self.client = InfluxDBClient(
            config['url'],
            safe_get_key(config, 'port', 80),
            safe_get_key(config, 'user'),
            safe_get_key(config, 'password'),
            config['database']
        )

    def emit(self, tilt_data: dict) -> None:
        """ Initializer

        Args:
            tilt_data (dict): data returned from valid tilt device scan
        """
        temperature_payload = self.temperature_template.render(
            color=tilt_data['color'],
            gravity=tilt_data['gravity'],
            mac=tilt_data['mac'],
            temp=tilt_data['temp'],
            timestamp=tilt_data['timestamp'],
        )
        gravity_payload = self.gravity_template.render(
            color=tilt_data['color'],
            gravity=tilt_data['gravity'],
            mac=tilt_data['mac'],
            temp=tilt_data['temp'],
            timestamp=tilt_data['timestamp'],
        )
        LOGGER.info('[influxdb] posting temperature data')
        self.client.write_points([json.loads(temperature_payload)])
        LOGGER.info('[influxdb] posting gravity data')
        self.client.write_points([json.loads(gravity_payload)])
