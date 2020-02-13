# -*- coding: utf-8 -*-
""" Webhook emitter """
import requests

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
        self.url = config['url']
        self.method = METHODS.get(config['method'])
        self.headers = config['headers']
        self.payload = config['payload']

    def emit(self, **kwargs):  # pylint: disable=no-self-use,unused-argument
        """ Initializer

        Args:
        """
        if self.headers and 'json' in self.headers.get('Content-Type'):
            return self.method(
                url=self.url,
                headers=self.headers,
                json=self.payload,
            )
        return self.method(
            url=self.url,
            headers=self.headers,
            data=self.payload,
        )
