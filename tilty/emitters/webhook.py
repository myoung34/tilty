# -*- coding: utf-8 -*-
""" Webhook emitter """
import datetime
import json
import logging
from typing import Callable, Dict, Union

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
        delay_minutes = config.get('delay_minutes')
        if delay_minutes:
            delay_minutes = int(delay_minutes)
        self.delay_minutes: Union[int, None] = delay_minutes
        self.headers: dict = json.loads(config['headers'])
        self.template: Template = Template(config['payload_template'])
        self.delay_until_identifier: str = config.get(
            'delay_until_identifier',
            'color'
        )
        self.delay_until: Dict[str, datetime.datetime] = dict()

    def emit(self, tilt_data: dict) -> None:
        """ Initializer

        Args:
            tilt_data (dict): data returned from valid tilt device scan
        """

        delay_until_identifier = str(tilt_data[self.delay_until_identifier])
        now = datetime.datetime.now(datetime.timezone.utc)
        delay_until = self.delay_until.get(delay_until_identifier)
        if delay_until and now < delay_until:
            return None

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

        if self.delay_minutes:
            timedelta = datetime.timedelta(minutes=self.delay_minutes)
            self.delay_until[delay_until_identifier] = now + timedelta

        if self.headers and 'json' in self.headers.get('Content-Type', {}):
            LOGGER.debug('[webhook] sending as json')
            return self.method(  # type: ignore
                url=self.url,
                headers=self.headers,
                json=payload,
            )
        LOGGER.debug('[webhook] sending as non-json')
        response = self.method(  # type: ignore
            url=self.url,
            headers=self.headers,
            data=payload,
        )
        response.raise_for_status()
        return None
