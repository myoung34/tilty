# -*- coding: utf-8 -*-
""" Prometheus emitter """
import json
import logging

from jinja2 import Template
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

from tilty.common import safe_get_key

LOGGER = logging.getLogger()


def __type__() -> str:
    return "Prometheus"


class Prometheus:  # pylint: disable=too-few-public-methods
    """ Class to represent the actual device """
    def __init__(self, config: dict) -> None:
        """ Initializer

        Args:
            config: (dict) represents the configuration for the emitter
        """
        # [prometheus]
        # url = localhost:80
        # gravity_gauge_name = tilty_gravity_g
        # temp_gauge_name = tilty_temperature_f
        # labels = {"color": "{{ color }}", "mac": "{{ mac }}"}
        # job_name = tilty
        self.job_name = safe_get_key(config, 'job_name', 'tilty')
        self.label_template = Template(config['labels'])
        self.url = config['url']

        self.registry = CollectorRegistry()
        label_dict = json.loads(self.label_template.render())
        self.gravity_gauge = Gauge(
            safe_get_key(config, 'gravity_gauge_name', 'tilty_gravity_g'),
            'The currently measured gravity',
            label_dict.keys(),
            registry=self.registry,
        )
        self.temp_gauge = Gauge(
            safe_get_key(config, 'temp_gauge_name', 'tilty_temperature_f'),
            'The currently measured temperature',
            label_dict.keys(),
            registry=self.registry,
        )

    def emit(self, tilt_data: dict) -> None:
        """ Initializer

        Args:
            tilt_data (dict): data returned from valid tilt device scan
        """

        label_payload = self.label_template.render(
            color=tilt_data['color'],
            gravity=tilt_data['gravity'],
            mac=tilt_data['mac'],
            temp=tilt_data['temp'],
            timestamp=tilt_data['timestamp'],
        )

        label_payload = json.loads(label_payload)

        self.gravity_gauge.labels(
            **label_payload
        ).set(tilt_data['gravity'])
        self.temp_gauge.labels(
            **label_payload
        ).set(tilt_data['temp'])

        LOGGER.info('[prometheus] posting data')
        push_to_gateway(self.url, job=self.job_name, registry=self.registry)
