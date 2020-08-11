# -*- coding: utf-8 -*-
""" Webhook emitter """
import json

import requests
from jinja2 import Template

METHODS = {
    "GET": requests.get,
    "POST": requests.post,
}


class Webhook:  # pylint: disable=too-few-public-methods
    """ Class to represent the actual device """
    def __init__(self, config):
        """ Initializer

        Args:
            config: (dict) represents the configuration for the emitter
        """
        # [webhook]
        # url = http://www.foo.com
        # self.headers = {"Content-Type": "application/json"}
        # payload_template = {"color": "{{ color }}", "gravity"...
        # method = GET
        self.url = config['url']
        self.method = METHODS.get(config['method'])
        self.headers = config['headers']
        self.template = Template(config['payload_template'])

    def emit(self, tilt_data):
        """ Initializer

        Args:
            tilt_data (dict): data returned from valid tilt device scan
        """
        payload = json.loads(self.template.render(
            color=tilt_data['color'],
            gravity=tilt_data['gravity'],
            mac=tilt_data['mac'],
            temp=tilt_data['temp'],
            timestamp=tilt_data['timestamp'],
        ))
        if self.headers and 'json' in self.headers.get('Content-Type'):
            return self.method(
                url=self.url,
                headers=self.headers,
                json=payload,
            )
        return self.method(
            url=self.url,
            headers=self.headers,
            data=payload,
        )
