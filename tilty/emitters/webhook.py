# -*- coding: utf-8 -*-
""" Webhook emitter """
import json
import logging
from typing import Callable, Dict

import requests
from jinja2 import Template

LOGGER = logging.getLogger()

METHODS: Dict[str, Callable] = {
    "GET": requests.get,
    "POST": requests.post,
}


def __type__() -> str:
    return 'Webhook'


class Webhook:  # pylint: disable=too-few-public-methods
    """ Class to represent the actual device """
    def __init__(self, config: dict) -> None:
        """ Initializer

        Args:
            config: (dict) represents the configuration for the emitter
        """
        # [webhook]
        # url = http://www.foo.com
        # self.headers = {"Content-Type": "application/json"}
        # payload_template = {"color": "{{ color }}", "gravity"...
        # method = GET
        self.url: str = config['url']
        self.method = METHODS.get(config['method'])
        if self.method is None:
            raise KeyError
        self.headers: dict = json.loads(config['headers'])
        self.template: Template = Template(config['payload_template'])

    def emit(self, tilt_data: dict) -> requests.Response:
        """ Initializer

        Args:
            tilt_data (dict): data returned from valid tilt device scan
        """

        payload: dict = json.loads(self.template.render(
            color=tilt_data['color'],
            gravity=tilt_data['gravity'],
            mac=tilt_data['mac'],
            temp=tilt_data['temp'],
            timestamp=tilt_data['timestamp'],
        ))

        LOGGER.debug(
            '[webhook] %s to %s with %s',
            self.method.__str__().split(' ')[1],
            self.url,
            payload,
        )

        if self.headers and 'json' in self.headers.get('Content-Type', {}):
            LOGGER.debug('[webhook] sending as json')
            return self.method(  # type: ignore
                url=self.url,
                headers=self.headers,
                json=payload,
            )
        LOGGER.debug('[webhook] sending as non-json')
        return self.method(  # type: ignore
            url=self.url,
            headers=self.headers,
            data=payload,
        )
