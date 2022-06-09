# -*- coding: utf-8 -*-
""" InfluxDB emitter """
import logging
from distutils import util as distutil  # noqa  # pylint: disable=line-too-long,deprecated-module,fixme  # TODO: fix this

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
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
        self.gravity_template = Template(config['gravity_payload_template'])  # noqa
        self.temperature_template = Template(config['temperature_payload_template'])  # noqa
        self.bucket = safe_get_key(config, 'bucket')

        verify_ssl = bool(distutil.strtobool(
            safe_get_key(config, 'verify_ssl', 'False')
        ))
        self.org = safe_get_key(config, 'org')
        client = InfluxDBClient(
            url=config['url'],
            org=self.org,
            token=safe_get_key(config, 'token'),
            verify_ssl=verify_ssl
        )
        self.write_api = client.write_api(write_options=SYNCHRONOUS)

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
        )
        gravity_payload = self.gravity_template.render(
            color=tilt_data['color'],
            gravity=tilt_data['gravity'],
            mac=tilt_data['mac'],
            temp=tilt_data['temp'],
        )
        LOGGER.info('[influxdb] posting temperature data')
        self.write_api.write(
            bucket=self.bucket,
            org=self.org,
            record=temperature_payload
        )
        LOGGER.info('[influxdb] posting gravity data')
        self.write_api.write(
            bucket=self.bucket,
            org=self.org,
            record=gravity_payload
        )
